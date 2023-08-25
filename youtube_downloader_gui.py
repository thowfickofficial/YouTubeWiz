import os
import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import threading
import subprocess

class YouTubeWiz:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTubeWiz - Your YouTube Video Companion")

        self.url_label = tk.Label(root, text="Enter YouTube Video URL:")
        self.url_label.pack()
        
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()
        
        self.output_label = tk.Label(root, text="Enter Output Directory (default is current directory):")
        self.output_label.pack()
        
        self.output_dir = tk.Entry(root, width=50)
        self.output_dir.pack()
        
        self.quality_label = tk.Label(root, text="Select Video Quality:")
        self.quality_label.pack()
        
        self.quality_var = tk.StringVar()
        self.quality_var.set("720p")  # Default quality
        
        self.quality_options = ["360p", "480p", "720p", "1080p"]
        self.quality_menu = ttk.Combobox(root, textvariable=self.quality_var, values=self.quality_options)
        self.quality_menu.pack()
        
        self.download_button = ttk.Button(root, text="Download Video", command=self.download_video)
        self.download_button.pack()

        self.audio_button = ttk.Button(root, text="Download Audio", command=self.extract_audio)
        self.audio_button.pack()
        
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack()

        self.progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.pack()
        
        self.history_button = ttk.Button(root, text="Download History", command=self.show_history)
        self.history_button.pack()

        self.history = []

    def download_video(self):
        video_url = self.url_entry.get()
        download_dir = self.output_dir.get()
        selected_quality = self.quality_var.get()
        
        try:
            yt = YouTube(video_url, on_progress_callback=self.progress_callback)
            stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=selected_quality).first()
            thread = threading.Thread(target=stream.download, args=(download_dir,))
            thread.start()

            # Add to download history
            self.history.append((yt.title, selected_quality))
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
    
    def extract_audio(self):
        video_url = self.url_entry.get()
        download_dir = self.output_dir.get()
        
        try:
            yt = YouTube(video_url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            thread = threading.Thread(target=audio_stream.download, args=(download_dir,))
            thread.start()

            # Add to download history
            self.history.append((yt.title, "Audio"))
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def progress_callback(self, stream, chunk, remaining_bytes):
        total_bytes = stream.filesize
        downloaded_bytes = total_bytes - remaining_bytes
        percentage = (downloaded_bytes / total_bytes) * 100
        self.progress_bar['value'] = percentage
        self.status_label.config(text=f"Downloading: {percentage:.2f}%")
    
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Download History")

        if not self.history:
            tk.Label(history_window, text="No downloads in history.").pack()
            return
        
        for title, format in self.history:
            tk.Label(history_window, text=f"Title: {title}, Format: {format}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeWiz(root)
    root.mainloop()
