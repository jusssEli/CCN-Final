import threading 
import pygame
import socket
import sys
import time
import random

posx = 300
posy = 200
bucketSpeed = 20
bucketSize = 55
screen_width = 550
screen_height = 700
bucket_angle = 0

startGame = False

def GameThread():
    pygame.init()
    starttime = pygame.time.get_ticks()
    speedup = pygame.time.get_ticks()
    #initializing colors
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    floorColor = (0, 0, 0)
    fallObj = []
    global posx
    global bucket_angle
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
        pygame.transform.scale(pygame.image.load('assets/whiteDisk.png').convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load('assets/blueDisk.png').convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load('assets/orangeDisk.png').convert_alpha(), (50, 60))
    ]
    bucket_img = pygame.image.load('assets/tron.png').convert_alpha()
    bucket_img = pygame.transform.scale(bucket_img, (bucketSize + 20, bucketSize + 20))
    bg_image = pygame.transform.scale(
        pygame.image.load('assets/background.png'),
        (screen_width, screen_height)
    )
    ##########################
    def makeShapes():
        img = random.choice(disk_images)
        x_pos = random.randint(20, screen_width - 20)
        rect = pygame.Rect(x_pos, 0, 50, 50)
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
        #screen.fill(background)
        screen.blit(bg_image, (0, 0))
        #position/draw shapes
        rectBucket.center = (posx, posy)
        angle = bucket_angle
        rotated_bucket = pygame.transform.rotate(bucket_img, angle)
        rotated_rect = rotated_bucket.get_rect(center=rectBucket.center)
        screen.blit(rotated_bucket, rotated_rect.topleft)

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
            initSpeed += 0.1
            bucketSpeed += 4
        elif not startGame:
            speedup = pygame.time.get_ticks()

        #text options
        font = pygame.font.Font(None, 25)
        text = "Score: " + str(currentScore)
        blockSpeedText = "Block Speed: " + str(initSpeed)
        bucketSpeedText = "Bucket Speed: " + str(bucketSpeed)

        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.midleft = (screen.get_width()-75, 20)
        screen.blit(text_surface, text_rect)

        text_surface2 = font.render(blockSpeedText, True, (0, 0, 0))
        text_rect2 = text_surface2.get_rect(center=(60, 30))
        screen.blit(text_surface2, text_rect2)

        text_surface3 = font.render(bucketSpeedText, True, (0, 0, 0))
        text_rect3 = text_surface3.get_rect(center=(69, 50))
        screen.blit(text_surface3, text_rect3)

        # Space to start
        if not startGame:
            start_text = pygame.font.Font(None, 36).render("Press SPACE to Start", True, (0, 0, 255))
            start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(start_text, start_rect)

        text = "Score: " + str(currentScore)
        blockSpeedText = "Block Speed: " + str(initSpeed)
        bucketSpeedText = "Bucket Speed: " + str(bucketSpeed)
        pygame.display.flip()

        pygame.display.update()
        fps.tick(60)
    pygame.quit()

def ServerThread():
    global posx
    global posy
    global bucketSpeed
    global bucket_angle
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
            bucket_angle = 90
        if data == 's' and posy <= screen_height-(bucketSize/2):
            posy += bucketSpeed
            time.sleep(0.05)
            bucket_angle = -90
        if data == 'a' and posx >= (bucketSize/2):
            posx -= bucketSpeed
            time.sleep(0.05)
            bucket_angle = 180
        if data == 'd' and posx <= screen_width-(bucketSize/2):
            posx += bucketSpeed
            time.sleep(0.05)
            bucket_angle = 0
    conn.close()  # close the connection

 
t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t1.start()
t2.start()