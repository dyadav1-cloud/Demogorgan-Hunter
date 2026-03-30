import pygame
import sys

pygame.init()


#Screen Dimension

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


#Game Screen

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Demogorgan Hunter')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30)) 
    pygame.display.flip()

pygame.quit()
sys.exit()