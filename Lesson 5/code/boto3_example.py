import boto3
s3 = boto3.client("s3")
bucket_name = "my-tomerbt-ai-bucket"
s3.create_bucket(Bucket=bucket_name)
