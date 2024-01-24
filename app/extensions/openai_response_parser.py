import re
import traceback
from typing import Dict, List

from app.models.question import Question


class OpenaiResponseParser:
    @staticmethod
    def extract_answer_mark(response: str):
        try:
            # we might have a double eol at the end
            last_line = [x for x in response.split("\n") if x][-1]
            match = re.findall(r"\d+\.\d+|\d+", last_line)
            if len(match) == 1:
                return float(match[0])
            if len(match) != 2:
                raise Exception("Mark not found")
            first = float(match[0])
            second = float(match[1])

            if int(first) == 10:
                return second

            if int(second) == 10:
                return first

            raise Exception("Mark not found")
        except:
            traceback.print_exc()
            return 0

    @staticmethod
    def extract_answers_to_questions(response: str, questions: List[Question]) -> Dict[str, str]:
        """
        :param response:
        :param questions:
        :return: A dictionary where the key is the question id and the value is the extract question answer
        """
        answers: Dict[str, str] = {}
        raw_answers = response.split("\n")
        for line in raw_answers:
            match = re.findall(r"\d+\.", line)

            question_index = int(match[0][:-1]) - 1  # remove the dot
            answer_text = line.replace(match[0], "").strip()
            matching_question = next(
                (item for item in questions if item.index == question_index), None
            )
            if not matching_question:
                continue

            answers[str(matching_question.get_id())] = answer_text
            # print("Answer", question_index, matching_question.text,  answer_text)

        return answers
