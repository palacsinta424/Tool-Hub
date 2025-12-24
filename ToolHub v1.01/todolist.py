import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os

DATA_FILE = "todolist_data.json"

# ---------------------------
# Load tasks
# ---------------------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        tasks = json.load(f)  # List of dicts: {"task":..., "deadline":..., "priority":...}
else:
    tasks = []

def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# ---------------------------
# Task functions
# ---------------------------
def add_task():
    task_name = task_entry.get().strip()
    deadline = deadline_entry.get().strip()
    priority = priority_var.get()

    if not task_name:
        messagebox.showwarning("Warning", "Please enter a task name.")
        return

    task_data = {
        "task": task_name,
        "deadline": deadline,
        "priority": priority
    }
    tasks.append(task_data)
    listbox.insert(tk.END, f"{task_name} | {deadline} | {priority}")
    save_tasks()
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    priority_var.set("Medium")

def remove_task():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a task to remove.")
        return
    for i in selected[::-1]:
        listbox.delete(i)
        del tasks[i]
    save_tasks()

def show_all_tasks():
    summary_window = tk.Toplevel(window)
    summary_window.title("All Tasks")
    summary_window.geometry("400x400")

    scroll_text = scrolledtext.ScrolledText(summary_window, wrap=tk.WORD)
    scroll_text.pack(expand=True, fill="both", padx=10, pady=10)

    if not tasks:
        scroll_text.insert(tk.END, "No tasks added yet.")
    else:
        for i, t in enumerate(tasks, start=1):
            scroll_text.insert(tk.END, f"{i}. {t['task']} | Deadline: {t['deadline']} | Priority: {t['priority']}\n")
    scroll_text.config(state="disabled")

# ---------------------------
# GUI Setup
# ---------------------------
window = tk.Tk()
window.title("To-Do List")
window.geometry("400x500")
window.resizable(False, False)

# Task name
tk.Label(window, text="Task Name:").pack(pady=5)
task_entry = tk.Entry(window, width=35)
task_entry.pack(pady=5)

# Deadline
tk.Label(window, text="Deadline (optional, e.g., 2025-12-31):").pack(pady=5)
deadline_entry = tk.Entry(window, width=35)
deadline_entry.pack(pady=5)

# Priority
tk.Label(window, text="Priority:").pack(pady=5)
priority_var = tk.StringVar(value="Medium")
priority_menu = tk.OptionMenu(window, priority_var, "High", "Medium", "Low")
priority_menu.pack(pady=5)

# Buttons
tk.Button(window, text="Add Task", width=25, command=add_task).pack(pady=5)
tk.Button(window, text="Remove Selected Task", width=25, command=remove_task).pack(pady=5)
tk.Button(window, text="Show All Tasks", width=25, command=show_all_tasks).pack(pady=5)

# Task list
listbox = tk.Listbox(window, width=55, height=15)
listbox.pack(pady=10)

# Load tasks into listbox
for t in tasks:
    listbox.insert(tk.END, f"{t['task']} | {t['deadline']} | {t['priority']}")

window.mainloop()
