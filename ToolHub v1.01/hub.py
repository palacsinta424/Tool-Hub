import tkinter as tk
import subprocess
import sys

# ---------------------------
# Launch external Python tools
# ---------------------------
def launch(tool_file):
    python = sys.executable
    subprocess.Popen([python, tool_file])

# ---------------------------
# Dark mode toggle
# ---------------------------
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = "#2E2E2E" if dark_mode else "SystemButtonFace"
    fg_color = "#FFFFFF" if dark_mode else "black"
    window.config(bg=bg_color)
    title_label.config(bg=bg_color, fg=fg_color)
    beta_label.config(bg=bg_color, fg=fg_color)
    credits_label.config(bg=bg_color, fg=fg_color)
    for btn in buttons:
        btn.config(bg=bg_color, fg=fg_color)

# ---------------------------
# GUI Setup
# ---------------------------
window = tk.Tk()
window.title("Tool Hub")
window.geometry("300x560")
window.resizable(False, False)

dark_mode = False
buttons = []

# ---------------------------
# Title & BETA label
# ---------------------------
title_label = tk.Label(window, text="🛠 Tool Hub", font=("Arial", 16, "bold"))
title_label.pack(pady=(15,2))

beta_label = tk.Label(window, text="IN BETA", font=("Arial",9,"italic"), fg="gray")
beta_label.pack(pady=(0,10))

# ---------------------------
# Tool buttons
# ---------------------------
tools = [
    ("Password Generator", "password_generator.py"),
    ("Password Bank", "password_bank.py"),
    ("To-Do List", "todolist.py"),
    ("Reaction Time Tester", "reaction_time.py"),
    ("CPS Counter", "cps_counter.py"),
    ("Internet Speed Tester", "internet_speed_test.py"),
    ("CPU/RAM Monitor", "cpu_ram_monitor.py"),
    ("Disk Space Checker", "disk_checker.py"),
    ("Unit Converter", "unit_converter.py")
]

for name, file in tools:
    btn = tk.Button(window, text=name, width=25, command=lambda f=file: launch(f))
    btn.pack(pady=5)
    buttons.append(btn)

# ---------------------------
# Dark mode & Exit
# ---------------------------
dark_btn = tk.Button(window, text="Toggle Dark Mode", width=25, command=toggle_dark_mode)
dark_btn.pack(pady=5)
buttons.append(dark_btn)

exit_btn = tk.Button(window, text="Exit", width=25, command=window.destroy)
exit_btn.pack(pady=10)
buttons.append(exit_btn)

# ---------------------------
# Credits
# ---------------------------
credits_label = tk.Label(window, text="Made by palacsinta424", font=("Arial", 8, "italic"), fg="gray")
credits_label.pack(side="bottom", pady=5)

window.mainloop()
