from dataclasses import dataclass
from typing import Dict

from app.models.candidate import Candidate


@dataclass
class CandidateDto(Candidate):
    answers: Dict[str, dict] = None

    @classmethod
    def from_db_data(cls, data):
        data["job_id"] = str(data["job_id"])
        return CandidateDto(**data)
