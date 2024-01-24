import openai
import os
from dotenv import load_dotenv
load_dotenv()

PROMPT = "Generate 10 interview questions for a candidate for Junior C++ engineer with 0-2 years of experience. The " \
         "candidate must know the following: C, data structures, algorithms. A maximum of 3 questions will be about " \
         "the following: C++, Windows Internals, Windows drivers. The questions should be technical, short and on " \
         "point so that the candidate can answer each orally in 1-4 minutes on a phone conversation. The questions " \
         "should seek if the candidate has a basic understanding of the given concepts. The last two questions should " \
         "be about corner cases or should be of a medium difficulty to test his knowledge. Your answer will contain " \
         "just the questions. The questions should be separated by a new line and should not be numbered."

openai.api_key = os.getenv("API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": PROMPT}
    ],
    # prompt=PROMPT,
    max_tokens=1024,
    temperature=0.9
)
print("Response", response)
