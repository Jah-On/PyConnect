version = b'a1.0'

try:
    import urllib.request
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    if (urllib.request.urlopen("https://raw.githubusercontent.com/Jah-On/PyConnect/master/version").read()[0:4] != version):
        newFile = open("host.py", "wb")
        newFile.write(urllib.request.urlopen("https://raw.githubusercontent.com/Jah-On/PyConnect/master/host.py").read())
        newFile.close()
        import subprocess
        proc = subprocess.Popen(["python host.py"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        exit = True
    else:
        exit = False
except:
    exit = False

if (exit):
    quit()

from mss import mss
from pynput.mouse import Controller
import autopy
import time
import socket
import netifaces as ni
import threading
import multiprocessing
from ctypes import c_char, c_bool, c_char_p, c_wchar, c_wchar_p
import psutil
import os
import sys
from dearpygui.core import *
from dearpygui.simple import *
import blosc
import numpy
import cv2
from screeninfo import get_monitors
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA

try:
    file = open("pswd.txt", "r")
    file.read()
    file.close()
except:
    file = open("pswd.txt", "w")
    file.close()

keyMap = {0:"0",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"a",11:"b",12:"c",13:"d",14:"e",15:"f",16:"g",17:"h",18:"i",19:"j",20:"k",21:"l",22:"m",23:"n",24:"o",25:"p",26:"q",27:"r",28:"s",29:"t",30:"u",31:"v",32:"w",33:"x",34:"y",35:"z",36:autopy.key.Code.BACKSPACE,37:"\t",39:autopy.key.Code.RETURN,40:autopy.key.Code.SHIFT,41:autopy.key.Code.CONTROL,42:autopy.key.Code.ALT,43:autopy.key.Code.PAUSE,44:autopy.key.Code.CAPS_LOCK,45:autopy.key.Code.ESCAPE,46:autopy.key.Code.SPACE,47:autopy.key.Code.PAGE_UP,48:autopy.key.Code.PAGE_DOWN,49:autopy.key.Code.END,50:autopy.key.Code.HOME,51:autopy.key.Code.LEFT_ARROW,52:autopy.key.Code.UP_ARROW,53:autopy.key.Code.RIGHT_ARROW,54:autopy.key.Code.DOWN_ARROW,58:autopy.key.Code.PRINT_SCREEN,59:autopy.key.Code.INSERT,60:autopy.key.Code.DELETE,63:autopy.key.Code.META,64:autopy.key.Code.META,66:autopy.key.Code.NUM0,67:autopy.key.Code.NUM1,68:autopy.key.Code.NUM2,69:autopy.key.Code.NUM3,70:autopy.key.Code.NUM4,71:autopy.key.Code.NUM5,72:autopy.key.Code.NUM6,73:autopy.key.Code.NUM7,74:autopy.key.Code.NUM8,75:autopy.key.Code.NUM9,76:autopy.key.Code.NUM_MULTIPLY,77:autopy.key.Code.NUM_ADD,79:autopy.key.Code.NUM_SUBTRACT,80:autopy.key.Code.NUM_DECIMAL,81:autopy.key.Code.NUM_DIVIDE,82:autopy.key.Code.F1,83:autopy.key.Code.F2,84:autopy.key.Code.F3,85:autopy.key.Code.F4,86:autopy.key.Code.F5,87:autopy.key.Code.F6,88:autopy.key.Code.F7,89:autopy.key.Code.F8,90:autopy.key.Code.F9,91:autopy.key.Code.F10,92:autopy.key.Code.F11,93:autopy.key.Code.F12,94:autopy.key.Code.F13,95:autopy.key.Code.F14,96:autopy.key.Code.F15,97:autopy.key.Code.F16,98:autopy.key.Code.F17,99:autopy.key.Code.F18,100:autopy.key.Code.F19,101:autopy.key.Code.F20,102:autopy.key.Code.F21,103:autopy.key.Code.F22,104:autopy.key.Code.F23,105:autopy.key.Code.F24,106:autopy.key.Code.NUM_LOCK,107:autopy.key.Code.SCROLL_LOCK,108:autopy.key.Code.SHIFT,109:autopy.key.Code.SHIFT,110:autopy.key.Code.CONTROL,111:autopy.key.Code.CONTROL,132:";",133:"=",134:",",135:"-",136:".",137:"/",138:"`",139:"[",140:"\\",141:"]",142:"\'"}

coreRunning = True
appRunning = multiprocessing.Array(c_bool, 1)
appRunning[0] = True
reset = multiprocessing.Array(c_bool, 1)
reset[0] = False
alive = multiprocessing.Array(c_bool, 1)
alive[0] = False

try:
    fileIO = open("temp.txt", "r")
    fileData = fileIO.read()
    fileIO.close()
    fileData = fileData.split("\n")
    if not psutil.pid_exists(int(fileData[0])):
        os.remove("temp.txt")
except:
    pass

def misc():
    global do
    while appRunning[0]:
        try:
            if (do == b'o'):
                if (sys.platform == "darwin"):
                    c3.send(b'om')
                elif (sys.platform == "linux"):
                    c3.send(b'ol')
                else:
                    c3.send(b'ow')
                do = b''
            if (do == b'd'):
                c3.send(b'd' + (str(get_monitors()[0].width) + ":" + str(get_monitors()[0].height)).encode("utf-8"))
                clientDisplay = c3.recv(32)
                while (clientDisplay == b'') and appRunning[0]:
                    time.sleep(0.01)
                    clientDisplay = c3.recv(32)
                alive[0] = True
                clientDisplay = clientDisplay.split(b':')
                global clientWidth, clientHeight
                clientWidth, clientHeight = int(clientDisplay[0]), int(clientDisplay[1])
        except:
            pass
        time.sleep(0.005)

def netInit():
    global clientWidth, clientHeight
    while appRunning[0]:
        if not coreRunning:
            return False
        global privateKey
        privateKey = RSA.generate(2048)
        global publicKey
        myPublicKey = privateKey.publickey()
        global decryptor
        decryptor = PKCS1_OAEP.new(key=privateKey)
        global authToken
        authToken = os.urandom(512)
        global c1, addr1
        try:
            c1, addr1 = s1.accept()
        except:
            return False
        threading.Thread(target=timeoutManager).start()
        c1.send(myPublicKey.export_key())
        global AESKey
        AESKey = c1.recv(2048)
        while (len(AESKey) < 1) and appRunning[0]:
            AESKey = c1.recv(2048)
            time.sleep(0.0005)
        alive[0] = True
        AESKey = decryptor.decrypt(AESKey)
        c1.send(b'\x30')
        global AESIV
        AESIV = c1.recv(2048)
        while (len(AESIV) < 1) and appRunning[0]:
            AESIV = c1.recv(2048)
            time.sleep(0.0005)
        alive[0] = True
        AESIV = decryptor.decrypt(AESIV)
        global AESC
        AESC = AES.new(AESKey, AES.MODE_CFB, AESIV)
        global AESD
        AESD = AES.new(AESKey, AES.MODE_CFB, AESIV)
        c1.send(b'\x30')
        recipVersion = c1.recv(2048)
        while (len(recipVersion) < 1) and appRunning[0]:
            recipVersion = c1.recv(2048)
            time.sleep(0.0005)
        alive[0] = True
        if (recipVersion == version):
            c1.send(b'y')
        else:
            c1.send(b'n')
            return False
        passwordTest = c1.recv(2048)
        while (len(passwordTest) < 1) and appRunning[0]:
            passwordTest = c1.recv(2048)
            time.sleep(0.0005)
        alive[0] = True
        passwordTest = AESD.decrypt(passwordTest)
        if (passwordTest == b'+=Null=+') and (len(password) == 0):
            c1.send(b'pass')
            while (len(c1.recv(1)) == 0) and appRunning[0]:
                time.sleep(.001)
            alive[0] = True
            c1.send((str(get_monitors()[0].width) + ":" + str(get_monitors()[0].height)).encode("utf-8"))
            clientDisplay = c1.recv(32)
            while (len(clientDisplay) < 1) and appRunning[0]:
                clientDisplay = c1.recv(32)
                time.sleep(0.001)
            alive[0] = True
            clientDisplay = clientDisplay.split(b':')
            clientWidth, clientHeight = int(clientDisplay[0]), int(clientDisplay[1])
            c1.send(AESC.encrypt(authToken))
            return True
        else:
            if passwordTest == password:
                c1.send(b'pass')
                while (len(c1.recv(1)) == 0) and appRunning[0]:
                    time.sleep(.001)
                alive[0] = True
                c1.send((str(get_monitors()[0].width) + ":" + str(get_monitors()[0].height)).encode("utf-8"))
                clientDisplay = c1.recv(32)
                while (len(clientDisplay) < 1) and appRunning[0]:
                    clientDisplay = c1.recv(32)
                    time.sleep(0.001)
                alive[0] = True
                clientDisplay = clientDisplay.split(b':')
                clientWidth, clientHeight = int(clientDisplay[0]), int(clientDisplay[1])
                c1.send(AESC.encrypt(authToken))
                return True
            else:
                c1.send(b'fail')
                return False

def timeoutManager():
    global alive
    global reset
    global appRunning
    while appRunning[0]:
        alive[0] = False
        time.sleep(3)
        if not alive[0] and appRunning[0]:
            appRunning[0] = False
            reset[0] = True
            break

def dataReciever():
    global appRunning
    global reset
    global strData
    c1.send(b'\x30')
    while appRunning[0]:
        try:
            controlDataStream = c1.recv(128)
            while ((len(controlDataStream) == 0) and appRunning[0]):
                controlDataStream = c1.recv(128)
                time.sleep(0.0005)
            alive[0] = True
            c1.send(b'\x30')
            controlData = AESD.decrypt(controlDataStream)
            while (len(controlData) != 300):
                controlData += b'\x30'
            strData[:] = controlData
        except:
            if alive[0]:
                appRunning[0] = False
                reset[0] = True

def one():
    global screenshots
    global screenshot
    global do
    while appRunning[0]:
        try:
            image1 = screenshot.grab(screenshot.monitors[1])
            tempMonitorSizeWidth, tempMonitorSizeHeight = get_monitors()[0].width, get_monitors()[0].height
            if ((tempMonitorSizeWidth * tempMonitorSizeHeight) == (clientWidth * clientHeight)):
                numpyImage = numpy.frombuffer(image1.rgb, dtype="uint8").reshape(-1).tobytes()
                comp1 = blosc.compress(numpyImage, cname="lz4")
                screenshots.append(comp1)
            elif ((tempMonitorSizeWidth * tempMonitorSizeHeight) > (clientWidth * clientHeight)):
                numpyImage = numpy.frombuffer(image1.rgb, dtype="uint8").reshape(tempMonitorSizeHeight, tempMonitorSizeWidth, 3)
                cvImage = cv2.resize(numpyImage, (clientWidth, clientHeight), interpolation=cv2.INTER_LANCZOS4)
                comp1 = blosc.compress(cvImage.reshape(-1).tobytes(), cname="lz4")
                screenshots.append(comp1)
            else:
                comp1 = blosc.compress(image1.rgb, cname="lz4")
                screenshots.append(comp1)
            while (len(screenshots) == 1) and appRunning[0]:
                time.sleep(0.0005)
        except:
            del screenshot
            screenshot = mss()
        do = b'd'

class ctrl:
    def __init__():
        threading.Thread(target=ctrl.dataManager).start()
        threading.Thread(target=ctrl.mousectrl.position).start()
        threading.Thread(target=ctrl.mousectrl.btn).start()
        threading.Thread(target=ctrl.mousectrl.wheel).start()
        threading.Thread(target=ctrl.keyboardctrl.kDM).start()
        threading.Thread(target=ctrl.keyboardctrl.kUM).start()
        ctrl.dataManager()

    def dataManager():
        global strData
        global listData
        global keyboardArray
        while (strData[0] == b'\\') and appRunning[0]:
            time.sleep(0.0005)
        while appRunning[0]:
            listData = strData[:].split(b'\xe2\x96\xac')
            keyboardArray = listData[4].split(b'\xe2\x96\xad')
            time.sleep(0.0005)

    class mousectrl:
        def position():
            while ((listData[0] == b'\x6e') or (listData[0] == b'')) and appRunning[0]:
                time.sleep(0.0005)
            while appRunning[0]:
                autopy.mouse.move(float(listData[0]), float(listData[1]))
                time.sleep(0.0005)

        def btn():
            global mouseDown
            while (len(listData[2]) == 0) and appRunning[0]:
                time.sleep(0.0005)
            while appRunning[0]:
                if ((listData[2][0:1] == b'\x31') and (not mouseDown[0])):
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
                    mouseDown[0] = True
                elif ((listData[2][0:1] != b'\x31') and (mouseDown[0])):
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
                    mouseDown[0] = False
                if ((listData[2][1:2] == b'\x31') and not (mouseDown[1])):
                    autopy.mouse.toggle(autopy.mouse.Button.RIGHT, True)
                    mouseDown[1] = True
                elif ((listData[2][1:2] != b'\x31') and (mouseDown[1])):
                    autopy.mouse.toggle(autopy.mouse.Button.RIGHT, False)
                    mouseDown[1] = False
                if ((listData[2][2:3] == b'\x31') and not (mouseDown[2])):
                    autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, True)
                    mouseDown[2] = True
                elif ((listData[2][2:3] != b'\x31') and (mouseDown[2])):
                    autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, False)
                    mouseDown[2] = False
                time.sleep(0.0005)

        def wheel():
            while (listData[3] == b'') and appRunning[0]:
                time.sleep(0.0005)
            while appRunning[0]:
                if not (listData[3] == b'\x30'):
                    mouseControl.scroll(0, int(listData[3]))
                time.sleep(0.0005)

    class keyboardctrl:
        def kDM():
            global keyboardArray
            global keysDown
            while appRunning[0]:
                for i in range(0, len(keyboardArray)):
                    if (keyboardArray[i] not in keysDown) and ((len(keyboardArray[i]) > 0) and (len(keyboardArray[i]) < 4)):
                        asInt = int(keyboardArray[i])
                        try:
                            autopy.key.toggle(keyMap[asInt], True)
                            keysDown.append(keyboardArray[i])
                        except:
                            pass
                time.sleep(.0005)

        def kUM():
            global keyboardArray
            global keysDown
            while appRunning[0]:
                positions = []
                for i in range(0, len(keysDown)):
                    if keysDown[i] not in keyboardArray:
                        asInt = int(keysDown[i])
                        autopy.key.toggle(keyMap[asInt], False)
                        positions.append(i)
                for j in range(0, len(positions)):
                    try:
                        del keysDown[j]
                    except:
                        pass
                time.sleep(.0005)

def dsp():
    global appRunning
    global listData
    global x
    global reset
    while appRunning[0]:
        try:
            while (len(screenshots) == 0) and appRunning[0]:
                time.sleep(0.0005)
            if x:
                while not (c2.recv(16) == b'\x31') and appRunning[0]:
                    time.sleep(0.0005)
                alive[0] = True
            c2.send(str(len(screenshots[0])).encode('utf-8'))
            while not (c2.recv(2) == b'\x30') and appRunning[0]:
                time.sleep(0.0005)
            alive[0] = True
            c2.sendall(AESC.encrypt(screenshots[0]))
            del screenshots[0]
            x = True
        except:
            if alive[0]:
                appRunning[0] = False
                reset[0] = True

def startOrRestart():
    if coreRunning:
        global password
        fileIO = open("pswd.txt", "rb")
        password = fileIO.read()
        fileIO.close()
        global keysDown
        keysDown = []
        global screenshot
        screenshot = mss()
        interfaces = ni.interfaces()
        for i in range(0, (len(interfaces))):
            try:
                ip = ni.ifaddresses(interfaces[i])[ni.AF_INET][0]['addr']
            except:
                pass
        global s1
        try:
            del s1
        except:
            pass
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s1.bind((ip, 1234))
        s1.listen(2)
        global reset
        reset[0] = False
        global x
        x = False
        global mouse
        mouse = []
        global mouseDown
        mouseDown = [False, False, False]
        global keyboard
        keyboard = []
        global keyboardArray
        keyboardArray = []
        global keyDown
        keysDown = []
        global mouseControl
        mouseControl = Controller()
        global strData
        strData = multiprocessing.Array(c_char, 300)
        global listData
        listData = [b'', b'', b'', b'', b'']
        global screenshots
        screenshots = []
        global appRunning
        appRunning[0] = True
        if netInit():
            global c2, addr2
            global c3, addr3
            try:
                authed = False
                while not authed and appRunning[0]:
                    c2, addr2 = s1.accept()
                    clientAuth = c2.recv(512)
                    while (len(clientAuth) < 1) and appRunning[0]:
                        clientAuth = c2.recv(512)
                        time.sleep(0.0005)
                    alive[0] = True
                    if (AESD.decrypt(clientAuth) == authToken):
                        authed = True
                authed = False
                while not authed and appRunning[0]:
                    c3, addr3 = s1.accept()
                    clientAuth = c3.recv(512)
                    while (len(clientAuth) < 1) and appRunning[0]:
                        clientAuth = c3.recv(512)
                        time.sleep(0.0005)
                    alive[0] = True
                    if (AESD.decrypt(clientAuth) == authToken):
                        authed = True
                global do
                do = b'o'
                threading.Thread(target=misc).start()
                multiprocessing.Process(target=dataReciever).start()
                time.sleep(.1)
                threading.Thread(target=one).start()
                threading.Thread(target=dsp).start()
                time.sleep(.1)
                threading.Thread(target=ctrl.__init__).start()
                while not (reset[0]):
                    time.sleep(0.01)
                s1.shutdown(socket.SHUT_RDWR)
                startOrRestart()
            except:
                startOrRestart()
        else:
            appRunning[0] = False
            startOrRestart()
    else:
        quit()

def fullClose(sender, data):
    global coreRunning
    global appRunning
    global reset
    global s1
    global c1
    global c2
    global c3
    try:
        s1.shutdown(socket.SHUT_RDWR)
        del s1
        del c1
        del c2
        del c3
    except:
        pass
    stop_dearpygui()
    coreRunning = False
    appRunning[0] = False
    reset[0] = True

def savePSWD(sender, data):
    global password
    password = get_value('##pswdInput').encode("utf-8")
    fileIO = open("pswd.txt", "wb")
    fileIO.write(password)
    fileIO.close()

def GUISys():
    global password
    global coreRunning
    try:
        fileIO = open("temp.txt", "r")
        fileData = fileIO.read()
        fileIO.close()
        fileData = fileData.split("\n")
        fileIO = open("temp.txt", "w")
        fileIO.write(fileData[0] + "\n" + "t")
        fileIO.close()
    except:
        threading.Thread(target=startOrRestart).start()
        fileIO = open("temp.txt", "w")
        fileIO.write(str(os.getpid()) + "\n" + "t")
        fileIO.close()
        fileIO = open("temp.txt", "r")
        fileData = fileIO.read()
        fileIO.close()
        fileData = fileData.split("\n")
        while coreRunning:
            fileIO = open("temp.txt", "r")
            fileData = fileIO.read()
            fileIO.close()
            fileData = fileData.split("\n")
            while (fileData[1] == "f") and (coreRunning):
                time.sleep(1)
                fileIO = open("temp.txt", "r")
                fileData = fileIO.read()
                fileIO.close()
                fileData = fileData.split("\n")

            set_vsync(True)
            set_main_window_title("PyConnect (Host)")
            set_theme("Gold")
            set_style_window_padding(0, 0)
            set_style_window_border_size(0.0)
            with window("##base"):
                add_text("##pswdLabel", default_value="Password:")
                add_same_line()
                while coreRunning:
                    try:
                        add_input_text("##pswdInput", password=True, callback=savePSWD, default_value=password.decode())
                        break
                    except:
                        time.sleep(0.004)
                add_button("Save", )
                add_same_line()
                add_button("Exit", tip="Click to fully exit PyConnect Host. Otherwise, close the GUI to run in the background.", callback=fullClose)
            start_dearpygui(primary_window="##base")
            fileIO = open("temp.txt", "w")
            fileIO.write(str(os.getpid()) + "\n" + "f")
            fileIO.close()

GUISys()
if not coreRunning:
    os.remove("temp.txt")
