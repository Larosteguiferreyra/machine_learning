# machine learning "dino dash" game

import pygame

# pygame setup
class Window:
    width = 800
    height = 600
window = Window()

floor_y = window.height * 0.9
screen = pygame.display.set_mode((window.width, window.height))
pygame.display.set_caption("Dino dash")
clock = pygame.time.Clock()
running = True

# asset setup
class Ball(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, colour, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       pygame.draw.ellipse(self.image, colour, [0, 0, width, height])

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x = window.width * 0.1
       self.rect.y = floor_y - self.rect.height

ball = Ball("white", window.height * 0.075 , window.height * 0.075)

# game loop
while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a colour to wipe away the last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE.
    screen.blit(ball.image, ball.rect)
    pygame.draw.line(screen, "white", [0, floor_y], [window.width, floor_y], int(window.height * 0.005)) # draw the floor

    # flip() the display to print all changes in the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()