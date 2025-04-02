# main.py
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = 'AIzaSyDKEqNxdilZfuE-IFymWgVnfOpjXqjabUg'


@app.route("/")
def hello():
    title = 'title'
    items = 'items'
    return render_template('index.html', title=title, items=items)

if __name__ == "__main__":
    # Flask's built-in server running on port 8080
    app.run(host="0.0.0.0", port=8080)
