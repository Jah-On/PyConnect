from tkinter import *
from PIL import Image
from PIL import ImageTk
import socket
import threading
import io
import time
import pickle

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s1.connect(('192.168.0.4', 1234))
s2.connect(('192.168.0.4', 1235))

imageBuffer = b''
state = True
img = ""
map = [1,2,3,4,5,6,"Null"]

def ctlsender():
    s2.send(pickle.dumps(map))
    root.after(1, ctlsender)

def mousemove(event):
    map[0] = event.x
    map[1] = event.y

class leftbtn():
    def down(event):
        map[2] = 1

    def up(event):
        map[2] = 0

class rightbtn():
    def down(event):
        map[3] = 1

    def up(event):
        map[3] = 0

class middlebtn():
    def down(event):
        map[4] = 1

    def up(event):
        map[4] = 0

class mousewheel():
    def up(event):
        map[5] = 1
        root.after(10)
        map[5] = 0

    def down(event):
        map[5] = -1
        root.after(10)
        map[5] = 0

class keys:
    def down(event):
        map[6] = (event.keysym)
        print(map[6])

    def up(event):
        map[6] = "Null"

def dummy(event):
    print(event)

root = Tk()
lbl = Label(root, image=img)
lbl.bind("<Motion>", mousemove)
lbl.bind("<ButtonPress-1>", leftbtn.down)
lbl.bind("<ButtonRelease-1>", leftbtn.up)
lbl.bind("<ButtonPress-3>", rightbtn.down)
lbl.bind("<ButtonRelease-3>", rightbtn.up)
lbl.bind("<ButtonPress-2>", middlebtn.down)
lbl.bind("<ButtonRelease-2>", middlebtn.up)
lbl.bind("<Button-4>", mousewheel.up)
lbl.bind("<Button-5>", mousewheel.down)
root.bind("<KeyPress>", keys.down)
root.bind("<KeyRelease>", keys.up)
root.after(1, ctlsender)
lbl.pack(expand="yes")

def reset():
    global imageBuffer
    global lbl
    global img
    imageLengthRaw = s1.recv(1000000)
    imageLength = int(imageLengthRaw.decode('utf-8'))
    if imageLength > 0:
        # past = time.time()
        s1.send(b'1')
        while not (len(imageBuffer) == imageLength):
            recved = s1.recv(1000000)
            imageBuffer = imageBuffer + recved

        imageIO = io.BytesIO(imageBuffer)
        img = ImageTk.PhotoImage(Image.open(imageIO))
        lbl.configure(image=img)
        # print(time.time() - past)
        imageBuffer = b''
        s1.send(b'2')

    root.after(1, reset)

root.after(1, reset)
root.mainloop()
