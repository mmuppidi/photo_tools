"""Module for functions to help with archiving images and pushing them to s3
"""

import logging
import os
import tarfile
import boto3
import botocore
from boto3.s3.transfer import TransferConfig

logger = logging.getLevelName(__name__)


def archive_directory(directory: str, tarfile_path: str):
    """Helper function to archive a directory 

    Args:
        directory (str): Directory to archive 
        tarfile_path (str): path to save the archive to
    """
    logging.info(f"Creating an archive for {directory} at {tarfile_path}")
    with tarfile.open(tarfile_path, "w:gz") as tar:
        tar.add(directory, arcname=os.path.basename(directory))


def push_to_s3(source: str, bucket: str, path: str):
    """Pushes a file to s3 and uses multipart upload if necessary

    Args:
        source (str): file to be pushed to s3
        bucket (str): s3 bucket to push to
        path (str): s3 key to save the file to
    """
    s3 = boto3.resource("s3")

    GB = 1024 ** 3

    # Ensure that multipart uploads only happen if the size of a transfer
    # is larger than S3's size limit for nonmultipart uploads, which is 5 GB.
    config = TransferConfig(multipart_threshold=5 * GB)
    count = 1
    logging.info(f"Uploading {source} to s3://{bucket}/{path}")
    while count <= 10:
        try:
            s3.meta.client.upload_file(
                source, bucket, path, Config=config,
            )
            break
        except botocore.exceptions.EndpointConnectionError:
            logger.error("Network Error: Please Check your Internet Connection")
        except Exception as e:
            logger.error(e)

        logging.info(f"Attempt {count}:Failed uploding retrying again..")
        count += 1


def generate_presigned_url(
    bucket: str, key: str, expires_in: int = 604800
) -> str:
    """Generates a presigned URL for a key in s3 

    Args:
        bucket (str): bucket where the object exists
        key (str): key of the object
        expires_in (int, optional): expiration time in seconds from the time
            of creation. Defaults to 604800.

    Returns:
        str: presigned url that expires in `expires_in` seconds
    """
    s3_client = boto3.client("s3")
    response = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    logging.info(f"Archive presigned url: {response}")
    logging.info(f"URL expires in {((expires_in/60.0)/60.0)/24.0} days")
    return response
