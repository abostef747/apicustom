# app.py
import subprocess
import uuid
from flask import Flask, request, jsonify, send_file
import requests
from werkzeug.utils import secure_filename
import os
import ffmpeg


def create_app():
    app = Flask(__name__, static_folder='uploads', static_url_path='/uploads')
    app.config['UPLOAD_FOLDER'] = '/app/uploads/'
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Other setup code...
    return app


app = create_app()


@app.route('/', methods=['GET'])
def homepage():
    return "Homepage"


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip
import requests
from urllib.parse import urlparse
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/video_length', methods=['POST'])
def video_length():
    data = request.json
    video_url = data['url']
    
    # Parse the url to get the video name
    a = urlparse(video_url)
    video_name = os.path.basename(a.path)

    # Download the video file
    with requests.get(video_url, stream=True) as r:
        r.raise_for_status()
        with open(video_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Load video file and get its duration
    clip = VideoFileClip(video_name)
    duration = clip.duration

    # Cleanup the downloaded video file
    os.remove(video_name)

    return jsonify({'length': duration})

if __name__ == '__main__':
    app.run(debug=True)
