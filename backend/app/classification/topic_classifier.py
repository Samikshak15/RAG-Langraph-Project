# import json
# from pathlib import Path


# class TopicClassifier:
#     def __init__(self, curriculum_path: str):
#         self.curriculum_path = Path(curriculum_path)

#         with open(self.curriculum_path, "r", encoding="utf-8") as f:
#             self.curriculum = json.load(f)

#     def get_topics(self) -> list[dict]:
#         return self.curriculum


import json

from app.services.llm_service import LLMService


class TopicClassifier:

    def __init__(self, curriculum_path: str):
        self.llm = LLMService()

        with open(curriculum_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.topics = data["topics"]

    def get_topics(self) -> list[dict]:
        return self.topics

    def classify(self, question: str, answer: str) -> dict:

        curriculum = json.dumps(
            self.topics,
            indent=2
        )

        prompt = f"""
You are an interview topic classifier.

Your task is to classify the interview question and candidate answer
into exactly ONE topic and ONE subtopic from the provided curriculum.

The candidate's answer is a speech-to-text transcription and will contain
phonetic misspellings of technical terms. Interpret these by sound before
classifying — for example "rack based" likely means "RAG-based", "victor
database" likely means "vector database", and "llama's judge" or "lamas
judge" likely means "Llama Guard" (a guardrail/content-safety model), not
"LLM-as-judge". Always consider what a technical term sounds like, not
just its literal spelling, and use the surrounding context of the answer
to disambiguate which real term a phonetic misspelling stands for.

STEP 1 — Pick the topic whose overall subject most closely matches what
the question and answer are actually discussing. If the question is broad
or generic but the answer names a specific technique, tool, or concept
from the curriculum (after accounting for transcription misspellings),
prefer the topic that matches that specific concept over a topic that
only matches the generic framing of the question — the answer's specific
technical content outweighs the question's wording.

STEP 2 — Within that topic, read every subtopic listed and pick the SINGLE
subtopic that is the most specific match to what is actually discussed.
Do not default to the first subtopic, or to whichever subtopic you most
recently picked for a previous question, just because the topic is
correct — re-read all of that topic's subtopics each time and choose the
one that best fits this specific question and answer.

FALLBACK RULE:
Use this fallback ONLY when the question and answer are about a subject
entirely absent from the curriculum below — for example: general career
questions, soft skills, project-management process, generic
architectural decision-making that is not tied to any specific concept
in the curriculum (e.g. "how do you choose between frameworks/models" in
the abstract, with no concrete technique named), or predictions/opinions
about future industry trends. Do NOT use this fallback for a question
that describes a real technical problem, challenge, or system behavior
involving concepts that ARE in the curriculum (such as debugging an
agent-based system, or explaining a design tradeoff) — those should
still be matched to their closest topic and subtopic. Return exactly:

{{
  "topic": "not_covered",
  "subtopic": "not_covered"
}}

IMPORTANT RULES:
1. Use ONLY topics and subtopics from the curriculum, or the
   "not_covered" fallback above.
2. Do not invent a new topic.
3. Do not invent a new subtopic.
4. Consider both the question and candidate answer.
5. Return JSON only.
6. Do not include markdown or explanations.

CURRICULUM:
{curriculum}

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Return exactly:

{{
  "topic": "topic from curriculum, or not_covered",
  "subtopic": "subtopic from curriculum, or not_covered"
}}
"""

        response = self.llm.generate(prompt)

        try:
            result = json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"LLM returned invalid JSON: {response}"
            ) from e

        return result