import tkinter as tk
from tkinter import messagebox, scrolledtext
import time
import json
import os

# ---------------------------
# Persistent storage
# ---------------------------
DATA_FILE = "cps_data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        cps_data = json.load(f)
else:
    cps_data = []  # List of dictionaries for each test

def save_cps_record(record):
    cps_data.append(record)
    with open(DATA_FILE, "w") as f:
        json.dump(cps_data, f, indent=4)

# ---------------------------
# CPS test logic
# ---------------------------
clicks = 0
start_time = None
DURATION = 10  # seconds

def register_click():
    global clicks, start_time
    if start_time is None:
        start_time = time.time()
        window.after(DURATION * 1000, end_test)
    clicks += 1
    clicks_label.config(text=f"Clicks: {clicks}")

def end_test():
    global clicks, start_time
    if start_time is None:
        return
    elapsed = time.time() - start_time
    cps = clicks / elapsed if elapsed > 0 else 0

    # Save the result
    record = {
        "time": elapsed,
        "clicks": clicks,
        "cps": round(cps, 2)
    }
    save_cps_record(record)

    messagebox.showinfo(
        "CPS Result",
        f"Test Time: {elapsed:.2f}s\n"
        f"Clicks: {clicks}\n"
        f"CPS: {cps:.2f}"
    )
    reset_test()

def reset_test():
    global clicks, start_time
    clicks = 0
    start_time = None
    clicks_label.config(text="Clicks: 0")

# ---------------------------
# Show summary
# ---------------------------
def show_summary():
    summary_window = tk.Toplevel(window)
    summary_window.title("CPS Summary")
    summary_window.geometry("400x400")

    scroll_text = scrolledtext.ScrolledText(summary_window, wrap=tk.WORD)
    scroll_text.pack(expand=True, fill="both", padx=10, pady=10)

    if not cps_data:
        scroll_text.insert(tk.END, "No CPS tests recorded yet.")
    else:
        for i, record in enumerate(cps_data, start=1):
            scroll_text.insert(
                tk.END,
                f"Test {i}:\n"
                f"  Time: {record['time']:.2f}s\n"
                f"  Clicks: {record['clicks']}\n"
                f"  CPS: {record['cps']:.2f}\n\n"
            )
    scroll_text.config(state="disabled")

# ---------------------------
# GUI setup
# ---------------------------
window = tk.Tk()
window.title("CPS Measurer")
window.geometry("320x300")
window.resizable(False, False)

title = tk.Label(window, text="CPS Measurer", font=("Arial", 16, "bold"))
title.pack(pady=10)

info = tk.Label(
    window,
    text=f"Click the button as fast as you can\nfor {DURATION} seconds!",
    font=("Arial", 10)
)
info.pack()

clicks_label = tk.Label(window, text="Clicks: 0", font=("Arial", 12))
clicks_label.pack(pady=10)

click_button = tk.Button(
    window,
    text="CLICK HERE",
    font=("Arial", 16),
    width=15,
    height=2,
    command=register_click
)
click_button.pack(pady=10)

reset_button = tk.Button(window, text="Reset", command=reset_test)
reset_button.pack(pady=5)

summary_button = tk.Button(window, text="Show Summary", command=show_summary)
summary_button.pack(pady=5)

window.mainloop()
