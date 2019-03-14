import pygame
pygame.init()

if __name__ == "__main__":
    screen = pygame.display.set_mode((424, 320))

    MAP_TILE_WIDTH = 24
    MAP_TILE_HEIGHT = 16
    MAP_CACHE = {
        'ground.png': load_tile_table('ground.png', MAP_TILE_WIDTH,
                                      MAP_TILE_HEIGHT),
    }

    level = Level()
    level.load_file('level.map')

    clock = pygame.time.Clock()

    background, overlay_dict = level.render()
    overlays = pygame.sprite.RenderUpdates()
    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
    screen.blit(background, (0, 0))
    overlays.draw(screen)
    pygame.display.flip()

game_over = False
while not game_over:

    # XXX draw all the objects here

    overlays.draw(screen)
    pygame.display.flip()
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            game_over = True
        elif event.type == pygame.locals.KEYDOWN:
            pressed_key = event.key