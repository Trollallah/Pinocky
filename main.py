
import pygame

# Initializes the pygame package
pygame.init()

#Create window
pygame.display.set_caption('Pinocky')
window_surface = pygame.display.set_mode((800, 600))

# Create surface, black
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

is_running = True

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.blit(background, (0, 0))

    pygame.display.update()
