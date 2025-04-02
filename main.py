import os
from flask import Flask, render_template, request, redirect, url_for, Response
from google.cloud import storage
import random
import string
import json
import requests
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

API_KEY = 'AIzaSyDKEqNxdilZfuE-IFymWgVnfOpjXqjabUg'



def getImageCaption(file):
    
    genai.configure(api_key=API_KEY)
    
    image = Image.open(file)
    
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    #   generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    PROMPT = "describe the image. end your response in json"


    response = model.generate_content()

    # print(response)
    print(response.text)


def generate_content(user_input):
    # Call the Google Generative AI API to generate content based on the user's input
    try:
        response = genai.generate_text(
            model="models/text-bison-001",  # Choose the model you want to use
            prompt=user_input,
            temperature=0.7,  # Adjust the temperature for creativity (0.0 to 1.0)
            max_output_tokens=150  # Max tokens in the response
        )
        return response.text.strip()
    except Exception as e:
        return f"Error generating content: {e}"






@app.route("/", methods=['GET', 'POST'])
def index():
    image_url = None
    generated_caption = None

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
            model="models/text-bison-001",  # You can choose another model if needed
            prompt=prompt,
            temperature=0.7,  # Control creativity level (0.0 to 1.0)
            max_output_tokens=50  # Limit caption length
        )

        # Return the generated caption
        return response.text.strip()

    except Exception as e:
        return f"Error generating caption: {str(e)}"








@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    print('upload worked')
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Flask's built-in server running on port 8080
    app.run(host="0.0.0.0", port=8080)
