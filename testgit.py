import cv2
import subprocess
from tkinter import Tk, Button, Label
from PIL import Image, ImageTk

# Initialisation interface
root = Tk()
root.title("Photobooth")
root.geometry("800x600")

# Ouverture de la carte de capture HDMI (devrait être /dev/video0 ou index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Impossible d'accéder au flux HDMI (webcam)")

# Label pour afficher la vidéo
video_label = Label(root)
video_label.pack()

def show_frame():
    ret, frame = cap.read()
    if ret:
        # Conversion pour Tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    video_label.after(10, show_frame)

def take_photo():
    try:
        filename = "photo_capture.jpg"
        subprocess.run([
            "gphoto2", "--capture-image-and-download", "--filename", filename
        ], check=True)
        print(f"Photo enregistrée : {filename}")
    except subprocess.CalledProcessError as e:
        print("Erreur lors de la capture :", e)

# Bouton photo
btn = Button(root, text="📸 Prendre une photo", command=take_photo)
btn.pack(pady=20)

# Lancer la vidéo
show_frame()
root.mainloop()

# Libérer la ressource vidéo à la fin
cap.release()