import os
import pygame
pygame.init()

SIZE = WIDTH, HEIGHT = 720, 480
BACKGROUND_COLOR = pygame.Color('black')
FPS = 60

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()



def load_images(path):
    images = []
    for file_name in os.listdir(path="data/courtmariocourt"):
        image = pygame.image.load(path + os.sep + file_name).convert()
        image = pygame.transform.scale(image, (50,60))
        images.append(image)
    return images



class SpriteAnimé(pygame.sprite.Sprite):

    def __init__(self, position, images):
        
        super(SpriteAnimé, self).__init__()

        size = (50, 60)  

        self.rect = pygame.Rect(position, size)
        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]  
        self.index = 0
        self.image = images[self.index]  

        self.velocity = pygame.math.Vector2(0, 0)

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt):
       
        if self.velocity.x > 0:  
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """
        if self.velocity.x > 0:  
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

    def update(self, dt):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        self.update_time_dependent(dt)
        

def main():
    imagesmario = load_images(path='data/courtmariocourt')  # Make sure to provide the relative or full path to the images directory.
    player = SpriteAnimé(position=(100, 100), images=imagesmario)
    all_sprites = pygame.sprite.Group(player)  

    running = True
    while running:

        dt = clock.tick(FPS) / 1000  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.velocity.x = 4
                elif event.key == pygame.K_LEFT:
                    player.velocity.x = -4
                elif event.key == pygame.K_DOWN:
                    player.velocity.y = 4
                elif event.key == pygame.K_UP:
                    player.velocity.y = -4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.velocity.x = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    player.velocity.y = 0

        all_sprites.update(dt)  

        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
