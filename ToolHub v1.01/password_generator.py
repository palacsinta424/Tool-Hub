import tkinter as tk
from tkinter import messagebox
import random
import string
import json
import os
import base64

# ---------------------------
# File paths
# ---------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "password_data.json")

# ---------------------------
# XOR key
# ---------------------------
XOR_KEY = "toolhub_secret_key"

# ---------------------------
# XOR encrypt / decrypt
# ---------------------------
def xor_encrypt(text):
    encrypted = ''.join(
        chr(ord(c) ^ ord(XOR_KEY[i % len(XOR_KEY)]))
        for i, c in enumerate(text)
    )
    return base64.b64encode(encrypted.encode()).decode()

def xor_decrypt(encoded_text):
    encrypted = base64.b64decode(encoded_text).decode()
    return ''.join(
        chr(ord(c) ^ ord(XOR_KEY[i % len(XOR_KEY)]))
        for i, c in enumerate(encrypted)
    )

# ---------------------------
# Load password data
# ---------------------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        password_data = json.load(f)
else:
    password_data = {}

current_password = ""

# ---------------------------
# Save encrypted password
# ---------------------------
def save_password(pw):
    encrypted_pw = xor_encrypt(pw)

    if password_data:
        max_num = max(int(k.replace("passwordsaved", "")) for k in password_data)
        next_num = max_num + 1
    else:
        next_num = 1

    password_data[f"passwordsaved{next_num}"] = encrypted_pw

    with open(DATA_FILE, "w") as f:
        json.dump(password_data, f, indent=4)

# ---------------------------
# Get latest decrypted password
# ---------------------------
def get_latest_password():
    if not password_data:
        return ""

    max_num = max(int(k.replace("passwordsaved", "")) for k in password_data)
    encrypted_pw = password_data[f"passwordsaved{max_num}"]
    return xor_decrypt(encrypted_pw)

# ---------------------------
# Password generation
# ---------------------------
def generate_password():
    global current_password
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Password length must be a number.")
        return

    chars = string.ascii_letters + string.digits + string.punctuation
    current_password = ''.join(random.choice(chars) for _ in range(length))

    result_label.config(text=current_password)
    save_password(current_password)

# ---------------------------
# Reveal password
# ---------------------------
def remind_password():
    global current_password

    if not password_data:
        messagebox.showinfo("No Password", "No password saved yet.")
        return

    if messagebox.askyesno("Reveal", "Are you sure you want to reveal the latest password?"):
        current_password = get_latest_password()
        result_label.config(text=current_password)

# ---------------------------
# Copy password
# ---------------------------
def copy_password():
    if not current_password:
        messagebox.showinfo("Nothing to Copy", "No password to copy.")
        return

    window.clipboard_clear()
    window.clipboard_append(current_password)
    window.update()
    messagebox.showinfo("Copied", "Password copied to clipboard.")

# ---------------------------
# GUI
# ---------------------------
window = tk.Tk()
window.title("Password Generator")
window.geometry("350x290")
window.resizable(False, False)

tk.Label(window, text="Password Length:").pack(pady=5)

length_entry = tk.Entry(window)
length_entry.pack(pady=5)
length_entry.insert(0, "12")

tk.Button(window, text="Generate", command=generate_password).pack(pady=5)
tk.Button(window, text="Remind", command=remind_password).pack(pady=5)
tk.Button(window, text="Copy", command=copy_password).pack(pady=5)

result_label = tk.Label(window, text="", font=("Arial", 12), wraplength=320)
result_label.pack(pady=10)

# 🔐 Encryption info label
tk.Label(
    window,
    text="All passwords are encrypted.",
    font=("Arial", 9),
    fg="gray"
).pack(pady=(0, 10))

window.mainloop()
