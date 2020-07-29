import pyscreenshot as ImageGrab
import pynput
import io
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller
import time
import socket
import threading
import pickle

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s1.bind(('192.168.0.4', 1234))
s2.bind(('192.168.0.4', 1235))

s1.listen(1)
s2.listen(1)
imageIO = io.BytesIO()

c1, addr = s1.accept()
c2, addr = s2.accept()
x = False

splited = ""

def sdm():
    global splited
    while True:
        get = c2.recv(1500)
        splited = pickle.loads(get)
        mousectl.threader()
        kb()

class mousectl:
    def threader():
        mousectl.position()
        mousectl.leftbtn()
        mousectl.rightbtn()
        mousectl.middlebtn()
        mousectl.mousewheel()

    def position():
        posx = splited[0]
        posy = splited[1]
        mouse.position = (posx, posy)

    def leftbtn():
        if (splited[2] == 1):
            mouse.press(Button.left)
        else:
            mouse.release(Button.left)

    def rightbtn():
        if (splited[3] == 1):
            mouse.press(Button.right)
        else:
            mouse.release(Button.right)

    def middlebtn():
        if (splited[4] == 1):
            mouse.press(Button.middle)
        else:
            mouse.release(Button.middle)

    def mousewheel():
        if (splited[5] == 1):
            mouse.scroll(0, 2)
        else:
            if (splited[5] == -1):
                mouse.scroll(0, -2)

# Issue with getting certain keys to register in pynput
def kb():
    if not (splited[6] == "Null"):
        if (len(splited[6]) > 1):
            key = splited[6].lower()
            if (key == 'return'):
                key = 'enter'
            try:
                keyboard.press(Key.(key))
                keyboard.release(Key.(key))
            except:
                print(key)

        else:
            keyboard.press(splited[6])
            keyboard.release(splited[6])

def dsp():
    global x
    global imageIO
    while True:
        imageIO = io.BytesIO()
        image = ImageGrab.grab(backend="mss",childprocess=False)
        image.save(imageIO, "JPEG", quality=92)
        if x:
            while not (c1.recv(16) == b'2'):
                pass
        c1.send(str(len(imageIO.getvalue())).encode('utf-8'))
        while not (c1.recv(16) == b'1'):
            pass
        c1.sendall(imageIO.getvalue())
        imageIO.close()
        x = True

dsp_thread = threading.Thread(target=dsp)
sdm_thread = threading.Thread(target=sdm)
dsp_thread.start()
sdm_thread.start()
