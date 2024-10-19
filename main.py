# machine learning "dino dash" game

# pygame setup
import pygame
import time
pygame.init()

class Window:
    width = 800
    height = 600
window = Window()

collisions = 0
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

class Obstacle(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, colour, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       self.image = pygame.Surface([width, height])
       pygame.draw.rect(self.image, colour, (0, 0, width, height))

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x = window.width
       self.rect.y = floor_y - self.rect.height
       self.velocity = 5

    # define the update function
    def update(self):
        self.rect.x -= self.velocity

ball = Player("white", window.height * 0.075 , window.height * 0.075)
obstacles = []
font = pygame.font.Font('freesansbold.ttf', 32)

text = font.render('YOU HAVE DIED. ERES MALO', True, 'white', 'black')
textRect = text.get_rect()
textRect.center = (window.width // 2, window.height // 2)

obstacles.append(Obstacle("red", 20, 50)) # this has to be inside the loop (put here for testing)

# Initialize Pygame and font
pygame.init()
font = pygame.font.Font(None, 36)

# Function to display the number of collisions
def display_collisions(screen, collisions):
    text = font.render(f"Collisions: {collisions}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

# Initialize variables
collisions = 0
obstacle_timer = 0
obstacle_interval = 1000  # Time in milliseconds between new obstacles

# Assuming window, ball, and obstacles are already defined
textRect.center = (window.width // 2, window.height // 2)

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

    # Create new obstacles at intervals
    if pygame.time.get_ticks() - obstacle_timer > obstacle_interval:
        obstacles.append(Obstacle("red", 20, 50))
        obstacle_timer = pygame.time.get_ticks()

    # check for death
    for obstacle in obstacles[:]:
        if ball.rect.colliderect(obstacle.rect):
            collisions += 1
            obstacles.remove(obstacle)

    # render all obstacles
    for obstacle in obstacles:
        obstacle.update()
        screen.blit(obstacle.image, obstacle.rect)
    
    # render the player
    ball.gravity()
    ball.update()
    screen.blit(ball.image, ball.rect)

    # draw the floor
    pygame.draw.line(screen, "white", [0, floor_y], [window.width, floor_y], int(window.height * 0.005)) # draw the floor

    # Display the number of collisions
    display_collisions(screen, collisions)
    
    # flip() the display to print all changes in the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit() 
# probando pull push

