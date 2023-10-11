from flask import Flask, jsonify
import requests
import os
import logging
from functools import lru_cache
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Access the access_token from the environment
access_token = os.getenv('')

# Add logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Use lru_cache as a simple caching mechanism
@lru_cache(maxsize=100)
def get_profile_data_from_api():
    # Get user ID
    response = requests.get(f'https://graph.instagram.com/me?fields=id&access_token={access_token}')
    if response.status_code == 200:
        user_id = response.json()['id']
    else:
        app.logger.error('Failed to get user ID from Instagram API')
        return None

    # Get profile data
    response = requests.get(f'https://graph.instagram.com/{user_id}?fields=id,username,account_type,media_count,followers_count&access_token={access_token}')

    if response.status_code == 200:
        profile_data = response.json()
        return profile_data
    else:
        app.logger.error('Failed to retrieve profile data from Instagram API')
        return None

@app.route('/')
def index():
    return 'Redirection is Successful'

@app.route('/profile_data')
def get_profile_data():
    profile_data = get_profile_data_from_api()
    if profile_data is not None:
        return jsonify(profile_data)
    else:
        return 'Error: Could not retrieve profile data'

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8080)
