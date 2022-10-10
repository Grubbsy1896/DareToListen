# September 8th 2022 
# MT Development

#    TEMPLATE FOR CREATING SPOTIFY CLIENT OBJECT
# 
# This is the easiest template file of all.


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Environment Variables
# client id and client secret. (Required in all templates)
cid     = 'REPLACE'
secret  = 'REPLACE'


# Required Scobe Variables
# NOTE: This is for the specific actions taking place.
#       You can miss include scopes so be weary when
#       combining scopes. 
scopes = ""

# Initializing the spotfiy client
# auth_manager=SpotifyOAuth(client_id=cid, client_secret = secret, scope=scopes, redirect_uri="http://127.0.0.1:9090")
# client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,)
# sp.auth_manager = auth_manager

#  NOTE: You're ready to use sp.


def get_spotify_client(cid, secret, scopes = None):
    #auth_manager=SpotifyOAuth(client_id=cid, client_secret = secret, redirect_uri="http://127.0.0.1:9090")
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,)
    #sp.auth_manager = auth_manager

    return sp

# Returns a dict 
def spotify_request_song(track_id):
    cid     = 'REPLACE'
    secret  = 'REPLACE'
    client = get_spotify_client(cid, secret)

    try:
        track = client.track(track_id)
    except Exception as e:
        print(e, "\nDidn't like the client")
        return {}

    artists = []
    for a in track['artists']:
        artists.append(a['name'])

    url = "None"
    for u in track['album']['images']:
        if u['height'] == 640:
            url = u['url']

    # Thought I would need the precision but I realized just storing a string
    # is better...
    #print(track['album']['release_date_precision'])

    data = {
        "title": track['name'], 
        "album": track['album']['name'], 
        "artists": artists, 
        "release_date": track['album']['release_date'],
        "duration": track['duration_ms']/1000, # In seconds
        "explicit": track['explicit'],
        "image_url": url,
        "external_url": track['external_urls']['spotify']
    }

    return data

def strip_url(url):
    return url.split("https://open.spotify.com/track/")[1].split("?si=")[0]

def clean_title(title):
    illegal_chars = list(" \"'!@#$%^&*()[]\{}")
    for char in illegal_chars:
        title = title.replace(char, "")
    return title