from pymongo.collection import Collection, ObjectId

from app.dto.candidate import CandidateDto
from app.exceptions import NotFoundException

from ..models.candidate import Candidate
from ..models.job import Job
from .db_service import DbService


class JobService(DbService):
    def list_jobs(self):
        with self.get_database() as db:
            jobs_coll: Collection = db["jobs"]
            jobs_dicts = jobs_coll.find()
            return [Job(**x) for x in jobs_dicts]

    def create_job(self, job: Job):
        with self.get_database() as db:
            jobs_coll: Collection = db["jobs"]
            resp = jobs_coll.insert_one(job.as_json())
            job.set_id(resp.inserted_id)

    def get_job(self, job_id: str):
        with self.get_database() as db:
            jobs_coll: Collection = db["jobs"]
            job_dict = jobs_coll.find_one({"_id": ObjectId(job_id)})

            if not job_dict:
                raise NotFoundException("Job not found")
            return Job(**job_dict)

    def add_candidate(self, job_id: str, candidate: Candidate):
        with self.get_database() as db:
            job_coll: Collection = db["jobs"]
            candidate_coll: Collection = db["candidates"]

            job_dict = job_coll.find_one({"_id": ObjectId(job_id)})
            if not job_dict:
                raise NotFoundException("Job not found")

            resp = candidate_coll.insert_one(candidate.as_db_model())
            candidate.set_id(resp.inserted_id)

    def list_candidates(self, job_id: str):
        with self.get_database() as db:
            job_coll: Collection = db["jobs"]
            candidate_coll: Collection = db["candidates"]
            answer_coll: Collection = db["answers"]

            job_dict = job_coll.find_one({"_id": ObjectId(job_id)})
            if not job_dict:
                raise NotFoundException("Job not found")

            raw_candidates = candidate_coll.find({"job_id": ObjectId(job_id)})
            candidates = []

            for candidate_dict in raw_candidates:
                candidate = CandidateDto.from_db_data(candidate_dict)
                answers = list(
                    answer_coll.find(
                        {"job_id": ObjectId(job_id), "candidate_id": candidate.get_id()}
                    )
                )
                candidate.answers = {str(x["question_id"]): x for x in answers}
                candidates.append(candidate)

            return candidates

    def get_candidate(self, candidate_id: str):
        with self.get_database() as db:
            candidate_coll: Collection = db["candidates"]

            candidate_dict = candidate_coll.find_one({"_id": ObjectId(candidate_id)})
            if not candidate_dict:
                raise NotFoundException("Candidate not found")

            return Candidate(**candidate_dict)
