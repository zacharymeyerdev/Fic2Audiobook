# file_manager.py
import os
from text_to_speech import text_to_speech

def save_chapter(text, title, chapter_number, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_name = f"{title}_Chapter_{chapter_number}.mp3"
    output_path = os.path.join(output_dir, file_name)
    text_to_speech(text, output_path)
