from dataclasses import dataclass

from pymongo.collection import ObjectId

from .abstract_model import AbstractModel


@dataclass
class Answer(AbstractModel):
    job_id: str
    question_id: str
    candidate_id: str
    text: str
    mark: float = 0
    analysis: str = ""
    _id: str = None

    def set_id(self, new_id: str):
        self._id = new_id

    def as_db_model(self):
        data = self.as_json()
        data["job_id"] = ObjectId(data["job_id"])
        data["question_id"] = ObjectId(data["question_id"])
        data["candidate_id"] = ObjectId(data["candidate_id"])
        return data
