from flask import Flask, request, jsonify
import urllib.request
import magic
import ffmpeg
import os
import tempfile
import parselmouth

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
        return_message = {"data": analyze()}

    return (return_message, 200, headers)


def pitch_track():
    return {"data": analyze()}


def get_file_path(filename):
    return os.path.join(tempfile.gettempdir(), filename)


def analyze():

    # 1. Preprocessing
    # Download sound file
    url = "https://firebasestorage.googleapis.com/v0/b/vocal-journal.appspot.com/o/audio_1638349605653?alt=media&token=fa52e757-0210-4a62-b0ed-17bdcbdd215c"
    input_name = "input.wav"
    input_path = get_file_path(input_name)
    urllib.request.urlretrieve(url, input_path)
    # print("Input: ", magic.from_file(input_file_path))

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

    return jitter_local, shimmer_local, hnr


# Process wav files to get Jitter, Shimmer, HNR, and MFCC

# def get_voice_data(_path):
#     # select .wav files only
#     wav_files = glob.glob(_path + "/*.wav")

#     n_list = []
#     tone_list = []
#     syllab_list = []

#     j_list = []
#     s_list = []
#     h_list = []

# for wav_file in wav_files:
# for wav_file in tqdm(wav_files): # tqdm shows the progress bar
#     sound = parselmouth.Sound(wav_file) # sound object from wav file
#     pitch = sound.to_pitch()
#     pulses = parselmouth.praat.call([sound, pitch], "To PointProcess (cc)")

#     # name analysis
#     name = os.path.basename(wav_file).split(".")[0]

#     ## tone
#     if "l" in name:
#         tone_list.append("l")
#     elif "n" in name:
#         tone_list.append("n")
#     elif "h" in name:
#         tone_list.append("h")

#     ## syllable
#     if "a" in name:
#         syllab_list.append("a")
#     elif "i" in name:
#         syllab_list.append("i")
#     elif "u" in name:
#         syllab_list.append("u")

#     # jitter
#     jitter_local = parselmouth.praat.call(pulses, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3) * 100

#     # shimmer
#     shimmer_local = parselmouth.praat.call([sound, pulses], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

#     # HNR
#     harmonicity = parselmouth.praat.call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
#     hnr = parselmouth.praat.call(harmonicity, "Get mean", 0, 0)

#     # Append to numpy array
#     n_list.append(name)
#     j_list.append(jitter_local)
#     s_list.append(shimmer_local)
#     h_list.append(hnr)

#     # MFCC
#     mfcc_object = sound.to_mfcc(number_of_coefficients=12)
#     mfcc_arr = mfcc_object.to_array()
#     mfcc_dic = {}
#     for i in range(0,len(mfcc_arr)):
#         mfcc_dic["MFCC-"+str(i)] = [statistics.mean(mfcc_arr[i])]
#     mfcc_df = pd.DataFrame.from_dict(mfcc_dic)
