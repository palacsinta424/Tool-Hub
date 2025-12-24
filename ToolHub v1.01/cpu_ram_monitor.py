import tkinter as tk
import psutil
import threading
import time
import sys
import os

# ---------------------------
# Request admin on Windows
# ---------------------------
def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    if sys.platform == "win32" and not is_admin():
        # Relaunch the script with admin privileges
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
        sys.exit()

# Uncomment this line to request admin on start
request_admin()

# ---------------------------
# GUI
# ---------------------------
window = tk.Tk()
window.title("CPU & RAM Monitor")
window.geometry("250x120")
window.resizable(False, False)
window.attributes("-topmost", True)  # Always on top

label = tk.Label(window, text="", font=("Arial", 12))
label.pack(pady=20)

# ---------------------------
# Update CPU/RAM usage
# ---------------------------
def update_usage():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        label.config(text=f"CPU Usage: {cpu}%\nRAM Usage: {ram}%")
        time.sleep(1)

threading.Thread(target=update_usage, daemon=True).start()
window.mainloop()
