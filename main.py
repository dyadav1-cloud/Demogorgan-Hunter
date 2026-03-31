import pygame, os



pygame.init()


#Screen Dimension
GAME_TITTLE = "Demogorgan Hunter!"
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
MAX_FPS = 60


#Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 51, 102)

#Player constants
PLAYER_COLOR = YELLOW
PLAYER_HEIGHT, PLAYER_WIDTH = 40, 60
PLAYER_SPEED = 400


#Sprite clasess
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        self.world_x = 0
        self.world_y = 0
        self.speed = PLAYER_SPEED

    def update(self, delta):
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
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self, delta):
        self.player.update(delta)

    def _draw_grid(self):
        grid_size = 100

        start_x = - (self.player.world_x % grid_size)
        start_y = - (self.player.world_y % grid_size)

        for x in range(int(start_x), WINDOW_WIDTH, grid_size):
            pygame.draw.line(self.screen, DARK_BLUE, (x, 0), (x, WINDOW_HEIGHT))

        for y in range(int(start_y), WINDOW_HEIGHT, grid_size):
            pygame.draw.line(self.screen, DARK_BLUE, (0, y), (WINDOW_WIDTH, y))

    def _draw(self):
        self.screen.fill(BLACK)

        self._draw_grid()

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
