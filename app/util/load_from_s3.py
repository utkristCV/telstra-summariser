import boto3
import logging
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)

def load_prompt_data(bucket: str, key: str):
    s3 = boto3.client("s3")

    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj["Body"].read()

        if not body:
            raise ValueError("S3 object is empty")
        
        data = body.decode('utf-8').strip()

        if not data:
            raise ValueError("Text file is empty or invalid")

        logger.info(f"Prompt data loaded successfully from S3: {bucket}/{key}")
        return data

    except ClientError as e:
        # S3 service-related errors (e.g. NoSuchBucket, NoSuchKey, AccessDenied)
        logger.error(f"S3 ClientError while accessing: {bucket}/{key}: {e}")
        raise

    except (BotoCoreError, ValueError) as e:
        # Other boto3 core issues or empty file
        logger.error(f"Failed to load Prompt data from: {bucket}/{key}: {e}")
        raise

    except Exception as e:
        # Catch-all fallback
        logger.exception(f"Unexpected error loading Prompt data from: {bucket}/{key}")
        raise
