import pygame, os, math



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
PLAYER_HEIGHT, PLAYER_WIDTH = 60, 40
PLAYER_SPEED = 400


#Sprite clasess
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("player_transparant.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (90, 120))

        
        self.image = self.original_image
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
        center_x = WINDOW_WIDTH // 2
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - center_x
        facing_left = dx < 0
        
        if facing_left:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.world_x = x
        self.world_y = y
        self.angle = angle
        self.speed = 800

    def update(self, delta):
        self.world_x += math.cos(self.angle) * self.speed * delta
        self.world_y += math.sin(self.angle) * self.speed * delta
        self.rect.center = (self.world_x, self.world_y)

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

        self.bullets = pygame.sprite.Group()

        self.gun_image = pygame.image.load("gun.png").convert_alpha()
        self.gun_image = pygame.transform.scale(self.gun_image, ((120, 40)))


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._shoot()

    def _update(self, delta):
        self.player.update(delta)
        self.bullets.update(delta)

    def _draw_grid(self):
        grid_size = 100

        start_x = - (self.player.world_x % grid_size)
        start_y = - (self.player.world_y % grid_size)

        for x in range(int(start_x), WINDOW_WIDTH, grid_size):
            pygame.draw.line(self.screen, DARK_BLUE, (x, 0), (x, WINDOW_HEIGHT))

        for y in range(int(start_y), WINDOW_HEIGHT, grid_size):
            pygame.draw.line(self.screen, DARK_BLUE, (0, y), (WINDOW_WIDTH, y))

    def _draw_gun(self):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - center_x
        dy = mouse_y - center_y

        angle = math.atan2(dy, dx)

        angle_degrees = -math.degrees(angle)

        facing_right = dx > 0

        gun_to_draw = self.gun_image

        if facing_right:
            gun_to_draw = pygame.transform.flip(self.gun_image, True, False)
        else:
            angle_degrees = -math.degrees(angle) + 180

        rotated_gun = pygame.transform.rotate(gun_to_draw, angle_degrees)

        gun_distance = 28
        gun_x = center_x + math.cos(angle) * gun_distance
        gun_y = center_y + math.sin(angle) * gun_distance

        gun_rect = rotated_gun.get_rect(center=(gun_x, gun_y))
        self.screen.blit(rotated_gun, gun_rect)

    def _shoot(self):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - center_x
        dy = mouse_y - center_y
        angle = math.atan2(dy, dx)

        gun_distance = 40
        bullet_x = center_x + math.cos(angle) * gun_distance
        bullet_y = center_y + math.sin(angle) * gun_distance

        bullet = Bullet(bullet_x, bullet_y, angle)
        self.bullets.add(bullet)

    def _draw(self):
        self.screen.fill(BLACK)
        self._draw_grid()
        self.all_sprites.draw(self.screen)
        self._draw_gun()
        self.bullets.draw(self.screen)
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
