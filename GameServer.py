import threading
import pygame
import socket
import sys
import time
import random
import os

# --- Globals ---
posx = 275
posy = 520
bucketSpeed = 10
bucketSize = 60
screen_width = 550
screen_height = 700
bucket_angle = 0

startGame = False

MENU_MAIN = "main"
MENU_SETTINGS = "settings"
MENU_PLAY = "play"

currentMenu = MENU_MAIN

def load_high_score():
    if os.path.exists('highscore.txt'):
        with open('highscore.txt', 'r') as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    else:
        return 0

def save_high_score(score):
    with open('highscore.txt', 'w') as file:
        file.write(str(score))

class Button:
    def __init__(self, x, y, width, height, text, base_color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = list(base_color)
        self.action = action
        self.font = pygame.font.Font(None, 40)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Animate color
        target_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        for i in range(3):
            if self.current_color[i] < target_color[i]:
                self.current_color[i] += min(5, target_color[i] - self.current_color[i])
            elif self.current_color[i] > target_color[i]:
                self.current_color[i] -= min(5, self.current_color[i] - target_color[i])

        pygame.draw.rect(screen, self.current_color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.centerx - text_surface.get_width()//2,
                                   self.rect.centery - text_surface.get_height()//2))

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

def GameThread():
    pygame.init()
    pygame.mixer.music.load('assets/techno.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    global posx, posy, bucketSpeed, bucketSize, screen_width, screen_height, startGame, currentMenu

    starttime = pygame.time.get_ticks()
    speedup = pygame.time.get_ticks()
    background = (204, 230, 255)
    fallObj = []
    initSpeed = 1
    currentScore = 0
    highScore = load_high_score()
    high_score_pulse = False
    pulse_alpha = 0
    pulse_direction = 1
    pulse_start_time = 0
    levelCount = 1
    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN Games')

    disk_images = [
        pygame.transform.scale(pygame.image.load('assets/whiteDisk.png').convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load('assets/blueDisk.png').convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load('assets/orangeDisk.png').convert_alpha(), (50, 65))
    ]
    bucket_img = pygame.image.load('assets/tron.png').convert_alpha()
    bucket_img = pygame.transform.scale(bucket_img, (bucketSize + 20, bucketSize + 20))
    bg_image = pygame.transform.scale(pygame.image.load('assets/background.png'), (screen_width, screen_height))

    rectBucket = pygame.Rect(0, 0, bucketSize, bucketSize)
    rectFloor = pygame.Rect(0, 0, 550, 80)
    rectFloor.center = (screen_width/2, 0)

    madeFirst = False
    font = pygame.font.Font(None, 36)

    #Button
    play_button = Button(screen_width//2 - 75, 300, 150, 50, "Play", (30, 60, 120), (80, 120, 220), lambda: set_menu(MENU_PLAY))
    settings_button = Button(screen_width//2 - 75, 370, 150, 50, "Settings", (30, 60, 120), (80, 120, 220), lambda: set_menu(MENU_SETTINGS))
    back_button = Button(20, 20, 100, 40, "Back", (30, 60, 120), (80, 120, 220), lambda: set_menu(MENU_MAIN))
    volume_up_button = Button(screen_width//2 - 100, 300, 200, 50, "Volume +", (30, 60, 120), (80, 120, 220), lambda: change_volume(0.1))
    volume_down_button = Button(screen_width//2 - 100, 370, 200, 50, "Volume -", (30, 60, 120), (80, 120, 220), lambda: change_volume(-0.1))

    def set_menu(menu_name):
        global currentMenu, startGame
        currentMenu = menu_name
        if menu_name == MENU_PLAY:
            startGame = True

    def change_volume(amount):
        new_volume = pygame.mixer.music.get_volume() + amount
        new_volume = max(0.0, min(1.0, new_volume))
        pygame.mixer.music.set_volume(new_volume)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if currentMenu == MENU_MAIN:
                play_button.check_click(event)
                settings_button.check_click(event)
            elif currentMenu == MENU_SETTINGS:
                back_button.check_click(event)
                volume_up_button.check_click(event)
                volume_down_button.check_click(event)

        screen.blit(bg_image, (0, 0))

        if currentMenu == MENU_MAIN:
            title = font.render("Welcome to CCN Games", True, (255, 255, 255))
            screen.blit(title, (screen_width//2 - title.get_width()//2, 200))
            play_button.draw(screen)
            settings_button.draw(screen)

        elif currentMenu == MENU_SETTINGS:
            settings_title = font.render("Settings", True, (255, 255, 255))
            screen.blit(settings_title, (screen_width//2 - settings_title.get_width()//2, 200))
            volume_up_button.draw(screen)
            volume_down_button.draw(screen)
            back_button.draw(screen)

        elif currentMenu == MENU_PLAY:
            rectBucket.center = (posx, posy)
            rotated_bucket = pygame.transform.rotate(bucket_img, bucket_angle)
            rotated_rect = rotated_bucket.get_rect(center=rectBucket.center)
            screen.blit(rotated_bucket, rotated_rect)
            pygame.draw.rect(screen, (0, 0, 0), rectFloor)

            if startGame and not madeFirst:
                rect, color = makeShapes(disk_images)
                fallObj.append((rect, color))
                madeFirst = True

            for rect, img in fallObj:
                screen.blit(img, rect.topleft)

            for rect, color in list(fallObj):
                rect.y += initSpeed
                if rect.colliderect(rectBucket):
                    fallObj.remove((rect, color))
                    rect, color = makeShapes(disk_images)
                    fallObj.append((rect, color))
                    currentScore += 1
                    if currentScore > highScore:
                        highScore = currentScore
                        save_high_score(highScore)
                        high_score_pulse = True
                        pulse_start_time = pygame.time.get_ticks()
                elif rect.y > screen_height:
                    pygame.quit()
                    sys.exit()

            if pygame.time.get_ticks() - starttime > 15000 and startGame:
                starttime = pygame.time.get_ticks()
                rect, color = makeShapes(disk_images)
                fallObj.append((rect, color))
                levelCount += 1

            if pygame.time.get_ticks() - speedup > 10000 and startGame:
                speedup = pygame.time.get_ticks()
                initSpeed += 0.1
                bucketSpeed += 3

            # HUD
            small_font = pygame.font.Font(None, 25)
            text_surface = small_font.render(f"Score: {currentScore}", True, (255, 255, 255))
            level_surface = small_font.render(f"Level: {levelCount}", True, (255, 255, 255))

            if high_score_pulse:
                if pygame.time.get_ticks() - pulse_start_time >= 2000:
                    high_score_pulse = False
                else:
                    pulse_alpha += pulse_direction * 5
                    if pulse_alpha >= 255:
                        pulse_alpha = 255
                        pulse_direction = -1
                    elif pulse_alpha <= 100:
                        pulse_alpha = 100
                        pulse_direction = 1
                purple_color = (pulse_alpha, 0, pulse_alpha)
                high_score_surface = small_font.render(f"High Score: {highScore}", True, purple_color)
            else:
                high_score_surface = small_font.render(f"High Score: {highScore}", True, (255, 255, 0))

            screen.blit(text_surface, (50, 20))
            screen.blit(level_surface, (480, 20))
            screen.blit(high_score_surface, (screen_width//2 - high_score_surface.get_width()//2, 20))

        pygame.display.flip()
        fps.tick(60)

def makeShapes(disk_images):
    img = random.choice(disk_images)
    x_pos = random.randint(20, screen_width - 20)
    rect = pygame.Rect(x_pos, 40, 50, 50)
    return rect, img

def ServerThread():
    global posx, posy, bucketSpeed, bucket_angle, bucketSize, screen_width, screen_height, startGame
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print(host)
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    print("Server enabled...")
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
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
    conn.close()

t1 = threading.Thread(target=GameThread)
t2 = threading.Thread(target=ServerThread)
t1.start()
t2.start()
