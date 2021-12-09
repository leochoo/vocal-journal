from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
import urllib.request
import magic
import ffmpeg
import os
import tempfile
import parselmouth


# Use a service account
print("Current direcotry path: ", os.getcwd())
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ".key/vocal-journal-firebase-adminsdk-oun5i-107f90e11f.json"
cred = credentials.Certificate(
    ".key/vocal-journal-firebase-adminsdk-oun5i-107f90e11f.json")
firebase_admin.initialize_app(cred)

db = firestore.AsyncClient()


def handle_request(request):
    # async def handle_request():
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
        # flask.Flask.make_response>`.
        `make_response <http://flask.pocoo.org/docs/1.0/api/
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
        # parse request parameters
        audioURL = request.args.get("audioURL")
        token = request.args.get("token")
        finalURL = audioURL+"&token="+token
        result = analyze(finalURL)
        print("Analysis result", result)
        return_message = {"data": result}

    return (return_message, 200, headers)


def get_file_path(filename):
    return os.path.join(tempfile.gettempdir(), filename)


def analyze(audioURL):
    # 1. Preprocessing
    # Download sound file
    input_name = "input.wav"
    input_path = get_file_path(input_name)
    urllib.request.urlretrieve(audioURL, input_path)

    # Save sound file to a temporary directory
    output_name = "output.wav"
    output_path = get_file_path(output_name)

    # Convert webm to wav
    stream = ffmpeg.input(input_path)
    stream = ffmpeg.output(stream, output_path)
    stream = ffmpeg.overwrite_output(stream)
    ffmpeg.run(stream)
    # print("Output: ", magic.from_file(output_file_path))

    # 2. Analyze

    # Read sound file
    sound = parselmouth.Sound(output_path)  # sound object from wav file
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch], "To PointProcess (cc)")

    # Get Jitter, Shimmer, HNR, MFCC

    # jitter
    jitter_local = parselmouth.praat.call(
        pulses, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3) * 100

    # shimmer
    shimmer_local = parselmouth.praat.call(
        [sound, pulses], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    # HNR
    harmonicity = parselmouth.praat.call(
        sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = parselmouth.praat.call(harmonicity, "Get mean", 0, 0)

    # jitter shimmer hnr object
    jsh_obj = {
        "jitter_local": jitter_local,
        "shimmer_local": shimmer_local,
        "HNR": hnr
    }

    # update firestore document
    doc_ref = db.collection("analysis")
    doc_ref.add(jsh_obj)

    print("Jitter result:", jitter_local)

    return jsh_obj
