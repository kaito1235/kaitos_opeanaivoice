import pickle
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key="sk_a32d218a5e81ca0adf3a48cdda41fa1a69542ac1fd3c5f4e")

try:
   with open('voice.pickle', 'rb') as f:
       voice = pickle.load(f)
except (OSError, IOError) as e:
   voice = client.clone(
       name="Ayo",
       description="test",
       files=["./9ja_voice.mp3"],
   )
   with open('voice.pickle', 'wb') as f:
       pickle.dump(voice, f)