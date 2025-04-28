import threading
import pygame
import socket
import sys
import time
import random
import os

posx1, posy1 = 275, 520
posx2, posy2 = 275, 100
bucketSpeed = 10
bucketSize = 60
screen_width = 650
screen_height = 800
bucket_angle1 = 0
bucket_angle2 = 0

startGame = False
num_players = 0
currentScore = 0
highScore = 0
pulse_alpha = 0
pulse_direction = 1
pulse_start_time = 0
levelCount = 1

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

def set_menu(menu_name):
    global currentMenu, startGame
    currentMenu = menu_name
    if menu_name == MENU_PLAY:
        startGame = False

def start_game(players):
    global num_players
    num_players = players
    set_menu(MENU_PLAY)

def change_volume(amount):
    new_volume = pygame.mixer.music.get_volume() + amount
    new_volume = max(0.0, min(1.0, new_volume))
    pygame.mixer.music.set_volume(new_volume)

def makeShapes(disk_images):
    img = random.choice(disk_images)
    x_pos = random.randint(20, screen_width - 20)
    rect = pygame.Rect(x_pos, 40, 50, 50)
    return rect, img

def GameThread():
    global startGame, bucketSpeed, currentScore, highScore, pulse_alpha, pulse_direction, pulse_start_time, levelCount

    pygame.init()
    pygame.mixer.music.load('assets/techno.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    starttime = pygame.time.get_ticks()
    speedup = pygame.time.get_ticks()
    background = (204, 230, 255)
    fallObj = []
    initSpeed = 1
    highScore = load_high_score()
    high_score_pulse = False

    fps = pygame.time.Clock()
    screen_size = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Welcome to CCN Games')

    disk_images = [
        pygame.transform.scale(pygame.image.load('assets/whiteDisk.png').convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load('assets/blueDisk.png').convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load('assets/orangeDisk.png').convert_alpha(), (50, 65))
    ]

    bucket1_img = pygame.transform.scale(pygame.image.load('assets/tron.png').convert_alpha(), (bucketSize + 20, bucketSize + 20))
    bucket2_img = pygame.transform.scale(pygame.image.load('assets/tron.png').convert_alpha(), (bucketSize + 20, bucketSize + 20))
    bg_image = pygame.transform.scale(pygame.image.load('assets/background.png'), (screen_width, screen_height))

    rectBucket1 = pygame.Rect(0, 0, bucketSize, bucketSize)
    rectBucket2 = pygame.Rect(0, 0, bucketSize, bucketSize)
    rectFloor = pygame.Rect(0, 0, 550, 80)
    rectFloor.center = (screen_width/2, 0)

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 25)

    one_player_button = Button(screen_width//2 - 75, 300, 200, 50, "One Player", (30, 60, 120), (80, 120, 220), lambda: start_game(1))
    two_player_button = Button(screen_width//2 - 75, 370, 200, 50, "Two Players", (30, 60, 120), (80, 120, 220), lambda: start_game(2))
    settings_button = Button(screen_width//2 - 75, 440, 200, 50, "Settings", (30, 60, 120), (80, 120, 220), lambda: set_menu(MENU_SETTINGS))
    back_button = Button(20, 20, 100, 40, "Back", (30, 60, 120), (80, 120, 220), lambda: set_menu(MENU_MAIN))
    volume_up_button = Button(screen_width//2 - 100, 300, 225, 50, "Volume +", (30, 60, 120), (80, 120, 220), lambda: change_volume(0.1))
    volume_down_button = Button(screen_width//2 - 100, 370, 225, 50, "Volume -", (30, 60, 120), (80, 120, 220), lambda: change_volume(-0.1))

    madeFirst = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if currentMenu == MENU_MAIN:
                one_player_button.check_click(event)
                two_player_button.check_click(event)
                settings_button.check_click(event)
            elif currentMenu == MENU_SETTINGS:
                back_button.check_click(event)
                volume_up_button.check_click(event)
                volume_down_button.check_click(event)

        screen.blit(bg_image, (0, 0))

        if currentMenu == MENU_MAIN:
            title = font.render("Welcome to CCN Games", True, (255, 255, 255))
            screen.blit(title, (screen_width//2 - title.get_width()//2, 200))
            one_player_button.draw(screen)
            two_player_button.draw(screen)
            settings_button.draw(screen)

        elif currentMenu == MENU_SETTINGS:
            settings_title = font.render("Settings", True, (255, 255, 255))
            screen.blit(settings_title, (screen_width//2 - settings_title.get_width()//2, 200))
            volume_up_button.draw(screen)
            volume_down_button.draw(screen)
            back_button.draw(screen)

        elif currentMenu == MENU_PLAY:
            rectBucket1.center = (posx1, posy1)
            outline_rect1 = rectBucket1.inflate(10, 10)
            pygame.draw.ellipse(screen, (0, 100, 255), outline_rect1)
            rotated_bucket1 = pygame.transform.rotate(bucket1_img, bucket_angle1)
            new_rect1 = rotated_bucket1.get_rect(center=rectBucket1.center)
            screen.blit(rotated_bucket1, new_rect1)


            if num_players == 2:
                rectBucket2.center = (posx2, posy2)
                outline_rect2 = rectBucket2.inflate(10, 10)
                pygame.draw.ellipse(screen, (255, 140, 0), outline_rect2)
                rotated_bucket2 = pygame.transform.rotate(bucket2_img, bucket_angle2)
                new_rect2 = rotated_bucket2.get_rect(center=rectBucket2.center)
                screen.blit(rotated_bucket2, new_rect2)


            pygame.draw.rect(screen, (0, 0, 0), rectFloor)

            if not startGame:
                press_space_text = font.render("Press SPACE to Start", True, (255, 255, 255))
                screen.blit(press_space_text, (screen_width // 2 - press_space_text.get_width() // 2, screen_height // 2))
            else:
                if startGame and not madeFirst:
                    rect, color = makeShapes(disk_images)
                    fallObj.append((rect, color))
                    madeFirst = True

                for rect, img in fallObj:
                    screen.blit(img, rect.topleft)
                for rect, color in list(fallObj):
                    rect.y += initSpeed
                    if rect.colliderect(rectBucket1) or (num_players == 2 and rect.colliderect(rectBucket2)):
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
                    initSpeed += 0.2
                    bucketSpeed += .8

                score_surface = small_font.render(f"Score: {currentScore}", True, (255, 255, 255))
                level_surface = small_font.render(f"Level: {levelCount}", True, (255, 255, 255))
                screen.blit(score_surface, (50, 20))
                screen.blit(level_surface, (480, 20))
                high_score_surface = small_font.render(f"High Score: {highScore}", True, (255, 255, 0))
                screen.blit(high_score_surface, (screen_width//2 - high_score_surface.get_width()//2, 20))

        pygame.display.flip()
        fps.tick(60)

def ServerThread(player_num):
    global posx1, posy1, posx2, posy2, bucketSpeed, bucket_angle1, bucket_angle2, screen_width, screen_height, startGame

    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print(f"Server started! Connect to IP address: {host}")

    port = 5000 + (player_num - 1)
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if data == 'space':
            startGame = True

        if data == 'w':
            if player_num == 1 and posy1 >= (bucketSize/2):
                posy1 -= bucketSpeed
                bucket_angle1 = 90
            if player_num == 2 and posy2 >= (bucketSize/2):
                posy2 -= bucketSpeed
                bucket_angle2 = 90
        if data == 's':
            if player_num == 1 and posy1 <= screen_height - (bucketSize/2):
                posy1 += bucketSpeed
                bucket_angle1 = -90
            if player_num == 2 and posy2 <= screen_height - (bucketSize/2):
                posy2 += bucketSpeed
                bucket_angle2 = -90
        if data == 'a':
            if player_num == 1 and posx1 >= (bucketSize/2):
                posx1 -= bucketSpeed
                bucket_angle1 = 180
            if player_num == 2 and posx2 >= (bucketSize/2):
                posx2 -= bucketSpeed
                bucket_angle2 = 180
        if data == 'd':
            if player_num == 1 and posx1 <= screen_width - (bucketSize/2):
                posx1 += bucketSpeed
                bucket_angle1 = 0
            if player_num == 2 and posx2 <= screen_width - (bucketSize/2):
                posx2 += bucketSpeed
                bucket_angle2 = 0

    conn.close()

game_thread = threading.Thread(target=GameThread)
game_thread.start()

while num_players == 0:
    time.sleep(0.1)

server1 = threading.Thread(target=ServerThread, args=(1,))
server1.start()

if num_players == 2:
    server2 = threading.Thread(target=ServerThread, args=(2,))
    server2.start()
