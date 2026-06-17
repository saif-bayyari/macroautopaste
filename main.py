import csv
import os
import threading
import time

import pyperclip
from pynput import keyboard as kb
from pynput.keyboard import Controller, Key

SNIPPETS_FILE = "snippets.csv"
RELOAD_INTERVAL = 5  # seconds between CSV checks


snippets = {}
snippets_lock = threading.Lock()


# SNIPPETS = {
#    "/greeting": "Hi there,\n\nThank you for reaching out.\n\nBest regards,\nSaif",
# "/closing": "Please let me know if you have any questions. Happy to help!\n\n— Saif",
# "/sig": "Saif | L1 Engineer @ Resolve Tech Solutions\nsaif@example.com",
#   "/tix": "Ticket acknowledged. I'm looking into this now and will update you within 1 business hour.",
#   "/tyvm": "Thank you very much — really appreciate it!",
# }
#
#

buffer = []
MAX_BUFFER = 30
controller = Controller()


def create_default_csv():
    with open(SNIPPETS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["command", "expansion"])
        writer.writerows(DEFAULT_SNIPPETS)
    print(f"  Created '{SNIPPETS_FILE}' with default snippets.")


def load_snippets():
    global snippets
    if not os.path.exists(SNIPPETS_FILE):
        create_default_csv()
    try:
        new_snippets = {}
        with open(SNIPPETS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                command = row["command"].strip()
                expansion = row["expansion"].strip().replace("\\n", "\n")
                if command:
                    new_snippets[command] = expansion
        with snippets_lock:
            snippets = new_snippets
        return new_snippets
    except Exception as e:
        print(f"  [!] Error reading CSV: {e}")
        return {}


def reload_loop():
    last_mtime = None
    while True:
        try:
            mtime = os.path.getmtime(SNIPPETS_FILE)
            if mtime != last_mtime:
                loaded = load_snippets()
                last_mtime = mtime
                print(f"  [↻] Snippets reloaded — {len(loaded)} command(s) active.")
        except FileNotFoundError:
            pass
        time.sleep(RELOAD_INTERVAL)


def delete_command(command: str):
    for _ in command:
        controller.tap(Key.backspace)
    time.sleep(0.05)


###from claude
def type_expansion(text: str):
    previous = pyperclip.paste()
    pyperclip.copy(text)
    time.sleep(0.05)
    with controller.pressed(Key.ctrl):
        controller.tap("v")
    time.sleep(0.1)
    pyperclip.copy(previous)


def on_press(key):
    global buffer

    if key in (Key.space, Key.enter, Key.esc, Key.tab):
        buffer = []
        return

    if key == Key.backspace:
        if buffer:
            buffer.pop()
        return

    try:
        char = key.char
        if char:
            buffer.append(char)
    except AttributeError:
        buffer = []
        return

    if len(buffer) > MAX_BUFFER:
        buffer = buffer[-MAX_BUFFER:]

    current = "".join(buffer)
    with snippets_lock:
        local_snippets = dict(snippets)

    for command, template in local_snippets.items():
        if current.endswith(command):
            time.sleep(0.05)
            delete_command(command)
            type_expansion(template)
            buffer = []
            return


def run():
    load_snippets()

    reloader = threading.Thread(target=reload_loop, daemon=True)
    reloader.start()

    with snippets_lock:
        cmds = list(snippets.keys())
    print("✓ Text expander running.")
    print(f"  Commands: {', '.join(cmds)}")
    print(f"  Edit '{SNIPPETS_FILE}' anytime — reloads within {RELOAD_INTERVAL}s.")
    print("  Press Ctrl+C to stop.\n")

    listener = kb.Listener(on_press=on_press)
    listener.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        listener.stop()
        print("\n✗ Text expander stopped.")


run()
