
import os
import threading
import time
import json
import pyperclip
from pynput import keyboard as kb
from pynput.keyboard import Controller, Key


path = 'snippets.json'
def load_snippets(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def save_snippets(path, snippets):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)

#load_snippets(path)
RELOAD_INTERVAL = 5


stop_event = threading.Event()


snippets = {}
snippets_lock = threading.Lock()


buffer = []
MAX_BUFFER = 30
controller = Controller()




def delete_command(command: str):
    for _ in command:
        controller.tap(Key.backspace)
    time.sleep(0.05)


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




# Global state
listener = None
reloader = None
running = False
stop_event = threading.Event()


def reload_loop():
    last_mtime = None

    while not stop_event.is_set():
        try:
            mtime = os.path.getmtime(path)

            if mtime != last_mtime:
                loaded = load_snippets(path)
                last_mtime = mtime

                print(
                    f"  [↻] Snippets reloaded — "
                    f"{len(loaded)} command(s) active."
                )

        except FileNotFoundError:
            pass

        # Wait without blocking the Tkinter thread.
        # stop_event.set() will wake this immediately.
        stop_event.wait(RELOAD_INTERVAL)



def start():
    global listener, reloader, running

    # Don't start multiple copies
    if running:
        print("Text expander is already running.")
        return

    print("Starting text expander...")

    # Load snippets immediately
    load_snippets(path)

    # Reset the stop signal
    stop_event.clear()

    running = True

    # Start the snippet reloader in the background
    reloader = threading.Thread(
        target=reload_loop,
        daemon=True
    )
    reloader.start()

    # Start keyboard listener in the background
    listener = kb.Listener(
        on_press=on_press
    )
    listener.start()

    with snippets_lock:
        cmds = list(snippets.keys())

   


def stop():
    global listener, reloader, running

    if not running:
        print("Text expander is already stopped.")
        return

    print("Stopping text expander...")

    # Tell reload_loop() to exit
    stop_event.set()

    # Stop keyboard listener
    if listener is not None:
        listener.stop()
        listener = None

    # The threads are daemon threads, so we don't need
    # to block the Tkinter GUI waiting for them.
    reloader = None

    running = False

    print("✗ Text expander stopped.")


def is_running():
    return running

