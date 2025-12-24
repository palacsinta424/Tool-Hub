import tkinter as tk
from tkinter import messagebox

def convert():
    try:
        val = float(entry.get())
    except:
        messagebox.showerror("Error", "Enter a valid number")
        return

    unit_from = from_var.get()
    unit_to = to_var.get()

    # Length conversion in meters
    length_units = {"m":1, "cm":0.01, "mm":0.001, "km":1000, "in":0.0254, "ft":0.3048}
    if unit_from in length_units and unit_to in length_units:
        meters = val * length_units[unit_from]
        result = meters / length_units[unit_to]
        result_label.config(text=f"{result:.4f} {unit_to}")
    else:
        messagebox.showerror("Error", "Invalid units")

window = tk.Tk()
window.title("Unit Converter")
window.geometry("300x250")

tk.Label(window, text="Enter value:").pack(pady=5)
entry = tk.Entry(window)
entry.pack(pady=5)

from_var = tk.StringVar(value="m")
to_var = tk.StringVar(value="cm")

tk.Label(window, text="From:").pack()
tk.OptionMenu(window, from_var, "m","cm","mm","km","in","ft").pack()

tk.Label(window, text="To:").pack()
tk.OptionMenu(window, to_var, "m","cm","mm","km","in","ft").pack()

tk.Button(window, text="Convert", command=convert).pack(pady=10)
result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
