import pickle
from elevenlabs import clone, set_api_key

set_api_key("Your API key here")  # Eleven labs

try:
    with open('voice.pickle', 'rb') as f:
        voice = pickle.load(f)
except (OSError, IOError) as e:
    voice = # Your code here
    with open('voice.pickle', 'wb') as f:
        pickle.dump(voice, f)
