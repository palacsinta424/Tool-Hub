import tkinter as tk
from tkinter import messagebox
import urllib.request
import time
import threading

TEST_URL = "http://ipv4.download.thinkbroadband.com/10MB.zip"
TEST_SIZE_MB = 10
TIMEOUT = 20

def test_speed():
    try:
        start_time = time.time()
        downloaded = 0

        with urllib.request.urlopen(TEST_URL, timeout=TIMEOUT) as response:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                downloaded += len(chunk)

        elapsed = time.time() - start_time
        speed_mbps = (downloaded * 8) / (elapsed * 1_000_000)

        result_label.config(
            text=f"Download Speed:\n{speed_mbps:.2f} Mbps"
        )

    except Exception as e:
        messagebox.showerror(
            "Speed Test Failed",
            "Could not test speed.\nCheck your internet or firewall."
        )

    finally:
        test_button.config(state="normal")

def start_test():
    result_label.config(text="Testing speed...\nPlease wait")
    test_button.config(state="disabled")

    threading.Thread(target=test_speed, daemon=True).start()

# ---------------------------
# GUI
# ---------------------------
window = tk.Tk()
window.title("Internet Speed Tester")
window.geometry("300x220")
window.resizable(False, False)

tk.Label(
    window,
    text="Internet Speed Tester",
    font=("Arial", 16, "bold")
).pack(pady=10)

result_label = tk.Label(
    window,
    text="Click Start to test",
    font=("Arial", 11),
    justify="center"
)
result_label.pack(pady=15)

test_button = tk.Button(
    window,
    text="Start Test",
    width=20,
    command=start_test
)
test_button.pack(pady=10)

tk.Label(
    window,
    text="Measures real download speed",
    font=("Arial", 9),
    fg="gray"
).pack(pady=5)

window.mainloop()
