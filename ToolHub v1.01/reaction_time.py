import tkinter as tk
from tkinter import messagebox
import random
import time

start_time = 0

def start_test():
    global start_time
    message_label.config(text="Wait for green...")
    window.after(random.randint(2000, 5000), show_go)

def show_go():
    global start_time
    message_label.config(text="CLICK NOW!", bg="green")
    start_time = time.time()
    click_button.config(state="normal")

def record_reaction():
    global start_time
    reaction = time.time() - start_time
    messagebox.showinfo("Reaction Time", f"Your reaction time: {reaction:.3f} seconds")
    message_label.config(text="Press start to try again", bg="SystemButtonFace")
    click_button.config(state="disabled")

window = tk.Tk()
window.title("Reaction Time Tester")
window.geometry("300x200")

message_label = tk.Label(window, text="Press Start to begin", font=("Arial", 12))
message_label.pack(pady=20)

tk.Button(window, text="Start Test", command=start_test).pack(pady=5)
click_button = tk.Button(window, text="Click Me!", state="disabled", command=record_reaction)
click_button.pack(pady=10)

window.mainloop()
