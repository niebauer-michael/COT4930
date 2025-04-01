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
import requests
from google.auth import compute_engine
from google import genai
from google import genai
from google.genai import types
import google.auth
from PIL import Image
from dotenv import load_dotenv


app = Flask(__name__)

# Connect to cloud storage bucket
def getBucket():
    bucket = 'cot4930private'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    return bucket

# Generate a random name for both images and json files
def randomNameGenerator():
    name_length = 6
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=name_length))
    return random_name

# Saves pictures that were uploaded by user to
# Google cloud storage
# The same of the image is the same as the associated json
def saveImagesToCloudStorage(file, randomName):
    bucket = getBucket()
    filename = file.filename
    fileType = os.path.splitext(filename)[1][1:].strip().lower()
    newName = randomName + '.' + fileType
    blob = bucket.blob(newName)
    blob.upload_from_file(file)

# Save JSON title and decription to google cloud bucket
# json file name is the same as the associated image
def saveJSONTOCloudStorage(randomName, json_data):
    bucket = getBucket()
    randomFileName = randomName + '.json'
    title = json_data["title"]
    description = json_data["description"]
    json_data = {"title": str(title), "description": str(description)}
    json_string = json.dumps(json_data)
    blob = bucket.blob(randomFileName)
    blob.upload_from_string(json_string, content_type='application/json')

# Use Google Gemini API to generate title and description of an image
# image is openned using pillow and sent to the API
def getImageDescription(file,GEMINI_API_KEY):
    image = Image.open(file)
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Generate a single title and description for this image in json format", image])
    # Format the text response - strip back ticks and json text
    description = response.text.replace('`','')
    description = description.replace('json','')
    description = json.loads(description)
    return description

# Get Gemini API key  from enviroment variable
def getAPIkey():
    load_dotenv()
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    return GEMINI_API_KEY

# Load images stored in cloud bucket
# Load and parse the json files with title and description
def loadImagesFromCloudStorage():
    bucket = getBucket()
    blobs = bucket.list_blobs()
    image_names = []
    titles = []
    descriptions = []
    for blob in blobs:
        # loop over blobs for image files
        # store the url in a list
        if blob.name.endswith(('.jpg', '.jpeg')):
            #image_urls.append(blob.public_url)
            image_names.append(blob.name)
            #print(image_names)
        # loop over blobs for json files
        # parse the json file for title and description   
        if blob.name.endswith(('.json')):
            json_data = blob.download_as_text()
            data = json.loads(json_data)
            titles.append(data.get('title'))
            descriptions.append(data.get('description'))
    return image_names,titles, descriptions

# Main entry point into app - returns index.html and passes all values to it
@app.route('/')
def index():
    image_filenames, titles, descriptions = loadImagesFromCloudStorage()
    num = len(image_filenames)
    return render_template('index.html', image_filenames=image_filenames, titles=titles, descriptions=descriptions,num = num)

# Serve image for html
@app.route('/image/<image_filename>')
def serve_image(image_filename):
    bucket = getBucket()
    blob = bucket.blob(image_filename)
    # Download the image as bytes
    image_data = blob.download_as_bytes()
    # Return the image with the appropriate content type
    return Response(image_data, mimetype='image/jpeg')

# function is called when the form is submitted 
# image is saved
# title and description are generated from Gemini API
# json file is stored in the same bucket with the image
# both image and json have the same random file name
@app.route('/upload', methods=['POST'])
def upload_image():
    randomName = randomNameGenerator()
    file = request.files['file']
    saveImagesToCloudStorage(file, randomName)
    KEY_API = getAPIkey()
    json_data =  getImageDescription(file, KEY_API)
    saveJSONTOCloudStorage(randomName, json_data)
    return redirect(url_for('index'))

# main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)