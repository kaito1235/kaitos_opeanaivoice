import pickle
from flask import Flask, request, send_file, render_template
import openai
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key="sk_6ef60c6acf145a83c8d06bfd1fa294afd3278b9172813d7c")

app = Flask(__name__)

API_KEY = "sk_6ef60c6acf145a83c8d06bfd1fa294afd3278b9172813d7c"  # Eleven labs
OPENAI_API_KEY = "sk-proj-bGR6GSiT1p1LtejwPXpZT3BlbkFJaZakQWvHvTW8ha7FKGQT"
MODEL_NAME = "gpt-3.5-turbo"
VOICE_PICKLE_FILE = 'voice.pickle'
RESPONSE_AUDIO_FILE = 'response_elevenlabs.mp3'
messages = [{"role": "system", "content": "Your initial prompt here"}]

def get_voice_from_pickle(file_path):
    # Loads and returns a voice object from a pickle file
    
    with open(file_path, 'rb') as f:
        voice = pickle.load(f)
    return voice

def get_response_text_from_model(messages):
    # Sends the messages to the OpenAI model and returns the generated response
    try:
        # Send the messages to the OpenAI model
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        
        # Extract the generated response text
        response_text = response.choices[0].message['content']
        return response_text
    
    except Exception as e:
        return str(e)

def write_audio_to_file(response_text, voice, file_path):
    # Writes the audio version of the response_text to the file_path
        url = "https://api.elevenlabs.io/v1/speech"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        'text': response_text,
        'voice': voice,
        'format': 'wav'
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
    # Returns the homepage
    # Your code here

@app.route('/message', methods=['POST'])
def process_message():
    # Processes the user message and returns an audio file with the response
    # This function calls the other functions in this file
    # Your code here
    
    return send_file(RESPONSE_AUDIO_FILE, mimetype='audio/mp3')

def main():
    # Sets the API keys and starts the server
    elevenlabs.set_api_key(API_KEY)
    openai.api_key = OPENAI_API_KEY
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':
    main()
