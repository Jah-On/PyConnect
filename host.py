import socket
import pynput
import io
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller
import os
import sys
import time
import pyscreenshot as ImageGrab
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

os.system("mkdir Temp")
os.system("sudo mount -t tmpfs -o rw,size=50M tmpfs Temp")

print('Enter IP address or Hostname this device should use.')
ip = input()

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

# From pyftpdlib documentation with minor changes
# Instantiate a dummy authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

# Define a new user having full r/w permissions and a read-only
# anonymous user
authorizer.add_user('user', '12345', 'Temp', perm='elradfmwMT')

# Instantiate FTP handler class
handler = FTPHandler
handler.authorizer = authorizer

# Specify a masquerade address and the range of ports to use for
# passive connections.  Decomment in case you're behind a NAT.
#handler.masquerade_address = '151.25.42.11'
#handler.passive_ports = range(60000, 65535)

# Instantiate FTP server class and listen on 0.0.0.0:2121
address = (str(ip), 1234)
server = FTPServer(address, handler)

# set a limit for connections
server.max_cons = 2
server.max_cons_per_ip = 2


s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((str(ip), 1235))
s2.listen(1)

connection2, addr2 = s2.accept()

def Output():
    global online
    global splited
    online = True
    while online:
        image = ImageGrab.grab()
        image.save("Temp/image.jpg")
        teller = '1'
        connection2.send(teller.encode('utf-8'))
        time.sleep(.0166)
        if splited[0] == '1':
            server.close_all()
            os.system('sudo umount Temp')
            break

def Input():
    global online
    global splited
    while online:
        # Data handlers
        get = connection2.recv(1500)
        get_decoded = get.decode("utf-8")
        splited = get_decoded.split(":", 50)

        # Session status checker
        if splited[0] == '1':
            print('Closing input thread')
            server.close_all()
            break

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
            keyboard.release('1')
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


# Define threads
output_thread = threading.Thread(target=Output)
input_thread = threading.Thread(target=Input)
output_thread.start()
input_thread.start()
server.serve_forever()
