# text_to_speech.py
from gtts import gTTS

def text_to_speech(text, output_file):
    tts = gTTS(text)
    tts.save(output_file)
