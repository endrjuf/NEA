import tkinter as tk
from tkinter import filedialog
import webbrowser

HEIGHT = 700
WIDTH = 1000

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

def show_frame(frame):
    frame.tkraise()

def clear_text():
   linkinput.delete(0, tk.END)

def browseFiles():
    ytvideo = tk.filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=[("Mp3 Files", "*.mp3")])
    #webbrowser.open(ytvideo)

frame1 = tk.Frame(root, bg="#AD8B84")
frame2 = tk.Frame(root, bg="blue")
frame3 = tk.Frame(root, bg="yellow")
frame4 = tk.Frame(root, bg="green")

for frame in (frame1, frame2, frame3, frame4):
    frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

############################################################## Frame 1 CODE
startkey = tk.PhotoImage(file="Start.png")
startsummarybutton = tk.Button(frame1, image=startkey, bd=0, bg="#AD8B84", activebackground="#AD8B84", command=lambda: show_frame(frame2))
startsummarybutton.place(relx=0.3, rely=0.3, width=147, height=65)

titlelable = tk.Label(frame1, text="SUMMARISATION APP", bg="#AD8B84", font=("Arial", 20))
titlelable.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.15)

settingsbutton = tk.Button(frame1, text="Settings", command=lambda: show_frame(frame4))
settingsbutton.place(relx=0, rely=0, relwidth=0.1, relheight=0.1)

managekey = tk.PhotoImage(file="Manage.png")
managesummariesbutton = tk.Button(frame1, image=managekey, bd=0, bg="#AD8B84", activebackground="#AD8B84", command=lambda: show_frame(frame3))
managesummariesbutton.place(relx=0.5, rely=0.29, width=147, height=65)

############################################################## Frame 2 CODE
titlelable = tk.Label(frame2, text="New Summary", bg="#AD8B84", font=("Arial", 20), bd=0)
titlelable.place(relx=0.3, rely=0., relwidth=0.4, relheight=0.15)

backbutton = tk.Button(frame2, text="Back", width=100, height=100, command=lambda:(show_frame(frame1), clear_text()))
backbutton.place(relx=0, rely=0.9, relwidth=0.1, relheight=0.1)

linkinput = tk.Entry(frame2)
linkinput.place(relx=0.2, rely=0.3, relwidth=0.3, relheight=0.05)

submitbutton = tk.Button(frame2, text="submit", command=lambda:(clear_text()))
submitbutton.place(relx=0.53, rely=0.3, relwidth=0.1, relheight=0.05)
root.bind('<Return>', lambda event:clear_text())

buttonexplore = tk.Button(frame2,text="Browse Files", command=browseFiles)
buttonexplore.place(relx=0.8, rely=0.3, relwidth=0.1, relheigh=0.1)

############################################################## Frame 3 CODE
titlelable = tk.Label(frame3, text="Manage Summary", bg="#AD8B84", font=("Arial", 20))
titlelable.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.15)

backbutton1 = tk.Button(frame3, text="Back", width=100, height=100, command=lambda:show_frame(frame1))
backbutton1.place(relx=0, rely=0.9, relwidth=0.1, relheight=0.1)



############################################################## Frame 4 CODE
titlelable = tk.Label(frame4, text="Settings", bg="#AD8B84", font=("Arial", 20))
titlelable.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.15)

backbutton2 = tk.Button(frame4, text="Back", width=100, height=100, command=lambda:show_frame(frame1))
backbutton2.place(relx=0, rely=0.9, relwidth=0.1, relheight=0.1)









show_frame(frame1)



root.mainloop() 