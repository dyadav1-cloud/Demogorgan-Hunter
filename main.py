import pygame, os, math, random

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
GREEN = (0, 255, 0)

#Player constants
PLAYER_COLOR = YELLOW
PLAYER_WIDTH, PLAYER_HEIGHT = 90, 120
PLAYER_SPEED = 400
PLAYER_HEALTH = 100
PLAYER_MAX_HEALTH = 100

#Enemy constants 
ENEMY_SPEED = 300
ENEMY_WIDTH, ENEMY_HEIGHT = 90, 120
ENEMY_HEALTH = 100
ENEMY_MAX_HEALTH = 100

#Bullet traits
DAMAGE = 34

#Sprite clasess
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("player_transparant.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

        
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        self.health = PLAYER_HEALTH
        self.max_health= PLAYER_MAX_HEALTH
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
    def __init__(self, world_x, world_y, angle):
        super().__init__()
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(world_x, world_y))
        self.damage = DAMAGE
        self.world_x = world_x
        self.world_y = world_y
        self.angle = angle
        self.speed = 800

    def update(self, delta):
        self.world_x += math.cos(self.angle) * self.speed * delta
        self.world_y += math.sin(self.angle) * self.speed * delta
        self.rect.center = (self.world_x, self.world_y)

    def draw(self, screen, player_world_x, player_world_y):
        screen_x = self.world_x - player_world_x + WINDOW_WIDTH // 2
        screen_y = self.world_y - player_world_y + WINDOW_HEIGHT // 2

        self.rect.center = (screen_x, screen_y)
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))

        self.rect = self.image.get_rect()

        self.health = ENEMY_HEALTH
        self.max_health = ENEMY_MAX_HEALTH
        self.world_x = x
        self.world_y = y
        self.speed = ENEMY_SPEED

    def update(self, delta, player_world_x, player_world_y):
        dx = player_world_x - self.world_x
        dy = player_world_y - self.world_y

        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance != 0:
            dx /= distance
            dy /= distance

        self.world_x += dx * self.speed * delta
        self.world_y += dy * self.speed * delta

    def draw_health_bar(self, screen, player_world_x, player_world_y):
        screen_x = self.world_x - player_world_x + WINDOW_WIDTH // 2
        screen_y = self.world_y - player_world_y + WINDOW_HEIGHT // 2

        bar_width = 50
        bar_height = 6
        health_ratio = self.health / self.max_health

        bar_x = screen_x - bar_width // 2
        bar_y = screen_y - ENEMY_HEIGHT // 2 - 12

        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

    def draw(self, screen, player_world_x, player_world_y):
        screen_x = self.world_x - player_world_x + WINDOW_WIDTH // 2
        screen_y = self.world_y - player_world_y + WINDOW_HEIGHT // 2

        self.rect.center = (screen_x, screen_y)
        screen.blit(self.image, self.rect)



class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITTLE)
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)
        self.all_sprites = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 1.0 #later on I will decrease this with stage or wave to make it harder. I will also introduce different types of enemies 

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

        for enemy in self.enemies:
            enemy.update(delta, self.player.world_x, self.player.world_y)

        self.enemy_spawn_timer += delta
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self._spawn_enemy()
            self.enemy_spawn_timer = 0

        for bullet in self.bullets.copy():
            for enemy in self.enemies.copy():
                dx = bullet.world_x - enemy.world_x
                dy = bullet.world_y - enemy.world_y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < 50:
                    enemy.health -= bullet.damage
                    bullet.kill()

                    if enemy.health <= 0:
                        enemy.kill()
                        self.score += 1
                    break

        for enemy in self.enemies.copy():
            dx = enemy.world_x - self.player.world_x
            dy = enemy.world_y - self.player.world_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 60:
                self.player.health -= 20
                enemy.kill()

                if self.player.health <= 0:
                    self.running = False
    
    def _draw_player_health(self):
        bar_width = 300
        bar_height = 20

        health_ratio = self.player.health / self.player.max_health

        bar_x = WINDOW_WIDTH - bar_width - 20
        bar_y = 20

        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(
            self.screen,
            GREEN,
            (bar_x, bar_y, int(bar_width * health_ratio), bar_height)
        )
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)


    def _draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))

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
        bullet_x = self.player.world_x + math.cos(angle) * gun_distance
        bullet_y = self.player.world_y + math.sin(angle) * gun_distance

        bullet = Bullet(bullet_x, bullet_y, angle)
        self.bullets.add(bullet)

    def _spawn_enemy(self):
        side = random.choice(["top","bottom","left","right"])
        margin = 200

        if side == "top":
            x = random.randint(-WINDOW_WIDTH, WINDOW_WIDTH)
            y = self.player.world_y - WINDOW_HEIGHT // 2 - margin
        elif side == "bottom":
            x = random.randint(-WINDOW_WIDTH, WINDOW_WIDTH)
            y = self.player.world_y + WINDOW_HEIGHT // 2 + margin
        elif side == "left":
            x = self.player.world_x - WINDOW_WIDTH // 2 - margin
            y = random.randint(-WINDOW_HEIGHT, WINDOW_HEIGHT)
        else:
            x = self.player.world_x + WINDOW_WIDTH // 2 + margin
            y = random.randint(-WINDOW_HEIGHT, WINDOW_HEIGHT)

        enemy = Enemy(x, y)
        self.enemies.add(enemy)

    def _draw(self):
        self.screen.fill(BLACK)
        self._draw_grid()
        for enemy in self.enemies:
            enemy.draw(self.screen, self.player.world_x, self.player.world_y)
            enemy.draw_health_bar(self.screen, self.player.world_x, self.player.world_y)
        self.all_sprites.draw(self.screen)
        self._draw_gun()
        for bullet in self.bullets:
            bullet.draw(self.screen, self.player.world_x, self.player.world_y)
        self._draw_player_health()
        self._draw_score()
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
