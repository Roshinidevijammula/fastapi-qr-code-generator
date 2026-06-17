import os
import boto3
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

print(f"Bucket: {S3_BUCKET}")
print(f"Region: {AWS_DEFAULT_REGION}")

try:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )
    # Try listing objects or checking bucket location to verify credentials
    response = s3.list_objects_v2(Bucket=S3_BUCKET, MaxKeys=1)
    print("S3 connection successful! Objects found:", "Contents" in response)
except Exception as e:
    print("S3 connection failed:", e)
