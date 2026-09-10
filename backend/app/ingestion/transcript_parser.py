import re


TURN_PATTERN = re.compile(
    r"\[(?P<timestamp>[^\]]+)\]\s+"
    r"(?P<speaker>Agent|User):\s*"
    r"(?P<text>.*)"
)


def parse_transcript(raw_text: str):
    turns = []

    for line in raw_text.splitlines():
        line = line.strip()

        if not line:
            continue

        match = TURN_PATTERN.match(line)

        if match:
            turns.append({
                "timestamp": match.group("timestamp"),
                "speaker": match.group("speaker"),
                "text": match.group("text"),
            })
        elif turns:
            turns[-1]["text"] += " " + line

    return turns

def classify_agent_turn(text: str) -> str:
    """
    Classify an Agent turn as:
    - question
    - feedback
    - continuation
    - other
    """

    lower_text = text.lower().strip()

    continuation_patterns = [
        "please go ahead and continue",
        "please continue",
        "you were explaining",
        "go ahead and continue",
    ]

    feedback_patterns = [
        "that's a great",
        "that's an excellent",
        "that's a good",
        "excellent explanation",
        "very impressive",
        "that's a fantastic",
        "that's a very well-thought-out",
    ]

    for pattern in continuation_patterns:
        if pattern in lower_text:
            return "continuation"

    for pattern in feedback_patterns:
        if pattern in lower_text:
            return "feedback"

    if "?" in text:
        return "question"

    return "other"    

# def extract_qa_pairs(turns):
#     qa_pairs = []

#     current_question = None
#     current_question_turn = None
#     current_answer_parts = []
#     answer_turns = []

#     for index, turn in enumerate(turns):

#         if turn["speaker"] == "Agent":

#             turn_type = classify_agent_turn(turn["text"])

#             if turn_type == "question":

#                 # Save previous question if one exists
#                 if current_question is not None and current_answer_parts:
#                     qa_pairs.append({
#                         "question_id": f"Q{len(qa_pairs) + 1:03d}",
#                         "question": current_question,
#                         "answer": " ".join(current_answer_parts),
#                         "question_turn": current_question_turn,
#                         "answer_turns": answer_turns,
#                     })

#                 current_question = turn["text"]
#                 current_question_turn = index + 1
#                 current_answer_parts = []
#                 answer_turns = []

#         elif turn["speaker"] == "User":

#             if current_question is not None:
#                 current_answer_parts.append(turn["text"])
#                 answer_turns.append(index + 1)

#     # Save final question
#     if current_question is not None and current_answer_parts:
#         qa_pairs.append({
#             "question_id": f"Q{len(qa_pairs) + 1:03d}",
#             "question": current_question,
#             "answer": " ".join(current_answer_parts),
#             "question_turn": current_question_turn,
#             "answer_turns": answer_turns,
#         })

#     return qa_pairs    

# def extract_qa_pairs(turns):
#     qa_pairs = []

#     current_question = None
#     current_question_turn = None
#     current_answer_parts = []
#     answer_turns = []

#     for index, turn in enumerate(turns):

#         turn_number = index + 1

#         # --------------------------------------------------
#         # AGENT
#         # --------------------------------------------------
#         if turn["speaker"] == "Agent":

#             text = turn["text"].strip()

#             # Does this Agent message contain a question?
#             if "?" in text:

#                 # Save previous Q&A
#                 if current_question is not None and current_answer_parts:

#                     qa_pairs.append({
#                         "question_id": f"Q{len(qa_pairs) + 1:03d}",
#                         "question": current_question,
#                         "answer": " ".join(current_answer_parts),
#                         "question_turn": current_question_turn,
#                         "answer_turns": answer_turns.copy(),
#                     })

#                 # Start new question
#                 current_question = text
#                 current_question_turn = turn_number

#                 current_answer_parts = []
#                 answer_turns = []

#         # --------------------------------------------------
#         # USER
#         # --------------------------------------------------
#         elif turn["speaker"] == "User":

#             if current_question is not None:

#                 current_answer_parts.append(
#                     turn["text"].strip()
#                 )

#                 answer_turns.append(turn_number)

#     # ------------------------------------------------------
#     # SAVE FINAL Q&A
#     # ------------------------------------------------------

#     if current_question is not None and current_answer_parts:

#         qa_pairs.append({
#             "question_id": f"Q{len(qa_pairs) + 1:03d}",
#             "question": current_question,
#             "answer": " ".join(current_answer_parts),
#             "question_turn": current_question_turn,
#             "answer_turns": answer_turns.copy(),
#         })

#     return qa_pairs

def extract_qa_pairs(turns):
    qa_pairs = []

    current_question = None
    current_question_turn = None

    current_answer_parts = []
    answer_turns = []

    for index, turn in enumerate(turns):

        turn_number = index + 1

        # -----------------------------------------
        # AGENT TURN
        # -----------------------------------------
        if turn["speaker"] == "Agent":

            text = turn["text"].strip()

            question = extract_question(text)

            # No question in this Agent message
            if question is None:
                continue

            # Save previous Q&A
            if current_question is not None and current_answer_parts:

                qa_pairs.append({
                    "question_id": f"Q{len(qa_pairs) + 1:03d}",
                    "question": current_question,
                    "answer": " ".join(current_answer_parts),
                    "question_turn": current_question_turn,
                    "answer_turns": answer_turns.copy(),
                })

            # Start new question
            current_question = question
            current_question_turn = turn_number

            current_answer_parts = []
            answer_turns = []

        # -----------------------------------------
        # USER TURN
        # -----------------------------------------
        elif turn["speaker"] == "User":

            if current_question is not None:

                current_answer_parts.append(
                    turn["text"].strip()
                )

                answer_turns.append(turn_number)

    # -----------------------------------------
    # SAVE FINAL Q&A
    # -----------------------------------------

    if current_question is not None and current_answer_parts:

        qa_pairs.append({
            "question_id": f"Q{len(qa_pairs) + 1:03d}",
            "question": current_question,
            "answer": " ".join(current_answer_parts),
            "question_turn": current_question_turn,
            "answer_turns": answer_turns.copy(),
        })

    return qa_pairs
    
# def extract_question(text: str):
#     """
#     Extract the question portion from an Agent message.

#     Everything before the first question-ending '?' is treated
#     as possible interviewer feedback/context.
#     """

#     text = text.strip()

#     question_end = text.find("?")

#     if question_end == -1:
#         return None

#     # Find the beginning of the sentence containing the question.
#     before_question = text[:question_end + 1]

#     lines = before_question.split("\n")

#     # Usually the final line contains the actual question.
#     question = lines[-1].strip()

#     if not question:
#         return None

#     return question

# def extract_question(text: str):
#     """
#     Extract the actual interview question from an Agent message.

#     Agent messages can contain:
#         feedback + question

#     Example:
#         "That's a great answer.

#         Let's dive into PySpark.
#         Can you explain what PySpark is?"

#     Returns:
#         "Let's dive into PySpark. Can you explain what PySpark is?"
#     """

#     text = text.strip()

#     if "?" not in text:
#         return None

#     # Split the text into sentences.
#     sentences = re.split(
#         r'(?<=[.!?])\s+',
#         text
#     )

#     # Find the sentence containing the question mark.
#     question_sentences = []

#     for sentence in sentences:

#         sentence = sentence.strip()

#         if "?" in sentence:
#             question_sentences.append(sentence)

#     if not question_sentences:
#         return None

#     return " ".join(question_sentences)


def extract_question(text: str):
    """
    Extract the actual interview question from an Agent message.

    The Agent message may contain feedback followed by
    the actual interview question.
    """

    text = text.strip()

    if "?" not in text:
        return None

    # Split into sentences while preserving punctuation.
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    question_start = None

    for i, sentence in enumerate(sentences):

        sentence = sentence.strip()

        if "?" in sentence:

            # Look backwards for a sentence that introduces
            # the question, such as:
            # "Let's dive into PySpark."
            if i > 0:
                previous = sentences[i - 1].strip()

                if (
                    previous.lower().startswith(
                        (
                            "let's",
                            "now,",
                            "could you",
                            "can you",
                            "what",
                            "why",
                            "how",
                            "explain",
                            "tell me"
                        )
                    )
                ):
                    question_start = i - 1
                else:
                    question_start = i
            else:
                question_start = i

            break

    if question_start is None:
        return None

    question_sentences = sentences[question_start:]

    return " ".join(
        sentence.strip()
        for sentence in question_sentences
    )