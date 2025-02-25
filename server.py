import os
import base64
import json
import random
from requests import get, post
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'Aerol'

# Load environment variables
load_dotenv()

# Get Spotify API credentials from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Function to fetch the token from Spotify
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


# Test the get_token function
token = get_token()
print(token)


# Serve the index.html file from the templates folder
@app.route('/')
def Home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
