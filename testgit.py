import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os

preview_process = None

def start_preview():
    global preview_process
    stop_preview()
    preview_process = subprocess.Popen([
        "gphoto2", "--capture-movie", "--stdout"
    ], stdout=subprocess.PIPE)

    mplayer_process = subprocess.Popen([
        "mplayer", "-"
    ], stdin=preview_process.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    preview_process.mplayer = mplayer_process

def stop_preview():
    global preview_process
    if hasattr(preview_process, 'mplayer'):
        preview_process.mplayer.terminate()
        preview_process.mplayer.wait()

def take_photo():
    stop_preview()
    try:
        filename = "capture.jpg"
        subprocess.run([
            "gphoto2", "--capture-image-and-download",
            "--filename", filename
        ], check=True)
        messagebox.showinfo("Photo prise", f"Photo enregistrée : {filename}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", "Échec de la capture photo.")
        print(e)
    start_preview()

def start_gui():
    root = tk.Tk()
    root.title("Photobooth")
    root.geometry("400x200")

    tk.Label(root, text="Appuyez pour prendre une photo").pack(pady=20)
    tk.Button(root, text="📸 Prendre une photo", command=take_photo).pack(pady=10)

    start_preview()
    root.protocol("WM_DELETE_WINDOW", lambda: (stop_preview(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    start_gui()