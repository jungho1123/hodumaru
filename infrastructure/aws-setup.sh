#!/bin/bash
# aws-setup.sh
# Sets up AWS S3 bucket with private access and lifecycle rules for auto-deletion.
# Usage: ./aws-setup.sh <bucket-name>

BUCKET_NAME=$1
REGION="us-east-1" # Change as needed

if [ -z "$BUCKET_NAME" ]; then
    echo "Usage: $0 <bucket-name>"
    exit 1
fi

echo "Creating S3 bucket: $BUCKET_NAME in $REGION..."

# Create Bucket
if aws s3api create-bucket --bucket "$BUCKET_NAME" --region "$REGION"; then
    echo "Bucket created (or already exists)."
else
    echo "Failed to create bucket. Ensure AWS CLI is configured and name is unique."
    exit 1
fi

# Block Public Access (Security Best Practice)
echo "Blocking public access..."
aws s3api put-public-access-block \
    --bucket "$BUCKET_NAME" \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Set Lifecycle Rule (Delete after 48 hours = 2 days)
echo "Setting lifecycle rule (48 hours expiration)..."
aws s3api put-bucket-lifecycle-configuration \
    --bucket "$BUCKET_NAME" \
    --lifecycle-configuration '{
        "Rules": [
            {
                "ID": "DeleteTempImages",
                "Status": "Enabled",
                "Filter": {
                    "Prefix": ""
                },
                "Expiration": {
                    "Days": 2
                }
            }
        ]
    }'

echo "AWS S3 Setup Complete for $BUCKET_NAME"
