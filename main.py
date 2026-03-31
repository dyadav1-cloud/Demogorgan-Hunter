import pygame

print("Welcome to Demogorgan Hunter!")

pygame.init()


#Screen Dimension

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


#Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 51, 102)

#Sprite clasess
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        
    

#class Demogorgan(pygame.sprite.Sprite):
    #super().__init__()


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Demogorgan Hunter')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((DARK_BLUE)) 
    pygame.display.flip()



pygame.quit()
