#FreeCodeCamp demo
#Mark Reuter
#2024 05 22

#import libraries
import pygame
import random
import math
from pygame import mixer

#initialize
pygame.init()

#create screen, width x height
screen = pygame.display.set_mode((800,600))

#alter window caption
pygame.display.set_caption("Space Invaders")

#background image
background = pygame.image.load('space.jpeg')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1) #play loop

#alter icon
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship64.png')
playerX = 380
playerY = 480
playerX_change = 0

#enermy
enermyImg = []
enermyX = []
enermyY = []
enermyX_change = []
enermyY_change = []
enermyCount = 12 #number of enermies to spawn initially

for i in range(enermyCount):
    enermyImg.append(pygame.image.load('ufo64.png'))
    enermyX.append(random.randint(20,720))
    enermyY.append(20)
    enermyX_change.append(0.3)
    enermyY_change.append(40)

#enermyImg = pygame.image.load('ufo64.png')
#enermyX = random.randint(20,720)
#enermyY = 20
#enermyX_change = 0.3
#enermyY_change = 40

#bullet
bullet = pygame.image.load('missile32.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bulletState = 'ready' #bullet not visible, fire = moving

def fire_bullet(x,y):
    global bulletState #access variable from function
    bulletState = 'fire'
    screen.blit(bullet,(x + 16,y + 10))


#function to draw player, called from within game loop
#arguments are x and y coordinates
def player(x,y):
        screen.blit(playerImg,(x,y))

#enermy function
def enermy(x,y,i):
    screen.blit(enermyImg[i],(x,y))

#collision
def isCollision(enermyX,enermyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enermyX-bulletX,2)) + (math.pow(enermyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#scoring
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value),True,(0,0,255))
    screen.blit(score,(x,y))

#game over logic
over_font = pygame.font.Font('freesansbold.ttf',52)

def game_over_text():
    gameOver = over_font.render("Game Over!",True,(0,0,255))
    screen.blit(gameOver,(240,250))
    pygame.mixer.music.stop()

#infinite game loop 
running = True
while running:

    #alter background colour
    screen.fill((10,0,0))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #print("keystroke")
            if event.key == pygame.K_LEFT:
                #print("left key")
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                #print("right key")
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                #print("key release")
                playerX_change = 0
        
    
    #change player X coord
    playerX += playerX_change
    
    #add boundaries for player
    if playerX <= 0:
        playerX = 0
    #800 - size of png
    elif playerX >= 736:
        playerX = 736
    
    #enermy movement
    for i in range(enermyCount):
        
        #game over logic
        if enermyY[i] > 440:
            for j in range(enermyCount):
                enermyY[j] = 2000
            game_over_text()
            break

        enermyX[i] += enermyX_change[i]

    #add boundaries for enermy
        if enermyX[i] <= 0:
            enermyX_change[i] = 0.5
            enermyY[i] += enermyY_change[i]
    #800 - size of png
        elif enermyX[i] >= 736:
            enermyX_change[i] = -0.5
            enermyY[i] += enermyY_change[i]
    #collision
        collision = isCollision(enermyX[i],enermyY[i],bulletX,bulletY)
    
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bulletState = "ready"
            score_value += 1
            #print(score)
            enermyX[i] = random.randint(20,720)
            enermyY[i] = 20
        
        enermy(enermyX[i],enermyY[i],i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    
    if bulletState is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    


    player(playerX,playerY)
    show_score(textX,textY)
   
    #update view
    pygame.display.update()


