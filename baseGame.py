import pygame
import sys
import keyboard
import threading 
import time
import random

posx = 300
posy = 200

def GameThread():
    pygame.init()
    #initializing colors
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    floorColor = (0, 0, 0)
    COLORS = [(255, 95, 31), (77, 77, 255), (57, 255, 20)]
    fallObj = []
    global posx
    global posy
    initSpeed = 3
    bucketSize = 50
    
    fps = pygame.time.Clock()
    
    screen_size = screen_width, screen_height = 450, 600
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN games')
    
    def makeShapes():
        color = random.choice(COLORS)
        x_pos = random.randint(20, screen_width - 20)
        rect = pygame.Rect(x_pos, 0, 20, 20)
        return rect, color
    
    for n in range(COLORS.__len__()):
        rect, color = makeShapes()
        fallObj.append((rect, color))
        
    #making bucket, floor shapes
    rectBucket = pygame.Rect(0, 0, bucketSize, bucketSize)
    rectFloor = pygame.Rect(0, 0, 450, 10)
    rectFloor.center = (screen_width/2, screen_height-5)

    #giving shapes a color
    colorRect =  (shapeColor)
    colorFloor = (floorColor)
    
    #while loop for the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(background)
        
        #position shapes
        rectBucket.center = (posx, posy)
        #draw shapes
        pygame.draw.rect(screen, colorRect, rectBucket)
        pygame.draw.rect(screen, colorFloor, rectFloor)
        collision = rectBucket.colliderect(rectFloor)

        #drawing falling rect
        for rect, color in fallObj:
            pygame.draw.rect(screen, color, rect)
            
        #collision of falling objects
        for rect, color in list (fallObj):
            rect.y += initSpeed
            if rect.colliderect(rectBucket):
                fallObj.remove((rect,color))
            elif rect.y > screen_height:
                pygame.quit()
                sys.exit()
        
        if keyboard.is_pressed('a') and posx >= (bucketSize/2):
            #client_socket.send('a'.encode())  # send message
            posx -= 10
            time.sleep(0.05)
        if keyboard.is_pressed('d') and posx <= screen_width-(bucketSize/2):
            #client_socket.send('d'.encode())  # send message
            posx += 10
            time.sleep(0.05)
        if keyboard.is_pressed('s') and not collision:
            #client_socket.send('s'.encode())  # send message
            posy += 10
            time.sleep(0.05)
        if keyboard.is_pressed('w') and posy >= (bucketSize/2):
            #client_socket.send('w'.encode())  # send message
            posy -= 10
            time.sleep(0.05)
           
        pygame.display.update()
        fps.tick(60)
    pygame.quit()

t1 = threading.Thread(target=GameThread, args=[])
t1.start()