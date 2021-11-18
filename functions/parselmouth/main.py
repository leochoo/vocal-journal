import urllib.request
import magic
import ffmpeg

# magic.from_file("audio/sample.wav")


def handle_request(request):
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


def analyze():
    return_string = ""
    url = "https://firebasestorage.googleapis.com/v0/b/vocal-journal.appspot.com/o/leo_audio_1637128699906?alt=media&token=92c37c3a-f519-453e-a21a-9d8f022c4d0c"
    urllib.request.urlretrieve(url, "audio/input.wav")
    print("Input: ", magic.from_file("audio/input.wav"))

    # return_string += magic.from_file("audio/sample.wav")
    stream = ffmpeg.input("audio/sample.wav")
    stream = ffmpeg.output(stream, "audio/output.wav")
    ffmpeg.run(stream)

    print("Output: ", magic.from_file("audio/output.wav"))

    return "Input: " + magic.from_file("audio/input.wav") + "\n" + "Output: " + magic.from_file("audio/output.wav")
