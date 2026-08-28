# Sentiment Analysis CLI

A command-line sentiment analysis tool that tells you whether a piece of text sounds **Positive**, **Negative**, or **Neutral** — powered by VADER (NLTK's rule-based sentiment model), fully offline after the initial lexicon download.

## Core Purpose

Give it a sentence, a paragraph, or a text file full of lines, and it scores the sentiment of each — no API calls, no internet required once the VADER lexicon is downloaded.

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Analyze a single sentence** | Type in text, get its sentiment and scores back instantly. |
| 2 | **Analyze a whole file** | Point it at a `.txt` file with one sentence per line — every line gets scored in one pass. |
| 3 | **View history** | See every analysis you've ever run; results are saved automatically. |
| 4 | **View statistics** | Breakdown of Positive/Negative/Neutral counts as percentages, plus an average sentiment score. |
| 5 | **Clear history** | Wipe saved results for a fresh start. |
| 6 | **Clear screen / Exit** | Basic housekeeping options. |

## Architecture

The project follows a clean separation of concerns across five files:

```
main.py         → Entry point — wires everything together and starts the app
cli.py          → Interactive menu / user interface layer
service.py      → Core logic — runs text through VADER, classifies it, computes stats
repository.py   → Persistence — saves/loads results to and from sentiment_history.json
models.py       → Data shape — defines what a "sentiment result" looks like
```

**Dependency flow:**

```
main.py → cli.py → service.py → repository.py → models.py
```

## Summary

In short, this is a small, self-contained sentiment-tracking tool — a mini analytics log for "how does this text sound," with persistent history and basic reporting, built with clean separation between data, logic, storage, and UI.
