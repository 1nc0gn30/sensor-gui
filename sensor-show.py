import tkinter as tk
import subprocess
import re

UPDATE_INTERVAL = 3000  # in milliseconds (3 seconds)

def get_sensor_output():
    result = subprocess.run(["sensors"], stdout=subprocess.PIPE)
    return result.stdout.decode()

def parse_sensors(output):
    lines = output.split("\n")
    temps = []
    fans = []
    for line in lines:
        line = line.strip()
        if re.search(r'Core \d+|Package id', line):
            temps.append(line)
        elif re.search(r'fan\d+:\s+\d+\s+RPM', line, re.IGNORECASE):
            fans.append(line)
    return temps, fans

def update_display():
    output = get_sensor_output()
    temps, fans = parse_sensors(output)

    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, "🔥 CPU Temps\n", "header")
    for t in temps:
        text_widget.insert(tk.END, f"{t}\n", "temp")

    text_widget.insert(tk.END, "\n🌀 Fan Speeds\n", "header")
    for f in fans:
        text_widget.insert(tk.END, f"{f}\n", "fan")

    root.after(UPDATE_INTERVAL, update_display)

# GUI Setup
root = tk.Tk()
root.title("HeatCheck - CPU Temp Monitor")
root.geometry("420x300")
root.configure(bg="#111")

text_widget = tk.Text(root, bg="#111", fg="#eee", font=("Courier", 12), bd=0)
text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Styling tags
text_widget.tag_config("header", foreground="#00ffd5", font=("Courier", 12, "bold"))
text_widget.tag_config("temp", foreground="#ff5555")
text_widget.tag_config("fan", foreground="#ffaa00")

update_display()
root.mainloop()

