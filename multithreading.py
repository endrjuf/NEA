import os
import time
from datetime import datetime
import shutil
import threading
from tkinter import *
try: import tkinter
except ImportError:
    import Tkinter as tkinter
    import ttk
else: from tkinter import ttk

def submit():
    for i in range(0,100000000):
        print(i)


def start_submit_thread(event):
    global submit_thread
    submit_thread = threading.Thread(target=submit)
    submit_thread.daemon = True
    progressbar.start()
    submit_thread.start()
    root.after(20, check_submit_thread)

def check_submit_thread():
    if submit_thread.is_alive():
        root.after(20, check_submit_thread)
    else:
        progressbar.stop()

root = Tk()
frame = ttk.Frame(root)
frame.pack()
progressbar = ttk.Progressbar(frame, mode='indeterminate')
progressbar.grid(column=1, row=0, sticky=W)

ttk.Button(frame, text="Check",
       command=lambda:start_submit_thread(None)).grid(column=0,    row=1,sticky=E)
root.mainloop()