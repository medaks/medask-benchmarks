from logging import getLogger
from typing import TYPE_CHECKING, Any, Dict

from medask.models.comms.models import CMessage
from medask.models.orm.models import Role
from medask.ummon.openai import UmmonOpenAI
from medask.util.concurrency import exec_concurrently

from medask.tools.benchmark.simulator import NaiveSimulator

if TYPE_CHECKING:
    from medask.tools.benchmark.experiment_result import ExperimentResult

logger = getLogger("benchmark.evaluate")
_ummon_openai = UmmonOpenAI("gpt-4o")


def _get_score(obtained_diagnoses: str, correct_diagnosis: str) -> int:
    body = f"""Given a list of differential diagnoses and the correct diagnosis, determine if
        any of the diagnoses in the list is very similar to the correct diagnosis. If it is,
        specify its position, starting from 1, else write -1. Respond in the following format:
        Correct diagnosis present: YES/NO \nPosition: [number]

        OBTAINED DIAGNOSES: {obtained_diagnoses}
        CORRECT DIAGNOSIS: {correct_diagnosis}
    """
    cmsg = CMessage(user_id=1, body=body, role=Role.SYSTEM)
    out = _ummon_openai.inquire(cmsg).body
    try:
        position = int(out.split("Position:")[1])
        if "YES" in out:
            return position
        elif "NO" in out:
            # logger.info(f"NO: {correct_diagnosis=}\n\n{obtained_diagnoses=}\n\n")
            return -1
        else:
            logger.error(f"Bad evaluation response: {out=}")
            return -4
    except Exception:
        logger.exception(f"FAILED: {obtained_diagnoses=} {correct_diagnosis=} {out=}")
        return -3


def get_score(obtained_diagnoses: str, correct_diagnosis: str) -> float:
    params = [
        {"obtained_diagnoses": obtained_diagnoses, "correct_diagnosis": correct_diagnosis}
        for _ in range(3)
    ]
    positions = exec_concurrently(_get_score, params, 3)
    print(f"{positions=}\t{correct_diagnosis}\t{obtained_diagnoses}")
    if good_positions := [p for p in positions if p > 0]:
        position = round(sum(good_positions) / len(good_positions), 1)
    else:
        combined = "".join(str(abs(x)) for x in positions)
        position = -1 * int(combined)
    return position


def evaluate(result: "ExperimentResult") -> Dict[int, Dict[str, Any]]:
    """
    Evaluation.
    Super hacky for now, we need to reconstruct the right Simulator, to know if the
    chat successfully finish and to extract the diagnosis.
    :return: For each experiment from <num_experiments>, a dict of experiment results.
    """
    result = result.copy()  # Make sure we don't accidentally modify the results.
    # TODO fix fucked up implementation land.
    results: Dict[int, Dict[str, Any]] = {i: {} for i in range(result.num_experiments)}
    for i in range(result.num_experiments):
        positions = []
        chats = result.chats[i]
        for chat, vignette in zip(chats, result.vignettes):
            simulator = NaiveSimulator(vignette, None, None)
            simulator.chat_doctor = chat
            if not simulator.diagnosis_finished:
                logger.warning("Simulation did not finish with a diagnosis.")
                positions.append(-2)
                continue

            # Here we enter nice land, we have the chat, simulator and vignette.
            # Call _evaluate or do whatever.
            obtained_diagnoses = simulator.extract_diagnoses()
            correct_diagnosis = vignette.correct_diagnosis
            positions.append(get_score(obtained_diagnoses, correct_diagnosis))  # type: ignore

        logger.info(f"Results of run {i=}")
        goods = [p for p in positions if p >= 1]  # Positions of correct diagnoses.
        avg_position = sum(goods) / len(goods) if goods else -1
        print(f"\t{positions=}")
        print(f"\tNumber of correct diagnoses: {len(goods)} / {len(positions)}")
        print(f"\tAverage position of correct diagnosis: {avg_position}")
        print("\n\n")
        results[i]["n_correct"] = len(goods)
        results[i]["positions"] = positions

    # Not storing any evaluation results in ExperimentResult because I think
    # What we want to evaluate will change frequently, so it's more important
    # To be able to re-evaluate stored ExperimentResults.
    # But I'm still leaving the option to do it, use it if you like. :)
    return results
