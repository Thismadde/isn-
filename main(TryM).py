import pygame
import time
pygame.init()



HEIGTH_display = 768
WIDTH_display = 1280
x = 50
y = 768-3*64
width = 50
height = 60
vel = 2
TILESIZE = 64

FPS = 500


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
goomba_img = pygame.transform.scale(goomba_img, (50,50))
coin_img = pygame.image.load("data/sprites/coin-64.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (30,30))
background_img = pygame.image.load("data/map/mapclean.png").convert()
width_fond = background_img.get_width()
print(width_fond)

brick_img = pygame.image.load("data/sprites/brick_64.png").convert()
terre = pygame.image.load("data/sprites/sol_2-64.png").convert()
terre_herbe = pygame.image.load("data/sprites/sol_1-64.png").convert()
Block_surprise = pygame.image.load("data/sprites/BlockUuh-64.png").convert()

run = True
CanDoIt = True

RED = (255,0,0)
BLUE = (0, 0, 50)
BROWN = (150,75,0)

niveau = "data/map/mapclean.txt"
rang_colonne = 0
rang = 0
time_sleep = 500

ciel = []
brick = []
brick = []
terre_herbe_array = []
terre_array = []
surprise_array = []

all_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()
goomba_sprites = pygame.sprite.Group()
sol_sprites = pygame.sprite.Group()
ciel_sprites = pygame.sprite.Group()

''' FONT SYSTEM : '''
myfont = pygame.font.SysFont("monospace",30)
''''''''''''''''''''


#def Updating_After_Player(x,y):
#    map.draw()
"""
    x_ancien = round(x/TILESIZE)*TILESIZE
    y_ancien = round(y/TILESIZE)*TILESIZE
    for i in range(-2,3):
        for z in range(-2,3):
            if(x_ancien+(i*TILESIZE),y_ancien+z*TILESIZE) in ciel:
                win.blit(blue_img,((x_ancien+i*TILESIZE),y_ancien+z*TILESIZE))
"""
class goomba(pygame.sprite.Sprite):
    def __init__(self,x,y,win):
        pygame.sprite.Sprite.__init__(self,goomba_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = goomba_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.x = x
        self.Vgravite = 1
        self.orientation = "Right"
        self.canCollind = True
        self.health = 1
    def Afficher(self):
        self.win.blit(self.image,(self.x,self.y))
        
    def lives(self):
        if self.health == 0:
            map.draw()
            self.canCollind = False
        
        
class coin(pygame.sprite.Sprite):
    def __init__(self,x,y,win):
        pygame.sprite.Sprite.__init__(self,coin_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.x = x
        self.win = win
    def Afficher(self):
        self.win.blit(self.image,(self.x,self.y))

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
        pygame.sprite.Sprite.__init__(self)
        self.width = 50
        self.height = 60
        self.image = pygame.Surface((self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.Vgravite = 1
        self.orientation = "Right"
        self.isCollinding = True
        self.isJumping = False
        self.jumpCount = 10
        self.vies = 3
        self.health = 1
        self.pieces = 0
        
    def pickup(self):
        if player.collision_with_coin() == True:
            player.pieces += 1

    def lives(self):
        if self.health == 0:
            self.vies -=  1
            map.draw()
            self.rect.x = 50
            self.rect.y = 768-3*64
            camera.update(player)
            self.health = 1
        if self.pieces == 100:
            self.vies += 1
            self.pîeces = 0

    def updatelives(self):
        win.blit(mario_vie,(360,5))
        textfont = myfont.render("X"+str(self.vies),3,RED)
        win.blit(textfont,(400,5))

    def updatecoin(self):
        win.blit(coin_img,(260,5))
        textfont = myfont.render("X"+str(self.pieces),3,RED)
        win.blit(textfont,(295,5))

    def isCollindingWithGround(self): #Fonction pour vérifier si touche le sol , marche pas vraiment pour l'instant
        self.rect.y += 10
        blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
        self.rect.y -= 10
        if not(blocks_hit_list == []):
            self.isCollinding = True
            return True
        else:
            self.isCollinding = False
            while not self.isCollinding:
                self.rect.y += 10
                blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
                self.rect.y -= 10
                if (blocks_hit_list == []):
                    self.rect.y += self.Vgravite
                    print(self.rect.y)
                    self.orientation = "Down"
                    self.draw_player()
                else:
                    self.isCollinding = True
                    print("False")
                    return True         
                time.sleep(0.01)   
                    
    def collision_while_jumping(self,negative):
        if(self.isJumping):
            self.rect.y -= self.jumpCount ** 2 * 0.5 * negative
            blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
            if not(blocks_hit_list == []):
                self.rect.y += (self.jumpCount ** 2 * 0.5 * negative)*2
                return True
            else:
                self.rect.y += (self.jumpCount ** 2 * 0.5 * negative)
                return False

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

    def collision_with_coin(self):
        if self.orientation == "Right":
            self.rect.x += vel
            coin_hit_list = pygame.sprite.spritecollide(self,coin_sprites,False)
            if not(coin_hit_list == []):
                return True
            else:
                return False
        if self.orientation == "Left":
            self.rect.x -= vel
            coin_hit_list = pygame.sprite.spritecollide(self,coin_sprites,False)
            if not(coin_hit_list == []):
                return True
            else:
                return False
        if self.orientation == "Down":
            self.rect.y += vel
            coin_hit_list = pygame.sprite.spritecollide(self,coin_sprites,False)
            if not(coin_hit_list == []):
                return True
            else:
                return False
        if self.orientation == "Up":
            self.rect.y -= vel
            coin_hit_list = pygame.sprite.spritecollide(self,coin_sprites,False)
            if not(coin_hit_list == []):
                return True
            else:
                return False

    def draw_player(self):
        if (self.orientation == "Right"):
            x_new = camera.apply_player([self.rect.x])
            win.blit(mario_up,(x_new,self.rect.y))
        if (self.orientation == "Left"):
            x_new = camera.apply_player([self.rect.x])
            win.blit(mario_left,(x_new,self.rect.y))
        if (self.orientation == "Up"):
            x_new = camera.apply_player([self.rect.x])
            win.blit(mario_up,(x_new,self.rect.y))
        if (self.orientation == "Down"):
            x_new = camera.apply_player([self.rect.x])
            win.blit(mario_up,(x_new,self.rect.y))

    def moove(self,keys):
        #self.isCollindingWithGround()
        if keys[pygame.K_LEFT]:
            self.orientation = "Left"
            if not(self.x - vel<0) and not self.collision_with_walls():
                map.draw()
                self.rect.x -= vel
                camera.update(player)
                self.draw_player()
        if keys[pygame.K_RIGHT]:
            self.orientation = "Right"
            if not self.collision_with_walls():
                map.draw()
                self.rect.x += vel
                camera.update(player)
                self.draw_player()
        if not (self.isJumping):
            if keys[pygame.K_DOWN]:
                self.orientation = "Down"
                if not ((self.y+vel)>HEIGTH_display-height)and not self.collision_with_walls():
                    map.draw()
                    self.rect.y += vel
                    camera.update(player)
                    self.draw_player()
            if keys[pygame.K_UP]:
                self.orientation = "Up"
                if not ((self.y-vel)<0)and not self.collision_with_walls():
                    map.draw()
                    self.rect.y -= vel
                    camera.update(player)
                    self.draw_player()
            #self.draw_player()
            #if keys[pygame.K_SPACE]:
            #   self.isJumping = True
        """if (self.isJumping): Fonction de saut a ameliorer
            if self.jumpCount >= -10:
                negative = 1
                self.orientation = "Up"
                if self.jumpCount < 1:
                    self.orientation = "Down"
                    negative = -1
                if not self.collision_while_jumping(negative):
                #if not ((y - jumpCount ** 2 * 0.1) < 0):
                # y -= jumpCount*0.01 * 2 * 0.5
                    Updating_After_Player(self.rect.x,self.rect.y)
                    self.rect.y -= self.jumpCount ** 2 * 0.5 * negative
                    self.draw_player()
                    self.jumpCount -= 1
                #print("Jump " + str(jumpCount))
                #else :
                #   jumpCount = 10
                #  isJumping = False
            else:
                self.isJumping = False
                self.jumpCount = 10
            """
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
        self.y = y
        self.x = x
        brick.append((self.x,self.y))
        self.win = win
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

class Map(pygame.sprite.Sprite):
    def __init__(self,WIDTH_display,HEIGHT_display,First_Load):
        z = 5
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
                        rang = rang + 1
                    rang_colonne += 1
                    rang = 0
                rang_colonne = 0
            #print(ciel)
            self.load = False
        else:

            win.blit(background_img, (camera.apply_player([0]),-64*2))
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
all_sprites.add(player)
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
#font = ImageFont.truetype('Roboto-Bold.ttf', size=4)
'''def draw_vie():
    pygame.draw.rect(win,RED,[0,0,150,50],2)
    win.blit(mario_vie,(2,5))
    draw.text((42,35/2), "x"+self.vies, font=font )
'''
while run:
    clock = pygame.time.Clock()
    milliseconds = clock.tick(FPS)
    #if (time_sleep > -500):
     #   time_sleep -= -1
    #else:
     #   time_sleep = 500

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            print("Moyenne des FPS :" + str(fps_all/number))
        #Compteur de FPS
        elif event.type == USEREVENT:
            fps_label = font_cambria.render('FPS : {:.2f}'.format(timer.get_fps()), True, RED)
            fps_all += timer.get_fps()
            number += 1
            fps_rect = fps_label.get_rect()
    keys = pygame.key.get_pressed()
    player.moove(keys)
    #Compteur de FPS :
    dt = timer.tick() / 1000
    win.blit(blue_img,(0,0))
    win.blit(blue_img,(TILESIZE,0))
    win.blit(fps_label,fps_rect)
    #draw_vie()
    #Fin du compteur
    player.updatelives()
    player.updatecoin()
    pygame.display.update()

    
     

pygame.quit()
