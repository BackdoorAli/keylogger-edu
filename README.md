# 🔐 Educational Python Keylogger

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Repo size](https://img.shields.io/github/repo-size/Mira2720/keylogger-edu)

**Created by Mira2720 (GitHub: https://github.com/Mira2720)**  
⚠️ **For educational purposes only. Unauthorized use is strictly prohibited.**

This is a cross-platform Python keylogger built to demonstrate red team tactics and teach ethical cybersecurity awareness.

## 🚀 Features

- ✅ Cross-platform: Windows, macOS, Linux
- 📋 Clipboard monitoring
- 📩 Auto email logs every X minutes
- 🖥️ Logs active window titles
- 🧠 Dumps system info on start
- 🫥 Stealth mode (Windows + silent Linux/macOS)

## 🛠️ Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/Mira2720/keylogger-edu.git
   cd keylogger-edu
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. (Linux only) Install `xdotool`:
   ```bash
   sudo apt install xdotool
   ```

4. Edit your email/password in `keylogger.py` before running.

5. Run the script:
   ```bash
   python keylogger.py
   ```

## 🔒 Ethical Use

This project is intended to help defenders understand attacker tactics. Use it only in controlled lab environments.

📘 See the [CASE_STUDY.md](./CASE_STUDY.md) for a practical walkthrough.
