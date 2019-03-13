#Ideally this application should be split into various files
#It is recommended to take advantage of OOP when building large
#and complex applications

#Keep you models in a models.py file and import it into the main app.py files
#Separate config files as well; keep any sensitive information away from the
#main source files

#THIS IS FOR DEMMO PURPOSES RATHER THAN PRODUCTION CODE

import os
from flask import Flask, request, redirect
import json
from flask_sqlalchemy import SQLAlchemy

#Base DB configuration
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,"userdata.db"))

#Base app configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

#Define User model class

class UserData(db.Model):
    phone_number = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    session_id = db.Column(db.String(125), nullable=False)
    level = db.Column(db.Integer(), nullable=False)
    voice_note = db.Column(db.String(125), nullable=False)
    last_input = db.Column(db.String(10), nullable=False)
    file = db.Column(db.String(125), nullable=False)

    def __repr__(self):
        return "User Phone Number: {}".format(phone_number)

#This function checks whether the value has been returned as a stringself.
#It will be removed in future interations

def value_check(val):
    if type(val) != str:
        return str(val)
    else:
        return val

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
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="woman">'
    response += 'Playing your last recorded file</Say>'
    response += '<Play url="https://something.something"></Play>'
    response += '</Response'
    return response

def play_random_recording():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="woman">'
    response += 'Playing your random recording for the day</Say>'
    response += '<Play url="https://something.something"></Play>'
    response += '</Response'
    return response

def play_previous_recording_not_found():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="woman">'
    response += 'No recordings found</Say>'
    response += '<Play url="https://something.something"></Play>'
    response += '</Response'
    return response

def actions_menu():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="woman">'
    response += 'Press 1 followed by the pound sign to record a message.Press 2 followed by the pound sign to listen</Say>'
    response += '</Response'
    return response

#Define level and subscriber details

level = 0
file = User(file="https://s3.eu-west-2.amazonaws.com/at-voice-sample/play.mp3")



#Define application routes and functions

@app.route("/")
def index():
    response = "It lives"
    return response

#If a user shows up and they are part of the service, they will be redirected back to the main menu
#If they are new, their details will be saved on the database and they will also be redirected into the main menu

@app.route("/voice/service", methods=["GET","POST"])
def voice_service():
    if method == "POST":
        session_id = request.values.get("sessionId")
        phone_number = request.values.get("phoneNumber")
        file = User(file="https://s3.eu-west-2.amazonaws.com/at-voice-sample/play.mp3")
        level = 1
        check_phone_number = User.filter_by(phone_number=phone_number).first()
        str_check_phone_number = str(check_phone_number)

        if not phone_number and str_check_phone_number == phone_number:
            redirect(actions_menu)
        else:
            db.session.add(
                phone_number = phone_number,
                session_id = session_id,
                level = level,
                file = file
            )
            db.session.commit()
            redirect(voice_menu)

#This function serves the main menu and handles most of the interactions that we we will be running

@app.route("/voice/menu", methods=["GET","POST"])
def voice_menu():
    value = request.values.get("dtmfDigits")
    value = value_check(value)
    phone_number = request.values.get("callerNumber")
    str_phone_number = str(phone_number)
    check_phone_number = User.filter_by(phone_number=phone_number).first()
    str_check_phone_number = str(check_phone_number)

    if value == "1":
        if not phone_number and str_check_phone_number == phone_number:
            record_phrase()
        else:
            db.session.add(
                phone_number = phone_number,
                session_id = session_id,
                level = level,
                last_input = value
                file = file
            )
            db.session.commit()



#This function manages the file retrieval and playback

@app.route("/voice/service/file", methods=["GET","POST"])
def service_file():
    pass



#We start the server and check whether the environment will avail a port
#alternatively, we can assign port 3000 to the application

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT") or 3000, debug=True)
