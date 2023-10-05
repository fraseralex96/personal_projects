import pygame
import random
import math
from pygame import mixer

# initialise the pygame
pygame.init()

# create screen
# two brackets v important
screen = pygame.display.set_mode((512, 512))

# background
background = pygame.image.load('src/img/background.png')

# background sound
mixer.music.load('src/sounds/background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('src/img/spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('src/img/spaceship.png')
playerX = 256
playerY = 430
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('src/img/alien.png'))
    enemyX.append(random.randint(1, 512))
    enemyY.append(50)
    enemyX_change.append(1)
    enemyY_change.append(30)

# bullet
# ready - you cant see the bullet on the screen
# fire - the bullet is currently moving

bulletImg = pygame.image.load('src/img/bullet.png')
bulletX = 256
bulletY = 430
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 40)


def show_score(x, y):
    score = font.render(str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (150, 250))


def player(x, y):
    # draws an image
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x-6, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 35:
        return True
    else:
        return False

def isPlayerCollision(enemyX, enemyY, PlayerX, playerY):
    distance = math.sqrt((math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2)))
    if distance < 35:
        return True
    else:
        return False


# game loop
# creates a window that can be closed
# anything continuous needs to be in here
running = True
while running:

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_UP:
                playerY_change = -4
            if event.key == pygame.K_DOWN:
                playerY_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('src/sounds/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # player movement
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 512:
        playerX = 512
    if playerY <= 0:
        playerY = 0
    elif playerY >= 462:
        playerY = 462

    # enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 512:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('src/sounds/explosion.wav')
            collision_sound.play()
            bulletY = 256
            bulletX = 430
            bullet_state = "ready"
            enemyX[i] = random.randint(1, 512)
            enemyY[i] = 30
            score_value += 1

        # player collision
        playerCollision = isPlayerCollision(enemyX[i], enemyY[i], playerX, playerY)
        if playerCollision:
            collision_sound = mixer.Sound('src/sounds/explosion.wav')
            collision_sound.play()
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
