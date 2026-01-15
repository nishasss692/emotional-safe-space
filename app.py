# -----------------------------
# IMPORTS
# -----------------------------
from flask import Flask, render_template, request, redirect
import mysql.connector


# -----------------------------
# APP INITIALIZATION
# -----------------------------
app = Flask(__name__)


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@nisha.s123",   # <-- replace this
    database="emotional_safe_space"
)

cursor = db.cursor(dictionary=True)


# -----------------------------
# HOME ROUTE (SHOW POSTS)
# -----------------------------
@app.route('/')
def home():
    emotion_filter = request.args.get('emotion')

    if emotion_filter:
        cursor.execute(
            "SELECT * FROM posts WHERE emotion=%s ORDER BY id DESC",
            (emotion_filter,)
        )
    else:
        cursor.execute(
            "SELECT * FROM posts ORDER BY id DESC"
        )

    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)


# -----------------------------
# POST ROUTE (ADD NEW POST)
# -----------------------------
@app.route('/post', methods=['POST'])
def post():
    emotion = request.form.get('emotion')
    message = request.form.get('message')

    # Basic validation
    if not emotion or not message:
        return redirect('/')

    sql = "INSERT INTO posts (emotion, message) VALUES (%s, %s)"
    cursor.execute(sql, (emotion, message))
    db.commit()

    return redirect('/')


# -----------------------------
# "I HEAR YOU" ROUTE
# -----------------------------
@app.route('/hear/<int:post_id>', methods=['POST'])
def hear(post_id):
    cursor.execute(
        "UPDATE posts SET hear_you = hear_you + 1 WHERE id = %s",
        (post_id,)
    )
    db.commit()

    return redirect('/')
@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    db.commit()
    return redirect("/")


# -----------------------------
# RUN THE APP
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
