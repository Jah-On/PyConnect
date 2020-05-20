import pygame
import socket
import time
import sys
from PIL import Image
import threading
from ftplib import FTP
from io import BytesIO

pygame.init()
dsp = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption('PyConnect ')
ip = str(input())
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((ip, 1235))
surface = pygame.Surface((255,255))
server = FTP()
server.connect(ip, 1234)
server.login('user', '12345')

def Input():
    global stayOpen
    stayOpen = True
    while stayOpen:
        image_store=BytesIO()
        try:
            server.retrbinary('RETR image.png', image_store.write)
            readfrombuf = Image.open(image_store)
            binary_image = readfrombuf.tobytes('raw','RGB')
            image = pygame.image.frombuffer(binary_image, (1600,900), 'RGB')
            dsp.blit(image, (0,0))
            pygame.display.flip()
        except:
            time.sleep(.01)

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

            send = close_session + ":" + mouseposx + ":" + mouseposy + ":" + mousebutton1 + ":" + mousebutton3 + ":" + kb_0 + ":" + kb_1 + ":" + kb_2 + ":" + kb_3 + ":" + kb_4 + ":" + kb_5 + ":" + kb_6 + ":" + kb_7 + ":" + kb_8 + ":" + kb_9
            s2.send(send.encode("utf-8"))

            if close_session == "1":
                s2.close()
                pygame.display.quit()
                stayOpen = False

            if (pygame.key.get_pressed()[pygame.K_ESCAPE] & pygame.key.get_pressed()[pygame.K_RCTRL] & pygame.key.get_pressed()[pygame.K_RALT]):
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
