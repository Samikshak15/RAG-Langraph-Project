from app.services.s3_service import S3Service

def inspect():
    s3 = S3Service()
    for uid in ["1", "1086", "1103", "1236"]:
        prefix = f"simulation_training/{uid}/"
        objs = s3.list_objects(prefix=prefix)
        transcripts = [o for o in objs if o["Key"].endswith("_transcript.txt")]
        print(f"User ID: {uid} | Total S3 Objs: {len(objs)} | Transcript Objs: {len(transcripts)}")
        for t in transcripts[:3]:
            print(f"   -> {t['Key']}")

if __name__ == "__main__":
    inspect()
