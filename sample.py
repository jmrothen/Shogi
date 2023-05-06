import pygame
import random
import math
from pygame import mixer



# initialize
pygame.init()

# make window
screen = pygame.display.set_mode((800, 600))

# title and icon for window
pygame.display.set_caption("Space Inbader")
icon = pygame.image.load('weirdchamp32x32.png')
pygame.display.set_icon(icon)

# background picture
background = pygame.image.load('space.png')

# background music
mixer.music.load('musiv.wav')
mixer.music.play(-1)


# Player
playerImg = pygame.image.load('pierre.png')
playerx = 370
playery = 500
playerxdif = 0
playerydif = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Emeny
enemyImg = []
enemyx = []
enemyy = []
enemyxdif = []
enemyydif = []
numEn = 10

for i in range(numEn):
    if (i % 2) == 0:
        imgtemp = 'POGCHAMP.png'
    else:
        imgtemp = 'weirdchamp32x32.png'
    enemyImg.append(pygame.image.load(imgtemp))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50,150))
    enemyxdif.append(.2)
    enemyydif.append(0)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Laser
laserImg = pygame.image.load('laser.png')
laserx = 0
lasery = 480
laserydif = -.7
laserxdif = 0
laserState = "ready"  # ready if not on screen, fire if shoot


def shoot(x, y):
    global laserState
    laserState = "fire"
    screen.blit(laserImg, (laserx + 16, lasery + 10))

# Score!

scoreVal = 0
font = pygame.font.Font('freesansbold.ttf',24)
textx = 10
texty = 10
def showscore(x,y):
    score = font.render("Power Lebel : " + str(scoreVal), True, (0,240,0))
    screen.blit(score, (x,y))

# gameover check

font2 = pygame.font.Font('Silver Medal.ttf',48)
def gameover():
    overtext = font2.render("GAME OVER",True, (255,0,0))
    screen.blit(overtext, (200, 250))

# collide?

def isCol(enemyx, enemyy, laserx, lasery):
    enemyxt =enemyx+8
    enemyyt = enemyy
    laserxt = laserx+16
    laseryt = lasery+16
    dist = math.sqrt(math.pow(enemyxt - laserxt, 2) + (math.pow(enemyyt - laseryt, 2)))
    if dist < 32:
        return True
    else:
        return False


# Game Loop~~~

running = True
while running:
    # Background RGB
    screen.fill((220, 220, 220))
    screen.blit(background, (0, 0))
    # event tracking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerxdif = -.3
            if event.key == pygame.K_RIGHT:
                playerxdif = .3
            if event.key == pygame.K_SPACE:
                if laserState is "ready":
                    pew = mixer.Sound('pew.wav')
                    pew.play()
                    laserx = playerx
                    shoot(laserx, lasery)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerxdif = 0

    # record movements
    playerx += playerxdif
    playery += playerydif

    # Boundaries
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    # Enemy Boundary, and movement
    for i in range(numEn):
        #gameover
        if enemyy[i] > 400:
            for j in range(numEn):
                enemyy[j] =2000
            gameover()
            break

        enemyx[i] += enemyxdif[i]
        enemyy[i] += enemyydif[i]
        if enemyx[i] <= 0:
            enemyx[i] = 0
            enemyy[i] += 50
            enemyxdif[i] = .2
        elif enemyx[i] >= 736:
            enemyx[i] = 736
            enemyy[i] += 50
            enemyxdif[i] = -.2
        coll = isCol(enemyx[i], enemyy[i], laserx, lasery)
        if coll:
            ded = mixer.Sound('ow.wav')
            ded.play()
            lasery = 480
            laserState = "ready"
            scoreVal += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(16, 200)
        enemy(enemyx[i], enemyy[i], i)
    # laser update
    if lasery <= 0:
        lasery = 480
        laserState = "ready"

    if laserState is "fire":
        shoot(laserx, lasery)
        lasery += laserydif

    # Update Characters
    player(playerx, playery)
    showscore(textx,texty)
    pygame.display.update()
