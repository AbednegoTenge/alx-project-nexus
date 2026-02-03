import boto3
from django.conf import settings
from django.core.mail import send_mail
import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


logger = logging.getLogger(__name__)

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


def send_email(email_address, subject, body, html=True):
    """
    Sends an email to the specified address.
    """

    
    try:
        if html:
            message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=email_address,
                subject=subject,
                html_content=body
            )
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            logger.info(response.status_code)
            logger.info(response.body)
            logger.info(response.headers)
        else:
            message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=[email_address],
                subject=subject,
                plain_text_content=body
            )
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            logger.info(response.status_code)
            logger.info(response.body)
            logger.info(response.headers)
        logger.info(f"Email sent successfully to {email_address}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {email_address}: {str(e)}")
        return False