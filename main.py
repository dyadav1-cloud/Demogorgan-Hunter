import pygame
import sys

pygame.init()

#Game Screen

screen = pygame.display.set_mode((800, 600))
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