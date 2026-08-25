# İZ — Personal Daily Journal

Harvard CS50x 2026 Final Project by [Resul Kılınç](https://github.com/resulkilinc)

**Demo video:** https://youtu.be/MZZ1zOmwQuQ  
**Certificate:** https://cs50.harvard.edu/certificates/04abccaa-20f0-4993-bf6b-dcde72ebad88

Stack: Flask · SQLite · Jinja · custom CSS

[![CS50x](https://img.shields.io/badge/CS50x-2026%20Final%20Project-A51C30)](https://cs50.harvard.edu/x/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Public portfolio project. CS50 problem-set solutions are **not** included in this repository (academic honesty).


## Overview

**İZ** is my CS50x 2026 final project: a calm personal journal web application. The name means “trace” in Turkish. The idea is simple but useful: leave short traces of your days — a title, a short text, and a mood — then find them later with search and filters, or glance at mood statistics over time.

I chose this project because it combines several skills from the course in one coherent product. From Week 9 I reuse Flask routes, Jinja templates, and SQLite through CS50’s SQL library. From Week 8 I bring intentional HTML structure and custom CSS. From earlier weeks I bring careful validation and clear separation between data, logic, and presentation. The app is small enough to finish well, but large enough to demonstrate real design choices: schema, routes, UX, and visual identity.

İZ is intentionally not a clone of a famous todo app or stock portfolio. It is a quiet writing tool with a distinct visual language (moss greens, warm paper tones, Fraunces + Manrope typography). The goal was something I would actually open: a private notebook for moods and short reflections.

## What the app does

- Create journal entries with title, body text, and mood (1–5).
- List all entries on the home page, newest first.
- Search entries by title or body text.
- Filter entries by mood.
- Open a single entry page and delete an entry.
- View a stats page with mood distribution bars.
- Read an about page that explains the project.

Server-side validation rejects empty titles/bodies and invalid moods. Flash messages confirm saves and deletions.

## File structure and responsibilities

### `app.py`
This is the Flask application. It configures the app, connects to `iz.db`, creates the `entries` table if needed, and defines all routes:

- `GET /` — list + search/filter
- `GET/POST /new` — create entry
- `GET /entry/<id>` — show one entry
- `POST /entry/<id>/delete` — delete entry
- `GET /stats` — mood counts and percentages
- `GET /about` — project blurb

Mood labels live in a Python dictionary so templates stay simple. Timestamps are stored as readable strings when an entry is created.

### `requirements.txt`
Lists dependencies: `Flask` and `cs50` (for the SQL helper).

### `static/styles.css`
All visual design lives here: layout shell, navigation, hero, cards, forms, mood pills, stats bars, responsive rules, and a short entrance animation. I avoided generic “AI purple dashboard” aesthetics and instead used a paper/moss palette so the brand feels like a notebook by the sea.

### `templates/layout.html`
Base template with navigation, flash area, and footer. Other pages extend this layout.

### `templates/index.html`
Home feed: hero, search/filter form, and entry cards.

### `templates/new.html`
Create form with radio mood choices and textarea.

### `templates/entry.html`
Single-entry view with delete confirmation.

### `templates/stats.html`
Horizontal bar chart built with CSS widths from percentages computed in Python.

### `templates/about.html`
Short description of purpose and stack.

### `iz.db`
SQLite database created automatically on first run. Not hand-edited; the app owns its schema.

### `README.md`
This documentation file (required for CS50 final project submission).

## Design decisions

**Why Flask + SQLite?**  
Week 9 already taught this stack, and it fits a personal journal perfectly: forms post to routes, rows persist in SQLite, pages re-render with Jinja. No external API is required, so the demo is reliable offline in Codespace.

**Why moods as integers 1–5?**  
Integers are easy to store, filter, and aggregate (`GROUP BY mood`). Labels/emoji are mapped in Python so the UI can stay expressive without cluttering the database.

**Why search with `LIKE`?**  
For a small personal notebook, full-text engines are overkill. `LIKE` with bound parameters is enough and avoids SQL injection.

**Why no user accounts?**  
Scope control. Adding login would expand the project into authentication/session territory I already practiced in Finance. For a final project of this size, a single-user local journal keeps the focus on product quality and clarity. If I continued the project later, multi-user auth would be the next feature.

**Why custom CSS instead of only Bootstrap?**  
I wanted a memorable brand. Bootstrap is great for speed, but for İZ I preferred full control over typography, cards, and atmosphere so the site feels like one composition rather than a default dashboard.

## How to run

```bash
cd project
pip install -r requirements.txt
flask run
```

Open the printed URL, add a few entries, try search/filter, check stats, delete one entry.

## How I tested

- Create entries with each mood.
- Reject empty form fields.
- Search by partial title/body text.
- Filter by mood alone and combined with search.
- Open entry detail and delete with confirmation.
- Confirm stats percentages update after adds/deletes.
- Check mobile-width layout for nav and filters.

## Acknowledgments

Built for CS50x 2026 as the final project by **Resul Kılınç** (GitHub: `resulkilinc`, edX: `kilincresul722`). Thanks to CS50 staff for the curriculum that made this possible — especially Flask, SQL, and the web weeks that shaped İZ.
