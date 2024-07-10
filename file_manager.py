import os
from gtts import gTTS
import pyttsx3

def save_chapter_text(chapter_text, title, chapter_number, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f"{title}_Chapter_{chapter_number}.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(chapter_text)

def save_combined_text(chapter_texts, title, output_dir):
    combined_text = '\n\n'.join(chapter_texts)
    file_path = os.path.join(output_dir, f"{title}_Combined.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(combined_text)

def save_chapter_audio(chapter_text, title, chapter_number, output_dir, voice, speed):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f"{title}_Chapter_{chapter_number}.mp3")
    tts = gTTS(text=chapter_text, lang='en')
    tts.save(file_path)

def save_combined_audio(chapter_texts, title, output_dir, voice, speed):
    combined_text = '\n\n'.join(chapter_texts)
    file_path = os.path.join(output_dir, f"{title}_Combined.mp3")

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')

    if voice == 'Male':
        engine.setProperty('voice', voices[0].id)
    elif voice == 'Female':
        engine.setProperty('voice', voices[1].id)

    engine.setProperty('rate', rate * (speed / 100))

    engine.save_to_file(combined_text, file_path)
    engine.runAndWait()
