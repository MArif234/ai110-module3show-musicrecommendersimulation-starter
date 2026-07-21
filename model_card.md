# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

A tiny music recommender that matches songs to a listener's stated taste. It is a
classroom project, not a real product.

---

## 2. Intended Use  

VibeMatch suggests songs from a small list based on a listener's taste. A taste
profile is four things: favorite genre, favorite mood, target energy, and whether
they like acoustic music. The system scores every song and returns the top 5, each
with a short reason.

It assumes the listener knows their own taste and can describe it. It also assumes
the song list is fixed and already labeled.

**What it is for:** learning how recommenders work. Classroom exploration only.

**What it is not for:** real users or real playlists. It should not be used to judge
artists, pick real music, or stand in for a real app. The song list is tiny and the
scoring is simple, so the results are for practice, not real decisions.

---

## 3. How the Model Works  

The system gives every song a score, then sorts the songs from highest to lowest.
A song earns points like this:

- Same genre the listener asked for: **+2 points**.
- Same mood: **+1 point**.
- Close to the energy level they want: **up to +1 point** (closer means more points).
- Matches their acoustic preference: **+0.5 points**.

Genre is worth the most because it is the strongest sign of taste. Energy is scored by
*closeness* — a song near the target scores high, a song far away scores low. The song
with the most points is the top pick. Each pick comes with a plain reason, like
"genre match (pop)".

Changes from the starter: I filled in the empty functions, grew the song list from 10
to 18, added the reasons, tuned the point values, and fixed a bug where an out-of-range
energy request could subtract points instead of adding them.

---

## 4. Data  

The catalog has **18 songs**. I started with 10 and added 8 to cover more styles.

Each song has: title, artist, genre, mood, energy, tempo, valence (how happy it
sounds), danceability, and acousticness. The scoring uses four of these: genre, mood,
energy, and acousticness.

Genres include pop, lofi, rock, jazz, ambient, hip hop, edm, metal, folk, and more.
Moods include happy, chill, intense, melancholy, and others.

Limits: the list is tiny, so some genres have only one song. It only covers audio-style
traits. There are no lyrics, no language, and no artist popularity. So a lot of what
shapes real taste is missing.

---

## 5. Strengths  

It works well for listeners with a clear, common taste. A "chill lofi" fan or a
"high-energy pop" fan gets sensible, on-target picks.

It is honest. Every recommendation comes with a plain reason, so you can see why a song
was chosen.

It also spreads across different tastes. Very different profiles get very different
lists, which is what you would want.

The energy "closeness" scoring matched my intuition. Calm listeners get calm songs, and
the scores fade smoothly instead of being all-or-nothing.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly.

**Weakness discovered during experiments: a genre "filter bubble."** During testing I
noticed that the "Chill Lofi" user received an all-lofi top 3, and the weight-shift
experiment confirmed why: genre is weighted +2.0 while a perfect energy or mood match
is worth only +1.0, so genre almost always decides the ranking. This interacts badly
with the dataset, which is uneven — lofi has 3 of 18 songs (the largest group) while
13 of the genres have only a single song each. As a result, users whose favorite genre
is over-represented get a narrow, repetitive list of near-identical songs, while users
of a single-song genre get one on-genre match followed by unrelated "filler" songs that
only happened to have a similar energy. The system also uses *exact* genre matching, so
an "indie pop" fan gets zero genre credit for a "pop" song — meaning a great match can
be excluded over a one-word label difference. In short, the scoring over-prioritizes
genre and amplifies whatever imbalance exists in the catalog, which is exactly how
real recommenders create filter bubbles.

Other limitations: the bimodal energy data (few mid-range songs, nothing below 0.22)
gives middle-ground and ultra-calm listeners systematically weaker matches; genre-agnostic
listeners are underserved because energy can never outweigh a genre mismatch; and the
acoustic bonus largely re-rewards the same calm songs the energy rule already favors.

---

## 7. Evaluation  

I evaluated the recommender by running it (`python -m src.main`) against six user
profiles: three realistic listener types and three deliberately "adversarial"
edge cases designed to try to trick the scoring logic. For each I looked at
whether the top 5 made intuitive sense and whether the reasons matched the ranking.

### Realistic profiles

**High-Energy Pop** — a pop fan who wants an energetic, non-acoustic sound.

```
  #1  Sunrise City - Neon Echo        Score: 4.42  (genre +2.0; mood +1.0; energy +0.92; non-acoustic +0.5)
  #2  Gym Hero - Max Pulse            Score: 3.47  (genre +2.0; energy +0.97; non-acoustic +0.5)
  #3  Rooftop Lights - Indigo Parade  Score: 2.36  (mood +1.0; energy +0.86; non-acoustic +0.5)
  #4  Storm Runner - Voltline         Score: 1.49  (energy +0.99; non-acoustic +0.5)
  #5  Neon Overdrive - Pulse Grid     Score: 1.45  (energy +0.95; non-acoustic +0.5)
```

**Chill Lofi** — a calm, acoustic-leaning studier.

```
  #1  Library Rain - Paper Lanterns   Score: 4.50  (genre +2.0; mood +1.0; energy +1.0; acoustic +0.5)
  #2  Midnight Coding - LoRoom        Score: 4.43  (genre +2.0; mood +1.0; energy +0.93; acoustic +0.5)
  #3  Focus Flow - LoRoom             Score: 3.45  (genre +2.0; energy +0.95; acoustic +0.5)
  #4  Spacewalk Thoughts - Orbit Bloom Score: 2.43 (mood +1.0; energy +0.93; acoustic +0.5)
  #5  Coffee Shop Stories - Slow Stereo Score: 1.48 (energy +0.98; acoustic +0.5)
```

**Deep Intense Rock** — high energy, intense mood, non-acoustic.

```
  #1  Storm Runner - Voltline         Score: 4.49  (genre +2.0; mood +1.0; energy +0.99; non-acoustic +0.5)
  #2  Gym Hero - Max Pulse            Score: 2.47  (mood +1.0; energy +0.97; non-acoustic +0.5)
  #3  Neon Overdrive - Pulse Grid     Score: 1.45  (energy +0.95; non-acoustic +0.5)
  #4  Iron Verdict - Ashfall          Score: 1.43  (energy +0.93; non-acoustic +0.5)
  #5  Sunrise City - Neon Echo        Score: 1.42  (energy +0.92; non-acoustic +0.5)
```

All three behaved as expected: the song matching genre + mood + energy wins
clearly, then partial matches follow. Good sign the recipe is calibrated.

### Adversarial / edge-case profiles

**1. Conflicting Signals** — `genre=edm, mood=melancholy, energy=0.95, acoustic=True`
(an energetic edm fan who also asked for a melancholy mood and acoustic sound).

```
  #1  Neon Overdrive - Pulse Grid     Score: 3.00  (genre +2.0; energy +1.0)      <- edm + high energy
  #2  Paper Boats - Hazel Grove       Score: 1.88  (mood +1.0; energy +0.38; acoustic +0.5) <- the only melancholy song
  #3  Backroad Memories - Dusty Boots Score: 1.10  (energy +0.6; acoustic +0.5)
  #4  Gym Hero - Max Pulse            Score: 0.98  (energy +0.98)
  #5  Iron Verdict - Ashfall          Score: 0.98  (energy +0.98)
```

Result: the genre + energy signals win decisively and the melancholy mood is
almost ignored (the one melancholy song lands at #2 but only because it also
matched mood + acoustic). This confirms the genre-over-mood bias: when
preferences conflict, genre and energy dominate.

**2. Unknown Categories** — `genre=k-pop, mood=euphoric` (neither exists in the catalog).

```
  #1  Night Drive Loop - Neon Echo    Score: 1.45  (energy +0.95; non-acoustic +0.5)
  #2  Rooftop Lights - Indigo Parade  Score: 1.44  (energy +0.94; non-acoustic +0.5)
  #3  Concrete Dreams - Flow State    Score: 1.42  (energy +0.92; non-acoustic +0.5)
  #4  Island Time - Sunset Riddim     Score: 1.40  (energy +0.9; non-acoustic +0.5)
  #5  Sunrise City - Neon Echo        Score: 1.38  (energy +0.88; non-acoustic +0.5)
```

Result: no crash — it degrades gracefully to ranking by energy closeness alone.
But every score is low and the picks are an arbitrary mix of genres, showing the
exact-match cold-start weakness: an unknown genre/mood contributes nothing.

**3. Out-of-Range Energy** — `energy=2.0` (invalid; the scale is 0-1).

Before the fix, this exposed a real **bug**. Because `1 - |2.0 - energy|` is
negative for every song, the energy rule *subtracted* points instead of adding
them, and the reason string printed a nonsensical `+-0.18`:

```
  #1  Sunrise City - Neon Echo        Score: 3.32  (genre +2.0; mood +1.0; energy +-0.18; non-acoustic +0.5)
  #2  Gym Hero - Max Pulse            Score: 2.43  (genre +2.0; energy +-0.07; non-acoustic +0.5)
  #3  Rooftop Lights - Indigo Parade  Score: 1.26  (mood +1.0; energy +-0.24; non-acoustic +0.5)
  #4  Iron Verdict - Ashfall          Score: 0.47  (energy +-0.03; non-acoustic +0.5)
  #5  Neon Overdrive - Pulse Grid     Score: 0.45  (energy +-0.05; non-acoustic +0.5)
```

I fixed it by flooring the closeness at 0 (`max(0.0, 1 - abs(...))`), so an
out-of-range target can never subtract points — the worst case is now +0.00.
The reason string also formats to two decimals. Same profile after the fix:

```
  #1  Sunrise City - Neon Echo        Score: 3.50  (genre +2.0; mood +1.0; energy +0.00; non-acoustic +0.5)
  #2  Gym Hero - Max Pulse            Score: 2.50  (genre +2.0; energy +0.00; non-acoustic +0.5)
  #3  Rooftop Lights - Indigo Parade  Score: 1.50  (mood +1.0; energy +0.00; non-acoustic +0.5)
  #4  Storm Runner - Voltline         Score: 0.50  (energy +0.00; non-acoustic +0.5)
  #5  Night Drive Loop - Neon Echo    Score: 0.50  (energy +0.00; non-acoustic +0.5)
```

### Profile comparisons (what changed between pairs, in plain language)

Think of the system as handing out points to each song. A song earns points for
being the right genre, points for being the right mood, and points for being close
to the energy level the listener asked for. The song with the most points goes to
the top. Comparing two listeners at a time makes it clear what each preference is
really doing:

- **Happy Pop fan vs. Chill Lofi fan:** these two get completely different lists,
  with no songs in common. The pop fan gets bright, upbeat, high-energy songs; the
  lofi fan gets calm, quiet, acoustic ones. That is exactly what we want to see — one
  person asked for loud and lively, the other for soft and mellow, so the lists should
  look nothing alike.
- **Happy Pop fan vs. Intense Rock fan:** both want loud, high-energy music, so the
  only real difference is the style they picked. Sure enough, the very top song changes
  with the style (a pop song leads the pop list, a rock song leads the rock list), but
  further down both lists share the same energetic songs. In other words, the *style*
  choice decides the winner, and the *energy* choice fills in the rest.
- **Chill Lofi fan vs. Intense Rock fan:** these are the two most opposite listeners,
  and their lists have nothing in common. This is reassuring — it shows the system can
  serve very different tastes instead of pushing the same few popular songs on everyone.
- **The "confused" listener vs. a normal EDM fan:** one test listener asked for
  high-energy dance music but *also* a sad, melancholy mood — two things that rarely go
  together. The system leaned on the style and energy and mostly ignored the sad-mood
  request, so it returned upbeat dance songs anyway. That tells us mood is the weakest of
  the three preferences.
- **The "made-up taste" listener vs. the Happy Pop fan:** one listener asked for a genre
  and mood that don't exist in our song list at all. The pop fan got a clear favorite at
  the top; the made-up-taste listener got a flat, tied jumble of songs with no clear
  winner, because the only thing left to judge on was energy. This shows the genre and
  mood matches are what make a recommendation feel confident and personal.
- **The "impossible energy" listener vs. the Happy Pop fan:** one listener asked for an
  energy level that's off the scale. After the bug fix, the system simply gives everyone
  zero energy points instead of breaking, so the list is decided by style and mood alone.
  The top few songs stay in the same order as the normal pop fan — just with lower scores
  — which is the safe, sensible way to handle bad input.

### Why does "Gym Hero" keep showing up for people who just want "Happy Pop"?

This surprised me, so here it is in plain terms. A listener asks for **happy pop**.
*Gym Hero* is a pop song, but its mood is tagged **intense** (it's a workout track),
not happy — yet it still lands at #2 on the happy-pop list. Why? Because the system
gives *Gym Hero* full credit for two things: it **is** pop (the style matches), and it
is **very high energy**, which is close to what this listener wanted. It only misses
out on the "happy" points. Since matching the style is worth more than matching the
mood, being the right genre plus high energy is enough to beat most other songs, even
though the song's *feeling* is wrong. So the listener wanted "happy and poppy" but got
"poppy and intense" — a reasonable-looking pick that's subtly off. This is the clearest
sign that the system leans too hard on genre and energy and treats mood as an
afterthought, which is the main weakness described in the Limitations section.

### What surprised me / fixes applied

- **Fixed:** the energy rule was **not clamped** to a valid range. Flooring the
  closeness at 0 (`max(0.0, 1 - abs(...))`) means out-of-range input can never
  subtract points, and the reason string now formats cleanly (`+0.00`, not
  `+-0.18`). The adversarial test caught this before it could affect real users.
- When preferences conflict, genre + energy reliably beat mood, which is the
  same bias documented in the README, now confirmed experimentally.
- A remaining idea: validate `target_energy` is within 0-1 at input time and
  warn the user, rather than silently accepting an impossible value.

---

## 8. Future Work  

1. **Fuzzy genre matching.** Right now "indie pop" gets no credit for a "pop" request.
   I would treat similar genres as partial matches so close styles still count.
2. **Make mood matter more.** Mood is the weakest signal now, which is why a workout
   song can sneak into a happy-pop list. I would raise its weight or let the listener
   choose what matters most to them.
3. **Add variety to the top 5.** I would stop it from returning three near-identical
   songs in a row, so the list feels less repetitive.

---

## 9. Personal Reflection  

I learned that a recommendation is really just math. You turn taste into numbers and
sort them. The surprising part was how much the point values shape the results. Small
weight choices quietly decide who gets served well and who does not. Testing weird
profiles also showed me that bugs and bias hide in the edge cases, not the obvious ones.
It made me realize the music apps I use are making lots of hidden choices for me.
