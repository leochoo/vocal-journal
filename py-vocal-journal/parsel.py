from flask import Flask, request, jsonify
import parselmouth
import glob
import os.path

app = Flask(__name__)

# @app.route('/pitch_track', methods=['POST'])


@app.route('/')
def pitch_track():
    # Save the file that was sent, and read it into a parselmouth.Sound
    for wave_file in glob.glob("audio/*.wav"):
        print("Processing {}...".format(wave_file))
        sound = parselmouth.Sound(wave_file)
        # Calculate the pitch track with Parselmouth
        pitch_track = sound.to_pitch().selected_array['frequency']
        # Convert the NumPy array into a list, then encode as JSON to send back
        return jsonify(list(pitch_track))
