import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time

class PhotoBoothApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Photobooth")
        self.window.geometry("800x600")

        self.video_source = 0  # L'index de la webcam USB HDMI (parfois 1 si autre webcam active)
        self.vid = cv2.VideoCapture(self.video_source)

        self.label = tk.Label(window)
        self.label.pack()

        self.capture_btn = tk.Button(window, text="📸 Prendre une photo", command=self.take_snapshot)
        self.capture_btn.pack(pady=10)

        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Convertir l'image au format compatible tkinter
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.window.after(10, self.update)

    def take_snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"photo_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✅ Photo enregistrée : {filename}")

    def on_close(self):
        self.vid.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoBoothApp(root)
    root.mainloop()