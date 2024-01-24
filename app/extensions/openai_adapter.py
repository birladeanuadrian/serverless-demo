import os

import openai

from app.exceptions import RateLimitException


class OpenaiAdapter:
    def __init__(self, api_key):
        openai.api_key = api_key

    def make_request(self, prompt: str, temperature=0.99999) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=512,
            )
            print("Openai response", response)
            return response["choices"][0]["message"]["content"]
        except openai.error.RateLimitError:
            raise RateLimitException("Model is overloaded. Please try again")


def get_openai_adapter():
    return OpenaiAdapter(os.getenv("OPENAI_API_KEY"))
