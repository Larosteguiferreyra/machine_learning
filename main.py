# machine learning "dino dash" game

# pygame setup
import pygame
from random import randint
pygame.init()

class Window:
    width = 800
    height = 600
window = Window()

screen = pygame.display.set_mode((window.width, window.height))
pygame.display.set_caption("Dino dash")
clock = pygame.time.Clock()


# declare variables
collisions = 0
floor_y = window.height * 0.9
running = True
G = 3000 #gravity value
collisions = 0
avoided = 0
obstacle_timer = 0
obstacle_interval = 0
font = pygame.font.Font(None, 36)


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
    def gravity(self, dt):
        self.velocity += G * dt

    # check if the ball is touching the floor
    def grounded(self):
        return self.rect.y >= floor_y - self.rect.height

    # define the update function
    def update(self, dt):
        self.rect.y += self.velocity * dt

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
       self.velocity = 300

    # define the update function
    def update(self, dt):
        self.rect.x -= self.velocity * dt

# Function to display the number of collisions
def display_collisions(screen, collisions):
    text = font.render(f"Collisions: {collisions}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

# function to display the number of obstacles avoided
def display_avoided(screen, avoided):
    text = font.render(f"Obstacles avoided: {avoided}", True, (255, 255, 255))
    screen.blit(text, (10, 50))


#initialize assets
ball = Player("white", window.height * 0.075 , window.height * 0.075)
obstacles = []
previous_time = pygame.time.get_ticks()

# game loop
while running:
    # calculate delta time
    current_time = pygame.time.get_ticks()
    dt = (current_time - previous_time) / 1000 #get the delta time in seconds
    previous_time = current_time

    # process input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and ball.grounded():
        ball.velocity = -1000

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
        obstacle_interval = randint(500, 2000)

    # check for death and remove obstacles when they move out of the screen
    for obstacle in obstacles[:]:
        if ball.rect.colliderect(obstacle.rect):
            collisions += 1
            obstacles.remove(obstacle)
        elif obstacle.rect.x < 0:
            avoided += 1
            obstacles.remove(obstacle)

    # render all obstacles
    for obstacle in obstacles:
        obstacle.update(dt)
        screen.blit(obstacle.image, obstacle.rect)
    
    # render the player
    ball.gravity(dt)
    ball.update(dt)
    screen.blit(ball.image, ball.rect)

    # draw the floor
    pygame.draw.line(screen, "white", [0, floor_y], [window.width, floor_y], int(window.height * 0.005))

    # Display the number of collisions and avoidances
    display_collisions(screen, collisions)
    display_avoided(screen, avoided)

    # flip() the display to print all changes in the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit() 