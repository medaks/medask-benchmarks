import json
import os
from abc import abstractmethod
from logging import getLogger
from typing import Any, Dict, List, Literal

from pydantic import BaseModel

logger = getLogger(__file__)


class Vignette(BaseModel):
    data: Dict[str, Any]

    @property
    @abstractmethod
    def correct_diagnosis(self) -> str:
        """The correct diagnosis of this vignette."""
        pass

    @property
    @abstractmethod
    def demographics(self) -> str:
        """Demographics info about the patient."""
        pass

    @property
    @abstractmethod
    def current_history(self) -> str:
        """Description or current history of the patient's affliction."""
        pass

    @property
    @abstractmethod
    def primary_complaints(self) -> str:
        """Primary complaints because of which the patient has come to the doctor."""
        pass

    @property
    @abstractmethod
    def additional_information(self) -> str:
        """Any additional information about the patient or their disease."""
        pass


class AgentClinicVignette(Vignette):
    @property
    def correct_diagnosis(self) -> str:
        return self.data["correct_diagnosis"]

    @property
    def demographics(self) -> str:
        return self.data["demographics"]

    @property
    def current_history(self) -> str:
        return self.data.get("history", "No history")

    @property
    def primary_complaints(self) -> str:
        return self.data.get("primary_symptom", "No primary simptoms")

    @property
    def additional_information(self) -> str:
        return f"""
            SECONDARY SYMPTOMS: {str(self.data.get("secondary_symptoms", ""))}
            TEMPERATURE: {self.data.get("temperature", "")}
            PAST MEDICAL HISTORY: {self.data.get("past_medical_history", "")}
            SOCIAL HISTORY: {self.data.get("social_history", "")}
            REVIEW OF SYSTEMS: {self.data.get("review_of_systems", "")}
        """


class AveyVignette(Vignette):
    @property
    def correct_diagnosis(self) -> str:
        return self.data["correct_diagnosis"]

    @property
    def demographics(self) -> str:
        return self.data["demographics"]

    @property
    def current_history(self) -> str:
        return self.data["presentation"]

    @property
    def primary_complaints(self) -> str:
        return self.data["chief_complaints"]

    @property
    def additional_information(self) -> str:
        return f"""
            "ABSENT FINDINGS": {self.data["absent_findings"]}
            "PHYSICAL HISTORY": {self.data["physical_history"]}
            "FAMILY HISTORY": {self.data["family_history"]}
            "SOCIAL HISTORY": {self.data["social_history"]}
        """


def load_vignettes(name: Literal["avey", "agentclinic"]) -> List[Vignette]:
    directory = os.path.dirname(os.path.abspath(__file__))

    file_path = f"{directory}/vignettes/{name}_vignettes.jsonl"
    with open(file_path) as f:
        dicts = [json.loads(line) for line in f]

    if name == "avey":
        return [AveyVignette(data=d) for d in dicts]
    else:
        return [AgentClinicVignette(data=d) for d in dicts]
