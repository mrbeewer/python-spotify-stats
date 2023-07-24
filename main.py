import circlify as circ
import pandas as pd

from spotify_wrapper import SpotipyWrapper
from display_results import Visualizer

# Initialize our spotipy wrapper with a scope
spotify_data = SpotipyWrapper("user-top-read")

# Authenticate with env credentials
spotify_data.authenticate()

# Get the top tracks for time ranges ("short_term", "medium_term", "long_term")
spotify_data.get_user_top_tracks(["short_term", "medium_term", "long_term"])

# Import a time range to visualize
df = pd.read_csv("csv/short_term.csv")
top_tracks = df.head(5)

# Unique Artists
artist_df = df.sort_values(["artist", "artist_id"], ascending=[True, False]).groupby("artist").first().reset_index()

# Hit the API for images and genres
artist_df["filename"], artist_df["genres"] = zip(
    *[spotify_data.get_artist_info(artist_id) for artist_id in artist_df["artist_id"]]
)

# Create artist dataframe with counts and sort descending
artist_df = artist_df.merge(df["artist"].value_counts().reset_index(name="counts"), on="artist").sort_values(
    by=["counts"], ascending=False
)

# Get the top X
top_artists = artist_df.head(5)

# Genre counts based on top tracks
top_genres = (artist_df["genres"] * artist_df["counts"]).explode().value_counts().reset_index(name="counts")

# Circle pack based on the counts value (smallest to largest)
artist_packed_circles = circ.circlify(
    data=list(top_artists["counts"]), show_enclosure=False, target_enclosure=circ.Circle(x=0, y=0, r=500)
)

# Draw the visual
visual = Visualizer()
visual.simple(top_tracks, top_genres, top_artists, artist_packed_circles)
