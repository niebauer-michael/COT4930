# Michael Niebauer
# COT 5930-007 COT 4930-001: Cloud Native Development
# Project 2
# Leverage the Gemini AI API in Google Cloud (multi modal LLM API) to get a caption and extract a description from the image

# Imports
import os
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import storage
import random
import string
import json
import requests
from google.auth import compute_engine
from google import genai
import google.auth
from PIL import Image
from dotenv import load_dotenv

app = Flask(__name__)

# Generate a random name for the image and json files
def randomNameGenerator():
    name_length = 6
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=name_length))
    return random_name

# Saves pictures that were uploaded by user to
# google cloud storage
# the same of the image is the same as the associated json
# file
def saveImagesToCloudStorage(file, randomName):
    bucket = 'cot4930-001-bucket'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    filename = file.filename
    print(filename)
    fileType = os.path.splitext(filename)[1][1:].strip().lower()
    newName = randomName + '.' + fileType
    print(fileType)
    blob = bucket.blob(newName)
    blob.upload_from_file(file)

# Save JSON title and decription to google cloud bucket
# json file name is the same as the associated image
def saveJSONTOCloudStorage(randomName, json_data):
    bucket = 'cot4930-001-bucket'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
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
    print(GEMINI_API_KEY)
    return GEMINI_API_KEY

# load images stored in cloud bucket
# load and parse the json files with title and description
def loadImagesFromCloudStorage():
    bucket = 'cot4930-001-bucket'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blobs = bucket.list_blobs()
    image_urls = []
    titles = []
    descriptions = []
    for blob in blobs:
        # loop over blobs for image files
        # store the url in a list
        if blob.name.endswith(('.jpg', '.jpeg')):
            image_urls.append(blob.public_url)
        # loop over blobs for json files
        # parse the json file for title and description   
        if blob.name.endswith(('.json')):
            json_data = blob.download_as_text()
            data = json.loads(json_data)
            titles.append(data.get('title'))
            descriptions.append(data.get('description'))
    return image_urls, titles, descriptions

# Fuction to return index.html
# a call to load images is called
# lists, for image urls, titles, description and the length of the list
# is passed to index.
@app.route('/')
def index():
    image_urls, titles, descriptions = loadImagesFromCloudStorage()
    length = len(image_urls)
    return render_template('index.html', image_urls=image_urls, titles = titles, descriptions = descriptions, length = length)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
