import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, url_for
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "iz-journal-resul-cs50-2026"
app.config["TEMPLATES_AUTO_RELOAD"] = True

# CS50 SQL: dosya yoksa önce oluştur
if not os.path.exists("iz.db"):
    open("iz.db", "a").close()

db = SQL("sqlite:///iz.db")

# Create table on startup
db.execute(
    """
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        mood INTEGER NOT NULL,
        created_at TEXT NOT NULL
    )
    """
)

MOODS = {
    1: {"label": "Sakin", "emoji": "🌊"},
    2: {"label": "Düşünceli", "emoji": "🍃"},
    3: {"label": "Nötr", "emoji": "◎"},
    4: {"label": "Enerjik", "emoji": "☀️"},
    5: {"label": "Mutlu", "emoji": "✦"},
}


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Ana sayfa: giriş listesi + isteğe bağlı arama/filtre"""
    q = (request.args.get("q") or "").strip()
    mood = request.args.get("mood")

    sql = "SELECT * FROM entries WHERE 1=1"
    params = []

    if q:
        sql += " AND (title LIKE ? OR body LIKE ?)"
        like = f"%{q}%"
        params.extend([like, like])

    if mood and mood.isdigit() and int(mood) in MOODS:
        sql += " AND mood = ?"
        params.append(int(mood))

    sql += " ORDER BY created_at DESC, id DESC"
    entries = db.execute(sql, *params)

    for entry in entries:
        entry["mood_meta"] = MOODS.get(entry["mood"], MOODS[3])

    return render_template(
        "index.html",
        entries=entries,
        moods=MOODS,
        q=q,
        selected_mood=mood or "",
    )


@app.route("/new", methods=["GET", "POST"])
def new_entry():
    """Yeni günlük kaydı oluştur"""
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        body = (request.form.get("body") or "").strip()
        mood_raw = request.form.get("mood")

        if not title or not body:
            flash("Başlık ve metin zorunlu.")
            return render_template("new.html", moods=MOODS, form=request.form)

        try:
            mood = int(mood_raw)
        except (TypeError, ValueError):
            flash("Geçerli bir ruh hali seç.")
            return render_template("new.html", moods=MOODS, form=request.form)

        if mood not in MOODS:
            flash("Geçerli bir ruh hali seç.")
            return render_template("new.html", moods=MOODS, form=request.form)

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        db.execute(
            "INSERT INTO entries (title, body, mood, created_at) VALUES (?, ?, ?, ?)",
            title,
            body,
            mood,
            created_at,
        )
        flash("İz kaydedildi.")
        return redirect("/")

    return render_template("new.html", moods=MOODS, form={})


@app.route("/entry/<int:entry_id>")
def show_entry(entry_id):
    """Tek kaydı göster"""
    rows = db.execute("SELECT * FROM entries WHERE id = ?", entry_id)
    if len(rows) != 1:
        flash("Kayıt bulunamadı.")
        return redirect("/")
    entry = rows[0]
    entry["mood_meta"] = MOODS.get(entry["mood"], MOODS[3])
    return render_template("entry.html", entry=entry)


@app.route("/entry/<int:entry_id>/delete", methods=["POST"])
def delete_entry(entry_id):
    """Kaydı sil"""
    db.execute("DELETE FROM entries WHERE id = ?", entry_id)
    flash("İz silindi.")
    return redirect("/")


@app.route("/stats")
def stats():
    """Ruh hali özet istatistikleri"""
    total = db.execute("SELECT COUNT(*) AS n FROM entries")[0]["n"]
    by_mood = db.execute(
        "SELECT mood, COUNT(*) AS n FROM entries GROUP BY mood ORDER BY mood"
    )
    chart = []
    for mood_id, meta in MOODS.items():
        found = next((row for row in by_mood if row["mood"] == mood_id), None)
        count = found["n"] if found else 0
        pct = round((count / total) * 100) if total else 0
        chart.append({"mood": mood_id, "meta": meta, "count": count, "pct": pct})

    return render_template("stats.html", total=total, chart=chart)


@app.route("/about")
def about():
    return render_template("about.html")
