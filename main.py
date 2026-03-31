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

#Player constants
PLAYER_COLOR = 'YELLOW'
PLAYER_HEIGHT, PLAYER_WIDTH = 40, 60
PLAYER_SPEED = 300


#Sprite clasess
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_HEIGHT, PLAYER_WIDTH))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        self.world_x = 0
        self.world_y = 0
        self.player_speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.world_y -= self.speed * delta
        if keys[pygame.K_s]:
            self.world_y += self.speed * delta
        if keys[pygame.K_a]:
            self.world_x -= self.speed * delta
        if keys[pygame.K_d]:
            self.world_x += self.speed * delta

        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

#class Demogorgan(pygame.sprite.Sprite):
    #super().__init__()

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITTLE)
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        self.box_x = 200
        self.box_y = 100

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self, delta):
        self.player.update(delta)

    def _draw(self):
        self.screen.fill(BLACK)

        box_screen_x = self.box_x - self.player.world_x + WINDOW_WIDTH // 2
        box_screen_y = self.box_y - self.player.world_y + WINDOW_HEIGHT // 2

        pygame.draw.rect(self.screen, RED, (box_screen_x, box_screen_y, 50, 50))

        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            delta = self.clock.tick(MAX_FPS) / 1000.0
            self._handle_events()
            self._update(delta)
            self._draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
