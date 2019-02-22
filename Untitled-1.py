import pygame, sys, random
 
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
 
BOX_WIDTH, BOX_HEIGHT, BOX_COUNT = 20, 20, 25
 
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 390
 
class Box(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BOX_WIDTH, BOX_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def update(self):
        self.rect.y += 1
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -1 * BOX_HEIGHT
 
pygame.init()
pygame.display.set_caption('RenderUpdates example')
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
 
# Here your declare RenderUpdates Sprite Group
all_sprites = pygame.sprite.RenderUpdates()
box_sprites = pygame.sprite.RenderUpdates()
 
# adding player
player = Box(RED, [0, 0])
all_sprites.add(player)
 
# adding other boxes
for i in range(BOX_COUNT):
    tmpx = random.randrange(0, SCREEN_WIDTH)
    tmpy = random.randrange(0, SCREEN_HEIGHT)
    tmpbox = Box(WHITE, [tmpx, tmpy])
    box_sprites.add(tmpbox)
    all_sprites.add(tmpbox)
 
pygame.mouse.set_visible(False)
 
# using an image for background to test if this actually works
background = pygame.image.load('mario_droit.png').convert()
screen.blit(background, [0, 0])
# if you don't call the update you will get a black screen
pygame.display.update()
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            player.rect.topleft = pygame.mouse.get_pos()
 
    box_sprites.update()
 
    pygame.sprite.spritecollide(player, box_sprites, True)
 
    # draw background over the Sprites
    all_sprites.clear(screen, background)
 
    # blit the Sprite images and track changed areas
    # returns a list of Rectangular areas on the screen that have been changed
    rectlist = all_sprites.draw(screen)
 
    # update only the change areas
    pygame.display.update(rectlist)