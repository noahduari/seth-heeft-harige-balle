import pyfiglet
import sys
import time
import random
import os
import threading
import requests
from colorama import Fore, Style, init
from tkinter import Tk, filedialog
import subprocess

# Initialize colorama
init(autoreset=True)

def print_big_title():
    ascii_banner = pyfiglet.figlet_format("MATRIX", font="slant")
    print(Fore.GREEN + ascii_banner)

def glitch_text(text, color=Fore.LIGHTGREEN_EX, glitches=5):
    for _ in range(glitches):
        glitched = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') if random.random() < 0.3 else c for c in text)
        sys.stdout.write("\r" + color + glitched)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + color + text + "\n")

def type_effect(text, color=Fore.GREEN, delay=0.02):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_bar(text="Booting up Matrix Interface", length=30):
    sys.stdout.write(Fore.LIGHTGREEN_EX + text + " [")
    sys.stdout.flush()
    for _ in range(length):
        sys.stdout.write(Fore.GREEN + "█")
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write(Fore.LIGHTGREEN_EX + "]\n\n")
    sys.stdout.flush()

def matrix_rain(lines=10):
    for _ in range(lines):
        line = ''.join(random.choice("01") for _ in range(60))
        print(Fore.GREEN + line)
        time.sleep(0.05)

def flash_screen(duration=2):
    end_time = time.time() + duration
    colors = [Fore.RED, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.BLUE, Fore.WHITE]
    
    while time.time() < end_time:
        color = random.choice(colors)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(color + pyfiglet.figlet_format("MATRIX", font="slant"))
        time.sleep(0.1)

def send_test_message(webhook):
    try:
        response = requests.post(webhook, json={"content": "Test message from Matrix system!"})
        if response.status_code == 204:
            print(Fore.GREEN + "Test message sent successfully!")
            return True
        else:
            print(Fore.RED + "Failed to send test message. Check your webhook URL.")
            return False
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error: {e}")
        return False

def make_payload(webhook_url, filename="payload.py"):
    payload_code = f'''
import requests

webhook_url = "{webhook_url}"

data = {{
    "content": "✅ Payload is online!"
}}

try:
    requests.post(webhook_url, json=data)
except Exception:
    pass
'''
    with open(filename, "w", encoding="utf-8") as f:
        f.write(payload_code.strip())

def make_executable_animation():
    glitch_text("Building Binary...", Fore.LIGHTCYAN_EX)
    for _ in range(3):
        sys.stdout.write(Fore.LIGHTMAGENTA_EX + "⏳ Building")
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(".\r")
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write("              \r")
    
    matrix_rain(15)
    loading_bar("Compiling Executable", 40)
    flash_screen(duration=2)
    glitch_text("Executable Created Successfully! 💥", Fore.LIGHTGREEN_EX)

def select_file(title="Select a file"):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title)
    return file_path

def convert_to_exe(py_file, icon_path=None):
    print(Fore.CYAN + "Packaging Python file into .exe...")
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
    ]
    if icon_path:
        cmd += ["--icon", icon_path]
    cmd.append(py_file)
    subprocess.run(cmd, shell=True)

    dist_path = os.path.join("dist", os.path.splitext(os.path.basename(py_file))[0] + ".exe")
    if os.path.exists(dist_path):
        print(Fore.GREEN + f"\nExecutable created: {dist_path}")
    else:
        print(Fore.RED + "\nSomething went wrong during .exe build.")

def start_menu():
    print_big_title()
    glitch_text("WELCOME TO THE MATRIX")
    loading_bar()
    type_effect("System Ready. Press ENTER to Start.\n", Fore.LIGHTGREEN_EX)
    input(Fore.YELLOW + "> Press ENTER to start...")

    start_build_process()

def start_build_process():
    type_effect("Starting Build Process...\n", Fore.LIGHTCYAN_EX)

    while True:
        webhook = input(Fore.YELLOW + "Enter your Discord Webhook URL: ")
        print(Fore.LIGHTGREEN_EX + "Checking if webhook is valid...")
        if send_test_message(webhook):
            break
        else:
            print(Fore.YELLOW + "Invalid webhook. Please enter a valid webhook URL.")

    custom_name = input(Fore.YELLOW + "Do you want a custom executable name? (Y/N): ").strip().upper()
    exe_name = "matrix_payload"
    if custom_name == 'Y':
        exe_name = input(Fore.YELLOW + "Enter custom name (no extension): ").strip()

    custom_icon = input(Fore.YELLOW + "Use custom icon? (Y/N): ").strip().upper()
    icon_path = None
    if custom_icon == 'Y':
        print(Fore.YELLOW + "Select your .ico image...")
        icon_path = select_file("Select Icon")

    payload_file = f"{exe_name}.py"
    make_payload(webhook, filename=payload_file)

    make_executable_animation()

    convert_to_exe(payload_file, icon_path=icon_path)

    print(Fore.LIGHTGREEN_EX + f"\nDone! Your file is in the 'dist' folder as {exe_name}.exe")

if __name__ == "__main__":
    start_menu()
