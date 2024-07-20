import requests
import base64
import webbrowser
from spotipy.oauth2 import SpotifyOAuth
import spotipy

CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
REDIRECT_URI = "REDIRECT_URI"

def get_spotify_token_and_user_id(client_id, client_secret, redirect_uri):
    """
    Function to get an access token and user ID from Spotify
    """
    auth_manager = SpotifyOAuth(client_id=client_id,
                                client_secret=client_secret,
                                redirect_uri=redirect_uri,
                                scope='playlist-modify-public')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    token_info = auth_manager.get_cached_token()

    if not token_info:
        print("Error getting token")
        return None, None

    token = token_info['access_token']
    user_id = sp.current_user()['id']
    return token, user_id



def create_spotify_playlist(token, user_id, playlist_name):
    """
    Function to create a Spotify playlist
    """
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": playlist_name,
        "description": "Playlist created via Spotifytrick",
        "public": False
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 201:
        print("Error in creating Spotify playlist")
        return None

    return response.json().get('id')

def add_tracks_to_playlist(token, playlist_id, track_uris):
    """
    Function to add tracks to a Spotify playlist
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "uris": track_uris
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 201:
        print("Error in adding tracks to Spotify playlist")
        return False

    return True

def search_spotify(track_name, artist_name, token):
    """
    Function to search for a track on Spotify
    """
    query = f"{track_name} artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error in Spotify API call")
        return None

    results = response.json().get('tracks', {}).get('items', [])
    if not results:
        print("No results found")
        return None

    return results[0].get('uri', '')

def open_spotify_link(track_name, artist_name):
    token, user_id = get_spotify_token_and_user_id(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    if not token:
        print("Failed to get Spotify token")
        return

    track_uri = search_spotify(track_name, artist_name, token)
    if track_uri:
        webbrowser.open(track_uri)
    else:
        print("No track found")
