import urllib.request
import magic
import ffmpeg
from flask import Flask, request, jsonify
# import parselmouth
# import glob
# import os.path


app = Flask(__name__)

# @app.route('/pitch_track', methods=['POST'])


@app.route('/')
def pitch_track():
    return jsonify(analyze())


def analyze():
    url = "https://firebasestorage.googleapis.com/v0/b/vocal-journal.appspot.com/o/leo_audio_1637128699906?alt=media&token=92c37c3a-f519-453e-a21a-9d8f022c4d0c"
    urllib.request.urlretrieve(url, "audio/input.wav")
    print("Input: ", magic.from_file("audio/input.wav"))

    stream = ffmpeg.input("audio/input.wav")
    stream = ffmpeg.output(stream, "audio/output.wav")
    stream = ffmpeg.overwrite_output(stream)
    ffmpeg.run(stream)
    print("Output: ", magic.from_file("audio/output.wav"))

    # return "done"
    return "Input: " + magic.from_file("audio/input.wav") + "\n" + "Output: " + magic.from_file("audio/output.wav")
