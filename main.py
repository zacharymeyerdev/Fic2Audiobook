import subprocess
import sys
import os
import pyttsx3

# Function to install packages
def install_packages():
    try:
        # Upgrade pip to the latest version
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--user"])

        # Install packages from requirements.txt
        with open('requirements.txt', 'r') as f:
            packages = f.readlines()
        for package in packages:
            package = package.strip()
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing package: {e}")
        sys.exit(1)

# Ensure all dependencies are installed
install_packages()

# Import necessary modules
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scraper import scrape_fanfiction
from cleaner import clean_text
from file_manager import save_chapter_text, save_combined_text, save_chapter_audio, save_combined_audio
from splitter import split_into_chapters

class Fanfiction2AudiobookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fanfiction2Audiobook")
        
        self.url_label = ttk.Label(root, text="Fanfiction URL:")
        self.url_label.grid(column=0, row=0, padx=10, pady=5)
        
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.grid(column=1, row=0, padx=10, pady=5)
        
        self.site_label = ttk.Label(root, text="Website:")
        self.site_label.grid(column=0, row=1, padx=10, pady=5)
        
        self.site_var = tk.StringVar()
        self.site_combobox = ttk.Combobox(root, textvariable=self.site_var)
        self.site_combobox['values'] = ('fanfiction.net', 'ao3', 'royalroad', 'wattpad', 'tumblr')
        self.site_combobox.grid(column=1, row=1, padx=10, pady=5)
        
        self.title_label = ttk.Label(root, text="Fanfiction Title:")
        self.title_label.grid(column=0, row=2, padx=10, pady=5)
        
        self.title_entry = ttk.Entry(root, width=50)
        self.title_entry.grid(column=1, row=2, padx=10, pady=5)

        self.start_chapter_label = ttk.Label(root, text="Start Chapter:")
        self.start_chapter_label.grid(column=0, row=3, padx=10, pady=5)

        self.start_chapter_entry = ttk.Entry(root, width=50)
        self.start_chapter_entry.grid(column=1, row=3, padx=10, pady=5)

        self.end_chapter_label = ttk.Label(root, text="End Chapter:")
        self.end_chapter_label.grid(column=0, row=4, padx=10, pady=5)

        self.end_chapter_entry = ttk.Entry(root, width=50)
        self.end_chapter_entry.grid(column=1, row=4, padx=10, pady=5)
        
        self.output_label = ttk.Label(root, text="Output Directory:")
        self.output_label.grid(column=0, row=5, padx=10, pady=5)
        
        self.output_button = ttk.Button(root, text="Browse", command=self.browse_directory)
        self.output_button.grid(column=1, row=5, padx=10, pady=5, sticky='w')
        
        self.output_option_label = ttk.Label(root, text="Output Option:")
        self.output_option_label.grid(column=0, row=6, padx=10, pady=5)

        self.output_option_var = tk.StringVar()
        self.output_option_combobox = ttk.Combobox(root, textvariable=self.output_option_var)
        self.output_option_combobox['values'] = ('Text Only', 'MP3 Only', 'Both')
        self.output_option_combobox.grid(column=1, row=6, padx=10, pady=5)
        self.output_option_combobox.bind('<<ComboboxSelected>>', self.output_option_changed)
        
        self.voice_label = ttk.Label(root, text="Voice:")
        self.voice_label.grid(column=0, row=7, padx=10, pady=5)
        
        self.voice_var = tk.StringVar()
        self.voice_combobox = ttk.Combobox(root, textvariable=self.voice_var)
        self.voice_combobox['values'] = ('Male', 'Female')
        self.voice_combobox.grid(column=1, row=7, padx=10, pady=5)
        self.voice_combobox.bind('<<ComboboxSelected>>', self.play_voice_sample)
        self.voice_combobox.config(state='disabled')
        
        self.speed_label = ttk.Label(root, text="Speaking Speed (%):")
        self.speed_label.grid(column=0, row=8, padx=10, pady=5)
        
        self.speed_var = tk.IntVar(value=100)
        self.speed_slider = ttk.Scale(root, from_=1, to=200, orient='horizontal', variable=self.speed_var)
        self.speed_slider.grid(column=1, row=8, padx=10, pady=5)
        self.speed_slider.config(state='disabled')
        
        self.convert_button = ttk.Button(root, text="Convert", command=self.convert_fanfiction)
        self.convert_button.grid(column=1, row=9, padx=10, pady=20, sticky='e')
        
        self.output_dir = ''
    
    def browse_directory(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_label.config(text=f"Output Directory: {self.output_dir}")
        
    def validate_chapters(self, start_chapter, end_chapter):
        if not start_chapter.isdigit() or not end_chapter.isdigit():
            return False, "Chapters must be positive integers."
        
        start_chapter = int(start_chapter)
        end_chapter = int(end_chapter)
        
        if start_chapter <= 0 or end_chapter <= 0:
            return False, "Chapters must be greater than zero."
        
        if start_chapter > end_chapter:
            return False, "Start chapter must be less than or equal to end chapter."
        
        return True, ""
    
    def output_option_changed(self, event):
        output_option = self.output_option_var.get()
        if output_option in ('MP3 Only', 'Both'):
            self.voice_combobox.config(state='normal')
            self.speed_slider.config(state='normal')
        else:
            self.voice_combobox.config(state='disabled')
            self.speed_slider.config(state='disabled')

    def play_voice_sample(self, event):
        voice = self.voice_var.get()
        speed = self.speed_var.get()

        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if voice == 'Male':
            engine.setProperty('voice', voices[0].id)
        elif voice == 'Female':
            engine.setProperty('voice', voices[1].id)
            
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate * (speed / 100))
        
        engine.say(f"This is a voice sample of the {voice} type.")
        engine.runAndWait()

    def convert_fanfiction(self):
        url = self.url_entry.get()
        site = self.site_var.get()
        title = self.title_entry.get()
        start_chapter = self.start_chapter_entry.get()
        end_chapter = self.end_chapter_entry.get()
        output_option = self.output_option_var.get()
        voice = self.voice_var.get()
        speed = self.speed_var.get()
        
        if not url or not site or not title or not start_chapter or not end_chapter or not self.output_dir or not output_option:
            messagebox.showerror("Error", "Please fill all fields and select an output directory.")
            return
        
        valid, message = self.validate_chapters(start_chapter, end_chapter)
        if not valid:
            messagebox.showerror("Error", message)
            return

        start_chapter = int(start_chapter)
        end_chapter = int(end_chapter)
        
        chapters = scrape_fanfiction(url, site, start_chapter, end_chapter)
        chapter_texts = []
        
        fanfiction_dir = os.path.join(self.output_dir, title)
        os.makedirs(fanfiction_dir, exist_ok=True)
        
        txt_dir = os.path.join(fanfiction_dir, 'txt files')
        mp3_dir = os.path.join(fanfiction_dir, 'mp3 files')
        os.makedirs(txt_dir, exist_ok=True)
        os.makedirs(mp3_dir, exist_ok=True)
        
        for i, chapter in enumerate(chapters, start=start_chapter):
            cleaned_chapter = clean_text(chapter)
            if output_option in ('Text Only', 'Both'):
                save_chapter_text(cleaned_chapter, title, i, txt_dir)
                chapter_texts.append(cleaned_chapter)
            if output_option in ('MP3 Only', 'Both'):
                save_chapter_audio(cleaned_chapter, title, i, mp3_dir, voice, speed)
        
        if output_option in ('Text Only', 'Both'):
            save_combined_text(chapter_texts, title, txt_dir)
        if output_option in ('MP3 Only', 'Both'):
            save_combined_audio(chapter_texts, title, mp3_dir, voice, speed)
        
        messagebox.showinfo("Success", "Conversion completed successfully!")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Fanfiction2AudiobookApp(root)
    root.mainloop()
