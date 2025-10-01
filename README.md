"""
mouse_juggler.py
----------------
A simple "Mouse Juggler + Anti-Sleep" tool using pyautogui, ctypes, threading, and tkinter.

WHAT IT DOES
- Moves the mouse slightly at a regular interval to prevent the system from idling.
- Calls the Windows API SetThreadExecutionState to request the system and display stay awake.
- Provides a small Tkinter GUI with Start and Stop buttons.

IMPORTANT NOTES
- This script uses Windows-only API (ctypes.windll.kernel32.SetThreadExecutionState).
- Intended for legitimate use-cases (kiosk, presentation, testing). Do NOT use to bypass
  workplace/school monitoring policies or to deceive time-tracking systems.
- Requires Python and the `pyautogui` package installed:
    pip install pyautogui
"""

import pyautogui
import time
import threading
import tkinter as tk
import ctypes

# -------------------------
# Windows API flags for SetThreadExecutionState
# -------------------------
ES_CONTINUOUS = 0x80000000       # Informs system the state should remain in effect until cleared
ES_SYSTEM_REQUIRED = 0x00000001 # Prevents system from sleeping
ES_DISPLAY_REQUIRED = 0x00000002# Prevents display from turning off

# Flag to control the background loop
running = False

def start_juggler():
    """
    Start the mouse-juggling loop in a background (daemon) thread.
    Updates the GUI status label to indicate running state.
    """
    global running
    if running:
        return  # already running; ignore duplicate starts
    running = True
    status_label.config(text="🟢 Running")
    # Start the mouse loop on a daemon thread so it won't block the GUI
    threading.Thread(target=mouse_loop, daemon=True).start()

def stop_juggler():
    """
    Stop the mouse-juggling loop and clear the keep-awake request so Windows
    can return to normal power/screen settings.
    """
    global running
    running = False
    status_label.config(text="🔴 Stopped")
    # Clear the keep-awake signal: request continuous state only (clears previous flags)
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

def mouse_loop():
    """
    Main loop that runs while `running` is True.
    - Repeatedly calls SetThreadExecutionState to tell Windows to remain awake.
    - Moves the mouse a little left/right to simulate activity.
    - Sleeps briefly between moves to avoid CPU hogging.
    """
    while running:
        # Request that the system and display remain awake until we clear the request
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
        )

        # Move mouse a tiny bit and back. Using moveRel keeps it relative to current position.
        # duration=0 makes the movement immediate (no visible animation).
        pyautogui.moveRel(10, 0, duration=0)
        pyautogui.moveRel(-10, 0, duration=0)

        # A short sleep prevents this loop from consuming too much CPU.
        # You can increase this to 1.0 (one second) or more depending on how often
        # you want the mouse nudged. Very frequent nudges are unnecessary.
        time.sleep(1.0)

# -------------------------
# GUI setup (Tkinter)
# -------------------------
root = tk.Tk()
root.title("🖱️ Mouse Juggler + Anti-Sleep")
root.geometry("320x160")
root.resizable(False, False)

# Status label shows whether the juggler is running
status_label = tk.Label(root, text="🔴 Stopped", font=("Arial", 14))
status_label.pack(pady=10)

# Start button: green
start_button = tk.Button(
    root, text="Start", command=start_juggler, bg="green", fg="white", width=15
)
start_button.pack(pady=5)

# Stop button: red
stop_button = tk.Button(
    root, text="Stop", command=stop_juggler, bg="red", fg="white", width=15
)
stop_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
