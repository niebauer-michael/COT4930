# main.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!!!!!!!!!!!"

if __name__ == "__main__":
    # Flask's built-in server running on port 8080
    app.run(host="0.0.0.0", port=8080)
