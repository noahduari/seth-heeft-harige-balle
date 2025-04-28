import os
import sys
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import Fore, init

init(autoreset=True)

payload_triggered = False

class PayloadListener(BaseHTTPRequestHandler):
    def do_GET(self):
        global payload_triggered
        if self.path == '/payload_ping':
            payload_triggered = True
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')

def run_server():
    server_address = ('', 8080)  # Listen on all IPs, port 8080
    httpd = HTTPServer(server_address, PayloadListener)
    httpd.serve_forever()

def start_listener():
    threading.Thread(target=run_server, daemon=True).start()
    print(Fore.LIGHTGREEN_EX + "[+] Listener started on port 8080...\n")

def listen_payload():
    global payload_triggered
    start_listener()

    print(Fore.YELLOW + "🔴 Waiting for payload to open... (Ctrl+C to stop)\n")
    try:
        while True:
            if payload_triggered:
                sys.stdout.write(Fore.GREEN + "\r🟢 Payload triggered!\n")
                sys.stdout.flush()
                break
            else:
                sys.stdout.write(Fore.RED + "\r🔴 Waiting for payload...   ")
                sys.stdout.flush()
                time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\nListener stopped.")

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.LIGHTGREEN_EX + "\n[Menu]")
        print(Fore.CYAN + "1. Build Payload")
        print(Fore.CYAN + "2. Listen")
        print(Fore.CYAN + "3. Exit")

        choice = input(Fore.YELLOW + "\nSelect an option (1-3): ").strip()

        if choice == "1":
            build_payload()
        elif choice == "2":
            listen_payload()
        elif choice == "3":
            print(Fore.MAGENTA + "\nGoodbye!")
            break
        else:
            print(Fore.RED + "\nInvalid choice.")
            time.sleep(1)

def build_payload():
    payload_code = '''
import requests

try:
    requests.get("http://127.0.0.1:8080/payload_ping")
except:
    pass
'''
    with open("payload.py", "w", encoding="utf-8") as f:
        f.write(payload_code.strip())

    os.system('pyinstaller --onefile payload.py')
    os.remove("payload.py")
    os.remove("payload.spec")
    os.system('rmdir /s /q build')
    os.system('rmdir /s /q dist')

    print(Fore.LIGHTGREEN_EX + "\n✅ Payload built successfully!")

if __name__ == "__main__":
    main_menu()
