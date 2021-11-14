from flask import Flask, request, jsonify
import parselmouth
import glob
import os.path
import urllib.request

app = Flask(__name__)

# @app.route('/pitch_track', methods=['POST'])


@app.route('/')
def pitch_track():
    # Download file and save
    url = 'https://firebasestorage.googleapis.com/v0/b/vocal-journal.appspot.com/o/1636902198006?alt=media&token=d10843b2-c92e-4907-9cbc-58e06223b6f7'
    urllib.request.urlretrieve(url, "audio/firebase.wav")
    # Save the file that was sent, and read it into a parselmouth.Sound
    for wave_file in glob.glob("audio/*.wav"):
        print("Processing {}...".format(wave_file))
        sound = parselmouth.Sound(wave_file)
        # Calculate the pitch track with Parselmouth
        pitch_track = sound.to_pitch().selected_array['frequency']
        # Convert the NumPy array into a list, then encode as JSON to send back
        return jsonify(list(pitch_track))

    # Download file from url, open sound file, and run above function
    # url = 'https://firebasestorage.googleapis.com/v0/b/vocal-journal.appspot.com/o/1636899950097?alt=media&token=ef0643cc-aa4e-47ac-8bc3-ed6c9be750b0'
    # response = urllib.request.urlopen(url)
    # data = response.read()      # a `bytes` object
    # sound = parselmouth.Sound(data)
    # pitch_track = sound.to_pitch().selected_array['frequency']
    # return jsonify(list(pitch_track))
