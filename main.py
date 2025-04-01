# Michael Niebauer
# COT 5930-007 COT 4930-001: Cloud Native Development
# Project 2
# Leverage the Gemini AI API in Google Cloud (multi modal LLM API) to get a caption and extract a description from the image

# Imports
import os
from flask import Flask, render_template, request, redirect, url_for, Response
from google.cloud import storage
import random
import string
import json

app = Flask(__name__)



# Main entry point into app - returns index.html and passes all values to it
@app.route('/')
def index():
    return render_template('index.html')


# main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)