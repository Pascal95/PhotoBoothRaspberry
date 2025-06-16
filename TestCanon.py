import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os
import threading

class LiveViewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photobooth Live View")
        self.root.geometry("800x600")

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.capture_button = tk.Button(root, text="📸 Prendre une photo", command=self.capture_photo)
        self.capture_button.pack(pady=10)

        self.running = True
        self.video_thread = threading.Thread(target=self.live_view_loop)
        self.video_thread.start()

    def live_view_loop(self):
        while self.running:
            os.system("gphoto2 --capture-preview --filename preview.jpg > /dev/null 2>&1")
            if os.path.exists("preview.jpg"):
                img = Image.open("preview.jpg")
                img = img.resize((800, 500))
                imgtk = ImageTk.PhotoImage(img)
                self.video_label.config(image=imgtk)
                self.video_label.image = imgtk

    def capture_photo(self):
        self.capture_button.config(state="disabled")
        subprocess.call(["gphoto2", "--capture-image-and-download", "--filename", "capture.jpg"])
        if os.path.exists("capture.jpg"):
            img = Image.open("capture.jpg")
            img.show()
        self.capture_button.config(state="normal")

    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveViewApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()