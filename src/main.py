"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os

try:
    # Works when run as a module from the project root: `python -m src.main`
    from src.recommender import load_songs, recommend_songs
except ImportError:
    # Works when run directly: `python src/main.py`
    from recommender import load_songs, recommend_songs

# Absolute path to data/songs.csv, resolved relative to THIS file, so the
# program works no matter which directory you run it from.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS_CSV = os.path.join(PROJECT_ROOT, "data", "songs.csv")


def main() -> None:
    songs = load_songs(SONGS_CSV)
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Clean, readable terminal layout: a header with the profile, then a
    # ranked block per song showing title, artist, score, and the specific
    # reasons the scoring function produced.
    profile_str = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    print()
    print("=" * 64)
    print(f"  Top {len(recommendations)} recommendations")
    print(f"  Profile: {profile_str}")
    print("=" * 64)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} - {song['artist']}")
        print(f"      Score: {score:.2f}")
        print(f"      Reasons:")
        for reason in explanation.split("; "):
            print(f"        - {reason}")
    print()


if __name__ == "__main__":
    main()
