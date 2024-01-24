from dataclasses import dataclass

from pymongo.collection import ObjectId

from .abstract_model import AbstractModel


@dataclass
class Question(AbstractModel):
    job_id: str
    index: int
    text: str
    ideal_answer: str = ""
    _id: str = None

    @classmethod
    def from_db_model(cls, data: dict):
        data["job_id"] = str(data["job_id"])
        return Question(**data)

    def set_id(self, new_id: str):
        self._id = new_id

    def get_id(self):
        return self._id

    def as_db_model(self):
        data = self.as_json()
        data["job_id"] = ObjectId(data["job_id"])
        return data
