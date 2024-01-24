from typing import List

from app.models.answer import Answer
from app.models.job import Job
from app.models.question import Question


class PromptGenerator:
    @staticmethod
    def generate_create_questions_prompt(job: Job, questions: int) -> str:
        no_opt = questions // 3
        prompt = f"Generate {questions} interview questions for a candidate for {job.title} with {job.seniority} years of experience. "
        prompt += f"The candidate must know the following: {', '.join(job.mandatory_knowledge)}. "
        prompt += f"A maximum of {no_opt} questions will be about the following: {', '.join(job.optional_knowledge)}. "
        prompt += "The questions should be technical, short and on point so that the candidate can answer each orally in 1-4 minutes on a phone conversation. "

        if job.is_junior():
            prompt += "The questions should seek if the candidate has a basic understanding of the given concepts. The last two questions should be about corner cases or should be of a medium difficulty to test his knowledge. "
        elif job.is_mid():
            prompt += "The questions should seek if the candidate has a medium understanding of the desired concepts. The last two questions should be more advanced. "
        elif job.is_senior():
            prompt += " The questions should seek if the candidate has a very advanced, very rare, world-class understanding of the desired concepts and their inner workings. The last two questions should be close to impossible. "
            prompt += " At least one question should be about his experience mentoring a younger coworker. "

        prompt += "Your answer will contain just the questions. "
        prompt += "The questions should be separated by a new line, without any other separator, and should not be numbered."
        return prompt

    @staticmethod
    def generate_validate_answer_prompt(job: Job, question: Question, answer: Answer):
        prompt = f"A candidate has applied for the position of {job.title} with a desired experience of {job.seniority} years. "
        prompt += f'At interview he was asked the question: "{question.text}". '
        prompt += f"His answer is below: \n```\n{answer.text}\n```\n"
        prompt += (
            "Evaluate his answer taking into consideration  each of the factors: correctness, richness of "
            "information, "
            "language, clarity of thought in regard to both the question and the level of "
            "experience. If he made a mistake, pinpoint the mistake and the correct answer. At the end, "
            "on the last line, write only a mark from 0 to 10. The mark should be a float. Do not write anything else after this line. "
        )

        return prompt

    @staticmethod
    def generate_ideal_answer_prompt(job: Job, question: Question):
        return (
            f"For a candidate to the position of {job.title} with {job.seniority} years of experience, write what "
            f"would be the ideal answer to the question: `{question.text}`."
        )

    @staticmethod
    def generate_coding_challenge_prompt(job: Job):
        return (
            f"There is a candidate for the position of {job.title} with a desired experience of {job.seniority} years. "
            + " Taking into account his experience, on the first line, write a coding challenge for him that he can solve"
            + " in 2 hours or less. On the second line, generate some input data to be used."
        )

    @staticmethod
    def generate_extract_answers_prompt(questions: List[Question], transcript_segment: str):
        formatted_questions = "\n".join([f"{x.index + 1}. {x.text}" for x in questions])

        return f"""In an interview with a candidate, the following questions were asked:
```
{formatted_questions}
```
The following is the transcript of the interview:
```
{transcript_segment}
```
Extract the candidate's answers to each question. Do not modify them. If the question wasn't asked or an answer was not given, leave it blank. Do not add anything that wasn't said.
""".strip()
