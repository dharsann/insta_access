from flask import Flask, jsonify, request, render_template
import requests
import os
import logging
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Access the access token from the environment
access_token = os.getenv('ACCESS_TOKEN')

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

@app.route('/')
def home():
    return render_template('redirect.html')

@app.route('/profile')
def get_instagram_profile_data():
    try:
        # Get user ID
        user_id = get_user_id()

        if user_id:
            profile_data = get_user_profile(user_id)
            if profile_data:
                return jsonify(profile_data)
            else:
                raise Exception('Failed to retrieve profile data from Instagram API')
        else:
            raise Exception('Failed to get user ID from Instagram API')

    except Exception as e:
        # Log the error and return an error response
        app.logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)})

def get_user_id():
    response = requests.get(f'https://graph.instagram.com/v13.0/me?fields=id&access_token={access_token}')
    if response.status_code == 200:
        return response.json().get('id')
    return None

def get_user_profile(user_id):
    response = requests.get(f'https://graph.instagram.com/v13.0/{user_id}?fields=id,username,account_type,media_count,followers_count&access_token={access_token}')
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == '__main__':
    app.run(port=1111, debug=True)
