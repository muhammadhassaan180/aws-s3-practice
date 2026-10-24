#!/usr/bin/env python3
"""Small S3 file manager for practice.

Usage:
    python3 s3_file_manager.py list
    python3 s3_file_manager.py upload <local-file> [key]
    python3 s3_file_manager.py download <key> <local-file>
    python3 s3_file_manager.py delete <key>

The bucket comes from --bucket or the S3_BUCKET environment variable.
"""

import argparse
import os
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


def get_client():
    """Create an S3 client using the region from the environment."""
    region = os.environ.get("AWS_DEFAULT_REGION") or os.environ.get("AWS_REGION")
    if region:
        return boto3.client("s3", region_name=region)
    return boto3.client("s3")


def list_objects(s3, bucket):
    response = s3.list_objects_v2(Bucket=bucket)
    contents = response.get("Contents", [])

    if not contents:
        print(f"No objects in '{bucket}'.")
        return

    print(f"Objects in '{bucket}':")
    for obj in contents:
        size = obj["Size"]
        modified = obj["LastModified"].strftime("%Y-%m-%d %H:%M")
        print(f"  {obj['Key']:<40} {size:>8} bytes  {modified}")


def upload_file(s3, bucket, path, key=None):
    path = Path(path)
    if not path.is_file():
        sys.exit(f"File not found: {path}")

    key = key or path.name
    s3.upload_file(str(path), bucket, key)
    print(f"Uploaded '{path}' to s3://{bucket}/{key}")


def download_file(s3, bucket, key, destination):
    s3.download_file(bucket, key, destination)
    print(f"Downloaded s3://{bucket}/{key} to '{destination}'")


def delete_object(s3, bucket, key):
    s3.delete_object(Bucket=bucket, Key=key)
    print(f"Deleted s3://{bucket}/{key}")


def main():
    parser = argparse.ArgumentParser(description="Small S3 file manager")
    parser.add_argument(
        "--bucket",
        default=os.environ.get("S3_BUCKET"),
        help="S3 bucket name (or set the S3_BUCKET environment variable)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List objects in the bucket")

    upload_parser = subparsers.add_parser("upload", help="Upload a file")
    upload_parser.add_argument("file", help="Path to the local file")
    upload_parser.add_argument("key", nargs="?", help="Object key (default: file name)")

    download_parser = subparsers.add_parser("download", help="Download an object")
    download_parser.add_argument("key", help="Object key in the bucket")
    download_parser.add_argument("file", help="Where to save the file")

    delete_parser = subparsers.add_parser("delete", help="Delete an object")
    delete_parser.add_argument("key", help="Object key in the bucket")

    args = parser.parse_args()

    if not args.bucket:
        parser.error("Provide --bucket or set the S3_BUCKET environment variable")

    s3 = get_client()

    try:
        if args.command == "list":
            list_objects(s3, args.bucket)
        elif args.command == "upload":
            upload_file(s3, args.bucket, args.file, args.key)
        elif args.command == "download":
            download_file(s3, args.bucket, args.key, args.file)
        elif args.command == "delete":
            delete_object(s3, args.bucket, args.key)
    except ClientError as error:
        print(f"AWS error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
