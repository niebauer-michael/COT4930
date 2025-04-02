import os
from flask import Flask, render_template, request, redirect, url_for, Response, send_file
from google.cloud import storage
import random
import string
import json
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
import mimetypes

app = Flask(__name__)

#genai.configure(api_key="AIzaSyDKEqNxdilZfuE-IFymWgVnfOpjXqjabUg")  # Optionally, use a service account for authentication

genai.set_api_key('AIzaSyDKEqNxdilZfuE-IFymWgVnfOpjXqjabUg')

#img = Image.open('image.jpg')

#img = 'image.jpg'

# Check the MIME type based on the file extension
#mime_type, encoding = mimetypes.guess_type(img)

#print(f"The MIME type of the image is: {mime_type}")

#genai.configure(api_key=os.environ['GEMINI_API'])


response = genai.generate_text(
    prompt="Tell me a joke about computers.",
    model="text-bison-001"  # Example model name, verify in docs
)

print(response['text'])


# Configure the Google Generative AI API client (using API key or authentication)
genai.configure(api_key="AIzaSyDKEqNxdilZfuE-IFymWgVnfOpjXqjabUg")  # Optionally, use a service account for authentication

# Route for home page and form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', message="No file part")
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', message="No selected file")
        
        # Read the file into memory (don't save it)
        image_bytes = file.read()
        
        # Send the image directly back to the user
        return render_template('index.html', image_data=image_bytes)
    
    return render_template('index.html')



if __name__ == "__main__":
    # Flask's built-in server running on port 8080
    app.run(host="0.0.0.0", port=8080)
