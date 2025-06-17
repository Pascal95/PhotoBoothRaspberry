import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os

preview_process = None

def start_preview():
    global preview_process
    stop_preview()  # on arrête si déjà lancé
    preview_process = subprocess.Popen(
        ["gphoto2", "--capture-movie", "--stdout"],
        stdout=subprocess.DEVNULL,  # pas affiché pour l'instant
        stderr=subprocess.DEVNULL
    )
    print("Live démarré")

def stop_preview():
    global preview_process
    if preview_process and preview_process.poll() is None:
        preview_process.terminate()
        preview_process.wait()
        print("Live arrêté")

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