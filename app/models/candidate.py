from dataclasses import dataclass

from pymongo.collection import ObjectId

from .abstract_model import AbstractModel


@dataclass
class Candidate(AbstractModel):
    name: str
    job_id: str
    _id: str = None

    def set_id(self, new_id: str):
        self._id = new_id

    def get_id(self):
        return self._id

    def as_db_model(self):
        data = self.as_json()
        data["job_id"] = ObjectId(data["job_id"])
        return data
