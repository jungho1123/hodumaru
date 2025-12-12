import json
import boto3
import os
import base64
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    """
    1. Receives image data (base64) or download URL.
    2. Uploads to S3 Private Bucket.
    3. Generates Presigned URL (valid 15 mins).
    4. Returns URL.
    """
    try:
        body = json.loads(event.get('body', '{}'))
        image_data = body.get('image_base64') # Assuming base64 for simplicity
        image_name = body.get('filename', str(uuid.uuid4()) + ".jpg")
        
        if not BUCKET_NAME:
            raise Exception("BUCKET_NAME environment variable not set")

        if not image_data:
             return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No image_base64 provided'})
            }

        # Decode and Upload
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=image_name,
            Body=base64.b64decode(image_data),
            ContentType='image/jpeg' 
        )

        # Generate Presigned URL
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': image_name},
            ExpiresIn=900 # 15 minutes
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                's3_key': image_name,
                'presigned_url': url
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
