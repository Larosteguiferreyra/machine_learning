# machine learning "dino dash" game

import pygame

# pygame setup
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Dino dash")
clock = pygame.time.Clock()
running = True

while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a colour to wipe away the last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to print all changes in the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()