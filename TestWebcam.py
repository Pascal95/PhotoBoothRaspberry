import cv2
import subprocess
import threading
import time
import os
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
from datetime import datetime

class PhotoBoothApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Photobooth - Live View + Capture")
        self.window.geometry("800x600")

        self.video_label = Label(self.window)
        self.video_label.pack()

        self.capture_button = Button(self.window, text="📸 Prendre une photo", command=self.capture_photo, font=("Arial", 14), bg="green", fg="white")
        self.capture_button.pack(pady=10)

        self.running = True
        self.start_video_loop()

    def start_video_loop(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        if self.running:
            self.window.after(10, self.update_frame)

    def capture_photo(self):
        # Étape 1 : Unmount automatique (à adapter selon le nom de ton volume)
        try:
            subprocess.run(["gio", "mount", "-u", "gphoto2://Canon_Inc._Canon_Digital_Camera/"], check=True)
            print("✅ Volume démonté avec succès.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Impossible de démonter le volume (peut-être déjà démonté) : {e}")

        # Étape 2 : Prendre la photo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        try:
            subprocess.run(["gphoto2", "--capture-image-and-download", "--filename", filename], check=True)
            print(f"✅ Photo capturée : {filename}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de la capture : {e}")

    def on_close(self):
        self.running = False
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        self.window.destroy()

if __name__ == "__main__":
    root = Tk()
    app = PhotoBoothApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
