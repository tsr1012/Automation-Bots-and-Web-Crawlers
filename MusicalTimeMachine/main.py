import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from web_scraper import WebScraper

ID = os.getenv("ID")
SECRET = os.getenv("SECRET")
scope = "playlist-modify-public"

# --- Billboard 100 songs --- #
data_top100 = WebScraper()
data_top100.date = input("Which year you want to travel to? Type the date format in YYYY-MM-DD: ")
items = data_top100.get_songs()

# --- Spotify Authentication --- #
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=ID,
        client_secret=SECRET,
        scope=scope,
        redirect_uri="http://example.com",
        show_dialog=True,
        cache_path="token.txt"))
user_id = sp.current_user()["id"]

# --- Checking if desired playlist already exists --- #
user_playlists = sp.user_playlists(user=user_id)
for playlist in user_playlists["items"]:
    if playlist["name"][:10] == data_top100.date:
        print(f"\n{'—'*29}\nThis playlist already exists.")
        print(f"{playlist['name']}\n{'—'*29}\n")
        exit()

# --- Creating new playlist --- #
uri_list = []
print(f"{'—'*100}\n{'': <5}{'Music': <60}Artist\n{'—'*100}")
for i, item in enumerate(items, 1):
    result = sp.search(q=f"track{item['song']}artist:{item['artist']}",
                       type="track", market="us", limit=1)
    print(f"{i: <5}{item['song']: <60}{item['artist']}")
    # print(json.dumps(result))
    try:
        uri_list.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"\n{item['song']} by {item['artist']} doesn't exist in spotify. Skipped.\n")

playlist_id = sp.user_playlist_create(user=user_id,
                                      name=f"{data_top100.date} Billboard 100",
                                      public=True,
                                      collaborative=False,
                                      description="Top 100 Billboard songs from past.")

sp.playlist_add_items(playlist_id=playlist_id["id"], items=uri_list)

print(f"\n{'—'*34}\nPlaylist: {data_top100.date} Billboard 100\nCreated successfully.\n{'—' * 34}")
