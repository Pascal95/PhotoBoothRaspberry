import cv2
from tkinter import Tk, Label
from PIL import Image, ImageTk

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
root.mainloop()
cap.release()