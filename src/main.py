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


# Distinct "normal" listener profiles.
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    # --- Adversarial / edge-case profiles (meant to try to "trick" the scorer) ---
    # 1) Conflicting signals: an energetic edm fan who also wants a melancholy mood.
    "Conflicting Signals (edge)": {
        "favorite_genre": "edm",
        "favorite_mood": "melancholy",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
    # 2) Unknown categories: genre/mood that do not exist in the catalog, so no
    #    categorical match is possible and ranking falls back to energy alone.
    "Unknown Categories (edge)": {
        "favorite_genre": "k-pop",
        "favorite_mood": "euphoric",
        "target_energy": 0.7,
        "likes_acoustic": False,
    },
    # 3) Out-of-range energy: 2.0 is off the 0-1 scale, so (1 - |2.0 - energy|)
    #    goes negative and can SUBTRACT points -- a numeric edge case.
    "Out-of-Range Energy (edge)": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 2.0,
        "likes_acoustic": False,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs, k: int = 5) -> None:
    """Print a clean, ranked block of top-k recommendations for one profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    profile_str = ", ".join(f"{key}={value}" for key, value in user_prefs.items())

    print()
    print("=" * 64)
    print(f"  {name} - Top {len(recommendations)} recommendations")
    print(f"  Profile: {profile_str}")
    print("=" * 64)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} - {song['artist']}")
        print(f"      Score: {score:.2f}")
        print(f"      Reasons:")
        for reason in explanation.split("; "):
            print(f"        - {reason}")
    print()


def main() -> None:
    songs = load_songs(SONGS_CSV)
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
