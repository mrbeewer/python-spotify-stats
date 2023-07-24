import textwrap

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class Visualizer:
    def __init__(self):
        pass

    def simple(self, top_tracks, top_genres, top_artists, artist_packed_circles):
        """ """
        # Create the matplotlib objects:
        _, (plt_top_tracks, plt_top_genres, plt_top_artists) = plt.subplots(
            3, figsize=(6, 9), facecolor="white", height_ratios=[2, 1, 4]
        )

        # Set the overall title of the visual
        plt.suptitle("Spotify Stats", size=15, weight="bold")

        # Set the Top Tracks
        top_five_tracks_str = "\n".join(
            [
                str(row[0] + 1) + ". " + row[1] + " - " + row[2]
                for row in zip(top_tracks["rank"], top_tracks["title"], top_tracks["artist"])
            ]
        )
        plt_top_tracks.axis("off")
        plt_top_tracks.set_aspect("equal")
        plt_top_tracks.set_title("Top 5 Tracks")
        plt_top_tracks.text(
            0.5,
            1,
            top_five_tracks_str,
            fontsize=14,
            horizontalalignment="center",
            verticalalignment="top",
            transform=plt_top_tracks.transAxes,
            multialignment="left",
        )

        # Set the Top Genres
        top_genres_str = " | ".join(top_genres.head(3)["index"].str.title().tolist())
        plt_top_genres.axis("off")
        plt_top_genres.set_aspect("equal")
        plt_top_genres.set_title("Top 3 Genres")
        plt_top_genres.text(
            0.5,
            1,
            top_genres_str,
            fontsize=14,
            horizontalalignment="center",
            verticalalignment="top",
            transform=plt_top_genres.transAxes,
        )

        # Display the Top Artists
        plt_top_artists.set_title("Top 5 Artists")
        plt_top_artists.axis("off")
        plt_top_artists.set_aspect("equal")

        # Find the plot's x and y limits based on circle locations and size:
        xlim_max = max([circle.x + circle.r for circle in artist_packed_circles])
        xlim_min = min([circle.x - circle.r for circle in artist_packed_circles])
        ylim_max = max([circle.y + circle.r for circle in artist_packed_circles])
        ylim_min = min([circle.y - circle.r for circle in artist_packed_circles])

        # Set the plot xy limits
        plt.xlim(xlim_min, xlim_max)
        plt.ylim(ylim_min, ylim_max)

        # Set the pad space between circles (1 = no space)
        SPACING = 0.98

        # Circlify outputs smallest to largest, reverse artist_counts to match
        top_artists = top_artists[::-1]

        # Loop through circles and plot:
        for circle, label, artist_image in zip(artist_packed_circles, top_artists["artist"], top_artists["filename"]):
            # Get the position and radius of the circle
            x, y, r = circle

            # IMAGE
            # Open the image
            img = Image.open(artist_image)

            # Convert to array
            im = np.asarray(img)

            # Place the image and size to the circle
            im = plt_top_artists.imshow(im, extent=(int(x - r * SPACING), int(x + r), int(y - r), int(y + r)))

            # Create the mask for the image crop
            patch = patches.Circle((x, y), radius=(r * SPACING), transform=plt_top_artists.transData)

            # Set the clip for the image using the patch
            im.set_clip_path(patch)

            # Add a color overlay so text stands out better
            plt_top_artists.add_patch(plt.Circle((x, y), r * SPACING, color=(0.1, 0.2, 0.5, 0.75)))

            # TEXT
            # Wrap based on length and r - magic numbers
            width = 14
            if r > 180:
                width = 10
            label = "\n".join(textwrap.wrap(label, width=width, break_long_words=False, max_lines=2))

            # Font is loosely based on radius
            font_size = int(0.075 * r) if int(0.075 * r) > 12 else 10

            # Apply annotation
            plt.annotate(
                label,
                (x, y),
                size=font_size,
                weight="bold",
                color="w",
                va="center",
                ha="center",
            )

        plt.savefig("generated_visual.png")
        plt.savefig("generated_visual.svg")
        plt.show()
