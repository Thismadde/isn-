import pygame
pygame.init()




HEIGTH_display = 768
WIDTH_display = 1280
x = 50
y = 768-3*64
width = 50
height = 60
vel = 5
TILESIZE = 64

FPS = 500


win = pygame.display.set_mode((WIDTH_display,HEIGTH_display))
pygame.display.set_caption("Super Mario Bross")
blue_img = pygame.image.load("data/sprites/blue.png").convert()
brick_img = pygame.image.load("data/sprites/brick_64.png").convert()
mario_up = pygame.image.load("data/sprites/mario_droit.png").convert_alpha()
mario_up = pygame.transform.scale(mario_up, (50,60))
background_img = pygame.image.load("data/map/background.png").convert()

run = True


RED = (255,0,0)
BLUE = (0, 0, 50)
BROWN = (150,75,0)

niveau = "data/map/map2.txt"
rang_colonne = 0
rang = 0
time_sleep = 500

ciel = []
brick = []
five = []
four = []
seven = []
six = []

all_sprites = pygame.sprite.Group()
sol_sprites = pygame.sprite.Group()
ciel_sprites = pygame.sprite.Group()


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
class Camera:
    def __init__(self,width,height):
        self.camera = pygame.Rect(0,0,width,height)
        self.width = width
        self.height = height
    def apply(self,entity):
        x_cam = entity[0] + self.camera.x
        return (x_cam)
    def update(self,target):
        x = -target.rect.x + (WIDTH_display/2)
        y = -target.rect.y + (HEIGTH_display/2)
        x = min(0, x)  # left
        self.camera = pygame.Rect(x,y,self.width,self.height)

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
        self.orientation = "Right"
        self.isCollinding = True
        self.isJumping = False
        self.jumpCount = 10
    """def isCollindingWithGround(self): Fonction pour vérifier si touche le sol , marche pas vraiment pour l'instant
        self.rect.y += 10
        blocks_hit_list = pygame.sprite.spritecollide(self,sol_sprites,False)
        print(blocks_hit_list)
        self.rect.y -= 10
        if not(blocks_hit_list == []):
            self.isCollinding = True
            print("True")
        else:
            self.isCollinding = False
            print("False")
    """
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


    def draw_player(self):
        x_new = camera.apply([self.rect.x])
        win.blit(mario_up,(x_new,self.rect.y))
    def moove(self,keys):
        #if (self.isCollinding):
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
    def __init__(self,x,y,win):
        pygame.sprite.Sprite.__init__(self, sol_sprites)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = brick_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.x = x
        brick.append((self.x,self.y))
        self.win = win
        self.Afficher()
    def Afficher(self):
        self.win.blit(brick_img,(self.x,self.y))

class Map(pygame.sprite.Sprite):
    def __init__(self,WIDTH_display,HEIGHT_display,First_Load):
        self.width = WIDTH_display
        self.height = HEIGHT_display
        self.load = First_Load
        self.draw()

    def draw(self):
        win.blit(background_img, (0, 0))
        global rang_colonne
        global rang
        global ciel
        global brick
        if self.load:
            with open(niveau,"r") as f:
                for ligne in f:
                    for i in ligne:
                        #if i == "0":
                            #Ciel(rang*TILESIZE,rang_colonne*TILESIZE,win) C'est en train d'être remplacé par le background
                            #ciel.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "2" or i == "1":
                            Sol(rang*TILESIZE,rang_colonne*TILESIZE,win)

                        rang = rang + 1
                    rang_colonne += 1
                    rang = 0
                rang_colonne = 0
            #print(ciel)
            self.load = False
        else:
            win.blit(background_img, (camera.apply([0]),0))
            for sprite in brick:
                win.blit(brick_img,(camera.apply(sprite),sprite[1]))
            """for sprite in ciel: Même chose remplacé par le background
                win.blit(blue_img,(camera.apply(sprite),sprite[1]))
            """





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
    #Fin du compteur

    pygame.display.update()
pygame.quit()
