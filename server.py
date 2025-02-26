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
# token = get_token()
# print(token)

# Function to get authorization header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



#FUNCTION TO SEARCH FOR AN ARTIST

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]   

    if len(json_result) == 0:
        print("No artist found")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]

    return json_result

token = get_token()
result = search_artist(token, "Ariana Grande")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
    
# To get the list of the artist's songs

for idx, songs in enumerate(songs):
    print(f"{idx + 1}. {songs['name']}")
else:
    print("Artist not found")


def get_artist_Image(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/images?country=US?limit=1"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result["images"][0]["url"]




@app.route('/')
def Home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
