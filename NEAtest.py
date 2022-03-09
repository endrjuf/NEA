import tkinter as tk
from tkinter import filedialog
import webbrowser
import os
from pytube import YouTube
import re
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr

r = sr.Recognizer()

HEIGHT = 900
WIDTH = 1200

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame1 = tk.Frame(root, bg="#AD8B84")
frame2 = tk.Frame(root, bg="blue")
frame3 = tk.Frame(root, bg="yellow")
frame4 = tk.Frame(root, bg="green")
frame5 = tk.Frame(frame2)

def assignfolder():
    open_folder = filedialog.askdirectory(initialdir="/", title="Select file")

def assignfile():
    open_file = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=[("txt files", "*.txt")])


def show_frame(frame):
    frame.tkraise()

def clear_text():
   linkinput.delete(0, tk.END)

def browseFiles():
    mp3audio = tk.filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=[("Mp3 Files", "*.mp3")])
    # webbrowser.open(mp3audio)

def update(data):
    audiolistbox.delete(0, tk.END)

    for item in data:
        audiolistbox.insert(tk.END, item)

def fillout(e):
    searchentry.delete(0, tk.END)

    searchentry.insert(0, audiolistbox.get(tk.ANCHOR))

def check(e):
    typed = searchentry.get()
    if typed == "":
        data = os.listdir("D:/mp3audio")
    else:
        data = []
        for item in os.listdir("D:/mp3audio"):
            if typed.lower() in item.lower():
                data.append(item)
    update(data)


def textfile():
    # start editable vars #
    outputfile = "D:/mp3list.txt"  # file to save the results to
    folder = "D:/mp3audio"  # the folder to inventory
    exclude = ['Thumbs.db', '.tmp']  # exclude files containing these strings
    pathsep = "/"  # path seperator ('/' for linux, '\' for Windows)
    # end editable vars #

    with open(outputfile, "w") as txtfile:
        for path, dirs, files in os.walk(folder):
            sep = path.split(pathsep)[len(path.split(pathsep)) - 1]
            for fn in sorted(files):
                if not any(x in fn for x in exclude):
                    filename = os.path.splitext(fn)[0]
                    txtfile.write("%s\n" % filename)
    txtfile.close()

def getittle():
    try:
        yt = YouTube(inputvalue)
        title = yt.title
        x = re.sub("['/|<\>:*?]", '', title)
        x = re.sub('[",.]', '', title)
        existancecheck(x)
    except:
        print("\nNot a youtube link")

def existancecheck(x):
    with open("D:/mp3list.txt", "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            if stripped_line == x:
                print("\nFile already downloaded")
                break
        else:
            ytDownload()

def ytDownload():
    yt = YouTube(inputvalue)
    video = yt.streams.filter(only_audio=True).first()
    desntination = "D:/mp3audio"
    out_file = video.download(desntination)
    base, ext = os.path.splitext(out_file)
    # print(base)
    # print(ext)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    completed = tk.Label(frame2, text="Successfully downloaded", bg="blue")
    completed.place(relx=0.3, rely=0.35, relwidth=0.2, relheight=0.1)
    completed.after(3000, lambda: completed.destroy())
    textfile()

def retrieve_input():
    global inputvalue
    inputvalue = linkinput.get()
    getittle()

def showSelected():
    text=audiolistbox.get(tk.ANCHOR)
    if text == "":
        print("\nNothing Selected!")
    else:
        print("\n" + text)
    path = ("D:/mp3audio/"+text)
    print(path)







for frame in (frame1, frame2, frame3, frame4):
    frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

############################################################## Frame 1 CODE
startkey = tk.PhotoImage(file="E:/NEA/Start.png")
startsummarybutton = tk.Button(frame1, image=startkey, bd=0, bg="#AD8B84", activebackground="#AD8B84", command=lambda: (show_frame(frame2)))
startsummarybutton.place(relx=0.3, rely=0.3, width=147, height=65)

titlelable = tk.Label(frame1, text="SUMMARISATION APP", bg="#AD8B84", font=("Arial", 20))
titlelable.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.15)

settingsbutton = tk.Button(frame1, text="Settings", command=lambda: show_frame(frame4))
settingsbutton.place(relx=0, rely=0, relwidth=0.1, relheight=0.1)

managekey = tk.PhotoImage(file="E:/NEA/Manage.png")
managesummariesbutton = tk.Button(frame1, image=managekey, bd=0, bg="#AD8B84", activebackground="#AD8B84", command=lambda: show_frame(frame3))
managesummariesbutton.place(relx=0.5, rely=0.29, width=147, height=65)

############################################################## Frame 2 CODE
titlelable = tk.Label(frame2, text="New Summary", bg="#AD8B84", font=("Arial", 20), bd=0)
titlelable.place(relx=0.3, rely=0., relwidth=0.4, relheight=0.15)

backbutton = tk.Button(frame2, text="Back", width=100, height=100,
                       command=lambda:(show_frame(frame1), clear_text(),searchentry.delete(0, tk.END), update(os.listdir("D:/mp3audio"))))
backbutton.place(relx=0, rely=0.9, relwidth=0.1, relheight=0.1)

linkinput = tk.Entry(frame2)
linkinput.place(relx=0.2, rely=0.3, relwidth=0.3, relheight=0.05)

refreshlistbox =  tk.Button(frame2, text="Refresh", command=lambda: (searchentry.delete(0, tk.END), update(os.listdir("D:/mp3audio"))))
refreshlistbox.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.05)

submitbutton = tk.Button(frame2, text="submit", command=lambda: (retrieve_input(), clear_text(),))
submitbutton.place(relx=0.53, rely=0.3, relwidth=0.1, relheight=0.05)
root.bind('<Return>', lambda event:clear_text())

buttonexplore = tk.Button(frame2, text="Browse Files", command=browseFiles)
buttonexplore.place(relx=0.8, rely=0.3, relwidth=0.1, relheigh=0.1)

frame5.place(relx=0.15, rely=0.65)

audiolistbox = tk.Listbox(frame5, fg="black", height=10, width=95)
audiolistbox.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(frame5, orient=tk.VERTICAL, command=audiolistbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

audiolistbox.config(yscrollcommand=scrollbar.set)

searchentry = tk.Entry(frame2)
searchentry.place(relx=0.15, rely=0.58, relwidth=0.6, relheight=0.05)

selectbutton = tk.Button(frame2, text="Proceed with selected", command=lambda:showSelected())
selectbutton.place(relx=0.78, rely=0.58, relheight=0.05, relwidth=0.15)


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

choosefolder = tk.Button(frame4, text="Choose audio folder", command=lambda:assignfolder())
choosefolder.place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.1)

choosetextfile = tk.Button(frame4, text="Choose textfile", command=lambda:assignfile())
choosetextfile.place(relx=0.5, rely=0.4, relwidth=0.2, relheight=0.1)






searchentry.bind("<KeyRelease>", check)

audiolistbox.bind("<<ListboxSelect>>", fillout)

update(os.listdir("D:/mp3audio"))

show_frame(frame1)

root.mainloop()