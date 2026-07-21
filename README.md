# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a **content-based** music recommender. It loads a catalog of 18 songs (each described by genre, mood, energy, and other audio attributes) and compares them against a user "taste profile." A weighted scoring rule turns those comparisons into a single number per song, and the highest-scoring songs are recommended, each with a plain-language explanation of *why* it was picked. The goal is recommendations that are accurate to the user's stated taste and fully explainable — not a black box.

---

## How The System Works

Real-world recommenders (like Spotify or YouTube) usually blend two ideas: **collaborative filtering**, which guesses what you'll like from the behavior of similar users ("people who liked this also liked that"), and **content-based filtering**, which matches songs to you using the songs' own attributes, like genre, mood, and energy. My version is purely content-based, and that's a deliberate choice: I have song attributes but no data on how other users behave (no likes, skips, or play counts), so the collaborative half simply isn't possible here — I left it out on purpose rather than fake it. Instead, my recommender prioritizes **accuracy to the user's stated taste**. It scores every song against a simple `UserProfile` (favorite genre, favorite mood, target energy, and whether they like acoustic music) and adds up weighted points: genre match counts the most because it's the strongest, most reliable signal of taste, followed by mood, then how *close* a song's energy is to the target, then a small bonus for matching the acoustic preference. The highest-scoring songs are recommended. I weighted it this way so the picks stay predictable and honest to what the user asked for, and because a rule-based content system can *explain* every recommendation in plain language — something a black-box model can't easily do on a catalog this small.

### Features used in the simulation

**`Song`** stores these fields (loaded from `data/songs.csv`):

- `id` — unique number for the song *(identifier, not scored)*
- `title` — song name *(display only, not scored)*
- `artist` — performer *(display only, not scored)*
- `genre` — e.g. pop, lofi, rock, jazz **(used for scoring)**
- `mood` — e.g. happy, chill, intense, moody **(used for scoring)**
- `energy` — 0.0–1.0, how energetic the track feels **(used for scoring)**
- `tempo_bpm` — beats per minute *(stored, not used in the current recipe)*
- `valence` — 0.0–1.0, musical positivity/happiness *(stored, reserved for a future experiment)*
- `danceability` — 0.0–1.0 *(stored, not used in the current recipe)*
- `acousticness` — 0.0–1.0, how acoustic vs. produced the track is **(used for scoring)**

**`UserProfile`** stores the listener's stated taste (every field is used for scoring):

- `favorite_genre` — the genre the user most wants (matched against `Song.genre`)
- `favorite_mood` — the mood the user most wants (matched against `Song.mood`)
- `target_energy` — 0.0–1.0, the energy level the user is in the mood for (compared to `Song.energy`)
- `likes_acoustic` — `True`/`False`, whether the user prefers acoustic tracks (compared to `Song.acousticness`)

So the recommender actively scores on **four features — genre, mood, energy, and acousticness** — while the rest of the `Song` fields are kept for display or saved for later experiments.

### How a score is computed (the Algorithm Recipe)

Every song starts at `0.0`. Four rules add points; higher total = better match:

| Rule | Condition | Points |
|---|---|---|
| **Genre match** | `song.genre == favorite_genre` | **+2.0** |
| **Mood match** | `song.mood == favorite_mood` | **+1.0** |
| **Energy similarity** | always (continuous) | **`(1 - abs(target_energy - song.energy)) * 1.0`** → 0 to +1.0 |
| **Acoustic agreement** (tiebreaker) | `likes_acoustic` and `acousticness >= 0.5`, OR `not likes_acoustic` and `acousticness < 0.5` | **+0.5** |

Maximum possible ≈ **4.5**. Genre is weighted highest (2.0) because it is the strongest, most reliable signal of taste — an identity signal, not a situational one. Mood (1.0) and a perfect energy match (also up to 1.0) fine-tune *within* a genre, and the acoustic bonus (0.5) is a light tiebreaker. The 2:1 genre-to-mood ratio reflects that a listener's genre rarely changes while their mood shifts with the moment.

**The energy rule rewards *closeness*, not "more" or "less."** It measures the distance between the user's target and the song (`abs(target_energy - song.energy)`) and flips it into a reward with `1 - distance`, so a song right at the target scores 1.0 and a song at the opposite extreme scores 0.0. Because `energy` is already on a 0–1 scale, this stays bounded without extra normalization.

Each rule that fires also records a short reason (e.g. "matches your favorite genre"), which is how the recommender explains its picks.

**Bias I expect from these weights:** because genre is worth double a mood match (2.0 vs. 1.0), the system will **over-prioritize genre and can overlook great songs that nail the user's mood but sit in a different genre.** For example, a user who wants a `chill` mood but lists `lofi` as their genre may never see an equally chill jazz or ambient track, since the 2.0 genre gap is hard for mood + energy to close. This is a deliberate trade-off (genre is a more stable taste signal), but it narrows discovery — the reason lowering the genre weight is one of the planned experiments below.

### How songs are chosen

1. Score every song in the catalog against the user profile.
2. Sort by score, highest first (ties broken by lower `id` for stable order).
3. Return the top `k` (default 5), each with its explanation.

### The taste profiles used for comparison

The user profile is a small dictionary of target values for the four scored features:

**Primary demo — "The Lofi Studier":**

```python
user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood":  "chill",
    "target_energy":  0.4,
    "likes_acoustic": True,
}
```

This user cleanly separates "chill lofi" from "intense rock" (e.g. Midnight Coding scores ~4.48 vs. Storm Runner ~0.49). Its one weakness is that all four preferences point at the same small cluster, so the top picks are all lofi — which is itself a useful demonstration of the "low variety" limitation below.

**Experiment profile — "Mixed Signals":**

```python
mixed_signals = {
    "favorite_genre": "rock",    # wants rock...
    "favorite_mood":  "chill",   # ...but a calm mood
    "target_energy":  0.3,       # ...and low energy (rock is usually high)
    "likes_acoustic": True,      # ...and acoustic
}
```

No song satisfies all four fields, so genre pulls one way while mood/energy/acoustic pull the other. This profile is used to show the scoring rule *reasoning* through conflicting preferences rather than acting as a simple genre filter.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

`python -m src.main` runs the recommender against six user profiles (three
realistic listeners plus three adversarial edge cases). Below is the real output
for the first profile, **High-Energy Pop**; the full six-profile run — including
the adversarial edge cases and a bug they uncovered — is documented in the
[model card](model_card.md) under *Evaluation*.

```
Loaded songs: 18

================================================================
  High-Energy Pop - Top 5 recommendations
  Profile: favorite_genre=pop, favorite_mood=happy, target_energy=0.9, likes_acoustic=False
================================================================

  #1  Sunrise City - Neon Echo
      Score: 4.42
      Reasons:
        - genre match (pop) (+2.0)
        - mood match (happy) (+1.0)
        - energy close to target (+0.92)
        - non-acoustic feel matches your preference (+0.5)

  #2  Gym Hero - Max Pulse
      Score: 3.47
      Reasons:
        - genre match (pop) (+2.0)
        - energy close to target (+0.97)
        - non-acoustic feel matches your preference (+0.5)

  #3  Rooftop Lights - Indigo Parade
      Score: 2.36
      Reasons:
        - mood match (happy) (+1.0)
        - energy close to target (+0.86)
        - non-acoustic feel matches your preference (+0.5)

  #4  Storm Runner - Voltline
      Score: 1.49
      Reasons:
        - energy close to target (+0.99)
        - non-acoustic feel matches your preference (+0.5)

  #5  Neon Overdrive - Pulse Grid
      Score: 1.45
      Reasons:
        - energy close to target (+0.95)
        - non-acoustic feel matches your preference (+0.5)
```

The result matches expectations: the pop + happy song (Sunrise City) wins outright. Note **Rooftop Lights** (an *indie pop*, happy song) ranks below Gym Hero only because `"indie pop"` does not exactly equal `"pop"` — a live example of the exact-match genre bias described above.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Planned experiments (fill in the observed results after running each):

1. **Weight shift — halve genre (2.0 → 1.0) and double energy (×1.0 → ×2.0).** Prediction: genre stops dominating, so songs that match mood/energy but sit in a different genre climb the rankings.
   **Result:** the *#1–2 picks stayed the same* for realistic profiles (the song matching genre + mood + energy still wins), but the scores below them compressed and cross-genre, energy-matching songs rose sharply. For **Chill Lofi**, the ambient track *Spacewalk Thoughts* jumped from 2.43 to 3.36, closing the gap to the #3 lofi song from 1.02 points to just 0.04. For the **Conflicting Signals** edge profile the top 5 actually *reordered* — high-energy songs (Gym Hero, Iron Verdict, Storm Runner) surged past the folk track that had ranked on mood alone.
   **Verdict:** the change made results *different, not more accurate*. Because the top pick rarely changed, it doesn't help a user who trusts their genre choice; it mostly boosts discovery/variety in the mid-ranks by trading away genre loyalty. I reverted to the finalized weights (genre 2.0, energy ×1.0) after this experiment. *(Weights live in the `*_WEIGHT` constants in `src/recommender.py`, so this is a one-line change to re-run.)*
2. **Add `valence` as a fifth rule** (closeness, weight ~0.5). Prediction: separates calm-happy songs from calm-sad ones that mood alone lumps together (e.g. Coffee Shop Stories vs. a melancholy track). *Result: TODO after running.*
3. **Run the "Mixed Signals" profile** (rock + chill + low energy + acoustic). Prediction: no perfect match, so the ranking reveals how genre weight trades off against mood/energy/acoustic. *Result: TODO after running.*
4. **Compare different listener types** (Lofi Studier vs. a hypothetical Hype Workout user). Prediction: the recommender returns clearly different top-5 lists, confirming it responds to the profile rather than always returning popular songs. *Result: TODO after running.*

---

## Limitations and Risks

- **Tiny catalog (18 songs).** Results are only as diverse as the data; some genres/moods appear only once.
- **Over-favors one cluster / low variety.** Because genre is weighted highest and correlated features (energy, acousticness) reinforce it, a lofi-chill user gets an all-lofi top 3. The system rarely surprises the user — the classic content-based "filter bubble."
- **Exact-string matching is brittle.** Genre and mood must match exactly. A user whose `favorite_genre` is `"indie"` or a mood of `"energetic"` that isn't spelled the same as the data gets zero points there, even for near-identical songs (a small-scale version of the cold-start problem).
- **No collaborative signal.** It uses only song attributes — no likes, skips, or play history — so it can't learn taste from behavior or find surprising cross-genre picks the way real systems do.
- **No understanding of lyrics, language, or culture.** It scores numbers and tags, not meaning.
- **Bias risk.** The fixed weights encode an opinion (genre matters most). Different weights would systematically advantage different artists/genres, and a thin catalog can under-represent some styles.

I go deeper on these in the model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

> Draft below — personalize it in your own words before submitting.

Building this made it concrete that a "recommendation" is really just **turning data into a number**. Each song and each user are represented as features, a scoring rule measures how well they line up (exact matches for categories, and *closeness* for numeric features like energy), and sorting those numbers produces the prediction. The most interesting part was that closeness scoring — rewarding how *near* a song is to the user's target rather than just favoring high or low values — is what lets the system tell "chill lofi" apart from "intense rock." It also showed me why real platforms combine this with collaborative filtering: content-based scoring alone tends to recommend more of the same and can't discover surprising picks.

I also saw where bias and unfairness can creep in. The weights are a hidden value judgment — deciding genre matters more than mood systematically advantages some songs over others, and no user ever voted on that choice. A thin or skewed catalog makes it worse: styles that appear rarely can barely be recommended, and exact-string matching quietly excludes anyone whose taste isn't spelled the way the data is. At scale, these same mechanics are how recommenders create filter bubbles and can under-serve less mainstream artists or listeners.



