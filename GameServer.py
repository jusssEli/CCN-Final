import threading 
import pygame
import socket
import sys
import time
import random

posx = 300
posy = 200
bucketSpeed = 20
bucketSize = 50
screen_width = 450
screen_height = 600

startGame = False

def GameThread():
    pygame.init()
    starttime = pygame.time.get_ticks()
    speedup = pygame.time.get_ticks()
    #initializing colors
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    floorColor = (0, 0, 0)
    COLORS = [(255, 95, 31), (77, 77, 255), (57, 255, 20)]
    fallObj = []
    global posx
    global posy
    global bucketSpeed
    global bucketSize
    global screen_width
    global screen_height
    global startGame
    initSpeed = 1
    currentScore = 0
    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN games')
    #images
    disk_images = [
        pygame.transform.scale(pygame.image.load('assets/whiteDisk.png').convert_alpha(), (20, 20)),
        pygame.transform.scale(pygame.image.load('assets/blueDisk.png').convert_alpha(), (20, 20)),
        pygame.transform.scale(pygame.image.load('assets/orangeDisk.png').convert_alpha(), (20, 20))
    ]
    bucket_img = pygame.image.load('assets/tron.png').convert_alpha()
    bucket_img = pygame.transform.scale(bucket_img, (bucketSize, bucketSize))
    
    def makeShapes():
        img = random.choice(disk_images)
        x_pos = random.randint(20, screen_width - 20)
        rect = pygame.Rect(x_pos, 0, 20, 20)
        return rect, img
        
    #making bucket, floor shapes
    rectBucket = pygame.Rect(0, 0, bucketSize, bucketSize)
    rectFloor = pygame.Rect(0, 0, 450, 10)
    rectFloor.center = (screen_width/2, screen_height-5)

    #giving shapes a color
    colorRect =  (shapeColor)
    colorFloor = (floorColor)

    madeFirst = False

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
        screen.blit(bucket_img, rectBucket.topleft)
        pygame.draw.rect(screen, colorFloor, rectFloor)

        if startGame and not madeFirst:
            rect, color = makeShapes()
            fallObj.append((rect, color))
            madeFirst = True

        #drawing falling rect
        for rect, img in fallObj:
            screen.blit(img, rect.topleft)

            
        #collision of falling objects
        for rect, color in list (fallObj):
            rect.y += initSpeed
            if rect.colliderect(rectBucket):
                fallObj.remove((rect,color))
                rect, color = makeShapes()
                fallObj.append((rect, color))
                currentScore += 1
            elif rect.y > screen_height:
                pygame.quit()
                sys.exit()
           
        if pygame.time.get_ticks() - starttime > 15000 and startGame:
            starttime = pygame.time.get_ticks()
            rect, color = makeShapes()
            fallObj.append((rect, color))
        elif not startGame:
            starttime = pygame.time.get_ticks()

        if pygame.time.get_ticks() - speedup > 10000 and startGame:
            speedup = pygame.time.get_ticks()
            initSpeed += 0.2
            bucketSpeed += 5
        elif not startGame:
            speedup = pygame.time.get_ticks()

        #text options
        font = pygame.font.Font(None, 25) #none is style, sze is 36
        text = "Score: " + str(currentScore)
        blockSpeedText = "Block Speed: " + str(initSpeed)
        bucketSpeedText = "Bucket Speed: " + str(bucketSpeed)

        text_surface = font.render(text, True, (0, 0, 0))  # black color text
        text_rect = text_surface.get_rect()  # Position in the center of the screen
        text_rect.midleft = (screen.get_width()-75, 20)
        screen.blit(text_surface, text_rect)

        text_surface2 = font.render(blockSpeedText, True, (0, 0, 0))  # black color text
        text_rect2 = text_surface2.get_rect(center=(60, 30))  # Position in the center of the screen
        screen.blit(text_surface2, text_rect2)

        text_surface3 = font.render(bucketSpeedText, True, (0, 0, 0))  # black color text
        text_rect3 = text_surface3.get_rect(center=(69, 50))  # Position in the center of the screen
        screen.blit(text_surface3, text_rect3)
        pygame.display.flip()

        pygame.display.update()
        fps.tick(60)
    pygame.quit()

def ServerThread():
    global posx
    global posy
    global bucketSpeed
    global bucketSize
    global screen_width
    global screen_height
    global startGame
    #get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print(host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket() # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
     # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))   
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break

        print("from connected user: " + str(data))
        if data == 'space':
            startGame = True
            time.sleep(0.05)
        if data == 'w' and posy >= (bucketSize/2):
            posy -= bucketSpeed
            time.sleep(0.05)
        if data == 's' and posy <= screen_height-(bucketSize/2):
            posy += bucketSpeed
            time.sleep(0.05)
        if data == 'a' and posx >= (bucketSize/2):
            posx -= bucketSpeed
            time.sleep(0.05)
        if data == 'd' and posx <= screen_width-(bucketSize/2):
            posx += bucketSpeed
            time.sleep(0.05)
    conn.close()  # close the connection

 
t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t1.start()
t2.start()