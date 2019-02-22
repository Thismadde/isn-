#http://www.mariouniverse.com/

import pygame
from pygame.locals import *
pygame.init()

displayW = 1280
displayH = 720

gameDisplay = pygame.display.set_mode((displayW,displayH)) #Création de fenetre
pygame.display.set_caption("Mario Bross")

#Définition de certaines couleurs
black = (0,0,0)
white = (255,255,255)


clock = pygame.time.Clock()
crashed = False
marioImg = pygame.image.load('Images\Personnage\mario_droit.png').convert_alpha()
marioImg.set_alpha(128)




<<<<<<< HEAD:mario.py
=======
back = pygame.image.load("Images\Level\level1_haut.png")
>>>>>>> bdbeac4e0faed8a6f4485b17a903b4e42f155cb7:Ancienne version/mario.py
x_back = 0

def mario(x,y):
    gameDisplay.blit(marioImg, (x,y))

x = (displayW * 0.45)
y = (displayH * 0.8)
x_change = 0
y_change = 0
mario_speed = 0
mario_width = 73


while not crashed: #Tout ce qui se passe tant que le jeu ne quitte pas donc loop infine

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            elif event.key == pygame.K_RIGHT:
                x_change = 5
            elif event.key == pygame.K_UP:
                y_change = -5
            elif event.key == pygame.K_DOWN:
                y_change = 5
            elif event.key == pygame.K_INSERT:
                crashed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                x_change = 0
                y_change = 0
    gameDisplay.blit(back,(-x,0))

    x += x_change
    y += y_change

    if x > (displayW - mario_width) or x < 0:
        gameExit = True

    mario(x, y)

    pygame.display.update()
    clock.tick(60)



pygame.quit()
quit()
