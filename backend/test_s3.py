import logging

from app.services.s3_service import S3Service

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

if __name__ == "__main__":
    service = S3Service()
    objects = service.list_objects()
    for obj in objects:
        print(obj["Key"])
