from app.services.s3_service import S3Service


def main():
    s3 = S3Service()

    objects = s3.list_objects(prefix="simulation_training/")
    transcripts = [obj for obj in objects if obj["Key"].endswith("_transcript.txt")]

    latest = max(transcripts, key=lambda obj: obj["LastModified"])

    print(f"Latest transcript: {latest['Key']} (modified {latest['LastModified']})")

    content = s3.get_object(latest["Key"])

    print("\n" + "=" * 80)
    print("RAW TRANSCRIPT")
    print("=" * 80)

    print(content.decode("utf-8"))

    print("=" * 80)


if __name__ == "__main__":
    main()
