import tkinter as tk
from tkinter import ttk, messagebox
import serial
import openpyxl
from datetime import datetime
import threading
import time


arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

file = "attendance.xlsx"
wb = openpyxl.load_workbook(file)
ws = wb.active

names = {
    "d1a6b37b": "Murtaza",
    "c33f3afe": "Suleman",
    "63730427": "Ahmad"
}

root = tk.Tk()
root.title("Attendance System")
root.geometry("1020x720")

title_label = tk.Label(root, text="Attendance System", font=("Arial", 16))
title_label.pack(pady=10)

columns = ("Name", "UID", "Date", "Time")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(pady=10, fill='both', expand=True)


def close_app():
    try:
        arduino.close()
    except:
        pass
    root.destroy()

exit_button = tk.Button(root, text="Exit", command=close_app, width=20, height=2)
exit_button.pack(pady=10)


def read_attendance():
    while True:
        try:
            data = arduino.readline().decode().strip()
            if data == "" or data.lower() == "ready":
                continue

            uid = data.lower()
            name = names.get(uid, "Unknown")

            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%I:%M:%S %p")

    
            ws.append([name, uid, date, time_str])
            wb.save(file)

            
            tree.insert('', 'end', values=(name, uid, date, time_str))
            print(f"✔ Attendance Marked: {name} at {time_str}")
            time.sleep(0.5)
        except Exception as e:
            print("Error:", e)
            time.sleep(1)

thread = threading.Thread(target=read_attendance, daemon=True)
thread.start()

root.mainloop()
