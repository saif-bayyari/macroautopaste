import tkinter as tk
from tkinter import messagebox
import main
import time
import json








window = tk.Tk()

window.geometry("400x300")

window.title("Macro Auto Paste - Saif")

toggle_button = None  






















open_windows = {}

def open_single(name, build_func):
    win = open_windows.get(name)
    if win is not None and win.winfo_exists():
        win.lift()
        win.focus_force()
        return
    win = tk.Toplevel(window)
    open_windows[name] = win
    build_func(win)




#def build_shortcut_window(new_window):
   # new_window.title("Make New Text Shortcut")
    # ... labels, text boxes, submit button ...




#new_button = tk.Button(button_frame, text="Make new text shortcut", width=25,
                      # command=lambda: open_single("shortcut", build_shortcut_window))



#def open_expander_window_v2():

   # pass




def open_expander_window(exwindow):
    global toggle_button
    #exwindow = tk.Toplevel(window)
    exwindow.title("Text Expander")
    exwindow.geometry("300x150")
    exwindow.resizable(False, False)

    status_label = tk.Label(
        exwindow,
        text="",
        font=("Arial", 12)
    )
    status_label.pack(pady=(20, 10))

    def update_status():
        if main.is_running():
            status_label.config(
                text="● Text Expander: ON",
                fg="green"
            )
            toggle_button.config(text="Turn Off")
        else:
            status_label.config(
                text="● Text Expander: OFF",
                fg="red"
            )
            toggle_button.config(text="Turn On")

    def toggle():
        if main.is_running():
            main.stop()
        else:
            main.start()

        update_status()


    if toggle_button is None or not toggle_button.winfo_exists():
        toggle_button = tk.Button(window, width=15, command=toggle)
        toggle_button.pack()
    else:
        toggle_button.config(command=toggle)   # point it at the new window's toggle

    update_status()






label = tk.Label(
    window,
    text="Text Expander is Running! Do CTRL + C within the command window to stop it.",
    font=("Arial", 16),
    fg="red"
)

show_label = False


def check_condition():
    global show_label

    if show_label:
        label.pack(pady=20)
    else:
        label.pack_forget()

    # Check again in 500ms
    window.after(50, check_condition)


def toggle():
    global show_label
    show_label = not show_label
    run()





def make_new_shortcut():


    def submit_shortcut():
        comName = text_box1.get("1.0", "end-1c")
        ts = text_box2.get("1.0", "end-1c")

        comName = ("/" + comName) if not comName.startswith("/") else comName[1:]

        existing = load_snippets(path)
        collisions = [
            trig for trig in existing
            if trig == comName or trig.startswith(comName) or comName.startswith(trig)
        ]

        if not comName or comName == "/":
            messagebox.showerror("Missing Command", "Enter a command name.")
            return
        if not ts.strip():
            messagebox.showerror("Missing Template", "Enter the text to paste.")
            return

        if collisions:
            conflict_list = ", ".join(collisions)
            messagebox.showerror(
                "Command Conflict",
                f"Can't use \"{comName}\" — it conflicts with the existing command(s): {conflict_list}\n\n"
                f"Try a different starting sequence that doesn't overlap with these."
            )
            return  # block save

        save_snippets(path, {**existing, comName: ts})

    # Create a new window
    new_window = tk.Toplevel(window)
    new_window.title("Make New Text Shortcut")
    new_window.geometry("400x600")
    new_window.resizable(False, False)  
    label1 = tk.Label(new_window, text="Command Name (it has to start with '/'):")
    label1.pack(side="top", padx=5)

    FORBIDDEN = set(' \t\n"\\')   # characters you don't want

    def allow_input(new_text):
        return not any(ch in FORBIDDEN for ch in new_text)

    vcmd = (new_window.register(allow_input), "%P")

 


    text_box1 = tk.Entry(new_window, width=50,
                        validate="key", validatecommand=vcmd)
    text_box1.pack(padx=10, pady=10)

    label2 = tk.Label(new_window, text="Text Shortcut/Template:")
    label2.pack(side="top", padx=5)

    text_box2 = tk.Text(new_window, width=50, height=1)
    text_box2.pack(side="top",padx=10,pady=10)





  













    submitBtn = tk.Button(
    new_window,
    text="submit",
    command=submit_shortcut  
)
    submitBtn.pack(padx=10, pady=10)

    def auto_resize(event=None):
        lines = int(text_box2.index("end-1c").split(".")[0])
        text_box2.config(height=max(1,lines))


    text_box2.bind("<KeyRelease>", auto_resize)




button_frame = tk.Frame(window)
button_frame.pack(pady=40)


new_button = tk.Button(button_frame, text="Make new text shortcut", width = 25, command=make_new_shortcut)
new_button.pack(pady=(0,20))

new_button2 = tk.Button(button_frame, text="Run Text Expander", width = 25, command=lambda:open_single("expander", open_expander_window))
new_button2.pack(pady=(0,20))



#check_condition()

































window.mainloop()