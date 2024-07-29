import pickle
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key="sk_6ef60c6acf145a83c8d06bfd1fa294afd3278b9172813d7c")

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