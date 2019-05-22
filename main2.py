import pygame
import os
import time
pygame.init()



HEIGTH_display = 768
WIDTH_display = 1280
x = 100
y = 768-6*64
width = 50
height = 60
vel = 2
TILESIZE = 64

FPS = 500

GameOverMenu = False
Tnul = False

win = pygame.display.set_mode((WIDTH_display,HEIGTH_display))
pygame.display.set_caption("Super Mario Bross")
blue_img = pygame.image.load("data/sprites/blue.png").convert()

mario_up = pygame.image.load("data/sprites/mario_droit.png").convert_alpha()
mario_up = pygame.transform.scale(mario_up, (50,60))
mario_left = pygame.image.load("data/sprites/mario_gauche.png").convert_alpha()
mario_left = pygame.transform.scale(mario_left, (50,60))
#mario_step_1 = pygame.image.load("data/sprites/mario step 1.png").convert_alpha()
#mario_step_1 = pygame.transform.scale(mario_step_1, (50,60))
#mario_step_2 = pygame.image.load("data/sprites/mario step 2.png").convert_alpha()
#mario_step_2 = pygame.transform.scale(mario_step_2, (50,60))
#mario_step_3 = pygame.image.load("data/sprites/mario step 3.png").convert_alpha()
#mario_step_3 = pygame.transform.scale(mario_step_3, (50,60))
mario_vie = pygame.image.load("data/sprites/tete mario.png")
mario_vie = pygame.transform.scale(mario_vie, (30,30))
goomba_img = pygame.image.load("data/sprites/goomba-64.png").convert_alpha()
#goomba_img = pygame.transform.scale(goomba_img, (50,50))
game_over = pygame.image.load("data/gameover/GameOver.png").convert()
attente = pygame.image.load("data/attente/fond noir.png").convert()

def load_images(path):
    global images
    images = []
    for file_name in os.listdir(path="data/courtmariocourt"):
        image = pygame.image.load(path + os.sep + file_name).convert()
        image = pygame.transform.scale(image, (50,60))
        images.append(image)
        print("okk")
    return images

images = load_images(path='data/courtmariocourt')  

background_img = pygame.image.load("data/map/mapclean_light.png").convert()
width_fond = background_img.get_width()

brick_img = pygame.image.load("data/sprites/brick_64.png").convert()
terre = pygame.image.load("data/sprites/sol_2-64.png").convert()
terre_herbe = pygame.image.load("data/sprites/sol_1-64.png").convert()
Block_surprise = pygame.image.load("data/sprites/BlockUuh-64.png").convert()
coin_img = pygame.image.load("data/sprites/coin-64.png").convert_alpha()
fin_img = pygame.image.load("data/sprites/damier.png")

run = True
CanDoIt = True

RED = (255,0,0)
BLUE = (0, 0, 50)
BROWN = (150,75,0)

niveau = "data/map/mapclean.txt"
rang_colonne = 0
rang = 0
time_sleep = 500
past_time = 0
old_time = 0

ciel = []
brick = []
brick = []
terre_herbe_array = []
terre_array = []
surprise_array = []
Coin_array = []
fin_array =[]
# Groupe de sprites nécaissaires pour tester les collisions entre groupe :
all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
sol_sprites = pygame.sprite.Group()
surprise_sprite = pygame.sprite.Group()
ciel_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()
goomba_sprites = pygame.sprite.Group()
fin_sprites = pygame.sprite.Group()

''' FONT SYSTEM : '''
myfont = pygame.font.SysFont("monospace",30)
''''''''''''''''''''

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
        self.orientation = 0
    def update(self):
        if self.exist:
            win.blit(self.image,(camera.apply_player([self.rect.x]),self.rect.y))
        self.collision()
    def collision(self):
        blocks_hit_list = pygame.sprite.spritecollide(self,player_sprite,False)
        if ((not (blocks_hit_list == [])) and (player.rect.y < (self.rect.y))):
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
            if self.orientation == 0:
                self.rect.x -= 0.01*vel
                blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                if not(blocks_hit_list == []):
                    self.rect.x += vel*2 
                else:
                    self.rect.x += vel
                    self.orientation = 1
            if self.orientation == 1:
                self.rect.x += 0.01*vel
                blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                if not(blocks_hit_list == []):
                    self.rect.x -= vel*2 
                else:
                    self.rect.x -= vel
                    self.orientation = 0
            
            self.draw_goomba()
            player.draw_player()
  
class Camera:
    def __init__(self,width,height):
        self.camera = pygame.Rect(0,0,width,height)
        self.width = width
        self.x = 0
        self.y = 0
        self.height = height
    def apply(self,entity):
        x_cam = entity[0] + self.camera.x
        return (True,x_cam)
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
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]  # Flipping every image.
        self.index = 0
        self.image = images[self.index]

       # super(Player, self).__init__()

        self.animation_time = 0.0005
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt):
        if self.orientation == "Right":  # Use the right images if sprite is moving right.
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

    def finivo(self):
         if self.rect.x == fin.rect.x:
             print("pouloulouh")
    def lives(self):
        if self.health == 0 or self.rect.y >=768:
            self.vies -=  1
            global Tnul
            Tnul = True
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
            if self.Vgravite < 1:
                self.rect.y += self.Vgravite
                self.Vgravite += 0.3
            if 1 < self.Vgravite < 1.5:
                self.rect.y += self.Vgravite
                self.Vgravite += 0.1
            else: 
                self.rect.y += self.Vgravite
                self.Vgravite += 0.05
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                Collision = True
                self.collision_with_ground = True
                while Collision: #Système de collision amélioré Pour etre sur que le joueur touche le sol pile poil a 100%
                    blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                    if not (blocks_hit_list == []):
                        self.rect.y -= 1
                        self.Vgravite = 0.25
                    else:
                        Collision = False
            else:
                #map.draw()
                player.draw_player()               
    def collision_with_walls(self):
        if self.orientation == "Right":
            self.rect.x += vel
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                self.rect.x -= vel*2
                return True
            else:
                self.rect.x -= vel
                return False
        if self.orientation == "Left":
            self.rect.x -= vel
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                self.rect.x += vel*2
                return True
            else:
                self.rect.x += vel
                return False
        if self.orientation == "Down":
            self.rect.y += vel
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                self.rect.y -= vel*2
                return True
            else:
                self.rect.y -= vel
                return False
        if self.orientation == "Up":
            self.rect.y -= vel
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                self.rect.y += vel*2
                return True
            else:
                self.rect.y += vel
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
            self.rect.y -= self.jumpCount**2 * 0.004
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                self.rect.y += self.jumpCount**2 * 0.004 ## Fonction carré donc saut en forme de parabole. **2 = au carré
                self.isJumping = False
                self.jumpCount = 50
            self.jumpCount -= 1
        else:
            self.isJumping = False
            self.jumpCount = 50
        #map.draw()
        self.draw_player()
    def move(self,keys):  
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
            if keys[pygame.K_RIGHT]:
                self.orientation = "Right"
                if not self.collision_with_walls():
                    self.rect.x += vel
                    camera.update(player)
                    self.update(dt)
            if (not self.isJumping):
                if keys[pygame.K_DOWN]:
                    self.orientation = "Down"
                    if not ((self.y+vel)>HEIGTH_display-height)and not self.collision_with_walls():
                        self.rect.y += vel
                        camera.update(player)
                        self.update(dt)    
                if keys[pygame.K_UP]:
                    if self.collision_with_ground:
                        self.isJumping = True
            return x,y
    """def walk(self):
        if keys[pygame.K_LEFT]:
            walk = True
            while walk = True:"
        Time a kan ycommence a marcher
Tant quetime clock – time commencer < 0.5sec 
Print Mario 1
tant que time clock – time commencer 0.5<t<1
Print Mario 2
Tant que time clock – time commencer 1<t<1.5
Print Mario 3
If tme clock – time commencer >= 1.5
Time commencer refresh.
"""

class Sol(pygame.sprite.Sprite):
    def __init__(self,x,y,win,image):
        pygame.sprite.Sprite.__init__(self, sol_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.x = x
        brick.append((self.x,self.y))
        self.win = win
class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y,win,image):
        pygame.sprite.Sprite.__init__(self,coin_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.x = x
        self.win = win
        self.exist = True
        #self.update()
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
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = Block_surprise
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.x = x
        self.win = win
    '''def Afficher(self):
        self.win.blit(self.image,(self.x,self.y))
    '''
class fin (pygame.sprite.Sprite):
    def __init__(self,x,y,win):
        pygame.sprite.Sprite.__init__(self, sol_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = fin_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.x = x
        self.win = win
    

class Map(pygame.sprite.Sprite):
    def __init__(self,WIDTH_display,HEIGHT_display,First_Load):
        self.width = WIDTH_display
        self.height = HEIGHT_display
        self.load = First_Load
        self.draw()
    #def Camera(self):

    def draw(self):
        win.blit(background_img, (0, -TILESIZE*2))
        global rang_colonne
        global rang
        global ciel
        global brick
        global terre_herbe_array
        global terre_array
        global surprise_array
        global Coin_array
        global fin_array
        self.data = []
        if self.load:
            with open(niveau,"r") as f:
                for ligne in f:
                    for i in ligne:
                        if i == "1":
                            Sol(rang*TILESIZE,rang_colonne*TILESIZE,win,brick_img)
                            brick.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "5":
                            Sol(rang*TILESIZE,rang_colonne*TILESIZE,win,terre)
                            terre_array.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "6":
                            Sol(rang*TILESIZE,rang_colonne*TILESIZE,win,terre_herbe)
                            terre_herbe_array.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "3":
                            Surprise(rang*TILESIZE,rang_colonne*TILESIZE,win)
                            surprise_array.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "a":
                            Coin(rang*TILESIZE,rang_colonne*TILESIZE,win,coin_img)
                            Coin_array.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "f":
                            fin(rang*TILESIZE,rang_colonne*TILESIZE,win)
                            fin_array.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        rang = rang + 1
                    rang_colonne += 1
                    rang = 0
                rang_colonne = 0
            #print(ciel)
            self.load = False
        else:

            win.blit(background_img, (camera.apply_player([0]),-64*2))
            player.updatelives()
            coin_sprites.update()
            goomba_sprites.update()

            '''
            for sprite in brick:
                win.blit(brick_img,(camera.apply(sprite[0]),sprite[1]))              
            for sprite in terre_herbe_array:
                win.blit(terre_herbe,(camera.apply(sprite[0]),sprite[1]))    
            for sprite in terre_array:
                win.blit(terre,(camera.apply(sprite[0]),sprite[1]))    
            for sprite in surprise_array:
                win.blit(Block_surprise,(camera.apply(sprite[0]),sprite[1]))    
            '''
            
            '''for sprite in brick:
                CanDoIt,x_new = camera.apply(sprite)
                if (CanDoIt == True):
                    win.blit(brick_img,(x_new,sprite[1]))              
            for sprite in terre_herbe_array:
                CanDoIt,x_new = camera.apply(sprite)
                if (CanDoIt == True):
                    win.blit(terre_herbe,(x_new,sprite[1]))    
            for sprite in terre_array:
                CanDoIt,x_new = camera.apply(sprite)
                if (CanDoIt == True):
                    win.blit(terre,(x_new,sprite[1]))    
            for sprite in surprise_array:
                CanDoIt,x_new = camera.apply(sprite)
                if (CanDoIt == True):
                    win.blit(Block_surprise,(x_new,sprite[1]))   
            '''


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

goomba1 = goomba(1000,768-3*64,win)
goomba2 = goomba(6000,768-3*64,win)
goomba1.update()
goomba2.update()
goomba1.collision()



USEREVENT = 24
pygame.time.set_timer(USEREVENT, 1000)
fps_all = 0
number = 0
while run:
    dt = timer.tick(FPS)
#    player.update(dt)


    if GameOverMenu == True:
        win.blit(game_over,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if event.button == 1 and 510 < position[0] <810 and 565 < position[1] < 865:
                    GameOverMenu = False  
                    player.vies = 3
                    player.health = 100
    if Tnul == True:
        old_time = time.time()
        time = True
    if time == True:
        newfond_time = time.time()
        if newfond_time - old_time < 3:
            win.blit(attente,(0,0))
            newfond_time = time.time()
        else:
            time = False
            Tnul = False


        
    else:
        map.draw()
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
            #Compteur de FPS
            elif event.type == USEREVENT:
                fps_label = font_cambria.render('FPS : {:.2f}'.format(timer.get_fps()), True, RED)
                fps_all += timer.get_fps()
                number += 1
                fps_rect = fps_label.get_rect()
        keys = pygame.key.get_pressed() 
        goomba1.move()
        player.move(keys)
        player.lives()
        
        #Player.update(player,dt)
        #Player.draw(screen)

        #Compteur de FPS :
        dt = timer.tick() / 1000
        win.blit(blue_img,(0,0))
        win.blit(blue_img,(TILESIZE,0))
        win.blit(fps_label,fps_rect)
        #Fin du compteur   
    pygame.display.update()

    
     

pygame.quit()
