"""
Answer evaluation for Phase 4.5.

Given a question, answer, and (optionally) its classified topic/subtopic,
produces a single structured evaluation: score, strengths, weaknesses,
missing_concepts, and feedback — in one LLM reasoning pass rather than
separate calls, so the qualitative judgments stay consistent with the
numeric score.
"""

import json

from app.services.llm_service import LLMService


class AnswerEvaluator:

    def __init__(self):
        self.llm = LLMService()

    def evaluate(
        self,
        question: str,
        answer: str,
        topic: str | None = None,
        subtopic: str | None = None,
    ) -> dict:

        topic = topic or "not_covered"
        subtopic = subtopic or "not_covered"

        if topic == "not_covered":
            grounding = """
This question/answer falls outside the interview curriculum, so there is
no specific topic or subtopic to grade against. Judge the answer purely
on general technical communication quality: correctness of any claims
made, clarity, depth of reasoning, and relevance to the question asked.
Do not penalize the candidate for the question being off-curriculum.
"""
        else:
            grounding = f"""
This question/answer has been classified under:
  Topic: {topic}
  Subtopic: {subtopic}

Use this ONLY as background context for identifying missing_concepts —
i.e. specific concepts from this subject area a strong answer could
plausibly have included. Do NOT use it to penalize the candidate for
omitting anything the question did not ask about, explicitly or
implicitly. Judge score, strengths, and weaknesses strictly against what
the question actually asked and what the candidate actually said — never
against a checklist of everything the subtopic could theoretically cover.
"""

        prompt = f"""
You are an expert technical interview evaluator.

Your task is to evaluate a candidate's answer to a single interview
question and return a structured evaluation.

The candidate's answer is a speech-to-text transcription and will
contain phonetic misspellings of technical terms. Interpret these by
sound before judging content — for example "rack based" likely means
"RAG-based", "victor database" likely means "vector database". Judge the
candidate on what they clearly meant, not on transcription artifacts,
and do not penalize the score for STT spelling errors.

{grounding}

SCORING RUBRIC (integer 0-10):
- 0-2: No real understanding demonstrated; answer is missing, off-topic,
  or fundamentally incorrect.
- 3-4: Partial or confused understanding; significant gaps or errors.
- 5-6: Adequate baseline understanding; correct but shallow or missing
  useful detail.
- 7-8: Strong, clear, mostly correct answer with good reasoning.
- 9-10: Excellent, expert-level answer; correct, well-reasoned, and
  demonstrates nuance or practical depth beyond the minimum expected.

For STRENGTHS and WEAKNESSES: identify specific, concrete points drawn
from what the candidate actually said. Do not restate generic praise or
criticism that could apply to any answer.

For MISSING_CONCEPTS: list specific concepts, terms, or considerations a
strong answer to THIS QUESTION would have included but this answer did
not mention. Leave this empty if the answer is already thorough.

MISSING CONCEPT RULES:

Only list a missing concept if it is directly required by the
interview question or expected answer and the candidate failed
to demonstrate it.

Do NOT use the curriculum topic or subtopic as evidence that a
concept is missing.

Never copy, repeat, or lightly paraphrase the topic name or
subtopic name as a missing concept.

For example:
- If the subtopic is "Agent loops", do not automatically say
  "agent loops" is missing.
- If the subtopic is "Serverless deployment", do not automatically
  say "serverless deployment specifics" is missing.

Identify the actual technical concept that the candidate failed
to explain based on the question.

If there is no clearly identifiable missing concept, return:
"missing_concepts": []

Distinguish these two cases:

Case 1 — Question asks about X, candidate explains X correctly.
Do NOT invent missing concepts just because the topic/subtopic
suggests related ideas exist. An answer that fully addresses what
was asked has no missing concepts.

Case 2 — Question asks about X, Y, and Z (multiple parts), and the
candidate only explains X. Y and Z are legitimate missing concepts,
because the question itself asked for them and the candidate did
not address them.

For FEEDBACK: 1-3 sentences of actionable improvement advice directed at
the candidate.

IMPORTANT RULES:
1. Return JSON only.
2. Do not include markdown or explanations outside the JSON.
3. score must be an integer from 0 to 10.
4. strengths, weaknesses, missing_concepts must be arrays of strings
   (use an empty array if there is nothing to list).

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Return exactly:

{{
  "score": <integer 0-10>,
  "strengths": ["...", ...],
  "weaknesses": ["...", ...],
  "missing_concepts": ["...", ...],
  "feedback": "..."
}}
"""

        response = self.llm.generate(prompt)

        try:
            result = json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"LLM returned invalid JSON: {response}"
            ) from e

        result["counts_toward_score"] = topic != "not_covered"

        return result
