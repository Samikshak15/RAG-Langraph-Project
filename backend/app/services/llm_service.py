from together import Together

from app.config import TOGETHER_API_KEY, TOGETHER_MODEL


class LLMService:

    def __init__(self):
        self.client = Together(
            api_key=TOGETHER_API_KEY
        )

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=TOGETHER_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content