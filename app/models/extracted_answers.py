from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Union

from pymongo.collection import ObjectId

from .abstract_model import AbstractModel


@dataclass
class ExtractedAnswers(AbstractModel):
    job_id: Union[str, ObjectId]
    candidate_id: Union[str, ObjectId]
    # dict where the keys are question ids and the values the answers extracted from the transcript
    answers: Dict[str, str]
    created_at: datetime = datetime.utcnow()
    _id: ObjectId = None
