from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
import os

app = Flask(__name__)

# REPLACE THESE OR SET ENV VARS
APP_ID = os.environ.get('META_APP_ID', 'YOUR_APP_ID_HERE')
APP_SECRET = os.environ.get('META_APP_SECRET', 'YOUR_APP_SECRET_HERE')
REDIRECT_URI = os.environ.get('REDIRECT_URI', 'https://localhost:5000/callback') # Must match ngrok if used

@app.route('/')
def home():
    """Renders the login page with Facebook SDK or manual flow."""
    return render_template('index.html', app_id=APP_ID, redirect_uri=REDIRECT_URI)

@app.route('/privacy')
def privacy():
    """Compliance: Privacy Policy Page."""
    return render_template('privacy.html')

@app.route('/tos')
def tos():
    """Compliance: Terms of Service Page."""
    return render_template('tos.html')

@app.route('/callback')
def callback():
    """Handles the OAuth2 redirect, exchanges code for access token."""
    code = request.args.get('code')
    if not code:
        return "Error: No code received", 400

    # Exchange code for token
    token_url = (
        f"https://graph.facebook.com/v18.0/oauth/access_token?"
        f"client_id={APP_ID}&redirect_uri={REDIRECT_URI}&client_secret={APP_SECRET}&code={code}"
    )
    
    try:
        resp = requests.get(token_url)
        data = resp.json()
        access_token = data.get('access_token')
        
        # In a real app, we would exchange this for a long-lived token here
        return f"<h1>Success!</h1><p>Access Token: {access_token}</p><p>Copy this to your n8n credentials or DB.</p>"
    except Exception as e:
        return f"Error exchanging token: {str(e)}", 500

@app.route('/deletion-status')
def deletion_status():
    """
    Compliance: User Data Deletion Status Tracker.
    This is where the user lands when clicking the URL from the Deletion Callback.
    """
    code = request.args.get('code')
    return render_template('deletion_status.html', code=code)

@app.route('/deletion-callback', methods=['POST', 'GET'])
def deletion_callback():
    """
    Simulation of the Lambda 'Data Deletion URL'.
    Meta calls this when a user removes the app.
    """
    # 1. Verification Request (GET)
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        if challenge:
            return challenge
        return "Verification Endpoint", 200

    # 2. Deletion Request (POST)
    try:
        # In production, you MUST parse 'signed_request' form field
        # For local test, we accept simple JSON
        user_id = "test_user"
        
        # If real signed_request exists, logic would go here
        if 'signed_request' in request.form:
            # decode_signed_request(request.form['signed_request'])
            pass

        confirmation_code = f"del_{user_id}_local"
        
        # Logic to delete user from local DB would go here
        # db.delete_user(user_id)

        status_url = f"{request.url_root}deletion-status?code={confirmation_code}"

        return jsonify({
            "url": status_url,
            "confirmation_code": confirmation_code
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':

    # Running on 5000
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')
