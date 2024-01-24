from pymongo.collection import Collection, ObjectId

from app.exceptions import NotFoundException
from app.models.answer import Answer
from app.models.job import Job
from app.models.question import Question

from ..extensions.openai_adapter import OpenaiAdapter
from ..extensions.openai_response_parser import OpenaiResponseParser
from ..extensions.prompt_generator import PromptGenerator
from .db_service import DbService


class QuestionService(DbService):
    def __init__(self, openai_adapter: OpenaiAdapter):
        super().__init__()
        self.openai_adapter = openai_adapter

    def generate_automatic_questions(self, job_id: str, number: int):
        with self.get_database() as db:
            job_coll: Collection = db["jobs"]
            questions_coll: Collection = db["questions"]
            job_dict = job_coll.find_one({"_id": ObjectId(job_id)})

            if not job_dict:
                raise NotFoundException("Job not found")

            job = Job(**job_dict)
            prompt = PromptGenerator.generate_create_questions_prompt(job, number)
            response = self.openai_adapter.make_request(prompt)
            questions = response.split("\n")
            raw_questions = [x for x in questions if x.strip()]

            idx = 0
            questions_docs = []
            for str_question in raw_questions:
                question = Question(job_id=job_id, text=str_question, index=idx)
                resp = questions_coll.insert_one(question.as_db_model())
                question.set_id(resp.inserted_id)
                questions_docs.append(question)
                idx += 1

            return questions_docs

    def list_questions(self, job_id: str):
        with self.get_database() as db:
            job_coll: Collection = db["jobs"]
            questions_coll: Collection = db["questions"]

            job_dict = job_coll.find_one({"_id": ObjectId(job_id)})
            if not job_dict:
                raise NotFoundException("Job not found")

            questions = questions_coll.find({"job_id": ObjectId(job_id)}).sort("index")
            return [Question.from_db_model(x) for x in questions]

    def add_answer(self, job_id: str, answer: Answer):
        with self.get_database() as db:
            job_coll: Collection = db["jobs"]
            answer_coll: Collection = db["answers"]
            questions_coll: Collection = db["questions"]

            job_dict = job_coll.find_one({"_id": ObjectId(job_id)})
            if not job_dict:
                raise NotFoundException("Job not found")
            job = Job(**job_dict)

            question_dict = questions_coll.find_one(
                {"_id": ObjectId(answer.question_id), "job_id": ObjectId(job_id)}
            )
            if not question_dict:
                raise NotFoundException("Question not found")
            question = Question(**question_dict)

            validate_prompt = PromptGenerator.generate_validate_answer_prompt(job, question, answer)
            chatgpt_response = self.openai_adapter.make_request(validate_prompt, 0.3)
            answer.analysis = chatgpt_response.strip()
            answer.mark = float(OpenaiResponseParser.extract_answer_mark(chatgpt_response))

            resp = answer_coll.insert_one(answer.as_db_model())
            answer.set_id(resp.inserted_id)

    def generate_ideal_answer(self, job_id: str, question_id: str):
        with self.get_database() as db:
            job_coll: Collection = db["jobs"]
            questions_coll: Collection = db["questions"]

            job_dict = job_coll.find_one({"_id": ObjectId(job_id)})
            if not job_dict:
                raise NotFoundException("Job not found")
            job = Job(**job_dict)

            question_dict = questions_coll.find_one(
                {"_id": ObjectId(question_id), "job_id": ObjectId(job_id)}
            )
            if not question_dict:
                raise NotFoundException("Question not found")

            question = Question(**question_dict)
            if question.ideal_answer:
                return question

            ideal_answer_prompt = PromptGenerator.generate_ideal_answer_prompt(job, question)
            ideal_answer = self.openai_adapter.make_request(ideal_answer_prompt, 0.7)
            question.ideal_answer = ideal_answer
            questions_coll.update_one(
                {"_id": ObjectId(question_id)}, {"$set": {"ideal_answer": ideal_answer}}
            )
            return question
