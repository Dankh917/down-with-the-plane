import pygame
import random
import math
from pygame import mixer

pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background and sound
back = pygame.image.load('fa8d09096d6868eb10b4c1538f26a82a.png')
mixer.music.load('2013-12-28_Skies_-_David_Fesliyan.ogg')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("down with the plane")
icon = pygame.image.load('jet.png')
pygame.display.set_icon(icon)

# player
player_icon = pygame.image.load('jet.png')
playerX = 0
playerY = 300
playerX_change = 0
playerY_change = 0


# enemy
enemy_icon = pygame.image.load('jet (2).png')
enemyX = random.randint(200, 734)
enemyY = random.randint(0, 600)
enemyX_change= 0
enemyY_change= 0

# missile
missile_icon = pygame.image.load('submarine-torpedo.png')
missileX = 0
missileY = 0
missileX_change = 10
missileY_change = 10
missile_state = "ready"

# enemy missile
enemy_missile_icon = pygame.image.load('output-onlinepngtools.png')
enemy_missileX = 0
enemy_missileY = 0
enemy_missileX_change = 10
enemy_missileY_change = 10
enemy_missile_state = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf',25)
txtx = 10
txty = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (57, 33, 33))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    real_score = font.render("your score: "+str(score),True,(57,33,33))
    screen.blit(real_score, (x, y))

def player(x,y):
    screen.blit(player_icon, (x, y))

def enemy(x, y):
    screen.blit(enemy_icon, (x, y))

def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missile_icon, (x+50, y+15))

def enemy_fire_missile(x, y):
    global enemy_missile_state
    enemy_missile_state = "fire"
    screen.blit(enemy_missile_icon, (x-15, y+15))

def iscollision(enemyX, enemyY, missileX , missileY ):
    distance = math.sqrt(math.pow(enemyX-missileX, 2)+math.pow(enemyY-missileY, 2))
    if distance < 27:
        return True
    else:
        return False


def enemy_iscollision(payerX, playerY, enemy_missileX , enemy_missileY ):
    distance = math.sqrt(math.pow(payerX-enemy_missileX, 2)+math.pow(playerY-enemy_missileY, 2))
    if distance < 27:
        return True
    else:
        return False

# game loop
running = True
while running:
    # color background
    screen.fill((192, 192, 192))
    # background
    screen.blit(back, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # keys for playing(key_input)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_d:
            playerX_change = 3
            player_icon = pygame.image.load('jet.png')
        if event.key == pygame.K_a:
            playerX_change = -3
        if event.key == pygame.K_w:
            playerY_change = -3.8
            player_icon = pygame.image.load('output-onlinepngtools (2).png')
        if event.key == pygame.K_s:
            playerY_change = 3.8
            player_icon = pygame.image.load('output-onlinepngtools (3).png')
        if event.key == pygame.K_a:
            playerX_change = -3
            player_icon = pygame.image.load('output-onlinepngtools (4).png')

        if event.key == pygame.K_SPACE:
            if missile_state is "ready":
             missle_sound = mixer.Sound('bottle rocket-soundbible.com-332895117.ogg')
             missle_sound.play()
             missileX = playerX
             missileY = playerY
             fire_missile(playerX, playerY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_d or event.key == pygame.K_a:
            playerX_change = 0
        if event.key == pygame.K_w:
            player_icon = pygame.image.load('jet.png')
            playerY_change = 0
        if event.key == pygame.K_s:
            player_icon = pygame.image.load('jet.png')
            playerY_change = 0

    # enemy brain
    enemyY_change = random.uniform(14, -14)
    chance = random.uniform(1, 11)
    if chance <= 1.2:
        if enemy_missile_state is "ready":
            enemy_missileX = enemyX
            enemy_missileY = enemyY
            enemy_fire_missile(enemyX, enemyY)

    playerY += playerY_change
    playerX += playerX_change
    enemyY += enemyY_change
    enemyX += enemyX_change

    # boundaries for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    else:
        pass
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # boundaries for enemy
    if enemyX <= 0:
        enemyX = 0
    elif enemyX >= 736:
        enemyX = 736
    else:
        pass
    if enemyY <= 0:
        enemyY = 0
    elif enemyY > 536 and enemyY < 1500 :
        enemyY = 536

    # missile movement
    if missile_state is "fire":
        fire_missile(missileX, missileY)
        missileX += 6
    if missileX >= 800:
        missile_state = "ready"

    # enemy missile movement
    if enemy_missile_state is "fire":
        enemy_fire_missile(enemy_missileX, enemy_missileY)
        enemy_missileX -= 6
    if enemy_missileX <= 0:
        enemy_missile_state = "ready"

    # collision
    collision = iscollision(enemyX, enemyY, missileX, missileY)
    if collision:
        explo_sound = mixer.Sound('explosion+7.ogg')
        explo_sound.play()
        score += 1
        missileX = 800
        enemyX = random.randint(200, 734)
        enemyY = random.randint(0, 600)

    # enemy_collision
    enemy_collison = enemy_iscollision(playerX, playerY, enemy_missileX , enemy_missileY)
    if enemy_collison:
        enemy_missileX = -100
        enemyY = 2000
        game_over_text()

    player(playerX, playerY)
    show_score(txtx, txty)
    enemy(enemyX, enemyY)
    pygame.display.update()



