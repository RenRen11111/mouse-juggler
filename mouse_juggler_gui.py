import pyautogui
import time
import threading
import tkinter as tk
import ctypes

running = False

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def start_juggler():
    global running
    running = True
    status_label.config(text="🟢 Running")
    threading.Thread(target=mouse_loop, daemon=True).start()

def stop_juggler():
    global running
    running = False
    status_label.config(text="🔴 Stopped")
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

def mouse_loop():
    while running:
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
        )

        pyautogui.moveRel(10, 0, duration=0)
        pyautogui.moveRel(-10, 0, duration=0)
        time.sleep(0)  

root = tk.Tk()
root.title("🖱️ Mouse Juggler + Anti-Sleep")
root.geometry("300x150")
root.resizable(False, False)

status_label = tk.Label(root, text="🔴 Stopped", font=("Arial", 14))
status_label.pack(pady=10)

start_button = tk.Button(root, text="Start", command=start_juggler, bg="green", fg="white", width=15)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=stop_juggler, bg="red", fg="white", width=15)
stop_button.pack(pady=5)


root.mainloop()
