
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------

def get_db():
    return sqlite3.connect("database.db", check_same_thread=False)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            emotion TEXT NOT NULL,
            hear_you INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, message, emotion, hear_you FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    conn.close()

    # Convert to dict for Jinja
    formatted_posts = []
    for p in posts:
        formatted_posts.append({
            "id": p[0],
            "message": p[1],
            "emotion": p[2],
            "hear_you": p[3]
        })

    return render_template("index.html", posts=formatted_posts)

@app.route("/post", methods=["POST"])
def post():
    message = request.form["message"]
    emotion = request.form["emotion"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (message, emotion) VALUES (?, ?)",
        (message, emotion)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/hear/<int:post_id>", methods=["POST"])
def hear(post_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE posts SET hear_you = hear_you + 1 WHERE id = ?",
        (post_id,)
    )
    conn.commit()
    conn.close()

    return redirect("/")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
