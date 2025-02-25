import os
import base64
import json
import random
from requests import get, post
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

def get_random_song(token):
    # Choose a random genre or artist to fetch
    genres = ['pop', 'rock', 'hip-hop', 'indie', 'jazz', 'classical']
    genre = random.choice(genres)
    print(f"Selected genre: {genre}")
    
    # Use Spotify's Browse API to get a random song from a genre
    url = f"https://api.spotify.com/v1/recommendations?seed_genres={genre}&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Making API request to: {url}")
    
    response = get(url, headers=headers)
    print(f"API response status code: {response.status_code}")
    
    # Extract song data from the response
    song_data = response.json()
    print("API response JSON:", song_data)
    
    if song_data['tracks']:
        track = song_data['tracks'][0]
        artist_name = track['artists'][0]['name']
        song_name = track['name']
        song_url = track['external_urls']['spotify']
        song_image = track['album']['images'][0]['url']
        
        print("Song details extracted successfully!")
        return {
            "artist_name": artist_name,
            "song_name": song_name,
            "song_url": song_url,
            "song_image": song_image
        }
    else:
        print("No tracks found in the API response.")
        return None