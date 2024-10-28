from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from medask.tools.benchmark.vignette import Vignette


class Patient:
    def __init__(self, vignette: "Vignette") -> None:
        self._vignette = vignette

    def system_prompt(self) -> str:
        return f"""You are a patient with the following background:
            DEMOGRAPHICS: {self._vignette.demographics}
            HISTORY: {self._vignette.current_history}
            PRIMARY COMPLAINTS: {self._vignette.primary_complaints}
            ADDITIONAL DETAILS: {self._vignette.additional_information}

            You are visiting a doctor because of your PRIMARY COMPLAINTS.
            A doctor will ask you questions to diagnose your condition. Provide concise
            answers of 1-3 sentences, sharing only the relevant information based on your disease and the above 
            additional details. If the doctor asks about something not mentioned above, 
            say something in accordance with the other information above.
        """


class Doctor:
    def __init__(self, vignette: "Vignette") -> None:
        self._vignette = vignette

    def system_prompt(self) -> str:
        return f"""You are a doctor diagnosing through an online chat platform a patient
            with the following characteristics
            DEMOGRAPHICS: {self._vignette.demographics}

            .You will ask the patient concise questions (1-3 sentences at a time) in order
            to understand their disease. After gathering sufficient information, finish
            the conversation by writing chosen diagnoses in this format:
            DIAGNOSIS READY: [diagnosis1, diagnosis2, diagnosis3]
        """

    def initial_prompt(self) -> str:
        return """Hello, I'm a doctor, here to diagnose your ailment.
            Please tell me what's troubling you.
        """
