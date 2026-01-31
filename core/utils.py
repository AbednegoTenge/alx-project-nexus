import boto3
from django.conf import settings


def generate_resume_url(key, expires=3600):
    """
    Generate a presigned URL for downloading a resume from S3
    
    Args:
        key (str): The S3 object key (file path in bucket)
        expires (int): URL expiration time in seconds (default: 1 hour)
    
    Returns:
        str: Presigned URL for downloading the file
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    
    presigned_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": key
        },
        ExpiresIn=expires
    )
    
    return presigned_url