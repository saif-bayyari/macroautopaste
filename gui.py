import tkinter as tk
from main import load_guitext_in_csv

window = tk.Tk()

window.geometry("400x300")

window.title("Macro Auto Paste - Saif")


def make_new_shortcut():


    def submit_shortcut():
        command_name = text_box1.get("1.0", "end-1c")
        text_shortcut = text_box2.get("1.0", "end-1c")
        print(f"Command Name: {command_name}")
        print(f"Text Shortcut: {text_shortcut}")
        load_guitext_in_csv(command_name, text_shortcut)

    # Create a new window
    new_window = tk.Toplevel(window)
    new_window.title("Make New Text Shortcut")
    new_window.geometry("400x250")
    label1 = tk.Label(new_window, text="Command Name (it has to start with '/'):")
    label1.pack(side="left", padx=5)

    text_box1 = tk.Text(new_window, width=50, height =1)
    text_box1.pack(side="left",padx=10,pady=10)

    label2 = tk.Label(new_window, text="Text Shortcut/Template:")
    label2.pack(side="left", padx=5)

    text_box2 = tk.Text(new_window, width=50, height=1)
    text_box2.pack(side="left",padx=10,pady=10)

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

window.mainloop()