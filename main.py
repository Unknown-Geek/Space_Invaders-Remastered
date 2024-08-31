import random
import math
import os
import pygame
from pygame import mixer
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://tve23cs131:tLnhbox1pcQAwjED@cluster0.szaod.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Access the database
db = client['SpaceInvaders']

# Access the collection
collection = db['users_scores']

# Example data to insert
data = {
    "player_name": "JohnDoe",
    "score": 12345,
    "level": 5,
    "timestamp": "2023-10-01T12:34:56"
}

# Insert the data into the collection
try:
    result = collection.insert_one(data)
    print(f"Data inserted with id: {result.inserted_id}")
except Exception as e:
    print(e)

# AI setup
detector = HandDetector(detectionCon=0.8, maxHands=2)
cap = cv2.VideoCapture(0)
tilt_threshold = 20

# Game setup
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Scrolling Background
background_img = pygame.image.load('background.jpg')
background_height = background_img.get_rect().height
background_rect1 = background_img.get_rect()
background_rect2 = background_img.get_rect()
background_rect1.bottom = SCREEN_HEIGHT
background_rect2.bottom = background_rect1.top
background_speed = 1

def update_background():
    global background_rect1, background_rect2
    background_rect1.y += background_speed
    background_rect2.y += background_speed

    if background_rect1.top >= SCREEN_HEIGHT:
        background_rect1.bottom = background_rect2.top
    if background_rect2.top >= SCREEN_HEIGHT:
        background_rect2.bottom = background_rect1.top

def draw_background(surface):
    surface.blit(background_img, background_rect1)
    surface.blit(background_img, background_rect2)

# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# BGM
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('arcade-game.png')
playerX = 400
playerY = 450
player_velocity = 0
player_acceleration = 0.5
player_lerp_factor = 0.1

# Bullet
bulletImg = pygame.image.load('bullet (1).png')
bullets = []
bullet_cooldown = 0.5
last_bullet_time = 0
bulletY_change = 15

# Enemy
no_enemies = 5
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_direction = []  # Track the vertical direction of each enemy
enemy_speed = 2.5

for i in range(no_enemies):
    enemyImg.append(pygame.image.load('icons8-spaceship-64.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))  # Limit initial vertical position
    enemyX_change.append(2)
    enemyY_change.append(1)
    enemy_direction.append(1)  # Start moving downwards

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 30)
title_font = pygame.font.Font('freesansbold.ttf', 64)

# Difficulty
difficulty_multiplier = 1.0
difficulty_increase_rate = 0.2
last_difficulty_increase = 0

def show_score():
    score_value = font.render('Score : ' + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))

def game_over():
    global score, playerX, playerY, bullets, enemyX, enemyY, enemy_direction
    mixer.music.stop()
    mixer.music.load('game_over.mp3')
    mixer.music.set_volume(2.5)
    mixer.music.play(1)
    gameoverImg = pygame.image.load('game over.png')
    for i in range(5, 0, -1):
        screen.blit(gameoverImg, (0, 0))
        scoreimg = font.render('YOU SCORED : ' + str(score), True, (255, 255, 255))
        screen.blit(scoreimg, (420, 480))
        exit_time = font.render('Game restarts in  ' + str(i) + ' sec', True, (255, 255, 255))
        screen.blit(exit_time, (420, 520))
        pygame.display.flip()
        pygame.time.delay(1000)
    # Reset game state
    score = 0
    playerX = 400
    playerY = 450
    bullets = []
    for i in range(no_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        enemy_direction[i] = 1
    mixer.music.load('background.wav')
    mixer.music.play(-1)

def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance < 30

def start_screen():
    input_active = True
    user_text = ''
    input_box = pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 50)
    color = pygame.Color('lightskyblue3')
    font = pygame.font.Font(None, 32)
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        
        update_background()
        draw_background(screen)
        
        title = title_font.render('SPACE INVADERS', True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        # Render the current text.
        txt_surface = font.render(user_text, True, color)
        width = max(10, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        
        prompt_text = font.render('Enter your name and press Enter:', True, (255, 255, 255))
        screen.blit(prompt_text, (SCREEN_WIDTH//2 - prompt_text.get_width()//2, 250))
        
        pygame.display.flip()
        clock.tick(30)
    
    return user_text

running = True
game_state = "START"

while running:
    dt = clock.tick(60) / 1000.0  # 60 FPS, convert to seconds

    if game_state == "START":
        if start_screen():
            game_state = "PLAYING"
        else:
            running = False
            continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw scrolling background
    update_background()
    draw_background(screen)

    # Increase difficulty over time
    current_time = pygame.time.get_ticks() / 1000.0
    if current_time - last_difficulty_increase > 10:  # Increase difficulty every 10 seconds
        difficulty_multiplier += difficulty_increase_rate
        last_difficulty_increase = current_time

    player_velocity = player_velocity * (1 - player_lerp_factor) 
    new_player_x = playerX + player_velocity * dt * 60

    # Boundary check
    if new_player_x < 0:
        new_player_x = 0
        player_velocity = 0
    elif new_player_x > 736:
        new_player_x = 736
        player_velocity = 0

    playerX = new_player_x  # Direct assignment instead of lerping

    # Enemy movement (zigzag pattern)
    for i in range(no_enemies):
        enemy_speed = enemyX_change[i] * difficulty_multiplier
        enemyX[i] += enemy_speed * dt * 60
        
        # Zigzag motion
        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] *= -1
            enemy_direction[i] *= -1
        
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] *= -1
            enemy_direction[i] *= -1

        if enemyY[i] <= 50:
            enemyY[i] = 50
            enemyY_change[i] *= -1
            enemy_direction[i] *= -1

        enemyY[i] += enemy_direction[i] * enemy_speed * dt * 5  # Adjust descent speed as needed

        # Ensure the enemy stays within vertical bounds
        enemyY[i] = max(0, min(450, enemyY[i]))

        # Game over condition
        if enemyY[i] > 430:
            game_over()
            game_state = "START"
            break

        # Collision detection
        for bullet in bullets[:]:
            if isCollision(enemyX[i], enemyY[i], bullet[0], bullet[1]) or isCollision(playerX, playerY, enemyX[i], enemyY[i]):
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bullets.remove(bullet)
                score += 10
                enemyX[i] = random.randint(10, 730)
                enemyY[i] = random.randint(50, 150)

        screen.blit(enemyImg[i], (int(enemyX[i]), int(enemyY[i])))

    # Bullet movement
    for bullet in bullets[:]:
        bullet[1] -= bulletY_change * dt * 60
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            screen.blit(bulletImg, (int(bullet[0]), int(bullet[1])))

    # AI hand tracking
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        for hand in hands:
            if hand['type'] == 'Right':
                wrist = hand['lmList'][0][:2]
                middle_finger_tip = hand['lmList'][12][:2]
                
                dx = middle_finger_tip[0] - wrist[0]
                dy = middle_finger_tip[1] - wrist[1]
                angle = math.degrees(math.atan2(dy, dx))
                
                if angle > -90 - tilt_threshold:
                    player_velocity -= player_acceleration
                elif angle < -90 + tilt_threshold:
                    player_velocity += player_acceleration
                
                cv2.line(img, tuple(wrist), tuple(middle_finger_tip), (255, 0, 0), 2)
                cv2.putText(img, f"Angle: {angle:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if hand['type'] == 'Left':
                fingerUp = detector.fingersUp(hand)
                if fingerUp == [1,1,1,1,1]:
                    current_time = pygame.time.get_ticks() / 1000.0
                    if current_time - last_bullet_time > bullet_cooldown:
                        laser_sound = mixer.Sound('laser.wav')
                        laser_sound.play()
                        bullets.append([playerX + 16, playerY - 20])
                        last_bullet_time = current_time 

    small_frame = cv2.resize(img, (0,0), fx=0.3, fy=0.25)
    cv2.imshow('frame', small_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    screen.blit(playerImg, (int(playerX), int(playerY)))
    show_score()
    pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
pygame.quit()