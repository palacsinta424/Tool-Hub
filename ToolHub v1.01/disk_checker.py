import tkinter as tk
import shutil
import threading
import time

def update_disk():
    while True:
        total, used, free = shutil.disk_usage("/")
        label.config(text=f"Free Space: {free//(1024**3)} GB")
        time.sleep(60)

window = tk.Tk()
window.title("Disk Space Checker")
window.geometry("200x100")

label = tk.Label(window, text="", font=("Arial",10))
label.pack(pady=10)

threading.Thread(target=update_disk, daemon=True).start()
window.mainloop()
