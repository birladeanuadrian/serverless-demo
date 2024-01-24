import unittest

from app.extensions.openai_response_parser import OpenaiResponseParser
from app.models.question import Question


class MyTestCase(unittest.TestCase):
    def test_extract_answer_mark(self):
        answer = """
        The candidate's answer is correct and concise, and demonstrates a good understanding of the differences between stack and queue data structures. However, it lacks some richness of information and professionalism, which could be improved upon.

In terms of correctness, the candidate correctly states that a stack follows a Last-In, First-Out (LIFO) ordering, while a queue follows a First-In, First-Out (FIFO) ordering. This is a fundamental difference between the two data structures.

The language used by the candidate is clear and easy to understand. However, the answer lacks some richness of information. For example, the candidate could have elaborated on the applications of stacks and queues, and provided examples of situations where one data structure might be more suitable than the other.

In terms of professionalism, the candidate's answer is somewhat brief and lacks context. The candidate could have demonstrated more professionalism by providing a more detailed and organized answer that explains the differences between stacks and queues in a more systematic manner.

Overall, considering the level of experience desired for the position, I would give this answer a score of 8 out of 10. The candidate shows a solid understanding of the topic, but could have provided more depth and professionalism in their response.
        """.strip()

        mark = OpenaiResponseParser.extract_answer_mark(answer)
        self.assertEqual(8, mark)

    def test_extract_answers_to_questions(self):
        response = """
1. Arrays are contiguous areas of memory consisting of cells of identical size. Linked lists consist of nodes allocated dynamically on the go. Each node contains a reference to the next node and optionally to the previous node.
2. I would use a double-linked list and hold references to both the first and the last node. This way, when adding a new node, I would make it be the first node in the list. And when I remove the last node, I will update the reference to the last node of the list to the second to last.
3. A recursion is when a function calls itself.
4. That I don't know.
5. 
6. 
7. 
8. I would compare the integer with the middle element of the list. If the integer is larger than the middle element, then the number I'm looking for is in the second half of the array, otherwise it's in the first half of the array. I would do a recursive function that does this until I find the right element.
        """.strip()
        questions = [
            Question(
                job_id="jobId",
                index=0,
                text="Explain the difference between arrays and linked lists.",
                _id="question1",
            ),
            Question(
                job_id="jobId",
                index=1,
                text="What data structure would you use to implement a queue and why?",
                _id="question2",
            ),
            Question(
                job_id="jobId",
                index=2,
                text="What is recursion and where might it be useful in programming?",
                _id="question3",
            ),
            Question(
                job_id="jobId",
                index=3,
                text="What is Big O notation and why is it important in algorithm analysis?",
                _id="question4",
            ),
            Question(
                job_id="jobId",
                index=4,
                text='What is the keyword "const" used for in C++?',
                _id="question5",
            ),
            Question(
                job_id="jobId",
                index=5,
                text="Explain the difference between pass by reference and pass by value in C++.",
                _id="question6",
            ),
            Question(
                job_id="jobId",
                index=6,
                text="Implement a function in C++ that reverses a given string.",
                _id="question7",
            ),
            Question(
                job_id="jobId",
                index=7,
                text="Given a sorted array of integers, how would you find the index of a specific integer using binary search?",
                _id="question8",
            ),
        ]

        answers = OpenaiResponseParser.extract_answers_to_questions(response, questions)

        self.assertEqual(
            answers,
            {
                "question1": "Arrays are contiguous areas of memory consisting of cells of identical size. Linked lists consist of nodes allocated dynamically on the go. Each node contains a reference to the next node and optionally to the previous node.",
                "question2": "I would use a double-linked list and hold references to both the first and the last node. This way, when adding a new node, I would make it be the first node in the list. And when I remove the last node, I will update the reference to the last node of the list to the second to last.",
                "question3": "A recursion is when a function calls itself.",
                "question4": "That I don't know.",
                "question5": "",
                "question6": "",
                "question7": "",
                "question8": "I would compare the integer with the middle element of the list. If the integer is larger than the middle element, then the number I'm looking for is in the second half of the array, otherwise it's in the first half of the array. I would do a recursive function that does this until I find the right element.",
            },
        )


if __name__ == "__main__":
    unittest.main()
