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
def handle_request():
    # For more information about CORS and CORS preflight requests, see:
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return_message = ""

    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return_message = request.args.get('message')
    elif request_json and 'message' in request_json:
        return_message = request_json['message']
    else:
        return_message = {"data": analyze()}

    return (return_message, 200, headers)


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
