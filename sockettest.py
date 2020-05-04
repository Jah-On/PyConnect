import socket
import pynput
from io import BytesIO
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller
import os
import time
import pyscreenshot as ImageGrab



mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.2.14", 1234))
print("server started")
s.listen(1)
print("listening")

connection, addr = s.accept()

while True:
    # buffer = BytesIO()
    # im = ImageGrab.grab()
    # connection.send(im.encode("uft-8"))
    # Data handlers
    get = connection.recv(1500)
    get_decoded = get.decode("utf-8")
    splited = get_decoded.split(":", 50)

    # Session status checker
    if splited[0] == "1":
        quit()

    # Mouse handlers
    posx = float(splited[1])
    posy = float(splited[2])
    mouse.position = (posx, posy)
    if splited[3] == "1":
        mouse.press(Button.left)
    else:
        mouse.release(Button.left)
    if splited[4] == "1":
        mouse.press(Button.right)
    else:
        mouse.release(Button.right)

    # Keyboard handlers
    if splited[5] == "1":
        keyboard.press('0')
    else:
        keyboard.release("0")
    if splited[6] == "1":
        keyboard.press('1')
    else:
        keyboard.release('0')
    if splited[7] == "1":
        keyboard.type('2')
    if splited[8] == "1":
        keyboard.type('3')
    if splited[9] == "1":
        keyboard.type('4')
    if splited[10] == "1":
        keyboard.type('5')
    if splited[11] == "1":
        keyboard.type('6')
    if splited[12] == "1":
        keyboard.type('7')
    if splited[13] == "1":
        keyboard.type('8')
    if splited[14] == "1":
        keyboard.type('9')
