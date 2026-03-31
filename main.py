import pygame, os



pygame.init()


#Screen Dimension
GAME_TITTLE = "Demogorgan Hunter!"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAX_FPS = 60


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

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITTLE)
        self.running = True
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def _draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self._handle_events()
            self._draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
