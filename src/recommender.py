import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.

    Numeric columns are converted from strings to numbers so they can be
    used in math later:
      - `id` and `tempo_bpm` become ints
      - `energy`, `valence`, `danceability`, `acousticness` become floats
    Text columns (title, artist, genre, mood) are left as strings.

    Required by src/main.py
    """
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

# --- Scoring weights (the Algorithm Recipe). Change these to run experiments. ---
# Finalized recipe: genre is the strongest taste signal, so it is weighted
# highest; mood and a perfect energy match are worth the same; acoustic is a
# light tiebreaker. (Experiment tried: halve genre + double energy -- see the
# README "Experiments" section for the result. Reverted to these values.)
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the finalized
    Algorithm Recipe:

      - Genre match ........ +2.0   (exact match on genre)
      - Mood match ......... +1.0   (exact match on mood)
      - Energy similarity .. up to +1.0, based on how CLOSE the song's
                             energy is to the target: (1 - |target - energy|)
      - Acoustic agreement . +0.5   (tiebreaker: the user's acoustic
                             preference agrees with the song)

    Accepts either key naming for the profile:
      favorite_genre/genre, favorite_mood/mood, target_energy/energy,
      likes_acoustic.

    Returns a tuple of (score, reasons), where `reasons` is a list of short
    strings explaining each point award, e.g. "genre match (+2.0)".

    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Read preferences, tolerating both naming styles.
    fav_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    fav_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))
    likes_acoustic = user_prefs.get("likes_acoustic")

    # Rule 1: genre match
    if fav_genre is not None and song["genre"] == fav_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({song['genre']}) (+{GENRE_WEIGHT})")

    # Rule 2: mood match
    if fav_mood is not None and song["mood"] == fav_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({song['mood']}) (+{MOOD_WEIGHT})")

    # Rule 3: energy similarity (up to ENERGY_WEIGHT) -- rewards CLOSENESS, not
    # higher or lower. energy is on a 0-1 scale, so 1 - distance normally
    # stays between 0 and 1. max(0.0, ...) floors it so an out-of-range
    # target (e.g. 2.0) can never SUBTRACT points -- the worst case is 0.
    if target_energy is not None:
        closeness = max(0.0, 1.0 - abs(target_energy - song["energy"]))
        points = round(closeness * ENERGY_WEIGHT, 2)
        score += points
        reasons.append(f"energy close to target (+{points:.2f})")

    # Rule 4: acoustic agreement (tiebreaker)
    if likes_acoustic is not None:
        is_acoustic = song["acousticness"] >= 0.5
        if likes_acoustic == is_acoustic:
            score += ACOUSTIC_WEIGHT
            if likes_acoustic:
                reasons.append(f"acoustic feel matches your preference (+{ACOUSTIC_WEIGHT})")
            else:
                reasons.append(f"non-acoustic feel matches your preference (+{ACOUSTIC_WEIGHT})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks the whole catalog for a user and returns the top `k` songs.

    Steps:
      1. Use score_song() as a "judge" to score every song.
      2. Sort all scored songs from highest to lowest score
         (ties broken by id, so the order is stable and repeatable).
      3. Return the top k as (song, score, explanation) tuples, where
         `explanation` is the song's reasons joined into one sentence.

    Required by src/main.py
    """
    # 1. Score every song. A list comprehension is the Pythonic way to
    #    build one list from another. score_song returns (score, reasons);
    #    we join the reasons into a single explanation string here.
    scored = [
        (song, *score_song(user_prefs, song))  # -> (song, score, reasons)
        for song in songs
    ]

    # 2. Sort highest score first. sorted() returns a NEW list and leaves
    #    the caller's `songs` list untouched. The key sorts by score
    #    descending (-score) and then by id ascending as a stable tiebreak.
    ranked = sorted(scored, key=lambda item: (-item[1], item[0]["id"]))

    # 3. Take the top k and turn the reasons list into an explanation string.
    results: List[Tuple[Dict, float, str]] = []
    for song, score, reasons in ranked[:k]:
        explanation = "; ".join(reasons) if reasons else "no strong matches"
        results.append((song, score, explanation))

    return results
