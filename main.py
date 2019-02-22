import pygame
pygame.init()



x = 50
y = 50
HEIGTH_display = 768
WIDTH_display = 1280
width = 40
height = 60
vel = 15
TILESIZE = 64

FPS = 120


win = pygame.display.set_mode((WIDTH_display,HEIGTH_display))
pygame.display.set_caption("Second Game")
blue_img = pygame.image.load("data/sprites/blue.png").convert_alpha()
brick_img = pygame.image.load("data/sprites/brick_64.png").convert_alpha()
mario_up = pygame.image.load("data/sprites/mario_droit.png").convert_alpha()
mario_up = pygame.transform.scale(mario_up, (50,60 ))

run = True
isJumping = False
jumpCount = 10

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


def Updating_After_Player(x,y):
    x_ancien = round(x/TILESIZE)*TILESIZE
    y_ancien = round(y/TILESIZE)*TILESIZE
    for i in range(-2,3):
        for z in range(-2,3):
            if(x_ancien+(i*TILESIZE),y_ancien+z*TILESIZE) in ciel:
                win.blit(blue_img,((x_ancien+i*TILESIZE),y_ancien+z*TILESIZE))
def Update_Map():
    win.fill((0,0,0))
    map.draw(WIDTH_display,HEIGTH_display,First_Load)#+
    player.draw_player()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def collision_with_walls(self):
        if(x + vel,y + vel) in brick:
            return True
        return False
    def draw_player(self,x,y):
        win.blit(mario_up,(x,y))
    def moove(self,keys,x,y):
        global isJumping
        global jumpCount
        if keys[pygame.K_LEFT]:
            if not(x - vel<0): # and not self.collision_with_walls:
                Updating_After_Player(x,y)
                x -= vel
                self.draw_player(x,y)
        if keys[pygame.K_RIGHT]:
            if not(x + vel > WIDTH_display -width):
                Updating_After_Player(x,y)
                x += vel
                self.draw_player(x,y)
        if not (isJumping):
            if keys[pygame.K_DOWN]:
                if not ((y+vel)>HEIGTH_display-height): #and not self.collision_with_walls:
                    Updating_After_Player(x,y)
                    y += vel
                    self.draw_player(x,y)
            if keys[pygame.K_UP]:
                if not ((y-vel)<0): #and not self.collision_with_walls:
                    Updating_After_Player(x,y)
                    y -= vel
                    self.draw_player(x,y)
            #self.draw_player()
            if keys[pygame.K_SPACE]:
                isJumping = True
        else:
            if jumpCount >= -10:
                negative = 1
                if jumpCount < 1:
                    negative = -1
                #if not ((y - jumpCount ** 2 * 0.1) < 0):
                # y -= jumpCount*0.01 * 2 * 0.5
                Updating_After_Player(x,y)
                y -= jumpCount ** 2 * 0.5 * negative
                self.draw_player(x,y)
                jumpCount -= 1
                #print("Jump " + str(jumpCount))
                #else :
                 #   jumpCount = 10
                  #  isJumping = False
            else:
                isJumping = False
                jumpCount = 10
        return x,y

class Map(pygame.sprite.Sprite):
    def __init__(self):
        z = 5
    def draw(self,WIDTH_display,HEIGHT_display,First_Load):
        global rang_colonne
        global rang
        global ciel
        global brick
        global five
        global four
        global seven
        global six
        self.data = []
        if(First_Load):
            with open(niveau,"r") as f:
                First_Load = False
                for ligne in f:
                    lenght_ligne = len(ligne)
                    for i in ligne:
                        #pos_image = (rang*WIDTH_display/TILESIZE,rang_colonne*HEIGHT_display/TILESIZE)
                        if i == "0":
                            ciel.append((rang*TILESIZE,rang_colonne*TILESIZE))
                            win.blit(blue_img,(rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "2" or i == "1":
                            brick.append((rang*TILESIZE,rang_colonne*TILESIZE))
                            win.blit(brick_img,(rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "5":
                            five.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "6":
                            six.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "7":
                            seven.append((rang*TILESIZE,rang_colonne*TILESIZE))
                        if i == "4":
                            four.append((rang*TILESIZE,rang_colonne*TILESIZE))
                            win.blit(brick_img,(rang*TILESIZE,rang_colonne*TILESIZE))
                        rang = rang + 1
                    rang_colonne += 1
                    rang = 0
                rang_colonne = 0
            #print(ciel)
        else:
            for f in ciel:
                win.blit(blue_img,ciel[f])
            for z in brick:
                win.blit(brick_img,brick[z])


ciel_sprites = pygame.sprite.RenderUpdates()





player = Player()
map = Map()
First_Load = True

map.draw(WIDTH_display,HEIGTH_display,First_Load)#+
player.draw_player(x,y)
pygame.display.update()



while run:
    clock = pygame.time.Clock()
    dt = clock.tick(FPS)
    #if (time_sleep > -500):
     #   time_sleep -= -1
    #else:
     #   time_sleep = 500
    player.draw_player(x,y)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    x,y = player.moove(keys,x,y)

    pygame.display.update()

pygame.quit()