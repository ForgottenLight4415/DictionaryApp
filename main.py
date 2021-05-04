import tkinter as tk
from tkinter import ttk
import json
import requests
import re


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def build_defs(data, wrapper_frame):
    main_frame = tk.LabelFrame(wrapper_frame)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill="both", expand="yes")

    yscrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    yscrollbar.pack(side=tk.RIGHT, fill='y')
    canvas.configure(yscrollcommand=yscrollbar.set)

    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    main_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    word_definitions = data['definitions']
    word_label = tk.Label(frame, text="Word: " + data['word'], font=('Arial', 10))
    word_label.pack()
    if data['pronunciation'] is not None:
        pronunciation_label = tk.Label(frame, text="Pronunciation: " + data['pronunciation'], font=('Arial', 10))
        pronunciation_label.pack(padx=10, pady=(0, 20))

    for d in word_definitions:
        type_label = tk.Label(frame, text=data['word'] + f" ({d['type']})", font=('Arial', 10))
        type_label.pack(anchor="w")
        definition_label = tk.Message(frame, text="Definition: " + d['definition'], font=('Arial', 10), justify=tk.LEFT,
                                      width=430)
        definition_label.pack(padx=10, pady=(0, 20), anchor="w")
        if d['example'] is not None:
            example_label = tk.Message(frame, text="Example: " + cleanhtml(d['example']), font=('Arial', 10),
                                       justify=tk.LEFT,
                                       width=300)
            example_label.pack(padx=10, pady=(0, 20), anchor="w")


def search_button_action(wrapper_frame):
    word_input = word.get()
    url = f"https://owlbot.info/api/v4/dictionary/{word_input}"
    token = "96c6c3419f7095c7d638dcbb09d15a9f306d7426"
    auth_header = {'Authorization': "Token " + token}
    try:
        response = requests.get(url, headers=auth_header)
        data = json.loads(response.content)
        clear_frame(wrapper_frame)
        try:
            build_defs(data, wrapper_frame)
        except TypeError:
            clear_frame(wrapper_frame)
            error_label = tk.Label(wrapper_frame, text="Word not found", font=('Arial', 15), fg="#FF3333")
            error_label.pack(anchor='n')
    except requests.exceptions.ConnectionError:
        clear_frame(wrapper_frame)
        error_label = tk.Label(wrapper_frame, text="Connection timed out", font=('Arial', 15), fg="#FF3333")
        error_label.pack(anchor='n')
    except json.decoder.JSONDecodeError:
        clear_frame(wrapper_frame)
        error_label = tk.Label(wrapper_frame, text="Not a valid word", font=('Arial', 15), fg="#FF3333")
        error_label.pack(anchor='n')
    wrapper_frame.pack(fill="both", expand="yes")


def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


home = tk.Tk()
home.geometry("500x500")
home.resizable(False, False)
home.title("Clicktionary - Type a word to search")

top_frame = tk.Frame(home)
word = tk.Entry(top_frame, width=50, font=('Arial', 10))
search_button = tk.Button(top_frame, text="Search", command=lambda: search_button_action(wrapper))

top_frame.pack(side=tk.TOP)
word.grid(padx=10, pady=10, row=0, column=0)
search_button.grid(padx=10, pady=10, row=0, column=1)

wrapper = tk.Frame()

home.mainloop()
