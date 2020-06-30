import pygame
import time
import sys
import fs
import threading
from ftplib import FTP
import io
from io import BytesIO
from io import StringIO

mem = fs.open_fs('mem://')
pygame.init()
dsp = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption('PyConnect ')
ip = str(input())
surface = pygame.Surface((255,255))
server = FTP()
server.connect(ip, 1234)
server.login('', '')

def Input():
    global stayOpen
    global Img2Gen
    stayOpen = True
    x = 1
    while stayOpen:
        teller = mem.open('teller.txt', 'rw')
        image = mem.open('image.jpg', 'rw')
        rcvd = mem.open('rcvd.txt', 'rw')
        server.retrbinary('RETR teller_h.txt', teller.write())
        tellerData = teller.read()
        if (tellerData == bytes('1', 'utf8')):
            teller.write('0')
            server.storbinary('STOR teller_h.txt', teller)
            server.retrbinary('RETR image.jpg', image.write())
            binary_image = image.read()
            image = pygame.image.frombuffer(binary_image, (1920,1080), 'RGB')
            dsp.blit(image, (0,0))
            pygame.display.flip()
            rcvd.write('1')
            server.storbinary('STOR recvedTeller.txt', rcvd)

def Output():
    global stayOpen
    global close_session
    global dspfullscreen
    dspfullscreen = 0
    close_session = "0"
    while stayOpen:
        try:
            time.sleep(.001)
            # Mouse data control
            mousepos = pygame.mouse.get_pos()
            mouseposx = str(mousepos[0])
            mouseposy = str(mousepos[1])
            if pygame.mouse.get_pressed()[0]:
                mousebutton1 = "1"
            else:
                mousebutton1 = "0"

            if pygame.mouse.get_pressed()[2]:
                mousebutton3 = "1"
            else:
                mousebutton3 = "0"

            # Keyboard data control
            getkeys = pygame.key.get_pressed()
            if getkeys[pygame.K_0]:
                kb_0 = "1"
            else:
                kb_0 = "0"
            if getkeys[pygame.K_1]:
                kb_1 = "1"
            else:
                kb_1 = "0"
            if getkeys[pygame.K_2]:
                kb_2 = "1"
            else:
                kb_2 = "0"
            if getkeys[pygame.K_3]:
                kb_3 = "1"
            else:
                kb_3 = "0"
            if getkeys[pygame.K_4]:
                kb_4 = "1"
            else:
                kb_4 = "0"
            if getkeys[pygame.K_5]:
                kb_5 = "1"
            else:
                kb_5 = "0"
            if getkeys[pygame.K_6]:
                kb_6 = "1"
            else:
                kb_6 = "0"
            if getkeys[pygame.K_7]:
                kb_7 = "1"
            else:
                kb_7 = "0"
            if getkeys[pygame.K_8]:
                kb_8 = "1"
            else:
                kb_8 = "0"
            if getkeys[pygame.K_9]:
                kb_9 = "1"
            else:
                kb_9 = "0"

            send = close_session + ":" + mouseposx + ":" + mouseposy + ":" + mousebutton1 + ":" + mousebutton3 + ":" + kb_0 + ":" + kb_1 + ":" + kb_2 + ":" + kb_3 + ":" + kb_4 + ":" + kb_5 + ":" + kb_6 + ":" + kb_7 + ":" + kb_8 + ":" + kb_9 + ":" + Img2Gen

            if close_session == "1":
                s2.close()
                pygame.display.quit()
                stayOpen = False

            if (pygame.key.get_pressed()[pygame.K_e] & pygame.key.get_pressed()[pygame.K_RCTRL] & pygame.key.get_pressed()[pygame.K_RALT]):
                close_session = "1"

            if (pygame.key.get_pressed()[pygame.K_LSHIFT] & pygame.key.get_pressed()[pygame.K_RCTRL] & pygame.key.get_pressed()[pygame.K_RALT] & pygame.key.get_pressed()[pygame.K_f]):
                if dspfullscreen == 0:
                    pygame.display.quit()
                    pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                    dspfullscreen = 1
                    time.sleep(.1)
                else:
                    pygame.display.quit()
                    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
                    dspfullscreen = 0
                    time.sleep(.1)

            pygame.event.pump()

        except:
            pass


input_thread = threading.Thread(target=Input)
output_thread = threading.Thread(target=Output)
input_thread.start()
output_thread.start()
