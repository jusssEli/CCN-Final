import pygame
import sys
import keyboard
import threading 
import time

posx = 300
posy = 200

def GameThread():
    pygame.init()
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    shapeColorOver = (255, 0, 204)

    global posx
    global posy
    
    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height = 600, 400
    rectBucket = pygame.Rect(0, 0, 50, 50)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN games')
    
    colorRect = (shapeColor)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(background)
        rectBucket.center = (posx, posy)
        pygame.draw.rect(screen, colorRect, rectBucket)
        #when collision occurs, add to score and disappear object
        if keyboard.is_pressed('a'):
            #client_socket.send('a'.encode())  # send message
            posx -= 10
            time.sleep(0.1)
        if keyboard.is_pressed('d'):
            #client_socket.send('d'.encode())  # send message
            posx += 10
            time.sleep(0.1)
        if keyboard.is_pressed('s'):
            #client_socket.send('s'.encode())  # send message
            posy += 10
            time.sleep(0.1)
        if keyboard.is_pressed('w'):
            #client_socket.send('w'.encode())  # send message
            posy -= 10
            time.sleep(0.1)
        pygame.display.update()
        fps.tick(60)
    pygame.quit()

t1 = threading.Thread(target=GameThread, args=[])
t1.start()