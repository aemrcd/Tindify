import os
import base64
import json
import random
import requests
from requests import get, post
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
import requests



# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("Flask_key")

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

# def search_artist(token, artist_name):
#     url = "https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     query = f"?q={artist_name}&type=artist&limit=1"

#     query_url = url + query
#     result = get(query_url, headers=headers)
#     json_result = json.loads(result.content)["artists"]["items"]   

#     if len(json_result) == 0:
#         print("No artist found")
#         return None
    
#     return json_result[0]

# def get_songs_by_artist(token, artist_id):
#     url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)["tracks"]

#     return json_result

# token = get_token()
# result = search_artist(token, "Kendrick Lamar")
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)
    
# # To get the list of the artist's songs

# for idx, songs in enumerate(songs):
#     print(f"{idx + 1}. {songs['name']}")
# else:
#     print("Artist not found")


# def get_artist_Image(token, artist_id):
#     url = f"https://api.spotify.com/v1/artists/{artist_id}/images?country=US?limit=1"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)
#     return json_result["images"][0]["url"]


def get_popular_artists(token):
    # Fetch a list of popular artists from Spotify (e.g., from a playlist or chart)
    url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF"  # Spotify's "Top 50 Global" playlist
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    data = response.json()

    if "tracks" not in data:
        return []

    # Extract unique artist names from the playlist
    artists = set()
    for track in data["tracks"]["items"]:
        for artist in track["track"]["artists"]:
            artists.add(artist["name"])
    return list(artists)

@app.route('/get_artist_info')
def get_artist_info():
    token = get_token()

    # Fetch a list of popular artists
    artists = get_popular_artists(token)
    if not artists:
        return jsonify({"error": "No artists found"}), 404

    # Select a random artist from the list
    artist_name = random.choice(artists)
    artist = search_artist(token, artist_name)

    if not artist:
        return jsonify({"error": "Artist not found"}), 404

    artist_id = artist["id"]
    artist_image = artist["images"][0]["url"] if artist["images"] else None

    # Get the top track of the artist
    top_track = get_top_track(token, artist_id)
    if not top_track:
        return jsonify({"error": "No tracks found"}), 404

    track_id = top_track["id"]
    track_name = top_track["name"]

    return jsonify({
        "artist_name": artist_name,
        "artist_image": artist_image,
        "track_id": track_id,
        "track_name": track_name
    })

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    return json_result[0] if json_result else None

def get_top_track(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

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


def fetch_artist_image(artist_name):
    if not artist_name:
        return None, "No artist name provided"
    
    # Fetch the Spotify access token
    access_token = get_token()
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = get_auth_header(access_token)
    
    # Make the request to the Spotify API
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, "Failed to fetch artist data"
    
    data = response.json()
    
    # Check if artist data exists
    if data.get("artists", {}).get("items"):
        artist = data["artists"]["items"][0]
        # Get the artist image URL
        artist_image = artist["images"][0]["url"] if artist["images"] else None
        return artist_image, None

    return None, "Artist not found"

@app.route('/')
def Home():
    return render_template('index.html')


@app.route('/Home')
def HomePage():
    artist_name = request.args.get("artist", "Kendrick Lamar")
    artist_image, error = fetch_artist_image(artist_name)

    if error:
        return render_template("Home.html", error=error)
    
    return render_template("Home.html", image_url=artist_image, artist_name=artist_name)




if __name__ == "__main__":
    app.run(debug=True)
