import threading
import time
import pyttsx3
import speech_recognition as sr
from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_socketio import SocketIO
from flask_cors import CORS
import urllib.parse

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for local testing

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Function to handle voice recognition and emit the recognized text
def recognize_voice():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    # SpeakText("Hello Aryan. Yazy ka weakling.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        print("Listening for voice command...")
        with microphone as source:
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            command=command.lower()
            print(f"Recognized: {command}")
            # Emit recognized command to connected clients
            if(command=="next"):
                socketio.emit('voice_command',  {'command': 'Next'})
                
            if(command=="exit"):
                break
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        time.sleep(0.5)  # Add a small delay to avoid rapid polling

# Flask route
@app.route('/')
def index():
    return "Flask and Voice Recognition Running"

def get_wikipedia_sections(url):
    # Make a request to fetch the content of the page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return []

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the section headings (h2, h3, h4, etc.)
    sections = []
    for heading in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
        section_title = heading.get_text().strip()
        temp=section_title.split(' ')
        final=""
        for i in temp:
            final=final+i
            if(i!=temp[len(temp)-1]):
                final=final+'_'
        sections.append(urllib.parse.quote(final))

    return sections

@app.route('/next', methods=['GET', 'POST'])
def next():
    url=request.json
    url=url['url']
    sections = get_wikipedia_sections(url)
    sections[0]='#'
    print(sections)
    x=url.split('#')
    newurl=x[0]
    if(len(x)==1):
        newurl=newurl+'#'+sections[1]
    else:
        ind=sections.index(x[1])
        if(ind==(len(sections)-1)):
            newurl=url
        else:
            newurl=newurl+'#'+sections[ind+1]
    print(newurl)
    # print(sections)
    # print(url)
    return jsonify({"url":newurl})
    # print(url["url"]['url'])
    # print(url.url)

if __name__ == '__main__':
    # Run the voice recognition in a separate thread
    threading.Thread(target=recognize_voice).start()
    socketio.run(app, host='localhost', port=5000)
