import csv
import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

scope = 'user-top-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.environ["SPOTIPY_CLIENT_ID"],
    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
    scope=scope))

ranges = ['short_term', 'medium_term', 'long_term']

exported_results = {}

for sp_range in ranges:
    print("range:", sp_range)
    exported_results[sp_range] = []
    results = sp.current_user_top_artists(time_range=sp_range, limit=50)
    for i, item in enumerate(results['items']):
        exported_results[sp_range].append([i, item['name'], item['genres'], item['images'][0]['url']])
        # genres = 'no genres'
        # if 'genres' in item['album']:
        #     genres = item['album']['genres']
        print(i, item['name'], '//', item['genres'], '//', item['images'][0]['url'])
    
    filename = "artists_{}.csv".format(sp_range)
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['rank','artist','genres','image'])
        for row in exported_results[sp_range]:
            writer.writerow(row)
    print()


