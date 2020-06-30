import pynput
import io
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller
import fs
import sys
import time
import pyscreenshot as ImageGrab
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging

mem = fs.open_fs('mem://')

# Thanks Giampaolo Rodolà of stackoverflow.com
# from pyftpdlib.log import config_logging
# config_logging(level=logging.ERROR)

print('Enter IP address or Hostname this device should use.')
ip = input()

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

# From pyftpdlib documentation with minor changes
# Instantiate a dummy authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

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
server.max_cons_per_ip = 1

online = True
gtg = False
telller1File = mem.open('teller_h.txt', 'rw')
recievedTellerFile = mem.open("recvedTeller.txt", 'rw')
recievedTellerFile.write('1')
telller1File.close()
recievedTellerFile.close()

def Bye():
    global online
    while online:
        try:
            # Session status checker
            if splited[0] == '1':
                print('Closing input thread')
                online = False
                gtg = False
                os.system('sudo umount Temp')

        except:
            pass

def FTP_Start():
    server.serve_forever()

def Output():
    global online
    global splited
    while online:
        recievedTellerFile = mem.open("recvedTeller.txt", 'rw')

        if str(recievedTellerFile.read()) == "1":
            recievedTellerFile.write('0')
            image = ImageGrab.grab()
            image.mem.save("image.jpg")
            teller1 = '1'
            telller1File = mem.open('Temp/teller_h.txt', 'rw')
            telller1File.write('1')
            telller1File.close()

        recievedTellerFile.close()

def Input():
    global online
    global splited
    global gtg
    while online:
        while gtg:

            # Mouse handlers
            def mousectl():
                global online
                global gtg
                try:
                    mosx = int(splited[1])
                    mosy = int(splited[2])
                    mouse.position(mosx, mosy)
                    if splited[3] == "1":
                        mouse.press(Button.left)
                    else:
                        mouse.release(Button.left)
                    if splited[4] == "1":
                        mouse.press(Button.right)
                    else:
                        mouse.release(Button.right)

                except:
                    pass

            mousectl()

def kb_top0():
    global gtg
    global splited
    time.sleep(.01)
    while online:
        while gtg:
            try:
                while splited[5] == "1":
                    keyboard.type('0')
                    time.sleep(.05)

            except:
                pass

# Define threads
Bye_thread = threading.Thread(target=Bye)
output_thread = threading.Thread(target=Output)
input_thread = threading.Thread(target=Input)
kb_top0_thread = threading.Thread(target=kb_top0)
FTP_Start_thread = threading.Thread(target=FTP_Start)
output_thread.start()
FTP_Start_thread.start()
# Bye_thread.start()
quit()
