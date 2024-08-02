from flask import Flask, request, send_file, render_template, jsonify
from elevenlabs.client import ElevenLabs
import openai
from elevenlabs import save
import requests
import pickle
import os

app = Flask(__name__)

API_KEY = "sk_a32d218a5e81ca0adf3a48cdda41fa1a69542ac1fd3c5f4e"  
OPENAI_API_KEY = "sk-proj-jrkhgJkR0L62EF4ey3JsT3BlbkFJbpApjU3BbHSv6JnNf2Jh"  
MODEL_NAME = "gpt-4o-mini"
VOICE_PICKLE_FILE = 'voice.pickle'
AUDIO_FOLDER = 'audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)
client = ElevenLabs(
  api_key="sk_a32d218a5e81ca0adf3a48cdda41fa1a69542ac1fd3c5f4e"
)

RESPONSE_AUDIO_FILE = os.path.join(AUDIO_FOLDER, 'response_elevenlabs.mp3')
messages = [{"role": "system", "content": "Your initial prompt here"}]

def get_voice_from_pickle(file_path):
    try:
        with open(file_path, 'rb') as f:
            voice = pickle.load(f)
            return voice
    except FileNotFoundError:
        # Raise a specific exception or return a clear error message
        raise ValueError("Voice pickle file not found. Please provide a valid voice ID.")

def get_response_text_from_model(messages):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=messages
        )
        response_text = response.choices[0].message['content']
        return response_text
    except Exception as e:
        return str(e)

def write_audio_to_file(response_text, voice, file_path):
    acsent = client.generate(text=response_text, voice=voice)
    save(acsent,file_path)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/message', methods=['GET', 'POST'])
def process_message():
    if request.method == 'POST':
        user_data = request.get_json()
        user_message = user_data.get('message')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        messages.append({"role": "user", "content": user_message})
        response_text = get_response_text_from_model(messages)
        
        voice = get_voice_from_pickle("voice.pickle")
        write_audio_to_file(response_text, voice, "response_elevenlabs.mp3")

        if os.path.exists("response_elevenlabs.mp3"):
            return send_file("response_elevenlabs.mp3", mimetype='audio/mp3')
        else:
            return jsonify({'error': 'Audio file not created'}), 500

    else:
        return render_template('index.html')

def main():
    openai.api_key = "sk-proj-jrkhgJkR0L62EF4ey3JsT3BlbkFJbpApjU3BbHSv6JnNf2Jh"
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':
    main()