import cv2
from tkinter import Tk, Label
from PIL import Image, ImageTk
import time
from tkinter import Button
import subprocess

# Choix de la source vidéo (0 ou 1 selon la carte de capture)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Impossible d’ouvrir le flux HDMI")

# Création de la fenêtre
root = Tk()
root.title("Live HDMI")
video_label = Label(root)
video_label.pack()

def update_frame():
    ret, frame = cap.read()
    if ret:
        # Redimensionne le flux pour s’adapter à la fenêtre si besoin
        frame = cv2.resize(frame, (800, 600))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
        video_label.imgtk = img
        video_label.configure(image=img)
    video_label.after(10, update_frame)

update_frame()

def prendre_photo():
    success = False
    attempts = 0
    max_attempts = 3

    while not success and attempts < max_attempts:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        try:
            # Démontage automatique du volume gphoto2
            subprocess.run([
                "gio", "mount", "-u", "gphoto2://Canon_Inc._Canon_Digital_Camera/"
            ], stderr=subprocess.DEVNULL)

            time.sleep(1)  # pause pour libérer l’USB

            # Capture réelle
            subprocess.run([
                "gphoto2",
                "--capture-image-and-download",
                f"--filename={filename}",
                "--keep",
                "--force-overwrite"
            ], check=True)

            print(f"✅ Photo enregistrée : {filename}")
            success = True
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Tentative {attempts+1} échouée : {e}")
            time.sleep(2)
            attempts += 1

    if not success:
        print("❌ Échec de la prise de photo après plusieurs tentatives.")

bouton_photo = Button(root, text="Prendre une photo", command=prendre_photo)
bouton_photo.pack(pady=10)

root.mainloop()
cap.release()