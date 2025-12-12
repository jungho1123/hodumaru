import json
import logging
import os
import hmac
import hashlib

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Handles Meta Data Deletion Callback.
    1. GET: Verification Request (if implemented via purely webhook, though deletion callback is usually POST)
    2. POST: Data Deletion Request
    """
    method = event.get('httpMethod')
    
    if method == 'POST':
        return handle_deletion_request(event)
    
    return {
        'statusCode': 405,
        'body': json.dumps({'error': 'Method not allowed'})
    }

def handle_deletion_request(event):
    try:
        body = json.loads(event.get('body', '{}'))
        user_id = body.get('user_id')
        
        # Parse signed request if necessary (Meta sends a signed_request field)
        # For this template, we simulate immediate successful deletion.
        
        logger.info(f"Received deletion request for user: {user_id}")
        
        # Generate a confirmation code (can be anything unique)
        confirmation_code = f"del_{user_id}_{context.aws_request_id}"
        
        # Verify the request signature (Optional but recommended for production)
        # app_secret = os.environ.get('APP_SECRET')
        # ... logic to verify signed_request ...

        # In a real scenario, you would delete user data from DB/S3 here.
        # delete_user_data(user_id)

        # Return the URL where the user can view the status of their deletion
        # This URL must be accessible publicly strictly for compliance check
        status_url = f"https://{event['headers']['Host']}/deletion-status?code={confirmation_code}"

        response_data = {
            "url": status_url,
            "confirmation_code": confirmation_code
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        logger.error(f"Error processing deletion: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
