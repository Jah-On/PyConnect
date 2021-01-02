version = b'a1.0'

try:
    import urllib.request
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    if (urllib.request.urlopen("https://raw.githubusercontent.com/Jah-On/PyConnect/master/version").read()[0:4] != version):
        newFile = open("client.py", "wb")
        newFile.write(urllib.request.urlopen("https://raw.githubusercontent.com/Jah-On/PyConnect/master/client.py").read())
        newFile.close()
        import subprocess
        proc = subprocess.Popen(["python client.py"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        exit = True
    else:
        exit = False
except:
    exit = False

if (exit):
    quit()

from dearpygui.core import *
from dearpygui.simple import *
import cv2
import socket
import threading
import multiprocessing
from ctypes import c_bool, c_char
import time
import numpy as np
import blosc
import math
import os
import sys
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto import Random

workingDir = os.getcwd()

try:
    file = open(workingDir + "/connections.list", "r")
    file.read()
    file.close()
except:
    file = open(workingDir + "/connections.list", "w")
    file.close()

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

keyMap = {mvKey_0:b'\x30',mvKey_1:b'\x31',mvKey_2:b'\x32',mvKey_3:b'\x33',mvKey_4:b'\x34',mvKey_5:b'\x35',mvKey_6:b'\x36',mvKey_7:b'\x37',mvKey_8:b'\x38',mvKey_9:b'\x39',mvKey_A:b'\x31\x30',mvKey_B:b'\x31\x31',mvKey_C:b'\x31\x32',mvKey_D:b'\x31\x33',mvKey_E:b'\x31\x34',mvKey_F:b'\x31\x35',mvKey_G:b'\x31\x36',mvKey_H:b'\x31\x37',mvKey_I:b'\x31\x38',mvKey_J:b'\x31\x39',mvKey_K:b'\x32\x30',mvKey_L:b'\x32\x31',mvKey_M:b'\x32\x32',mvKey_N:b'\x32\x33',mvKey_O:b'\x32\x34',mvKey_P:b'\x32\x35',mvKey_Q:b'\x32\x36',mvKey_R:b'\x32\x37',mvKey_S:b'\x32\x38',mvKey_T:b'\x32\x39',mvKey_U:b'\x33\x30',mvKey_V:b'\x33\x31',mvKey_W:b'\x33\x32',mvKey_X:b'\x33\x33',mvKey_Y:b'\x33\x34',mvKey_Z:b'\x33\x35',mvKey_Back:b'\x33\x36',mvKey_Tab:b'\x33\x37',mvKey_Clear:b'\x33\x38',mvKey_Return:b'\x33\x39',mvKey_Shift:b'\x34\x30',mvKey_Control:b'\x34\x31',mvKey_Alt:b'\x34\x32',mvKey_Pause:b'\x34\x33',mvKey_Capital:b'\x34\x34',mvKey_Escape:b'\x34\x35',mvKey_Spacebar:b'\x34\x36',mvKey_Prior:b'\x34\x37',mvKey_Next:b'\x34\x38',mvKey_End:b'\x34\x39',mvKey_Home:b'\x35\x30',mvKey_Left:b'\x35\x31',mvKey_Up:b'\x35\x32',mvKey_Right:b'\x35\x33',mvKey_Down:b'\x35\x34',mvKey_Select:b'\x35\x35',mvKey_Print:b'\x35\x36',mvKey_Execute:b'\x35\x37',mvKey_PrintScreen:b'\x35\x38',mvKey_Insert:b'\x35\x39',mvKey_Delete:b'\x36\x30',mvKey_Help:b'\x36\x31',mvKey_LWin:b'\x36\x32',mvKey_RWin:b'\x36\x33',mvKey_Apps:b'\x36\x34',mvKey_Sleep:b'\x36\x35',mvKey_NumPad0:b'\x36\x36',mvKey_NumPad1:b'\x36\x37',mvKey_NumPad2:b'\x36\x38',mvKey_NumPad3:b'\x36\x39',mvKey_NumPad4:b'\x37\x30',mvKey_NumPad5:b'\x37\x31',mvKey_NumPad6:b'\x37\x32',mvKey_NumPad7:b'\x37\x33',mvKey_NumPad8:b'\x37\x34',mvKey_NumPad9:b'\x37\x35',mvKey_Multiply:b'\x37\x36',mvKey_Add:b'\x37\x37',mvKey_Separator:b'\x37\x38',mvKey_Subtract:b'\x37\x39',mvKey_Decimal:b'\x38\x30',mvKey_Divide:b'\x38\x31',mvKey_F1:b'\x38\x32',mvKey_F2:b'\x38\x33',mvKey_F3:b'\x38\x34',mvKey_F4:b'\x38\x35',mvKey_F5:b'\x38\x36',mvKey_F6:b'\x38\x37',mvKey_F7:b'\x38\x38',mvKey_F8:b'\x38\x39',mvKey_F9:b'\x39\x30',mvKey_F10:b'\x39\x31',mvKey_F11:b'\x39\x32',mvKey_F12:b'\x39\x33',mvKey_F13:b'\x39\x34',mvKey_F14:b'\x39\x35',mvKey_F15:b'\x39\x36',mvKey_F16:b'\x39\x37',mvKey_F17:b'\x39\x38',mvKey_F18:b'\x39\x39',mvKey_F19:b'\x31\x30\x30',mvKey_F20:b'\x31\x30\x31',mvKey_F21:b'\x31\x30\x32',mvKey_F22:b'\x31\x30\x33',mvKey_F23:b'\x31\x30\x34',mvKey_F24:b'\x31\x30\x35',mvKey_NumLock:b'\x31\x30\x36',mvKey_ScrollLock:b'\x31\x30\x37',mvKey_LShift:b'\x31\x30\x38',mvKey_RShift:b'\x31\x30\x39',mvKey_LControl:b'\x31\x31\x30',mvKey_RControl:b'\x31\x31\x31',mvKey_LMenu:b'\x31\x31\x32',mvKey_RMenu:b'\x31\x31\x33',mvKey_Browser_Back:b'\x31\x31\x34',mvKey_Browser_Forward:b'\x31\x31\x35',mvKey_Browser_Refresh:b'\x31\x31\x36',mvKey_Browser_Stop:b'\x31\x31\x37',mvKey_Browser_Search:b'\x31\x31\x38',mvKey_Browser_Favorites:b'\x31\x31\x39',mvKey_Browser_Home:b'\x31\x32\x30',mvKey_Volume_Mute:b'\x31\x32\x31',mvKey_Volume_Down:b'\x31\x32\x32',mvKey_Volume_Up:b'\x31\x32\x33',mvKey_Media_Next_Track:b'\x31\x32\x34',mvKey_Media_Prev_Track:b'\x31\x32\x35',mvKey_Media_Stop:b'\x31\x32\x36',mvKey_Media_Play_Pause:b'\x31\x32\x37',mvKey_Launch_Mail:b'\x31\x32\x38',mvKey_Launch_Media_Select:b'\x31\x32\x39',mvKey_Launch_App1:b'\x31\x33\x30',mvKey_Launch_App2:b'\x31\x33\x31',mvKey_Colon:b'\x31\x33\x32',mvKey_Plus:b'\x31\x33\x33',mvKey_Comma:b'\x31\x33\x34',mvKey_Minus:b'\x31\x33\x35',mvKey_Period:b'\x31\x33\x36',mvKey_Slash:b'\x31\x33\x37',mvKey_Tilde:b'\x31\x33\x38',mvKey_Open_Brace:b'\x31\x33\x39',mvKey_Backslash:b'\x31\x34\x30',mvKey_Close_Brace:b'\x31\x34\x31',mvKey_Quote:b'\x31\x34\x32'}

set_main_window_title("PyConnect (Client)")
set_theme("Gold")

def misc():
    global hostOS
    global hostWidth
    global hostHeight
    while state[0]:
        data = s3.recv(32)
        while (data == b'') and state[0]:
            time.sleep(0.01)
            data = s3.recv(32)
        if (data[0:1] == b'o'):
            hostOS = data[1:2].decode('utf-8')
        if (data[0:1] == b'd'):
            hostDisplay = data[1:].split(b':')
            hostWidth, hostHeight = int(hostDisplay[0]), int(hostDisplay[1])
            s3.send((str(get_main_window_size()[0]) + ":" + str(get_main_window_size()[1])).encode("utf-8"))

def dataSender():
    global s1
    while state[0]:
        try:
            controlData = bytes(str(mouse[0]), "utf-8") + b'\xe2\x96\xac' + bytes(str(mouse[1]), "utf-8") + b'\xe2\x96\xac' + bytes(str(mouse[2]), "utf-8") + bytes(str(mouse[3]), "utf-8") + bytes(str(mouse[4]), "utf-8") + b'\xe2\x96\xac' + bytes(str(mouse[5]), "utf-8") + b'\xe2\x96\xac' + keyboardString[:][0:keyboardStringLength[0]] + b'\xe2\x96\xac'
            while ((len(s1.recv(1)) == 0) and state[0]):
                time.sleep(0.001)
            alive[0] = True
            s1.send(AESC.encrypt(controlData))
            time.sleep(.001)
        except:
            pass

def keyboardByteConstruct():
    global keyboardString
    while state[0]:
        localByteString = b''
        localKeyboard = keyboard
        if (len(localKeyboard) != 0):
            for i in range(0, len(localKeyboard)):
                localByteString += localKeyboard[i] + b'\xe2\x96\xad'
        keyboardStringLength[0] = len(localByteString)
        for i in range(len(localByteString), 100):
            localByteString += b'\x30'
        keyboardString[:] = localByteString
        time.sleep(0.0005)

def keyDown(sender, data):
    global keyboard
    try:
        if (keyMap[data[0]] not in keyboard):
            keyboard.append(keyMap[data[0]])
    except:
        pass

def keyUp(sender, data):
    global keyboard
    try:
        keyboard.remove(keyMap[data])
    except:
        pass

def remoteDisplayRuntime(sender, data):
    global images
    global error
    if reset:
        try:
            s1.shutdown(socket.SHUT_RDWR)
            s2.shutdown(socket.SHUT_RDWR)
            s3.shutdown(socket.SHUT_RDWR)
        except:
            pass
        state[0] = False
        error = "Connection timed out or disconnected."
        GUI.remoteScreenDelete(None, None)
        GUI.connectionError(None, None)
    if (len(images) != 0):
        add_texture("#sctTexture", images[0], get_main_window_size()[0], get_main_window_size()[1], format=mvTEX_RGB_INT)
        draw_image("canvas", "#sctTexture", [0,0], pmax=[get_main_window_size()[0], get_main_window_size()[1]])
        del images[0]

def mousePosition(sender, data):
    global mouse
    if not (((data[0] < 0) or (data[1] < 0)) or ((data[0] > get_main_window_size()[0]) or (data[1] > get_main_window_size()[1]))):
        mouse[0], mouse[1] = [int(data[0] * ((hostWidth)/(get_main_window_size()[0]))), int(data[1] * ((hostHeight)/(get_main_window_size()[1])))]

def mousePress(sender, data):
    global mouse
    if (data[0] == 0):
        mouse[2] = 1
    if (data[0] == 1):
        mouse[3] = 1
    if (data[0] == 2):
        mouse[4] = 1

def mouseRelease(sender, data):
    global mouse
    if (data == 0):
        mouse[2] = 0
    if (data == 1):
        mouse[3] = 0
    if (data == 2):
        mouse[4] = 0

def mouseWheelMotion(sender, data):
    global mouse
    global mouseWheelMoving
    mouseWheelMoving = True
    mouse[5] = data

def mouseWheelNoMotion():
    global mouse
    global mouseWheelMoving
    while state[0]:
        if not mouseWheelMoving:
            mouse[5] = 0
        mouseWheelMoving = False
        time.sleep(0.004)

def imageHandler():
    global lbl
    global images
    global imageLength
    global state
    global alive
    while state[0]:
        try:
            while (len(images) == 1) and state[0]:
                time.sleep(0.0005)
            imageLength = s2.recv(16)
            while (len(imageLength) < 1) and state[0]:
                time.sleep(0.0005)
                imageLength = s2.recv(16)
            alive[0] = True
            imageLength = int(imageLength.decode('utf-8'))
            s2.send(b'\x30')
            imageBuffer = b''
            while not (len(imageBuffer) == imageLength) and state[0]:
                recved = s2.recv(500000)
                imageBuffer += recved
            alive[0] = True
            try:
                decryptedImageBuffer = AESD.decrypt(imageBuffer)
                decomp = blosc.decompress(decryptedImageBuffer)
                if ((hostWidth * hostHeight) >= (get_main_window_size()[0] * get_main_window_size()[1])):
                    temp = np.frombuffer(decomp, dtype="uint8")
                    images.append(temp)
                else:
                    decomp = np.frombuffer(decomp, dtype="uint8")
                    decomp = decomp.reshape(hostHeight, hostWidth, 3)
                    decomp = cv2.resize(decomp, (get_main_window_size()[0], get_main_window_size()[1]), interpolation=cv2.INTER_LINEAR)
                    images.append(decomp.reshape(-1))
            except:
                pass
            s2.send(b'\x31')
        except:
            print("oop")

def timeoutManager():
    global alive
    global reset
    while state[0]:
        alive[0] = False
        time.sleep(3)
        if not alive[0] and state[0]:
            print("break!")
            reset = True
            break

class GUI:
    screen = ""
    previousConnectionButtons = []
    previousConnectionButtonsSameLine = []
    def addPreviousConnection(sender, data):
        if (get_value("##save")) and (hostOS != None):
            if (data[1] == ""):
                data = (data[0], "__blank__")
            addString = data[0] + "\n" + get_value("##name") + "\n" + hostOS + "\n" + data[1] + "\n\n\n\n"
            listFileObj = open(workingDir + "/connections.list", "a")
            listFileObj.write(addString)
            listFileObj.close()

    def deletePreviousConnection(sender, data):
        delete_item("buttonRightClick")
        delete_item(GUI.previousConnectionButtons[data])
        del GUI.previousConnectionButtons[data]
        listFileObj = open(workingDir + "/connections.list", "r")
        listFile = listFileObj.read().split("\n\n")
        listFileObj.close()
        listOfListData = []
        for i in range(len(listFile)):
            if (listFile[i] != ""):
                subData = listFile[i].split("\n")
                while "" in subData:
                    subData.remove("")
                listOfListData.append(subData)
        finalString = ""
        for section in range(len(listOfListData)):
            if (section != data):
                for y in range(len(listOfListData[section])):
                    if (y != (len(listOfListData[section]) - 1)):
                        finalString += listOfListData[section][y] + "\n"
                    else:
                         finalString += listOfListData[section][y]
                if (len(listOfListData) == 0) or (len(listOfListData[len(listOfListData) - 1]) == 0):
                    pass
                else:
                    finalString += "\n\n\n\n"
        listFileObj = open(workingDir + "/connections.list", "w")
        listFileObj.write(finalString)
        listFileObj.close()

    def editPreviousConnection(sender, data):
        listFileObj = open(workingDir + "/connections.list", "r")
        listFile = listFileObj.read().split("\n\n")
        listFileObj.close()
        listOfListData = []
        for i in range(len(listFile)):
            if (listFile[i] != ""):
                subData = listFile[i].split("\n")
                while "" in subData:
                    subData.remove("")
                listOfListData.append(subData)
        finalString = ""
        listOfListData[data][0], listOfListData[data][1], listOfListData[data][3] = get_value("##editIPH"), get_value("##editName"), get_value("##editPassword")
        if (listOfListData[data][2] == ""):
            listOfListData[data][2] = "__blank__"
        for section in range(len(listOfListData)):
            for y in range(len(listOfListData[section])):
                if (y != (len(listOfListData[section]) - 1)):
                    finalString += listOfListData[section][y] + "\n"
                else:
                     finalString += listOfListData[section][y]
            if (len(listOfListData[len(listOfListData) - 1]) == 0):
                pass
            else:
                finalString += "\n\n\n\n"
        listFileObj = open(workingDir + "/connections.list", "w")
        listFileObj.write(finalString)
        listFileObj.close()
        GUI.previousConnectionButtons.clear()
        set_render_callback(None)
        delete_item("##noClick")
        delete_item("##editConnectionPopup")
        GUI.mainScreenDelete(None, None, True)

    def closeEditPreviousConnectionPopup(sender, data):
        delete_item("##noClick")
        delete_item("##editConnectionPopup")

    def editPreviousConnectionPopup(sender, data):
        add_window("##noClick", no_close=True, no_collapse=True, no_title_bar=True, no_background=True, no_move=True, x_pos=0, y_pos=0, no_bring_to_front_on_focus=False, width=get_main_window_size()[0], height=get_main_window_size()[1])
        add_window("##editConnectionPopup", show=True, no_close=True, no_collapse=True, no_title_bar=True, autosize=True)
        listFileObj = open(workingDir + "/connections.list", "r")
        listFile = listFileObj.read().split("\n\n\n")
        for i in range(len(listFile)):
            if (i == data):
                if ((listFile[i] != "") and (listFile[i] != "\n")):
                    subData = listFile[i].split("\n")
                    while "" in subData:
                        subData.remove("")
        listFileObj.close()
        add_input_text("##editName", default_value=subData[1], parent="##editConnectionPopup")
        add_input_text("##editIPH", default_value=subData[0], parent="##editConnectionPopup")
        if (subData[3] == "__blank__"):
            add_input_text("##editPassword", default_value="", parent="##editConnectionPopup", password=True)
        else:
            add_input_text("##editPassword", default_value=subData[3], parent="##editConnectionPopup", password=True)
        add_button("Save", callback=GUI.editPreviousConnection, callback_data=data, parent="##editConnectionPopup")
        add_same_line(parent="##editConnectionPopup")
        add_button("Close", callback=GUI.closeEditPreviousConnectionPopup, parent="##editConnectionPopup")
        end()

    def prevListRightClick(sender, data):
        if (not (is_item_hovered("buttonRightClick")) and not (is_item_hovered("##previousConnectionDelete")) and not (is_item_hovered("##previousConnectionEdit")) and (is_mouse_button_clicked(mvMouseButton_Right) or is_mouse_button_clicked(mvMouseButton_Left) or is_mouse_button_clicked(mvMouseButton_Middle)) and does_item_exist("buttonRightClick")):
            delete_item("buttonRightClick")
        for i in range(len(GUI.previousConnectionButtons)):
            if (is_item_hovered(GUI.previousConnectionButtons[i]) and is_mouse_button_clicked(mvMouseButton_Right)):
                add_popup(GUI.previousConnectionButtons[i], "buttonRightClick")
                add_button("##previousConnectionEdit", parent="buttonRightClick", label="Edit", callback=GUI.editPreviousConnectionPopup, callback_data=i)
                add_button("##previousConnectionDelete", parent="buttonRightClick", label="Delete", callback=GUI.deletePreviousConnection, callback_data=i)
                end()

    def saveCheckboxClick(sender, data):
        configure_item("##name", show=get_value("##save"))
        configure_item("##nameIputSameLine", show=get_value("##save"))

    def mainScreenResize(sender, data):
        global justStarted
        if does_item_exist("##quickConnect") and not does_item_exist("##previousConnections"):
            set_render_callback(None)
            GUI.mainScreenDelete(None, None, True)

    def mainScreen(sender, data):
        global s1
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global s2
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global s3
        s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global AESKey
        AESKey = Random.new().read(AES.block_size)
        global AESIV
        AESIV = Random.new().read(AES.block_size)
        global AESC
        AESC = AES.new(AESKey, AES.MODE_CFB, AESIV)
        global AESD
        AESD = AES.new(AESKey, AES.MODE_CFB, AESIV)
        global error
        error = ""
        global images
        images = []
        global hostOS
        hostOS = None
        global state
        state = multiprocessing.Array(c_bool, 1)
        state[0] = True
        global reset
        reset = False
        global alive
        alive = multiprocessing.Array(c_bool, 1)
        alive[0] = False
        global mouse
        mouse = multiprocessing.Array("i", 6)
        global mouseWheelMoving
        mouseWheelMoving = False
        global keyboard
        keyboard = []
        global keysDown
        keysDown = []
        global keyboardString
        keyboardString = multiprocessing.Array(c_char, 100)
        global keyboardStringLength
        keyboardStringLength = multiprocessing.Array("i", 1)
        set_vsync(True)
        set_style_window_border_size(0.0)
        set_style_window_padding(0, 0)
        add_group("##quickConnect", parent="##base")
        add_text("IP or Hostname")
        add_same_line()
        add_input_text("##iphInput")

        add_text("Password      ")
        add_same_line()
        add_input_text("##pswdInput", password=True)

        add_button("Connect", callback=GUI.connect, callback_data=(get_value("##iphInput"), get_value("##pswdInput")))
        add_same_line()
        add_checkbox("##save", label="Save", callback=GUI.saveCheckboxClick)
        add_same_line(name="##nameIputSameLine", show=False)
        add_input_text("##name", default_value="Name...", show=False)
        end()

        add_group("##previousConnections", parent="##base")
        add_spacing()
        try:
            fileIO = open(workingDir + "/connections.list", "r+")
            listFile = fileIO.read().split("\n\n\n")
            fileIO.close()
            set_render_callback(GUI.prevListRightClick)
        except:
            listFile = []
        count = 0
        position = 1
        buttonSize = round(((get_main_window_size()[0]/8) + (get_main_window_size()[1]/4.5))/2)
        for i in range(len(listFile)):
            if ((listFile[i] != "") and (listFile[i] != "\n")):
                subData = listFile[i].split("\n")
                while "" in subData:
                    subData.remove("")
                if ((position + (buttonSize * 1.05)) >= (get_main_window_size()[0] - buttonSize)) or (i == 0):
                    position = 1
                    add_dummy(height=5, parent="##previousConnections")
                else:
                    add_same_line(name="pCSL" + str(count), parent="##previousConnections")
                    position += (buttonSize * 1.05)
                    count += 1

                if (subData[2] == "l"):
                    add_image_button("##prev" + str(i), "l.png", tip="Name: " + subData[1] +  "\nAddress: "+ subData[0], width=buttonSize, height=buttonSize, parent="##previousConnections", callback=GUI.connect, callback_data=(subData[0], subData[3]))
                elif (subData[2] == "d"):
                    add_image_button("##prev" + str(i), "a.png", tip="Name: " + subData[1] +  "\nAddress: "+ subData[0], width=buttonSize, height=buttonSize, parent="##previousConnections", callback=GUI.connect, callback_data=(subData[0], subData[3]))
                else:
                    add_image_button("##prev" + str(i), "w.png", tip="Name: " + subData[1] +  "\nAddress: "+ subData[0], width=buttonSize, height=buttonSize, parent="##previousConnections", callback=GUI.connect, callback_data=(subData[0], subData[3]))
                GUI.previousConnectionButtons.append("##prev" + str(i))
        end()
        set_resize_callback(GUI.mainScreenResize)

    def mainScreenDelete(sender, data, include):
        delete_item("##quickConnect")
        delete_item("##previousConnections")
        if does_item_exist("buttonRightClick"):
            delete_item("buttonRightClick")
        GUI.previousConnectionButtons.clear()
        if include:
            GUI.mainScreen(None, None)

    def connectionError(sender, data):
        add_group("##connectionError", parent="##base")
        add_text(error)
        add_same_line()
        add_button("OK", callback=GUI.connectionErrorDelete)
        end()

    def connectionErrorDelete(sender, data):
        delete_item("##connectionError")
        GUI.mainScreen(None, None)

    def canvasRescale(sender, data):
        windowSize = get_main_window_size()
        configure_item("canvas", width=windowSize[0])
        configure_item("canvas", height=windowSize[1])

    def remoteScreen(sender, data):
        windowSize = get_main_window_size()
        add_drawing("canvas", width=windowSize[0], height=windowSize[1], parent="##base")

    def remoteScreenDelete(sender, data):
        delete_item("canvas")
        set_render_callback(None)
        set_resize_callback(None)

    def connect(sender, data):
        global error
        global s1
        global alive
        if (data[0] == ''):
            iph = get_value("##iphInput")
            password = get_value("##pswdInput")
            data = (iph, password)
        else:
            iph, password = data
        passwordEncoded = password.encode("utf-8")
        state[0] = True
        try:
            threading.Thread(target=timeoutManager).start()
            s1.connect((iph, 1234))
            alive[0] = True
            connected = True
        except:
            connected = False
        if (connected):
            global publicKey
            publicKey = s1.recv(2048)
            while (len(publicKey) < 1) and state[0]:
                publicKey = s1.recv(2048)
            alive[0] = True
            global RSACipheror
            RSACipheror = PKCS1_OAEP.new(key=RSA.import_key(publicKey))
            s1.sendall(RSACipheror.encrypt(AESKey))
            while (len(s1.recv(1)) < 1) and state[0]:
                time.sleep(0.0005)
            alive[0] = True
            s1.sendall(RSACipheror.encrypt(AESIV))
            while (len(s1.recv(1)) < 1) and state[0]:
                time.sleep(0.0005)
            alive[0] = True
            s1.sendall(version)
            matchingVersion = s1.recv(1)
            while (len(matchingVersion) < 1)  and state[0]:
                matchingVersion = s1.recv(1)
                time.sleep(0.0005)
            alive[0] = True
            if (matchingVersion == b'y'):
                if ((passwordEncoded == b'') or (passwordEncoded == b'__blank__')):
                    passwordEncoded = b'+=Null=+'
                s1.sendall(AESC.encrypt(passwordEncoded))
                passwordMessage = s1.recv(4)
                while (len(passwordMessage) < 4) and state[0]:
                    passwordMessage = s1.recv(4)
                    time.sleep(0.001)
                alive[0] = True
                if (passwordMessage == b'pass'):
                    s1.send(b'\x30')
                    hostResolution = s1.recv(32)
                    while (len(hostResolution) < 1) and state[0]:
                        hostResolution = s1.recv(32)
                        time.sleep(0.001)
                    alive[0] = True
                    hostResolution = hostResolution.split(b':')
                    global hostWidth, hostHeight
                    hostWidth, hostHeight = int(hostResolution[0]), int(hostResolution[1])
                    s1.send((str(get_main_window_size()[0]) + ":" + str(get_main_window_size()[1])).encode("utf-8"))
                    authTokenData = s1.recv(512)
                    while (len(authTokenData) < 1) and state[0]:
                        authTokenData = s1.recv(512)
                        time.sleep(0.0005)
                    alive[0] = True
                    global authToken
                    authToken = AESD.decrypt(authTokenData)
                    while state[0]:
                        try:
                            s2.connect((iph, 1234))
                            break
                        except:
                            pass
                    s2.send(AESC.encrypt(authToken))
                    alive[0] = True
                    while state[0]:
                        try:
                            s3.connect((iph, 1234))
                            break
                        except:
                            pass
                    s3.send(AESC.encrypt(authToken))
                    alive[0] = True
                    threading.Thread(target=misc).start()
                    GUI.mainScreenDelete(None, None, False)
                    GUI.remoteScreen(None, None)
                    set_resize_callback(GUI.canvasRescale)
                    set_render_callback(remoteDisplayRuntime)
                    set_key_down_callback(keyDown)
                    set_key_release_callback(keyUp)
                    set_mouse_move_callback(mousePosition)
                    set_mouse_down_callback(mousePress)
                    set_mouse_release_callback(mouseRelease)
                    threading.Thread(target=mouseWheelNoMotion).start()
                    set_mouse_wheel_callback(mouseWheelMotion)
                    threading.Thread(target=imageHandler).start()
                    threading.Thread(target=keyboardByteConstruct).start()
                    time.sleep(0.1)
                    multiprocessing.Process(target=dataSender).start()
                    GUI.addPreviousConnection(None, data)
                else:
                    s1.close()
                    state[0] = False
                    del s1
                    error = "Incorrect password"
                    GUI.mainScreenDelete(None, None, False)
                    GUI.connectionError(None, None)
            else:
                s1.close()
                state[0] = False
                del s1
                error = "Incompatible version."
                GUI.mainScreenDelete(None, None, False)
                GUI.connectionError(None, None)
        else:
            state[0] = False
            error = "Invalid address or hostname, unreachable, or PyConnect host is not running."
            GUI.mainScreenDelete(None, None, False)
            GUI.connectionError(None, None)

with window("##base"):
    GUI.mainScreen(None, None)

if __name__ == "__main__":
    start_dearpygui(primary_window="##base")
    state[0] = False
    time.sleep(.1)
    try:
        s1.shutdown(socket.SHUT_RDWR)
        s2.shutdown(socket.SHUT_RDWR)
        s3.shutdown(socket.SHUT_RDWR)
    except:
        pass
