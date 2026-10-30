# AWS S3 File Manager

A small Python command-line tool for managing files in an Amazon S3 bucket. Built as my first AWS project to practice `boto3`, S3, and basic cloud security.

## Features

- **List** objects in a bucket
- **Upload** a local file
- **Download** an object
- **Delete** an object
- **Share** an object with a temporary presigned URL
- Clear error messages for AWS failures

## Requirements

- Python 3.10+
- `boto3`
- An AWS account with an S3 bucket

## Setup

### Option A: AWS CloudShell (no access keys)

1. Open **CloudShell** in the AWS Management Console.
2. Upload `s3_file_manager.py` using **Actions → Upload file**.
3. Install `boto3` if it is not already available:

   ```bash
   python3 -m pip install --user boto3
   ```

4. Set your bucket and region:

   ```bash
   export S3_BUCKET="your-bucket-name"
   export AWS_DEFAULT_REGION="ap-southeast-2"
   ```

5. Run a command:

   ```bash
   python3 s3_file_manager.py list
   ```

### Option B: Local machine

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure AWS credentials with the AWS CLI:

   ```bash
   aws configure
   ```

   Use an IAM user with access to the bucket, not your root account. Never commit access keys.

4. Set the bucket name:

   ```bash
   export S3_BUCKET="your-bucket-name"
   ```

## Usage

```bash
# List objects
python3 s3_file_manager.py list

# Upload a file (uses the file name as the object key)
python3 s3_file_manager.py upload s3-demo.txt

# Upload with a custom key
python3 s3_file_manager.py upload s3-demo.txt practice/s3-demo.txt

# Download an object
python3 s3_file_manager.py download s3-demo.txt downloaded-s3-demo.txt

# Delete an object
python3 s3_file_manager.py delete s3-demo.txt

# Create a temporary download link (default: 10 minutes)
python3 s3_file_manager.py share s3-demo.txt

# Create a link valid for 60 seconds
python3 s3_file_manager.py share s3-demo.txt --expires 60

# Override the bucket for one command
python3 s3_file_manager.py --bucket another-bucket list
```

## Static website

A one-page personal site lives in [`static-site/`](static-site/) and is hosted on S3:

**http://hassaan-static-site-2026.s3-website-ap-southeast-2.amazonaws.com**

The bucket is public because static website hosting requires it. Only public content belongs there.

To update the site, upload the files from `static-site/` to the bucket and refresh the page.

## What I learned

1. **S3 basics** — buckets, object keys, and how objects are stored by key rather than by folder.
2. **boto3** — creating a client, calling `list_objects_v2`, `upload_file`, `download_file`, `delete_object`, and `generate_presigned_url`.
3. **Presigned URLs** — giving temporary access to a private object without making the bucket public.
4. **Error handling** — catching `ClientError` instead of letting a stack trace crash the script.
5. **Credentials** — keeping access keys out of source code and using environment variables / AWS CLI configuration.
6. **Bucket security** — keeping the file-manager bucket private while using a separate public bucket for the static site.
7. **Static website hosting** — S3 website endpoints, index/error documents, bucket policies, and public access settings.

## Notes

- The file-manager bucket (`my-s3-practice-2026-1234`) is private. No public access is enabled.
- The static-site bucket (`hassaan-static-site-2026`) is public by design because it hosts the website.
- A presigned URL grants temporary access to anyone who has the link, until it expires. Treat it like a password.
- `s3-demo.txt` is a sample file used for testing.
- This is a learning project, not production tooling.

---

*Built as part of my Software Engineering learning journey at SSUET.*
