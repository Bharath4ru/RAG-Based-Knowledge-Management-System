import boto3
from botocore.exceptions import ClientError
from config import Config

class S3Storage:
    def __init__(self):
        if not Config.AWS_ACCESS_KEY or not Config.AWS_SECRET_KEY or not Config.AWS_BUCKET_NAME:
            raise ValueError("Missing AWS credentials. Check your .env file.")

        self.s3 = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY
        )
        self.bucket = Config.AWS_BUCKET_NAME

    def upload_file(self, file_obj, filename):
        """Uploads a file object to S3."""
        try:
            self.s3.upload_fileobj(file_obj, self.bucket, filename)
            print(f"File '{filename}' uploaded successfully to S3.")
            return True
        except ClientError as e:
            print(f"Error uploading file '{filename}': {e}")
            return False

    def get_file(self, filename):
        """Retrieves a file from S3 as a stream."""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=filename)
            print(f"File '{filename}' retrieved successfully from S3.")
            return response['Body'].read()  # Read the content of the file
        except ClientError as e:
            print(f"Error retrieving file '{filename}': {e}")
            return None
