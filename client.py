import pygame
import socket
import time
import sys

dspfullscreen = 0

pygame.init()
pygame.display.set_mode((0, 0), pygame.RESIZABLE)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("s is set")
s.connect(("192.168.2.14", 1234))
print("connection attempted")
close_session = "0"

while True:
    time.sleep(.025)

    # imageget = s.recv(1500000000)
    # print(pygame.display.get_surface().get_size())
    # print(imageget)
    # pygame.image.fromstring(imageget, pygame.display.get_surface().get_size(), "RGBA")

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
    s.send(send.encode("utf-8"))

    if close_session == "1":
        s.close()
        pygame.display.quit()
        sys.exit()

    if (pygame.key.get_pressed()[pygame.K_ESCAPE] & pygame.key.get_pressed()[pygame.K_RCTRL] & pygame.key.get_pressed()[pygame.K_RALT]):
        close_session = "1"

    if (pygame.key.get_pressed()[pygame.K_LSHIFT] & pygame.key.get_pressed()[pygame.K_RCTRL] & pygame.key.get_pressed()[pygame.K_RALT] & pygame.key.get_pressed()[pygame.K_f]):
        if dspfullscreen == 0:
            pygame.display.quit()
            pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
            dspfullscreen = 1
            time.sleep(.2)
        else:
            pygame.display.quit()
            pygame.display.set_mode((0, 0), pygame.RESIZABLE)
            dspfullscreen = 0

    # msg = input()
    # if msg == "quit()":
    #     s.send(msg.encode("utf-8"))
    #     quit()
    # else:
    #     s.send(msg.encode("utf-8"))


    pygame.event.pump()
