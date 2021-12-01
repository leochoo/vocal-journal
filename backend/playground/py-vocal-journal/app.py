import urllib.request
import magic
import ffmpeg
from flask import Flask, request, jsonify
# import parselmouth
# import glob
import os
import tempfile

app = Flask(__name__)

# @app.route('/pitch_track', methods=['POST'])


@app.route('/')
def pitch_track():
    return {"data": analyze()}


def get_file_path(filename):
    return os.path.join(tempfile.gettempdir(), filename)


def analyze():
    url = "https://firebasestorage.googleapis.com/v0/b/vocal-journal.appspot.com/o/audio_1638349605653?alt=media&token=fa52e757-0210-4a62-b0ed-17bdcbdd215c"

    input_filename = "input.wav"
    input_file_path = get_file_path(input_filename)

    urllib.request.urlretrieve(url, input_file_path)
    print("Input: ", magic.from_file(input_file_path))

    output_filename = "output.wav"
    output_file_path = get_file_path(output_filename)

    stream = ffmpeg.input(input_file_path)
    stream = ffmpeg.output(stream, output_file_path)
    stream = ffmpeg.overwrite_output(stream)
    ffmpeg.run(stream)
    print("Output: ", magic.from_file(output_file_path))

    # return "done"
    return "Input: " + magic.from_file(input_file_path) + "\n" + "Output: " + magic.from_file(output_file_path)
