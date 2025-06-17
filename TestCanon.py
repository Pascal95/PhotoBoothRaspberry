import subprocess
import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

class PhotoBooth:
    def __init__(self, root):
        self.root = root
        self.root.title("Photobooth Canon EOS 2000D")
        self.root.geometry("400x200")

        self.live_process = None

        self.start_button = tk.Button(root, text="Lancer Live View", command=self.start_live)
        self.start_button.pack(pady=10)

        self.capture_button = tk.Button(root, text="Prendre une photo", command=self.capture_photo)
        self.capture_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Quitter", command=self.exit)
        self.stop_button.pack(pady=10)

    def start_live(self):
        if self.live_process:
            return

        def run_live():
            self.live_process = subprocess.Popen(
                "gphoto2 --stdout --capture-movie | ffplay -window_title LiveView -",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        threading.Thread(target=run_live, daemon=True).start()

    def stop_live(self):
        if self.live_process:
            self.live_process.terminate()
            self.live_process = None
            time.sleep(1)

    def capture_photo(self):
        def capture():
            self.capture_button.config(state="disabled")
            self.stop_live()
            time.sleep(1)

            try:
                filename = f"photo_{int(time.time())}.jpg"
                result = subprocess.run(
                    ["gphoto2", "--capture-image-and-download", f"--filename={filename}"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                messagebox.showinfo("Photo prise", f"Image sauvegardée : {filename}")
                os.system(f"xdg-open {filename}")
            except subprocess.CalledProcessError as e:
                error_msg = f"Erreur lors de la capture:\n{e.stderr}"
                print(error_msg)
                messagebox.showerror("Erreur", error_msg)
            finally:
                time.sleep(1)
                self.start_live()
                self.capture_button.config(state="normal")

        threading.Thread(target=capture).start()

    def exit(self):
        self.stop_live()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoBooth(root)
    root.mainloop()