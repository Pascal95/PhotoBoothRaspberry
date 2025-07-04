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
        self.video_thread = threading.Thread(target=self.video_loop)
        self.video_thread.start()

    def video_loop(self):
        cap = cv2.VideoCapture(0)  # Logitech C920 généralement détectée à l'index 0
        while self.running:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            else:
                print("Erreur lors de la lecture de la webcam.")
            time.sleep(0.03)
        cap.release()

    def capture_photo(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        try:
            subprocess.run(["gphoto2", "--capture-image-and-download", "--filename", filename], check=True)
            print(f"✅ Photo capturée : {filename}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de la capture : {e}")

    def on_close(self):
        self.running = False
        self.window.destroy()

if __name__ == "__main__":
    root = Tk()
    app = PhotoBoothApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
