import os
from flask import Flask, render_template, request, redirect, url_for, Response
from google.cloud import storage
import random
import string
import json
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

API_KEY = 'AIzaSyDKEqNxdilZfuE-IFymWgVnfOpjXqjabUg'


app = Flask(__name__)

# Configure the Google Generative AI API client (using API key or authentication)
genai.configure(api_key="AIzaSyDKEqNxdilZfuE-IFymWgVnfOpjXqjabUg")  # Optionally, use a service account for authentication

# Route for home page and form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    generated_caption = None

    response = genai.generate_text(
    model="models/text-bison-001",  # Choose an appropriate model
    prompt="What is the capital of France?",
    temperature=0.5,
    max_output_tokens=50
    )
    print(response.text)


    if request.method == 'POST':
        # Get the uploaded image file
        file = request.files.get('image')
        if file:
            # Save the uploaded image temporarily (for displaying purposes)
            image_path = os.path.join("static", file.filename)
            file.save(image_path)

            # Generate caption using Google Generative AI
            generated_caption = generate_caption(image_path)
            
            # Set image URL for displaying on the webpage
            image_url = f"/static/{file.filename}"

    return render_template('index.html', image_url=image_url, generated_caption=generated_caption)


def generate_caption(image_path):
    """Generates a caption for the uploaded image using Google Generative AI."""
    try:
        # Construct the prompt with image-related context
        prompt = f"Generate a caption for this image: {image_path}"

        # Call the Google Generative AI API to generate text (caption)
        response = genai.generate_text(
            model="gemini-1.5-flash",  # You can choose another model if needed
            prompt=prompt,
            temperature=0.7,  # Control creativity level (0.0 to 1.0)
            max_output_tokens=50  # Limit caption length
        )

        # Return the generated caption
        return response.text.strip()

    except Exception as e:
        return f"Error generating caption: {str(e)}"


if __name__ == "__main__":
    # Flask's built-in server running on port 8080
    app.run(host="0.0.0.0", port=8080)
