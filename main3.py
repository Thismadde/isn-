import pygame
import time
import random
import os
pygame.init()



HEIGTH_display = 768
WIDTH_display = 1280
x = 100
y = 768-6*64
width = 50
height = 60
vel = 2
velgoomba = 1
TILESIZE = 64


FPS = 500

GameOverMenu = False
GamePauseMenu = False

win = pygame.display.set_mode((WIDTH_display,HEIGTH_display))
pygame.display.set_caption("Super Mario Bross")
blue_img = pygame.image.load("data/sprites/blue.png").convert()

mario_up = pygame.image.load("data/sprites/mario_droit.png").convert_alpha()
mario_up = pygame.transform.scale(mario_up, (50,60))
mario_left = pygame.image.load("data/sprites/mario_gauche.png").convert_alpha()
mario_left = pygame.transform.scale(mario_left, (50,60))
mario_vie = pygame.image.load("data/sprites/tete mario.png")
mario_vie = pygame.transform.scale(mario_vie, (30,30))
goomba_img = pygame.image.load("data/sprites/goomba-64.png").convert_alpha()
game_over = pygame.image.load("data/gameover/GameOver.png").convert()
game_pause = pygame.image.load("data/gameover/Menu_Pause.png").convert()
champi_img = pygame.image.load("data/sprites/champi.png")
up_img = pygame.image.load("data/sprites/1up.png")
up_img = pygame.transform.scale(up_img, (40,40))

def load_images(path):
    global images
    images = []
    for file_name in os.listdir(path="data/courtmariocourt"):
        image = pygame.image.load(path + os.sep + file_name).convert_alpha()
        image = pygame.transform.scale(image, (50,60))
        images.append(image)
        print("okk")
    return images

images = load_images(path='data/courtmariocourt')

background_img = pygame.image.load("data/map/map200.png").convert()
width_fond = background_img.get_width()

brick_img = pygame.image.load("data/sprites/brick_64.png").convert()
terre = pygame.image.load("data/sprites/sol_2-64.png").convert()
terre_herbe = pygame.image.load("data/sprites/sol_1-64.png").convert()
Block_surprise = pygame.image.load("data/sprites/BlockUuh-64.png").convert()
coin_img = pygame.image.load("data/sprites/coin-64.png").convert_alpha()

run = True
CanDoIt = True

RED = (255,0,0)
BLUE = (0, 0, 50)
BROWN = (150,75,0)

niveau = "data/map/map_200.txt"
rang_colonne = 0
rang = 0
time_sleep = 500
past_time = 0

all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
sol_sprites = pygame.sprite.Group()
surprise_sprites = pygame.sprite.Group()
ciel_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()
goomba_sprites = pygame.sprite.Group()
champi_sprites = pygame.sprite.Group()
up_sprites = pygame.sprite.Group()

myfont = pygame.font.SysFont("monospace",30)

class champi(pygame.sprite.Sprite):
    def __init__(self,x,y,win):
        pygame.sprite.Sprite.__init__(self,champi_sprites)
        self.width = TILESIZE
        self.height = TILESIZE 
        self.image = champi_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.Vgravite = 0.25
        self.exist = True
        self.x = x
        self.y = y
        self.orientation = "Right"

    def update(self):
        if self.exist:
            win.blit(self.image,(camera.apply_player([self.rect.x]),self.rect.y))
        self.collision()
    def collision(self):
        blocks_hit_list = pygame.sprite.spritecollide(self,player_sprite,False)
        if (not (blocks_hit_list == [])):
            self.exist = False
            if player.health < 150:
                player.health += 50
            else:
                player.score += 50
            champi_sprites.remove(self)  
    def draw_champi(self):
        x_new = camera.apply_player([self.rect.x])
        win.blit(champi_img,(x_new,self.rect.y))
    def move(self):
        if self.exist == True:
            if self.orientation == "Left":
                self.rect.x -= velgoomba
                blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                if not(blocks_hit_list == []):
                    self.rect.x += velgoomba 
                    self.orientation = "Right"
            if self.orientation == "Right":
                self.rect.x += velgoomba
                blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                if not(blocks_hit_list == []):
                    self.rect.x -= velgoomba*2 
                    self.orientation = "Left"
            self.gravity()
            self.draw_champi()
            player.draw_player()
    def gravity(self):
        self.collision_with_ground = False
        if not self.collision_with_ground:
            if self.Vgravite < 1.5:
                self.rect.y += self.Vgravite
                self.Vgravite += 0.3
            else: 
                self.rect.y += self.Vgravite
                self.Vgravite += 0.05
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                Collision = True
                self.collision_with_ground = True
                while Collision: 
                    blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                    if not (blocks_hit_list == []):
                        self.rect.y -= 1
                        self.Vgravite = 0.25
                    else:
                        Collision = False
            else:
                self.draw_champi()

class up(pygame.sprite.Sprite):
    def __init__(self,x,y,win):
        pygame.sprite.Sprite.__init__(self,up_sprites)
        self.width = TILESIZE
        self.height = TILESIZE 
        self.image = up_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.Vgravite = 0.25
        self.exist = True
        self.x = x
        self.y = y
        self.orientation = "Right"
    def update(self):
        if self.exist:
            win.blit(self.image,(camera.apply_player([self.rect.x]),self.rect.y))
            self.collision() 
    def collision(self):
        blocks_hit_list = pygame.sprite.spritecollide(self,player_sprite,False)
        if (not (blocks_hit_list == [])):
            self.exist = False
            player.vies += 1
            player.score += 100
            up_sprites.remove(self)  


    def draw_up(self):
        x_new = camera.apply_player([self.rect.x])
        win.blit(up_img,(x_new,self.rect.y))
    def move(self):
        if self.exist == True:
            if self.orientation == "Left":
                self.rect.x -= velgoomba
                blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                if not(blocks_hit_list == []):
                    self.rect.x += velgoomba 
                    self.orientation = "Right"
            if self.orientation == "Right":
                self.rect.x += velgoomba
                blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                if not(blocks_hit_list == []):
                    self.rect.x -= velgoomba*2 
                    self.orientation = "Left"
            self.gravity()
            self.draw_up()
            player.draw_player()
    def gravity(self):
        self.collision_with_ground = False
        if not self.collision_with_ground:
            if self.Vgravite < 1.5:
                self.rect.y += self.Vgravite
                self.Vgravite += 0.3
            else: 
                self.rect.y += self.Vgravite
                self.Vgravite += 0.05
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                Collision = True
                self.collision_with_ground = True
                while Collision:
                    blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                    if not (blocks_hit_list == []):
                        self.rect.y -= 1
                        self.Vgravite = 0.25
                    else:
                        Collision = False
            else:
                self.draw_up()       

class goomba(pygame.sprite.Sprite):
    def __init__(self,x,y,win):
        pygame.sprite.Sprite.__init__(self,goomba_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = goomba_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.Vgravite = 1
        self.exist = True
        self.health = 1
        self.x = x
        self.y = y
        self.orientation = "Left"
    def update(self):
        if self.exist:
            win.blit(self.image,(camera.apply_player([self.rect.x]),self.rect.y))
        self.collision()
    def collision(self):
        blocks_hit_list = pygame.sprite.spritecollide(self,player_sprite,False)
        if ((not (blocks_hit_list == [])) and (player.rect.y < (self.rect.y - 40))):
            self.exist = False
            player.score += 500
            goomba_sprites.remove(self)  
        elif ((player.collisionLocked == False) and not (blocks_hit_list == [])):  
            player.collisionLocked = True
            global past_time
            past_time = time.time()         
            player.health -= 50      
    def draw_goomba(self):
        x_new = camera.apply_player([self.rect.x])
        win.blit(goomba_img,(x_new,self.rect.y))
    def move(self):
        if self.exist == True:
            if self.orientation == "Left":
                self.rect.x -= velgoomba
                blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                if not(blocks_hit_list == []):
                    self.rect.x += velgoomba
                    self.orientation = "Right"
            if self.orientation == "Right":
                self.rect.x += velgoomba
                blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                if not(blocks_hit_list == []):
                    self.rect.x -= velgoomba
                    self.orientation = "Left"

  
class Camera:
    def __init__(self,width,height):
        self.camera = pygame.Rect(0,0,width,height)
        self.width = width
        self.x = 0
        self.y = 0
        self.height = height
    def apply_player(self,entity):
        x_cam = entity[0] + self.camera.x
        return x_cam    
    def update(self,target):
        self.x = -target.rect.x + (WIDTH_display/2)
        self.y = -target.rect.y + (HEIGTH_display/2)
        self.x = min(0, self.x)
        if(self.x < -width_fond + WIDTH_display):
            self.x = -width_fond + WIDTH_display
        self.camera = pygame.Rect(self.x,self.y,self.width,self.height)

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,player_sprite)
        self.width = 50
        self.height = 60
        self.image = pygame.Surface((self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.orientation = "Right"
        self.isCollinding = True
        self.isJumping = False
        self.jumpCount = 50
        self.vies = 3
        self.health = 100
        self.collision_with_ground = True
        self.score = 0
        self.collisionLocked = False
        self.Vgravite = 0.25
        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images] 
        self.index = 0
        self.image = images[self.index]
        self.animation_time = 150
        self.current_time = 0
        self.isWalking = "False"
    def update_time_dependent(self, dt):
        if self.orientation == "Right" : 
            self.images = self.images_right
        elif self.orientation == "Left":
            self.images = self.images_left

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
    def update(self, dt):
        self.update_time_dependent(dt)

    def lives(self):
        if self.health == 0 or self.rect.y >=768:
            self.vies -=  1
            player.draw_player()
            self.rect.x = 50
            self.rect.y = 768-3*64
            camera.update(player)
            self.health = 50
        if self.vies == 0:
            global GameOverMenu
            GameOverMenu = True
    def invincibilite(self):
        new_time = time.time()
        if new_time - past_time < 3:
            new_time = time.time()
        else:
            self.collisionLocked = False
    def updatelives(self):
        if self.collisionLocked == True:
            player.invincibilite()
        win.blit(mario_vie,(360,5))
        textfont = myfont.render("X"+str(self.vies),3,RED)
        win.blit(textfont,(400,5))  

        player_score = myfont.render("Pts X"+str(self.score),3,RED)
        win.blit(player_score,(500,5)) 

    def gravity(self):
        self.collision_with_ground = False
        if not self.collision_with_ground:
            if self.Vgravite < 1.5:
                self.rect.y += self.Vgravite
                self.Vgravite += 0.1
            else: 
                self.rect.y += self.Vgravite
                self.Vgravite += 0.05
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                Collision = True
                self.collision_with_ground = True
                old_y = self.rect.y
                while Collision: #Système de collision amélioré Pour etre sur que le joueur touche le sol pile poil a 100%
                    blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                    if not (blocks_hit_list == []):
                        self.rect.y -= 1
                        self.Vgravite = 0.25
                    else:
                        Collision = False
                    if old_y - self.rect.y > 10: #Eviter le bug du player qui passe au dessus
                        Collision = False
                        self.rect.y = old_y + 1
            else:
                player.draw_player()               
    def collision_with_walls(self):
        if self.orientation == "Right":
            self.rect.x += vel
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            self.rect.x -= vel
            if not(blocks_hit_list == []):
                return True
            else:
                return False
        if self.orientation == "Left":
            self.rect.x -= vel
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            self.rect.x += vel
            if not(blocks_hit_list == []):
                return True
            else:
                return False
        if self.orientation == "Down":
            self.rect.y += vel
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            self.rect.y -= vel
            if not(blocks_hit_list == []):
                return True
            else:
                return False
        if self.orientation == "Up":
            self.rect.y -= vel
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            self.rect.y += vel
            if not(blocks_hit_list == []):
                return True
            else:
                return False
    def draw_player(self):
        if (self.orientation == "Right"):
            x_new = camera.apply_player([self.rect.x])
            win.blit(self.image,(x_new,self.rect.y))
        if (self.orientation == "Left"):
            x_new = camera.apply_player([self.rect.x])
            win.blit(self.image,(x_new,self.rect.y))
        if (self.orientation == "Up"):
            x_new = camera.apply_player([self.rect.x])
            win.blit(self.image,(x_new,self.rect.y))
        if (self.orientation == "Down"):
            x_new = camera.apply_player([self.rect.x])
            win.blit(self.image,(x_new,self.rect.y))
    def jump(self):
        if 0<= self.jumpCount <=50:
            self.rect.y -= self.jumpCount**2 * 0.005
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            blocks_hit_list2 = pygame.sprite.spritecollide(self,surprise_sprites,False)
            for hit_blocks in blocks_hit_list2:
                hit_blocks.transform_to_rock()
            if not(blocks_hit_list == []):
                self.rect.y += self.jumpCount**2 * 0.005 
                self.isJumping = False
                self.jumpCount = 50
            self.jumpCount -= 1
        else:
            self.isJumping = False
            self.jumpCount = 50
        self.draw_player()
    def moove(self,keys):  
        if keys[pygame.K_ESCAPE]:
            global GamePauseMenu
            GamePauseMenu = True
            print("youpi")
        if self.isJumping:
            self.jump()
            if keys[pygame.K_LEFT]:
                self.orientation = "Left"
                if not(self.x - vel<0) and not self.collision_with_walls():
                    self.rect.x -= vel
                    camera.update(player)
                    self.update(dt)
            if keys[pygame.K_RIGHT]:
                self.orientation = "Right"
                if not self.collision_with_walls():
                    self.rect.x += vel
                    camera.update(player)
                    self.update(dt)
        else:
            self.gravity()
            if keys[pygame.K_LEFT]:
                self.orientation = "Left"
                if not(self.x - vel<0) and not self.collision_with_walls():
                    self.rect.x -= vel
                    camera.update(player)
                    self.update(dt)
                else:
                    camera.update(player)
                    self.draw_player()
            if keys[pygame.K_RIGHT]:
                self.orientation = "Right"
                if not self.collision_with_walls():
                    self.rect.x += vel
                    camera.update(player)
                    self.update(dt)
                else:
                    camera.update(player)
                    self.draw_player()
            if (not self.isJumping):
                if keys[pygame.K_DOWN]:
                    self.orientation = "Down"
                    if not ((self.y+vel)>HEIGTH_display-height)and not self.collision_with_walls():
                        self.rect.y += vel
                        camera.update(player)  
                        self.draw_player()
                if keys[pygame.K_UP]:
                    if self.collision_with_ground:
                        self.isJumping = True
            return x,y


class Sol(pygame.sprite.Sprite):
    def __init__(self,x,y,win,image):
        pygame.sprite.Sprite.__init__(self, sol_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.win = win
class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y,win,image):
        print("POPO")
        pygame.sprite.Sprite.__init__(self,coin_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.win = win
        self.exist = True
    def update(self):
        if self.exist:
            win.blit(self.image,(camera.apply_player([self.rect.x]),self.rect.y))
            self.collision()
    def collision(self):
        blocks_hit_list = pygame.sprite.spritecollide(self,player_sprite,False)
        if not (blocks_hit_list == []):
            coin_sprites.remove(self)
            self.exist = False
            player.score += 50

class Surprise(pygame.sprite.Sprite):
    def __init__(self,x,y,win):
        pygame.sprite.Sprite.__init__(self, sol_sprites)
        pygame.sprite.Sprite.__init__(self, surprise_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = Block_surprise
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.win = win
        self.exist = True
    def update(self):
        win.blit(self.image,(camera.apply_player([self.rect.x]),self.rect.y))
    def transform_to_rock(self):   
        liste = ["coin","up","champi","coin","coin","coin","coin","coin","coin","coin"]
        result = random.choice(liste)
        if result == "coin":
            Coin(self.rect.x, self.rect.y - 64, win,coin_img)
        elif result == "up":
            up(self.rect.x, self.rect.y, win)
        elif result == "champi":
            champi(self.rect.x, self.rect.y, win)
        self.image = brick_img
        surprise_sprites.remove(self)
        
        



class Map(pygame.sprite.Sprite):
    def __init__(self,WIDTH_display,HEIGHT_display,First_Load):
        self.width = WIDTH_display
        self.height = HEIGHT_display
        self.load = First_Load
        self.draw()

    def draw(self):
        win.blit(background_img, (0, -TILESIZE*2))
        global rang_colonne
        global rang
        if self.load:
            with open(niveau,"r") as f:
                for ligne in f:
                    for i in ligne:
                        if i == "4":
                            Sol(rang*TILESIZE,rang_colonne*TILESIZE,win,brick_img)
                        if i == "2":
                            Sol(rang*TILESIZE,rang_colonne*TILESIZE,win,terre)
                        if i == "3":
                            Sol(rang*TILESIZE,rang_colonne*TILESIZE,win,terre_herbe)
                        if i == "5":
                            Surprise(rang*TILESIZE,rang_colonne*TILESIZE,win)
                        if i == "a":
                            Coin(rang*TILESIZE,rang_colonne*TILESIZE,win,coin_img)
                        if i == "g":
                            goomba(rang*TILESIZE,rang_colonne*TILESIZE,win)
                        rang += 1
                    rang_colonne += 1
                    rang = 0
                rang_colonne = 0
            self.load = False
        else:

            win.blit(background_img, (camera.apply_player([0]),-64*2))
            player.updatelives()
            coin_sprites.update()
            goomba_sprites.update()
            champi_sprites.update()
            up_sprites.update()

camera = Camera(WIDTH_display,HEIGTH_display)
player = Player(x,y)
First_Load = True
map = Map(WIDTH_display,HEIGTH_display,First_Load)

player.draw_player()

pygame.display.update()


timer = pygame.time.Clock()
font_cambria = pygame.font.SysFont('Cambria',24)
fps_label = font_cambria.render('FPS : {}'.format(timer.get_fps()), True, RED)
fps_rect = fps_label.get_rect()

USEREVENT = 24
pygame.time.set_timer(USEREVENT, 1000)
fps_all = 0
number = 0
while run:
    if GamePauseMenu == True:
        print('yes')
        win.blit(game_pause,(0,0))
        
    dt = timer.tick(FPS)
    #player.update(dt)
    if GamePauseMenu == True:
        win.blit(game_pause,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    GamePauseMenu = False
    if GameOverMenu == True:
        win.blit(game_over,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if event.button == 1 and 510 < position[0] <810 and 565 < position[1] < 865:
                    GameOverMenu = False  
                    player.vies = 3
                    player.health = 50
    elif GameOverMenu == False and GamePauseMenu == False:
        map.draw()
        surprise_sprites.update()
        player.draw_player()
        clock = pygame.time.Clock()
        milliseconds = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print("Moyenne des FPS :" + str(fps_all/number))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.isJumping = True

            elif event.type == USEREVENT:
                fps_label = font_cambria.render('FPS : {:.2f}'.format(timer.get_fps()), True, RED)
                fps_all += timer.get_fps()
                number += 1
                fps_rect = fps_label.get_rect()
        keys = pygame.key.get_pressed() 

        for goomba_list in goomba_sprites:
            goomba_list.move()

        for champi_list in champi_sprites:
            champi_list.move()

        for up_list in up_sprites:
            up_list.move()

        player.moove(keys)
        player.lives()
        Player.update(player,dt)
        #Compteur de FPS :
        dt = timer.tick() / 1000
        win.blit(blue_img,(0,0))
        win.blit(blue_img,(TILESIZE,0))
        win.blit(fps_label,fps_rect)
        #Fin du compteur  
         
    pygame.display.update()

    
     

pygame.quit()
