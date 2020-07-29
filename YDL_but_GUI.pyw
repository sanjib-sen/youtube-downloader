import os
import shutil
import subprocess
import tkinter.filedialog
import threading
from tkinter import *
from tkinter import ttk
import time

#@Adding to PATH:
# python -u "d:\Coding\Side Projects\YDLGUI\Dv2.py"

def cd():
    ab= filedialog.askdirectory()
    global folder 
    folder = ab
    slfr.config(text =folder)
    f2 = open(os.path.join(__location__, 'usr.config'),'w');
    f2.write((folder))
    f2.close()
def step (k):
    prg['value'] = k

def starting():
    if(folder == ""):
        cd()
    if (var.get() == "Audio"):
        t = threading.Thread(target=Audio)
        t.daemon = True 
        t.start()
    elif (var.get() == "Playlist"):
        t = threading.Thread(target=Playlist)
        t.daemon = True 
        t.start()
    elif (var.get() == "Channel"):
        t = threading.Thread(target=Channel)
        t.daemon = True 
        t.start()
    else:
        t = threading.Thread(target=Video)
        t.daemon = True 
        t.start()

def Channel():
    status.config("Donloading Channel")
    hq = "main -ciw --write-auto-sub --write-srt --sub-lang en --convert-subs=srt -f 'bestvideo+bestaudio/bestvideo+bestaudio' --newline --merge-output-format mp4 --newline -o "+folder+"/'%(title)s.%(ext)s' "+ e.get()
    ab = '%SYSTEMROOT%\System32\WindowsPowerShell\\v1.0\powershell.exe -Command '+hq
    print(hq)
    process = subprocess.Popen(ab, shell = True,stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            line = str(output.strip().decode('ansi'))
            print(line)
            if(len(line.split())>4):
                if (line.split()[0] =="[download]"):
                    if (line.split(" ")[1]=='Downloading' and line.split(" ")[2]=='video' and line.split(" ")[4]=='of'):
                        plistlbl.config(text ="Downloading Video "+line.split(" ")[3]+" of "+line.split(" ")[5])
            if(len(line.split())>7):
                if (line.split()[0] =="[download]"):
                    if(line.split()[1] == '100'):
                        ml = Message(root, text = "Already Downloaded", width = 400).pack()
                        continue

                    pbar = line.split()[1][:-3]
                    try: int(pbar)
                    except: continue
                    spd = line.split()[5]
                    lbl.config(text = "Speed "+spd)
                    prc = line.split()[1]
                    prclbl.config(text = prc+" Done")
                    eta = line.split()[7]
                    etalbl.config(text="ETA "+ eta)
                    step (int(pbar))
                    root.update_idletasks()
                    time.sleep(.1)
                    print(int(pbar))
                    if (int(pbar) == 100):
                        lbl.config(text = "Download Completed")
                        status.config(text ="")
        rc = process.poll()


def Playlist():
    if(len(e.get())>0):
        sps = e.get().split('&list=')[1]
    status.config(text ="Donloading Playlist")
    hq = "main -i --write-auto-sub --write-srt --sub-lang en --convert-subs=srt -f 'bestvideo+bestaudio/bestvideo+bestaudio' --newline --merge-output-format mp4 --newline -o "+folder+"/'%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' "+ sps
    ab = '%SYSTEMROOT%\System32\WindowsPowerShell\\v1.0\powershell.exe -Command '+hq
    print(hq)
    process = subprocess.Popen(ab, shell = True,stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            line = str(output.strip().decode('ansi'))
            print(line)
            if(len(line.split())>4):
                if (line.split()[0] =="[download]"):
                    if (line.split(" ")[1]=='Downloading' and line.split(" ")[2]=='video' and line.split(" ")[4]=='of'):
                        plistlbl.config(text ="Downloading Video "+line.split(" ")[3]+" of "+line.split(" ")[5])
            if(len(line.split())>7):
                if (line.split()[0] =="[download]"):
                    if(line.split()[1] == '100'):
                        ml = Message(root, text = "Already Downloaded", width = 400).pack()
                        continue

                    pbar = line.split()[1][:-3]
                    try: int(pbar)
                    except: continue
                    spd = line.split()[5]
                    lbl.config(text = "Speed "+spd)
                    prc = line.split()[1]
                    prclbl.config(text = prc+" Done")
                    eta = line.split()[7]
                    etalbl.config(text="ETA "+ eta)
                    step (int(pbar))
                    root.update_idletasks()
                    time.sleep(.1)
                    print(int(pbar))
                    if (int(pbar) == 100):
                        lbl.config(text = "Download Completed")
                        status.config(text ="")
        rc = process.poll()

def Video():
    try: sps = e.get().split('&list=')[0]
    except: sps = e.get()
    status.config(text = "Donloading Video")
    hq = 'main '+sps+" --write-auto-sub --write-srt --sub-lang en --convert-subs=srt -f 'bestvideo+bestaudio/bestvideo+bestaudio' --newline --merge-output-format mp4"+' -o '+folder+"/'%(title)s.%(ext)s'"
    ab = '%SYSTEMROOT%\System32\WindowsPowerShell\\v1.0\powershell.exe -Command '+hq
    print(hq)
    process = subprocess.Popen(ab, shell = True,stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            line = str(output.strip().decode('ansi'))
            print(line)
            if(len(line.split())>7):
                if (line.split()[0] =="[download]"):
                    if(line.split()[1] == '100'):
                        ml = Message(root, text = "Already Downloaded", width = 400).pack()
                        continue

                    pbar = line.split()[1][:-3]
                    try: int(pbar)
                    except: continue
                    spd = line.split()[5]
                    lbl.config(text = "Speed "+spd)
                    prc = line.split()[1]
                    prclbl.config(text = prc+" Done")
                    eta = line.split()[7]
                    etalbl.config(text="ETA "+ eta)
                    step (int(pbar))
                    root.update_idletasks()
                    time.sleep(.1)
                    print(int(pbar))
                    if (int(pbar) == 100):
                        lbl.config(text = "Download Completed")
                        status.config(text ="")
        rc = process.poll()

def Audio():
    status.config(text = "Donloading Audio")
    hq = 'main '+e.get()+" --extract-audio --audio-format mp3"+' -o '+folder+"/'%(title)s.%(ext)s'"
    ab = '%SYSTEMROOT%\System32\WindowsPowerShell\\v1.0\powershell.exe -Command '+hq
    print(hq)
    process = subprocess.Popen(ab, shell = True,stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            line = str(output.strip().decode('ansi'))
            print(line)
            
            if(len(line.split())>7):


                    if(line.split()[1] == '100'):
                        ml = Message(root, text = "Already Downloaded", width = 400).pack()
                        continue

                    pbar = line.split()[1][:-3]
                    try: int(pbar)
                    except: continue
                    spd = line.split()[5]
                    lbl.config(text = "Speed "+spd)
                    prc = line.split()[1]
                    prclbl.config(text = prc+" Done")
                    eta = line.split()[7]
                    etalbl.config(text="ETA "+ eta)
                    step (int(pbar))
                    root.update_idletasks()
                    time.sleep(.1)
                    print(int(pbar))
                    if (int(pbar) == 100):
                        time.sleep(3)
                        lbl.config(text = "Download Completed")
                        status.config(text ="")
        rc = process.poll()



__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

f = open(os.path.join(__location__, 'usr.config'),'r');
line = f.readline()
folder = line.split(" ")[0]

root = Tk()
root.geometry('400x450')
root.resizable(False, False)
root.title('YDL_But_GUI')
top = Label(root, text = "        ").grid(row =0)
mlp = Label(root, text = "       Enter URL        ").grid(row =1, column = 1)
e = Entry(root, width = 20)
e.grid(row = 1, column =2)
brk1 = Label(root, text ="").grid(row = 2)
sltp = Label(root, text = "Select Type").grid(row =3, column = 1)
types = ["Video", "Audio", "Playlist", "Channel"]
var = StringVar()
var.set(types[0])
combo = OptionMenu(root, var, types[0], types[1], types[2], types[3]).grid(row =3, column =2)
brk2 = Label(root, text ="").grid(row = 4)
sldr = Label(root, text = "Save Location").grid(row =5, column = 1)
slfr = Label(root, text =folder)
slfr.grid(row =5, column =2)
cdButton = Button(root, text = "Change Directory", command = cd).grid(row =5, column = 3, padx = 10)
brk3 = Label(root, text ="").grid(row = 6)
formLbl =Label(root, text =" Quality").grid(row =7, column =1)
formLblShow =Label(root, text =" Maximum Quality ").grid(row =7, column =2)
slfrmButton = Button(root, text = "Change Quality" ).grid(row = 7, column =3)
brk4 = Label(root, text ="").grid(row = 8)
myButton = Button(root, text = "Download", command=starting , anchor = 'center').grid(row = 9, column =2)
brk5 = Label(root, text ="").grid(row = 10)
prg = ttk.Progressbar(root, orient =HORIZONTAL,length = 300, mode = 'determinate')
prg.grid(row =11, columnspan = 4)


form =  " -f best "
prclbl = Label(root)
prclbl.grid(row = 12, column =1)
etalbl = Label(root)
etalbl.grid(row = 12, column =3)
lbl = Label(root)
lbl.grid(row = 12, column =2)

brk7 = Label(root, text ="").grid(row = 13)

status = Label(root)
status.grid(row = 14, columnspan = 4)

brk8 = Label(root, text ="").grid(row = 15)
plistlbl = Label(root)
plistlbl.grid(row = 16, columnspan = 4)


root.mainloop()
