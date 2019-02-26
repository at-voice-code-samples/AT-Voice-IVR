import os
from flask import Flask

app = Flask(__name__)

#Define methods that build the necessary xml
def intro_response():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="15" callbackUrl="http://something.com">'
    response += '<Say voice="woman">'
    response += "Welcome to Voice Memo. Press 1 followed by the pound sign. Press 2 followed by the pound sign to exit."
    response += '</Say>'
    response += '</GetDigits>'
    response += '</Response>'
    return response

def exit_phrase():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="woman">'
    response += 'Bye bye for now'
    response += '</Say>'
    response += '</Response'
    return response

def record_phrase():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Record finishOnKey="#" maxLength="15" trimSilence="true" playBeep="true" callBackUrl="http://something.something">'
    response += '<Say voice="woman">'
    response += 'Press the pound sign to end the recording'
    response += '</Say>'
    response += '</Record>'
    response += '</Response>'
    return response

def play_previous_recording():
    pass

def play_random_recording():
    pass

def play_previous_recording_not_found():
    pass

@app.route("/")
def index():
    response = "It lives"
    return response

@app.route("/voice/service", methods=["GET","POST"])
def voice_service():
    pass