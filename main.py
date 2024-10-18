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
g = 1 #gravity value

# asset setup
class Player(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, colour, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       self.image = pygame.Surface([width, height])
       pygame.draw.ellipse(self.image, colour, [0, 0, width, height])

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x = window.width * 0.1
       self.rect.y = window.height // 2
       self.velocity = 0

    # define gravity
    def gravity(self):
        self.velocity += g

    # check if the ball is touching the floor
    def grounded(self):
        return self.rect.y >= floor_y - self.rect.height

    # define the update function
    def update(self):
        self.rect.y += self.velocity

        if self.grounded():
            self.rect.y = floor_y - self.rect.height
            self.velocity = 0

ball = Player("white", window.height * 0.075 , window.height * 0.075)

# game loop
while running:
    # process input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and ball.grounded():
        ball.velocity = -25

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a colour to wipe away the last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE.
    screen.blit(ball.image, ball.rect)
    pygame.draw.line(screen, "white", [0, floor_y], [window.width, floor_y], int(window.height * 0.005)) # draw the floor
    ball.gravity()
    ball.update()

    # flip() the display to print all changes in the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()