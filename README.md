# AWS S3 File Manager

A small Python command-line tool for managing files in an Amazon S3 bucket. Built as my first AWS project to practice `boto3`, S3, and basic cloud security.

## Features

- **List** objects in a bucket
- **Upload** a local file
- **Download** an object
- **Delete** an object
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

# Override the bucket for one command
python3 s3_file_manager.py --bucket another-bucket list
```

## What I learned

1. **S3 basics** — buckets, object keys, and how objects are stored by key rather than by folder.
2. **boto3** — creating a client, calling `list_objects_v2`, `upload_file`, `download_file`, and `delete_object`.
3. **Error handling** — catching `ClientError` instead of letting a stack trace crash the script.
4. **Credentials** — keeping access keys out of source code and using environment variables / AWS CLI configuration.
5. **Bucket security** — keeping Block Public Access enabled and using a private bucket.

## Notes

- The bucket in this project is private. No public access is enabled.
- `s3-demo.txt` is a sample file used for testing.
- This is a learning project, not production tooling.

---

*Built as part of my Software Engineering learning journey at SSUET.*
