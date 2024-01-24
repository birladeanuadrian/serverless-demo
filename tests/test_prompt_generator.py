import unittest

from app.extensions.prompt_generator import PromptGenerator
from app.models.answer import Answer
from app.models.job import Job
from app.models.question import Question


class PromptGeneratorTestCase(unittest.TestCase):
    def test_generate_junior_eng_prompt(self):
        job = Job(
            title="Junior C++ engineer",
            seniority="0-2",
            mandatory_knowledge=["C", "data structures", "algorithms"],
            optional_knowledge=["C++", "Windows Internals", "Windows drivers"],
        )
        prompt = PromptGenerator.generate_create_questions_prompt(job, 10)
        self.assertEqual(
            "Generate 10 interview questions for a candidate for Junior C++ engineer with 0-2 years of "
            "experience. The candidate must know the following: C, data structures, algorithms. A "
            "maximum of 3 questions will be about the following: C++, Windows Internals, "
            "Windows drivers. The questions should be technical, short and on point so that the "
            "candidate can answer each orally in 1-4 minutes on a phone conversation. The questions "
            "should seek if the candidate has a basic understanding of the given concepts. The last two "
            "questions should be about corner cases or should be of a medium difficulty to test his "
            "knowledge. Your answer will contain just the questions. The questions should be separated "
            "by a new line, without any other separator, and should not be numbered.",
            prompt,
        )

    def test_generate_validate_answer_prompt(self):
        job = Job(
            title="Junior C++ engineer",
            seniority="0-2",
            mandatory_knowledge=["C", "data structures", "algorithms"],
            optional_knowledge=["C++", "Windows Internals", "Windows drivers"],
        )
        question = Question(
            job_id="",
            index=0,
            text="Can you explain the difference between a stack and a queue data structure? ",
        )
        answer = Answer(
            job_id="",
            question_id="",
            candidate_id="",
            text="In a stack, the last element to be added is the first to be removed. In a queue, the first element to be added is the first element to be removed.",
        )
        prompt = PromptGenerator.generate_validate_answer_prompt(job, question, answer)
        self.assertEqual(
            """A candidate has applied for the position of Junior C++ engineer with a desired experience of 0-2 years. At interview he was asked the question: "Can you explain the difference between a stack and a queue data structure? ". His answer is below: 
```
In a stack, the last element to be added is the first to be removed. In a queue, the first element to be added is the first element to be removed.
```
Evaluate his answer taking into consideration  each of the factors: correctness, richness of information, language, clarity of thought in regard to both the question and the level of experience. If he made a mistake, pinpoint the mistake and the correct answer. At the end, on the last line, write only a mark from 0 to 10. The mark should be a float. Do not write anything else after this line. """,
            prompt,
        )

    def test_generate_ideal_answer_prompt(self):
        job = Job(
            title="Junior C++ engineer",
            seniority="0-2",
            mandatory_knowledge=["C", "data structures", "algorithms"],
            optional_knowledge=["C++", "Windows Internals", "Windows drivers"],
        )
        question = Question(
            job_id="",
            index=0,
            text="Can you explain the difference between a stack and a queue data " "structure? ",
        )
        prompt = PromptGenerator.generate_ideal_answer_prompt(job, question)
        self.assertEqual(
            "For a candidate to the position of Junior C++ engineer with 0-2 years of experience, "
            "write what would be the ideal answer to the question: `Can you explain the difference "
            "between a stack and a queue data structure? `.",
            prompt,
        )

    def test_generate_extract_answers_prompt(self):
        questions = [
            Question(
                job_id="", index=0, text="Explain the difference between arrays and linked lists."
            ),
            Question(
                job_id="",
                index=1,
                text="What data structure would you use to implement a queue and why?",
            ),
            Question(
                job_id="",
                index=2,
                text="What is recursion and where might it be useful in programming?",
            ),
        ]
        transcript = """
Henry: Hi! My name is Henry!
Mike: Hi Henry! I'm Mike.
Henry: So how are you feeling today ?
Mike: Energized! How about you ?
Henry: Fine! So let's get started with the interview. Explain the difference between arrays and linked lists.
Mike: Arrays are contiguous areas of memory consisting of cells of identical size. Linked lists consist of nodes allocated dynamically on the go. Each node contains a reference to the next node and optionally to the previous node.
Henry: Great, thank you! On to the next question. What data structure would you use to implement a queue and why?
Mike: I would use a double-linked list and hold references to both the first and the last node. This way, when adding a new node, I would make it be the first node in the list. And when I remove the last node, I will update the reference to the last node of the list to the second to last.
Henry: Alright. What is recursion ?
Mike: A recursion is when a function calls itself.
Henry: And how is it useful in programming ?
Mike: It's useful in backtracking.
Henry: Great! What is Big O notation and why is it important in algorithm analysis?
Mike: That I don't know.
Henry: That's ok. How would you find the index of a specific integer using binary search in a sorted list?
Mike: I would compare the integer with the middle element of the list. If the integer is larger than the middle element, then the number I'm looking for is in the second half of the array, otherwise it's in the first half of the array. I would do a recursive function that does this until I find the right element.
Henry: Ok. Let's proceed to your work history. Where have you worked before ?
Mike: My first job was at Microsoft, where I worked for 2 years. I started out as an intern, then became a junior software engineer, and then a mid software engineer.
Henry: So what did you do as an intern ?
Mike: The first 2 months I was following trainings for python, C and mysql. Then we moved on to more complicated stuff, such as assembly, reverse engineering, and cryptogrtaphy.



Henry: Alright! Thanks for the time! Have a great day!
Mike: Thanks! You too! Bye!
Henry: Bye!
        """.strip()

        prompt = PromptGenerator.generate_extract_answers_prompt(questions, transcript)

        self.assertEqual(
            f"""In an interview with a candidate, the following questions were asked:
```
1. Explain the difference between arrays and linked lists.
2. What data structure would you use to implement a queue and why?
3. What is recursion and where might it be useful in programming?
```
The following is the transcript of the interview:
```
{transcript}
```
Extract the candidate's answers to each question. Do not modify them. If the question wasn't asked or an answer was not given, leave it blank. Do not add anything that wasn't said.
""".strip(),
            prompt,
        )


if __name__ == "__main__":
    unittest.main()
