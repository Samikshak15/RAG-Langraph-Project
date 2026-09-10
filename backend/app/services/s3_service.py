import logging

import boto3
from app.config import (
   AWS_ACCESS_KEY_ID,
   AWS_SECRET_ACCESS_KEY,
   AWS_REGION,
   S3_BUCKET_NAME,
)

logger = logging.getLogger(__name__)

class S3Service:
   def __init__(self):
       self.bucket_name = S3_BUCKET_NAME
       self.client = boto3.client(
           "s3",
           region_name=AWS_REGION,
           aws_access_key_id=AWS_ACCESS_KEY_ID,
           aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
       )
       logger.info("S3Service initialized for bucket '%s' in region '%s'", self.bucket_name, AWS_REGION)

   def list_objects(self, prefix: str = ""):
       logger.info("Listing objects in bucket '%s' with prefix '%s'", self.bucket_name, prefix)
       paginator = self.client.get_paginator("list_objects_v2")
       contents = []
       for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
           contents.extend(page.get("Contents", []))
       logger.info("Found %d object(s)", len(contents))
       return contents

   def get_object(self, key: str) -> bytes:
       logger.info("Downloading object '%s'", key)

       response = self.client.get_object(
           Bucket=self.bucket_name,
           Key=key,
       )

       content = response["Body"].read()

       logger.info(
           "Downloaded '%s' (%d bytes)",
           key,
           len(content),
       )

       return content