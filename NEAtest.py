import tkinter as tk
from tkinter import filedialog
import webbrowser
import os
from pytube import YouTube
import re
import textwrap
from transformers import pipeline
import requests
import time
import shutil
from pathlib import Path
from progress.bar import Bar
from threading import Thread




print("Working dir:", os.getcwd())
os.chdir("C:/Users/black/PycharmProjects/NEA")
print("Working dir:", os.getcwd())



HEIGHT = 630
WIDTH = 980

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

root.resizable(False, False)

colorx = "#F4BE40"


frame1 = tk.Frame(root, bg=colorx)
frame2 = tk.Frame(root, bg=colorx)
frame3 = tk.Frame(root, bg=colorx)
frame4 = tk.Frame(root, bg=colorx)
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
    try:
        shutil.copy(mp3audio, 'music',  follow_symlinks=True)
    except:
        print("None selected")


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
        data = os.listdir("music")
    else:
        data = []
        for item in os.listdir("music"):
            if typed.lower() in item.lower():
                data.append(item)
    update(data)


def textfile():
    # start editable vars #
    outputfile = "titles.txt"  # file to save the results to
    folder = "music"  # the folder to inventory
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
    with open("titles.txt", "r") as a_file:
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
    destination = "music"
    out_file = video.download(destination)
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
    path = ("music/"+text)
    print(path)
    transcribe(path, text)


def transcribe(filename, nameoftranscription):
    x = nameoftranscription[:-4] + '-transcript.txt'
    path = ('transcripts/' + x)
    print(os.path.isfile(path))
    if os.path.exists(path) == True:
        print('Transcript Already exist, do you want to try to summarise')
        answer = str(input("y/n : "))
        if answer == 'y':
            y = nameoftranscription[:-4] + '-summary.txt'
            path2 = ('summaries/' + y)
            if os.path.exists(path2) == True:
                print("Summary already exists")
            else:
                txt = Path(path).read_text()
                summarisation(txt, nameoftranscription)
        elif answer == 'n':
            print("ok")
        else:
            print("Not right answer")
    else:

        #########################################################

        authKey = '39e03013f79342708b140a7f4668a0cd'

        headers = {
            'authorization': authKey,
            'content-type': 'application/json'
        }

        uploadUrl = 'https://api.assemblyai.com/v2/upload'
        transcriptUrl = 'https://api.assemblyai.com/v2/transcript'

        #########################################################
        def uploadMyFile(fileName):

            def _readmyFile(fn):

                chunkSize = 5242880

                with open(fn, "rb") as fileStream:

                    while True:
                        data = fileStream.read(chunkSize)

                        if not data:
                            break

                        yield data

            response = requests.post(
                uploadUrl,
                headers=headers,
                data=_readmyFile(fileName)

            )

            json = response.json()

            return json['upload_url']

        def startTranscription(aurl):

            response = requests.post(
                transcriptUrl,
                headers=headers,
                json={'audio_url': aurl}
            )

            json = response.json()

            return json['id']

        def getTranscription(tid):

            maxAttempts = 50
            timedout = False

            while True:
                response = requests.get(
                    f'{transcriptUrl}/{tid}',
                    headers=headers
                )

                json = response.json()

                if json['status'] == 'completed':
                    break

                maxAttempts -= 1
                timedout = maxAttempts <= 0

                print(maxAttempts)

                if timedout:
                    break

                time.sleep(3)

            return 'Timed out...' if timedout else json['text']

        #########################################################

        audioUrl = uploadMyFile(filename)

        #########################################################

        transcriptionID = startTranscription(audioUrl)

        #########################################################

        text = getTranscription(transcriptionID)

        wrapper = textwrap.TextWrapper(width=100)
        string = wrapper.fill(text=text)

        save_path = 'transcripts'
        name_of_file = nameoftranscription[:-4] + '-transcript'
        completeName = os.path.join(save_path, name_of_file + ".txt")
        file1 = open(completeName, 'w')
        file1.write(string)
        file1.close()
        print('Done transcribing')

        summarisation(text, nameoftranscription)


def summarisation(transcription, nameoftranscription):
    summarizer = pipeline("summarization", model='google/pegasus-large')

    numberofwords = len(transcription)

    if numberofwords < 50:
        print('Read it urself loser')
    else:

        max_chunk = (numberofwords//20)

        transcription = transcription.replace('.', '.<eos>')
        transcription = transcription.replace('?', '?<eos>')
        transcription = transcription.replace('!', '!<eos>')

        sentences = transcription.split('<eos>')
        current_chunk = 0
        chunks = []

        print("Start chunking")

        for sentence in sentences:
            if len(chunks) == current_chunk + 1:
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                print(current_chunk)
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])

        print("Done chunking")

        time.sleep(2)

        print('Starting summarising')

        def joining():
            print("We start pls we really do")
            res = summarizer(chunks, min_length=30, do_sample=False)
            text = ' '.join([summ['summary_text'] for summ in res])
            print(text)
            for i in range(0,100):
                print(i)

        def start_joining():
            print("WHHHHAio")
            t = Thread(target=joining, daemon=True)
            t.start()

        start_joining()


        # wrapper = textwrap.TextWrapper(width=100)
        # string = wrapper.fill(text=text)
        #
        # save_path = 'summaries'
        # name_of_file = nameoftranscription[:-4] + '-summary'
        # completeName = os.path.join(save_path, name_of_file + ".txt")
        # file1 = open(completeName, 'w')
        # file1.write(string)
        # file1.close()
        #
        # print('Done summarising')



for frame in (frame1, frame2, frame3, frame4):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)


############################################################## Frame 1 CODE
start_key = tk.PhotoImage(file="button_start-new-summary.png")
start_summary_button = tk.Button(frame1, image=start_key, bd=0, bg=colorx, activebackground=colorx, command=lambda: (show_frame(frame2)))
start_summary_button.place(relx=0.08, rely=0.4, relwidth=0.38, relheight=0.12)

title_label = tk.Label(frame1, text="Summarisation App", bg=colorx, font=("Segoe UI Semibold", 40))
title_label.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.3)

settings_key = tk.PhotoImage(file='png-transparent-button-computer-icons-setting-button-ribbon-black-desktop-wallpaper.png')
settingsbutton = tk.Button(frame1, image=settings_key, bd=0, bg=colorx, activebackground=colorx, command=lambda: show_frame(frame4))
settingsbutton.place(relx=0, rely=0, relwidth=0.11, relheight=0.145)

managekey = tk.PhotoImage(file="button_manage-summaries.png")
managesummariesbutton = tk.Button(frame1, image=managekey, bd=0, bg=colorx, activebackground=colorx, command=lambda: show_frame(frame3))
managesummariesbutton.place(relx=0.54, rely=0.4, relwidth=0.38, relheight=0.12)

############################################################## Frame 2 CODE
titlelable = tk.Label(frame2, text="New Summary", bg=colorx, font=("Segoe UI Semibold", 40))
titlelable.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.2)

back_key = tk.PhotoImage(file='button_back.png')
backbutton = tk.Button(frame2, image = back_key, bd=0, bg=colorx, activebackground=colorx,
                       command=lambda:(show_frame(frame1), clear_text(),searchentry.delete(0, tk.END), update(os.listdir("music"))))
backbutton.place(relx=0.0005, rely=0.85, relwidth=0.14, relheight=0.18)

youtubelink = tk.Label(frame2, text="Youtube Link:", bg=colorx, font=("Segoe UI Semibold", 20))
youtubelink.place(relx=0.12, rely=0.3, relwidth=0.25, relheight=0.09)

linkinput = tk.Entry(frame2, font=("Segoe UI Semibold", 13))
linkinput.place(relx=0.33, rely=0.3, relwidth=0.37, relheight=0.1)

refreshlistbox =  tk.Button(frame2, text="Refresh", command=lambda: (searchentry.delete(0, tk.END), update(os.listdir("music"))))
refreshlistbox.place(relx=0.5, rely=0.42, relwidth=0.1, relheight=0.05)

submit_key = tk.PhotoImage(file="button_submit.png")
submitbutton = tk.Button(frame2, image=submit_key, bd=0, bg=colorx, activebackground=colorx, command=lambda: (retrieve_input(), clear_text(),))
submitbutton.place(relx=0.7, rely=0.3, relwidth=0.16, relheight=0.11)
root.bind('<Return>', lambda event:clear_text())

# buttonexplore = tk.Button(frame2, text="Browse Files", command=browseFiles)
# buttonexplore.place(relx=0.65, rely=0.3, relwidth=0.1, relheight=0.05)

frame5.place(relx=0.15, rely=0.57)

audiolistbox = tk.Listbox(frame5, fg="black", height=15, width=95)
audiolistbox.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(frame5, orient=tk.VERTICAL, command=audiolistbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

audiolistbox.config(yscrollcommand=scrollbar.set)

searchentry = tk.Entry(frame2)
searchentry.place(relx=0.15, rely=0.5, width=590, relheight=0.05)

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

update(os.listdir("music"))
show_frame(frame1)

root.mainloop()