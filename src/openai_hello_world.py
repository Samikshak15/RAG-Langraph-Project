"""OpenAI Hello World

The simplest possible example of talking to a Generative AI model:
send one question to an OpenAI LLM and print its answer.

Setup:
    1. pip install -r requirements.txt
    2. Set your API key as an environment variable:
       - Windows PowerShell:  $env:OPENAI_API_KEY = "sk-..."
       - Or create a ".env" file in the project root with:
         OPENAI_API_KEY=sk-...

Run:
    python src/openai_hello_world.py
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI

# Load OPENAI_API_KEY from a local .env file, if present.
load_dotenv()

MODEL = "gpt-4o-mini"


def ask_hello_world(question: str = "Hello! In one sentence, what is Generative AI?") -> str:
    """Send a single question to an OpenAI LLM and return its answer."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Set it as an environment variable or "
            "add it to a .env file before running this script."
        )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    question = "Hello! In one sentence, what is Generative AI?"
    print(f"Question: {question}\n")

    answer = ask_hello_world(question)
    print(f"Answer: {answer}")
