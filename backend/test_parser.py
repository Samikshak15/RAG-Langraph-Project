# from app.ingestion.transcript_parser import parse_transcript
# from app.services.s3_service import S3Service


# def main():
#     s3 = S3Service()

#     objects = s3.list_objects(prefix="simulation_training/")
#     transcripts = [obj for obj in objects if obj["Key"].endswith("_transcript.txt")]

#     latest = max(transcripts, key=lambda obj: obj["LastModified"])
#     print(f"Parsing: {latest['Key']} (modified {latest['LastModified']})")

#     raw_text = s3.get_object(latest["Key"]).decode("utf-8")
#     turns = parse_transcript(raw_text)

#     print("\n" + "=" * 80)
#     print(f"PARSED {len(turns)} TURN(S)")
#     print("=" * 80)

#     for turn in turns:
#         print(f"[{turn['timestamp']}] {turn['speaker']}: {turn['text']}")

#     print("=" * 80)


# if __name__ == "__main__":
#     main()


from app.ingestion.transcript_parser import (
    parse_transcript,
    classify_agent_turn,
    extract_qa_pairs
)


def main():

    with open("data/sample_transcript.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()

    print("\n" + "#" * 100)
    print("RAW TRANSCRIPT")
    print("#" * 100)

    print(raw_text)

    turns = parse_transcript(raw_text)

    print(f"\nParsed {len(turns)} turns\n")

    for i, turn in enumerate(turns, start=1):

        if turn["speaker"] == "Agent":
            classification = classify_agent_turn(turn["text"])
        else:
            classification = "user_answer"

        print("=" * 80)
        print(f"TURN {i}")
        print("Speaker:", turn["speaker"])
        print("Type:", classification)
        print("Text:", turn["text"])

    qa_pairs = extract_qa_pairs(turns)

    print("\n")
    print("#" * 100)
    print(f"TOTAL Q&A PAIRS: {len(qa_pairs)}")
    print("#" * 100)

    for qa in qa_pairs:

        print("\n" + "=" * 100)

        print("Question ID:", qa["question_id"])
        print("Question:", qa["question"])
        print("Answer:", qa["answer"])

        print("Question Turn:", qa["question_turn"])
        print("Answer Turns:", qa["answer_turns"])


if __name__ == "__main__":
    main()