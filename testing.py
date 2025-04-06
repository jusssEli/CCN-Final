import pygame
import sys
import random
import threading
import time

# Global position
posx = 300
posy = 900

def GameThread():
    pygame.init()
    background = (204, 230, 255)
    bucket_color = (0, 51, 204)
    object_colors = [(255, 95, 31), (77, 77, 255), (57, 255, 20)]
    
    screen_width, screen_height = 600, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Catch the Falling Objects')
    
    bucket = pygame.Rect(posx, posy, 80, 40)
    objects = []
    score = 0
    object_speed = 3
    bucket_speed = 8
    spawn_interval = 1500  # in milliseconds
    
    last_spawn_time = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    
    def spawn_object():
        color = random.choice(object_colors)
        x_pos = random.randint(20, screen_width - 20)
        rect = pygame.Rect(x_pos, 0, 20, 20)
        return rect, color

    # Initial objects
    for _ in range(3):
        rect, color = spawn_object()
        objects.append((rect, color))

    running = True
    while running:
        screen.fill(background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            bucket.x -= bucket_speed
        if keys[pygame.K_d]:
            bucket.x += bucket_speed
        if keys[pygame.K_w]:
            bucket.y -= bucket_speed
        if keys[pygame.K_s]:
            bucket.y += bucket_speed

        # Keep bucket in bounds
        bucket.clamp_ip(screen.get_rect())

        # Object movement and collision detection
        for rect, color in list(objects):
            rect.y += object_speed
            if rect.colliderect(bucket):
                objects.remove((rect, color))
                score += 1
            elif rect.y > screen_height:
                print(f"Game Over! Final score: {score}")
                pygame.quit()
                sys.exit()

        # Draw bucket
        pygame.draw.rect(screen, bucket_color, bucket)

        # Draw falling objects
        for rect, color in objects:
            pygame.draw.rect(screen, color, rect)

        # Spawn new objects
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= spawn_interval:
            rect, color = spawn_object()
            objects.append((rect, color))
            last_spawn_time = current_time

            # Increase difficulty
            object_speed += 0.3
            bucket_speed += 0.2
            spawn_interval = max(300, spawn_interval - 30)

        pygame.display.update()
        clock.tick(60)

# Run the game in a thread
t1 = threading.Thread(target=GameThread)
t1.start()
