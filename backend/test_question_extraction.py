from app.ingestion.transcript_parser import (
    parse_transcript,
    extract_question,
)


with open(
    "data/sample_transcript.txt",
    "r",
    encoding="utf-8"
) as f:
    raw_text = f.read()


turns = parse_transcript(raw_text)


for index, turn in enumerate(turns, start=1):

    if turn["speaker"] != "Agent":
        continue

    question = extract_question(
        turn["text"]
    )

    if question:

        print("\n" + "=" * 100)
        print("TURN:", index)
        print("QUESTION:")
        print(question)