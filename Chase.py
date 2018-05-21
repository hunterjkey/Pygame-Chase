import pygame
import random
import time
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Chase!")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#setup
pygame.mouse.set_visible(False)
roboX = 400
roboY = 400
roboXspeed = 0
roboYspeed = 0
robochange = 1
powerupX = 500
powerupY = 400
boxesX = [700, 700]
boxesY = [700, 700]
BOXESX = 0
BOXESY = 0
score = 0
health = 8
healthX = 0
powerTryCount = 0
healthmove = 0
level = 1
boxboost = 1
#this variable checks to see if the player broke the game by having too many boxes to put down the powercube
broken = False

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            #pygame.quit()
    # --- Game logic should go here

    #level management
    if (level == 1):
        if (score >= 6):
            level = 2
            robochange += 1
            boxesX *= 0
            boxesY *= 0
            boxesX.append(700)
            boxesY.append(700)
    if (level == 2):
        if (score >= 20):
            level = 3
            boxboost += 1
            boxesX *= 0
            boxesY *= 0
            boxesX.append(700)
            boxesY.append(700)
    if (level == 3):
        if (score >= 50):
            level = 4
            boxboost += 1
            boxesX *= 0
            boxesY *= 0
            boxesX.append(700)
            boxesY.append(700)
    if (level == 4):
        if (score >= 80):
            level = 5
            boxboost += 1
            boxesX *= 0
            boxesY *= 0
            boxesX.append(700)
            boxesY.append(700)

            
    pos = pygame.mouse.get_pos()
    x = pos[0]-12
    y = pos[1]-12

    #to control the robot
    if (roboX < x):
        roboXspeed = 1
    elif (roboX > x):
        roboXspeed = -1
    else:
        roboXspeed = 0

    if (roboY < y):
        roboYspeed = 1
    elif (roboY > y):
        roboYspeed = -1
    else:
        roboYspeed = 0

    roboX += (roboXspeed*robochange)
    roboY += (roboYspeed*robochange)

    #powerup collision and wall building
    if (abs(powerupX-x)<8) and (abs(powerupY-y)<8):
        score += 1
        powerupX = random.randint(50,650)
        powerupY = random.randint(50,450)
        BOXESX = random.randint(50,650)
        BOXESY = random.randint(50,450)
        if (len(boxesX)<300):
            for i in range(boxboost):
                for i in range(len(boxesX)):
                    escape = False
                    while (escape == False):
                        if (abs(BOXESX-boxesX[i])<12) and (abs(BOXESY-boxesY[i])<12):
                            BOXESX = random.randint(50,650)
                            BOXESY = random.randint(50,450)
                        else:
                            escape = True
                boxesX.append(BOXESX)
                boxesY.append(BOXESY)
            for i in range(len(boxesX)):
                escape = False
                while (escape == False):
                    powerTryCount += 1
                    if (abs(powerupX-boxesX[i])<60) and (abs(powerupY-boxesY[i])<60):
                        powerupX = random.randint(50,650)
                        powerupY = random.randint(50,450)
                    elif (powerTryCount > 200):
                        done = True
                        escape = True
                        broken = True
                    else:
                        escape = True
                        powerTryCount = 0

    #collision detection
    if (abs(x-roboX)<12) and (abs(y-roboY)<12):
        health-=1
        healthmove += 12.5
        roboX = random.randint(50,650)
        roboY = random.randint(50,450)
    for i in range(len(boxesX)-1):
        if (abs(x-boxesX[i])<12) and (abs(y-boxesY[i])<12):
            health-=1
            healthmove += 12.5
            del(boxesX[i])
            del(boxesY[i])
        #for this code, the machine wasn't registering the most recently
        #made box as an object, this code fixed that!
    c = len(boxesX)-1
    if (abs(x-boxesX[c])<12) and (abs(y-boxesY[c])<12):
        health-=1
        healthmove += 12.5
        del(boxesX[c])
        del(boxesY[c])

    #health checking code
    if (health <= 0):
        done = True
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
 
    # --- Drawing code should go here
    
    for i in range(len(boxesX)):
        pygame.draw.rect(screen, BLUE, [boxesX[i], boxesY[i], 25, 25])
    for i in range(health):
        pygame.draw.rect(screen, RED, [250+healthX+healthmove, 40, 25, 25])
        healthX += 25
    healthX = 0
    pygame.draw.rect(screen, RED, [x, y, 25, 25])
    pygame.draw.rect(screen, GREEN, [roboX, roboY, 25, 25])
    pygame.draw.rect(screen, WHITE, [powerupX, powerupY, 25, 25])

    #Score/Health text
    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render("Score: " + str(score),True,WHITE)
    screen.blit(text, [310, 15])
    healthText = font.render(str(health),True,WHITE)
    screen.blit(healthText, [343, 40])
    LevelText = font.render("Level: " + str(level),True,WHITE)
    screen.blit(LevelText, [310, 65])
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
print(score)
if (broken == True):
    print("You broke my game, good job, there was no way for you to continue!")
pygame.quit()
 

