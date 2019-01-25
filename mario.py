import pygame
from pygame.locals import *
pygame.init()

displayW = 800
displayH = 600

gameDisplay = pygame.display.set_mode((displayW,displayH)) #Création de fenetre
pygame.display.set_caption("Mario Bross")

#Définition de certaines couleurs
black = (0,0,0)
white = (255,255,255)


clock = pygame.time.Clock()
crashed = False
marioImg = pygame.image.load('mario_droit.png').convert_alpha()

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

    x += x_change
    y += y_change

    if x > (displayW - mario_width) or x < 0:
        gameExit = True


    gameDisplay.fill(white)
    mario(x, y)

    pygame.display.update()
    clock.tick(60)



pygame.quit()
quit()
