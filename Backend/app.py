from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    passwords = [
        {"site": "Bank of America", "username": "alice_banking", "password": "••••••••", "category": "Banking", "tag": {"label": "Important", "color": "bg-pink-200"}},
        {"site": "Chase", "username": "bob123", "password": "••••••••", "category": "Banking", "tag": {"label": "Work", "color": "bg-purple-200"}},
        {"site": "Facebook", "username": "alice.fb", "password": "••••••••", "category": "Social Media", "tag": {"label": "Personal", "color": "bg-green-200"}},
        {"site": "Twitter", "username": "bob_tweets", "password": "••••••••", "category": "Social Media", "tag": {"label": "Side Project", "color": "bg-yellow-200"}},
    ]
    categories = ["All", "Banking", "Social Media"]
    return render_template("index.html", passwords=passwords, categories=categories)

@app.route("/add")
def add_password():
    return render_template("add_password.html")

if __name__ == "__main__":
    app.run(debug=True)
