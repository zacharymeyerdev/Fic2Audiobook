import subprocess
import sys

# Function to install packages
def install_packages():
    with open('requirements.txt', 'r') as f:
        packages = f.readlines()
    for package in packages:
        package = package.strip()
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure all dependencies are installed
install_packages()

# Import necessary modules
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scraper import scrape_fanfiction
from cleaner import clean_text
from file_manager import save_chapter
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
        
        self.output_label = ttk.Label(root, text="Output Directory:")
        self.output_label.grid(column=0, row=3, padx=10, pady=5)
        
        self.output_button = ttk.Button(root, text="Browse", command=self.browse_directory)
        self.output_button.grid(column=1, row=3, padx=10, pady=5, sticky='w')
        
        self.convert_button = ttk.Button(root, text="Convert", command=self.convert_fanfiction)
        self.convert_button.grid(column=1, row=4, padx=10, pady=20, sticky='e')
        
        self.output_dir = ''
    
    def browse_directory(self):
        self.output_dir = filedialog.askdirectory()
        
    def convert_fanfiction(self):
        url = self.url_entry.get()
        site = self.site_var.get()
        title = self.title_entry.get()
        
        if not url or not site or not title or not self.output_dir:
            messagebox.showerror("Error", "Please fill all fields and select an output directory.")
            return
        
        story_text = scrape_fanfiction(url, site)
        cleaned_text = clean_text(story_text)
        chapters = split_into_chapters(cleaned_text)
        
        for i, chapter in enumerate(chapters, start=1):
            save_chapter(chapter, title, i, self.output_dir)
        
        messagebox.showinfo("Success", "Conversion completed successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Fanfiction2AudiobookApp(root)
    root.mainloop()
