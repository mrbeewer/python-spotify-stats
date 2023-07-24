import csv
import os

import urllib.request
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


class SpotipyWrapper:
    def __init__(self, scope):
        self.scope = scope

        # Check/Create directories
        if not os.path.exists("img"):
            os.makedirs("img")
        if not os.path.exists("csv"):
            os.makedirs("csv")

    def authenticate(self):
        # Load Spotify credentials from .env
        load_dotenv()

        # Initialize the spotify helper
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.environ["SPOTIPY_CLIENT_ID"],
                client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
                scope=self.scope,
            )
        )

    def get_user_top_tracks(self, ranges):
        """
        Interact with Spotipy to get the current_user_top_tracks
        based on the supplied ranges.

        Parameters
        ----------
        ranges : List
            The only valid options are "short_term", "medium_term",
            and "long_term".

        Returns
        -------
        None - Will create local CSV files, named [range].csv
        """
        allowed_ranges = ["short_term", "medium_term", "long_term"]
        range_list = []

        # Check input
        if type(ranges) is str:
            range_list.append(ranges)
        elif type(ranges) is list:
            range_list = ranges
        else:
            raise ValueError(
                "Ranges must be a list. Allowed values are the " +
                "time ranges: %s" % allowed_ranges
            )

        # Only continue if ranges are in the allowed_ranges list
        if not all(item in allowed_ranges for item in range_list):
            raise ValueError("Allowed time ranges: %s" % allowed_ranges)

        # Container for top tracks
        results_to_csv = {}

        for sp_range in range_list:
            # Get the top tracks
            results = self.sp.current_user_top_tracks(
                time_range=sp_range,
                limit=100
            )

            # Initialize our data store
            results_to_csv[sp_range] = []

            # Loop through results and pull out the attributes we want
            for i, item in enumerate(results["items"]):
                results_to_csv[sp_range].append([
                        i,
                        item["name"],
                        item["artists"][0]["name"],
                        item["artists"][0]["id"]
                ])

            # Write out to a CSV for later use
            filename = "{}.csv".format(sp_range)
            fullfilename = os.path.join('csv', filename)
            with open(fullfilename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["rank", "title", "artist", "artist_id"])
                for row in results_to_csv[sp_range]:
                    writer.writerow(row)

    def get_artist_info(self, artist_id):
        """
        Interact with Spotipy to get the artist information
        based on a supplied artist ID (string).

        Parameters
        ----------
        artist_id : str
            String of the artist ID as provided by Spotify.

        Returns
        -------
        filename : str
            The image filename (which has been downloaded)
        genres : list
            List of string genres for that artist
        """
        if not type(artist_id) is str:
            return False

        # Get the artist information
        results = self.sp.artist(artist_id)

        # Get the artist image
        if 'images' in results:
            url = results['images'][0]['url']
            filename = "%s.png" % artist_id
            fullfilename = os.path.join('img', filename)

            # Don't download if we already have it
            if not os.path.isfile(fullfilename):
                urllib.request.urlretrieve(url, fullfilename)

        # Record the artist genres, if available
        genres = []
        if 'genres' in results:
            genres = results['genres']

        return fullfilename, genres
