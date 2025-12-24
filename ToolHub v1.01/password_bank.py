import tkinter as tk
from tkinter import messagebox
import json
import os
import pyperclip

DATA_FILE = "password_bank.json"
XOR_KEY = "storingpassword"

# ---------------------------
# XOR Encryption / Decryption
# ---------------------------
def xor_crypt(text):
    key = XOR_KEY
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

# ---------------------------
# Load passwords
# ---------------------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        raw_data = json.load(f)
        passwords = []
        for entry in raw_data:
            passwords.append({
                "name": entry["name"],
                "password": xor_crypt(entry["password"])
            })
else:
    passwords = []

def save_passwords():
    enc_data = [{"name": p["name"], "password": xor_crypt(p["password"])} for p in passwords]
    with open(DATA_FILE, "w") as f:
        json.dump(enc_data, f, indent=4)

# ---------------------------
# Task functions
# ---------------------------
def add_password():
    name = name_entry.get().strip()
    pwd = pwd_entry.get().strip()
    if not name or not pwd:
        messagebox.showwarning("Warning", "Please enter both name and password.")
        return
    passwords.append({"name": name, "password": pwd})
    listbox.insert(tk.END, name)
    save_passwords()
    name_entry.delete(0, tk.END)
    pwd_entry.delete(0, tk.END)

def remove_password():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a password to remove.")
        return
    for i in selected[::-1]:
        pwd_name = listbox.get(i)
        for p in passwords:
            if p["name"] == pwd_name:
                passwords.remove(p)
        listbox.delete(i)
    save_passwords()

def reveal_password():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a password to reveal.")
        return
    i = selected[0]
    pwd_name = listbox.get(i)
    for p in passwords:
        if p["name"] == pwd_name:
            messagebox.showinfo(f"Password for {pwd_name}", p["password"])
            pyperclip.copy(p["password"])
            return

# ---------------------------
# GUI
# ---------------------------
window = tk.Tk()
window.title("Password Bank")
window.geometry("350x480")

# Description
desc_label = tk.Label(window, text="Passwords are stored locally on only YOUR computer.", 
                      font=("Arial", 9, "italic"), fg="gray", wraplength=300, justify="center")
desc_label.pack(pady=(10,5))

tk.Label(window, text="Name / Account:").pack(pady=5)
name_entry = tk.Entry(window, width=30)
name_entry.pack(pady=5)

tk.Label(window, text="Password:").pack(pady=5)
pwd_entry = tk.Entry(window, width=30, show="*")
pwd_entry.pack(pady=5)

tk.Button(window, text="Add Password", width=25, command=add_password).pack(pady=5)
tk.Button(window, text="Remove Selected", width=25, command=remove_password).pack(pady=5)
tk.Button(window, text="Reveal Password", width=25, command=reveal_password).pack(pady=5)

listbox = tk.Listbox(window, width=40, height=15)
listbox.pack(pady=10)

# Load saved passwords into listbox
for p in passwords:
    listbox.insert(tk.END, p["name"])

window.mainloop()
