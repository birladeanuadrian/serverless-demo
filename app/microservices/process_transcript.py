import json
from typing import List, Tuple

import boto3

from app.constants import TRANSCRIPTS_BUCKET
from app.extensions.openai_adapter import OpenaiAdapter, get_openai_adapter
from app.extensions.openai_response_parser import OpenaiResponseParser
from app.extensions.prompt_generator import PromptGenerator
from app.models.extracted_answers import ExtractedAnswers
from app.services.db_service import DbService
from app.services.job_service import JobService
from app.services.question_service import QuestionService

MAX_CHARACTERS = 30_000
# MAX_CHARACTERS = 30_0


def chunk_is_safe(chunks: List[str]):
    total_characters = sum([len(x) for x in chunks])
    return total_characters <= MAX_CHARACTERS


def make_chunk_safe(start: int, chunk_end: int, lines: List[str]) -> Tuple[int, List[str]]:
    while chunk_is_safe(lines[start:chunk_end]) and chunk_end < len(lines):
        chunk_end += 1

    while not chunk_is_safe(lines[start:chunk_end]):
        chunk_end -= 1

    return chunk_end, lines[start:chunk_end]


def segment_transcript(transcript: str):
    if len(transcript) <= MAX_CHARACTERS:
        yield transcript
        return

    lines = transcript.split("\n")
    chunks = len(transcript) // MAX_CHARACTERS + 1
    chunk_size = len(lines) // chunks
    start = 1
    chunk_end = 0

    while chunk_end != len(lines):
        chunk_end, chunks = make_chunk_safe(
            start - 1, min(start - 1 + chunk_size, len(lines)), lines
        )
        yield "\n".join(chunks)
        start = chunk_end


class TranscriptProcessor(DbService):
    def __init__(
        self,
        openai_adapter: OpenaiAdapter,
        question_service: QuestionService,
        job_service: JobService,
        transcript_s3_key: str,
        candidate_id: str,
        job_id: str,
    ):
        self.openai_adapter = openai_adapter
        self.question_service = question_service
        self.job_service = job_service
        self.transcript_s3_key = transcript_s3_key
        self.candidate_id = candidate_id
        self.job_id = job_id

    def get_transcript(self):
        session = boto3.Session()
        s3 = session.client("s3")
        print("Reading file from s3", TRANSCRIPTS_BUCKET, self.transcript_s3_key)
        response = s3.get_object(Bucket=TRANSCRIPTS_BUCKET, Key=self.transcript_s3_key)
        return response["Body"].read().decode("utf-8")

    def process_transcript(self):
        transcript = self.get_transcript()
        questions = self.question_service.list_questions(self.job_id)
        answers = {}

        for transcript_segment in segment_transcript(transcript):
            prompt = PromptGenerator.generate_extract_answers_prompt(questions, transcript_segment)
            openai_response = self.openai_adapter.make_request(prompt)
            partial_answers = OpenaiResponseParser.extract_answers_to_questions(
                openai_response, questions
            )
            answers.update(partial_answers)

        extracted_answers = ExtractedAnswers(self.job_id, self.candidate_id, answers)
        with self.get_database() as db:
            extracted_answers_coll = db["extracted_answers"]
            extracted_answers_coll.insert_one(extracted_answers.as_json())


def handle_event(event: dict, *args, **kwargs):
    print("Handle Event", event)
    record = event["Records"][0]
    print("Record", record)
    data = json.loads(record["Sns"]["Message"])

    job_id = data["job_id"]
    candidate_id = data["candidate_id"]
    transcript_s3_key = data["transcript_s3_key"]

    openai_adapter = get_openai_adapter()
    question_service = QuestionService(openai_adapter)
    job_service = JobService()

    transcript_processor = TranscriptProcessor(
        openai_adapter, question_service, job_service, transcript_s3_key, candidate_id, job_id
    )
    transcript_processor.process_transcript()


if __name__ == "__main__":
    # todo: delete
    from dotenv import load_dotenv

    load_dotenv()

    handle_event(
        {
            "job_id": "643d40b69e1c3070f4b59a49",
            "candidate_id": "643d3e424430c17cb1690cd5",
            "transcript_s3_key": "discussion.txt",
        }
    )
