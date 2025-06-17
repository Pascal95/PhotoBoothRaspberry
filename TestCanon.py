import subprocess
import tkinter as tk
from tkinter import messagebox
import threading
import os
import time

class PhotoBooth:
    def __init__(self, root):
        self.root = root
        self.root.title("Live View Canon EOS 2000D")
        self.root.geometry("400x200")

        self.live_process = None

        self.start_button = tk.Button(root, text="Lancer Live View", command=self.start_live)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Arrêter Live View", command=self.stop_live)
        self.stop_button.pack(pady=10)

        self.capture_button = tk.Button(root, text="Prendre une photo", command=self.capture_photo)
        self.capture_button.pack(pady=10)

    def start_live(self):
        if self.live_process is not None:
            messagebox.showinfo("Info", "Live déjà en cours.")
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
            time.sleep(1)  # pause pour libérer le périphérique

    def capture_photo(self):
        self.stop_live()
        time.sleep(0.5)  # petite pause de sécurité
        try:
            filename = "photo.jpg"
            subprocess.run(["gphoto2", "--capture-image-and-download", f"--filename={filename}"], check=True)
            messagebox.showinfo("Photo prise", f"Image enregistrée : {filename}")
            os.system(f"xdg-open {filename}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Erreur", "Échec de la capture. Vérifie la connexion.")
        finally:
            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoBooth(root)
    root.mainloop()