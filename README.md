# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders (like Spotify or YouTube) usually blend two ideas: **collaborative filtering**, which guesses what you'll like from the behavior of similar users ("people who liked this also liked that"), and **content-based filtering**, which matches songs to you using the songs' own attributes, like genre, mood, and energy. My version is purely content-based, and that's a deliberate choice: I have song attributes but no data on how other users behave (no likes, skips, or play counts), so the collaborative half simply isn't possible here — I left it out on purpose rather than fake it. Instead, my recommender prioritizes **accuracy to the user's stated taste**. It scores every song against a simple `UserProfile` (favorite genre, favorite mood, target energy, and whether they like acoustic music) and adds up weighted points: genre match counts the most because it's the strongest, most reliable signal of taste, followed by mood, then how *close* a song's energy is to the target, then a small bonus for matching the acoustic preference. The highest-scoring songs are recommended. I weighted it this way so the picks stay predictable and honest to what the user asked for, and because a rule-based content system can *explain* every recommendation in plain language — something a black-box model can't easily do on a catalog this small.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



