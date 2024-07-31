from flask import Flask, request, send_file, render_template, jsonify
import openai
import requests
import pickle

app = Flask(__name__)

API_KEY = "YOUR_ELEVEN_LABS_API_KEY"  # Replace with your Eleven Labs API Key
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API Key
MODEL_NAME = "gpt-3.5-turbo"
VOICE_PICKLE_FILE = 'voice.pickle'
RESPONSE_AUDIO_FILE = 'response_elevenlabs.mp3'
messages = [{"role": "system", "content": "Your initial prompt here"}]

def get_voice_from_pickle(file_path):
    try:
        with open(file_path, 'rb') as f:
            voice = pickle.load(f)
        return voice
    except FileNotFoundError:
        return "Default Voice"  # Fallback to a default voice if pickle file not found

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
    url = "https://api.elevenlabs.io/v1/speech"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        'text': response_text,
        'voice': voice,
        'format': 'mp3'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open(file_path, 'wb') as audio_file:
            audio_file.write(response.content)
        print(f"Audio file saved as {file_path}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/message', methods=['POST'])
def process_message():
    user_data = request.get_json()
    user_message = user_data.get('message')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    messages.append({"role": "user", "content": user_message})
    response_text = get_response_text_from_model(messages)
    
    voice = get_voice_from_pickle(VOICE_PICKLE_FILE)
    write_audio_to_file(response_text, voice, RESPONSE_AUDIO_FILE)
    
    return send_file(RESPONSE_AUDIO_FILE, mimetype='audio/mp3')


def main():
    openai.api_key = OPENAI_API_KEY
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':
    main()
