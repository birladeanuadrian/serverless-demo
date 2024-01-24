from dataclasses import dataclass
from typing import List, Union

from .abstract_model import AbstractModel


@dataclass
class Job(AbstractModel):
    title: str
    seniority: str
    mandatory_knowledge: List[str] = None
    optional_knowledge: List[str] = None
    _id: str = None

    def set_id(self, new_id: Union[str, None]):
        self._id = new_id

    def is_junior(self):
        keywords = ["jr", "junior", "intern", "training", "trainee"]
        title = self.title.lower()
        for attempt in keywords:
            if attempt in title:
                return True

        return False

    def is_senior(self):
        keywords = ["lead", "senior", "staff", "sre", "sr"]
        title = self.title.lower()
        for attempt in keywords:
            if attempt in title:
                return True

        return False

    def is_mid(self):
        return not (self.is_senior() or self.is_junior())
