import os
import threading
import yt_dlp
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# Default download folder
download_folder = os.getcwd()

# Function to choose download folder
def choose_folder():
    global download_folder
    folder = filedialog.askdirectory()
    if folder:
        download_folder = folder
        folder_label.config(text=f"Save Location: {download_folder}")

# Function to update progress bar
def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)  # Avoid division by zero
        percent = (downloaded / total) * 100
        progress_bar["value"] = percent
        progress_label.config(text=f"Downloading... {percent:.2f}%")
    elif d['status'] == 'finished':
        progress_label.config(text="Download Complete!")

# Function to download video
def download_video(resolution="1080p"):
    platform = platform_var.get()
    video_url = url_entry.get().strip()

    if not video_url:
        messagebox.showerror("Error", "Please enter a valid video URL.")
        return

    download_button.config(state="disabled")
    progress_bar["value"] = 0
    progress_label.config(text="Starting Download...")

    def download_task():
        try:
            filename_template = os.path.join(download_folder, f"{platform}_%(title)s.%(ext)s")

            # Modify the ydl_opts to download 1080p by default
            ydl_opts = {
                "outtmpl": filename_template,
                "format": f"bestvideo[height={resolution}]+bestaudio/best" if resolution else "best",
                "progress_hooks": [progress_hook]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            messagebox.showinfo("Success", f"Download Completed at {resolution}!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            download_button.config(state="normal")

    threading.Thread(target=download_task).start()

# GUI Setup
root = tk.Tk()
root.title("Kaluwal Video Downloader")
root.geometry("700x500")
root.resizable(False, False)

# Platform Selection
tk.Label(root, text="Select Platform:", font=("Arial", 12)).pack(pady=5)
platform_var = tk.StringVar(value="YouTube")
platform_menu = ttk.Combobox(root, textvariable=platform_var, values=["YouTube", "TikTok", "Facebook", "Instagram Reels", "Twitter"], state="readonly", font=("Arial", 12))
platform_menu.pack(pady=5)

# URL Entry
tk.Label(root, text="Enter Video URL:", font=("Arial", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=60, font=("Arial", 12))
url_entry.pack(pady=5)

# Choose Folder Button
folder_label = tk.Label(root, text=f"Save Location: {download_folder}", font=("Arial", 10), fg="gray")
folder_label.pack(pady=5)
choose_folder_button = tk.Button(root, text="Choose Folder", font=("Arial", 10), command=choose_folder)
choose_folder_button.pack(pady=5)

# Progress Bar
progress_label = tk.Label(root, text="", font=("Arial", 10))
progress_label.pack(pady=5)
progress_bar = ttk.Progressbar(root, length=500, mode="determinate")
progress_bar.pack(pady=5)

# Download Button
download_button = tk.Button(root, text="Download 1080p", font=("Arial", 12), command=lambda: download_video("1080p"))
download_button.pack(pady=20)

# Disclaimer
tk.Label(root, text="Disclaimer: Ensure you have permission to download and use the content.", font=("Arial", 8), fg="gray").pack()

# Run the GUI
root.mainloop()
