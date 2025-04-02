import os
from flask import Flask, render_template, request, redirect, url_for, Response
from google.cloud import storage
import random
import string
import json
import requests
from PIL import Image
from dotenv import load_dotenv


app = Flask(__name__)

API_KEY = 'AIzaSyDKEqNxdilZfuE-IFymWgVnfOpjXqjabUg'




@app.route("/")
def hello():
    title = 'title'
    items = 'items'
    return render_template('index.html', title=title, items=items)

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    print('upload worked')
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Flask's built-in server running on port 8080
    app.run(host="0.0.0.0", port=8080)
