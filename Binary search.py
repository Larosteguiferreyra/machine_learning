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
avoided = 0
obstacle_timer = 0
obstacle_interval = 0
font = pygame.font.Font(None, 36)
next_obstacle = None
distance_to_obstacle_j = 0

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
       self.distance_to_obstacle = 0

    # define gravity
    def gravity(self, dt):
        self.velocity += G * dt

    def jump(self):
        if self.grounded():
            self.velocity = -1000

    # calculate distance to the first obstacle
    # the distance is taken from the leftmost border of the player's crash box rightmost border of the obstacle
    def calculate_distance(self, obstacle):
        self.distance_to_obstacle = obstacle.rect.x + obstacle.rect.width - self.rect.x


    # check if the ball is touching the floor
    def grounded(self):
        return self.rect.y >= floor_y - self.rect.height

    # define the update function
    def update(self, dt):
        self.rect.y += self.velocity * dt
        self.calculate_distance(next_obstacle)

        if self.grounded():
            self.rect.y = floor_y - self.rect.height
            self.velocity = 0

    # check if the obstacle was avoided
    def check_avoidance(self):
        global next_obstacle
        if next_obstacle:
            global avoided
            if next_obstacle.rect.x + next_obstacle.rect.width <= self.rect.x and not next_obstacle.avoided:
                avoided += 1
                next_obstacle.avoided = True
                #bot.calculate_jump_distance()
            else:
                pass


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

       # create a variable to store whether this particular obstacle was already avoided
       self.avoided = False

    # define the update function
    def update(self, dt):
        self.rect.x -= self.velocity * dt


class Machine():
    def __init__(self):
        self.jumps = {}
        self.jump_distance = 150
    #good or bad jump 
    """
    def good_jump(self, distance_to_obstacle):
        if ball.rect.y in [478, 479, 480]:
            distance_to_obstacle_j = self.distance_to_obstacle
            if self.distance_to_obstacle == x:
                append to list 
"""
            
    # decide whether to jump
    def jump(self):
        if ball.distance_to_obstacle <= self.jump_distance:
            ball.jump()

#    def calculate_jump_distance(self):
#        self.jump_distance = randint(0, ball.distance_to_obstacle)

# Function to display the number of collisions and avoidances
def display_text(screen, collisions, avoided):
    collisions_text = font.render(f"Collisions: {collisions}", True, (255, 255, 255))
    avoided_text = font.render(f"Obstacles avoided: {avoided}", True, (255, 255, 255))
    screen.blit(collisions_text, (10, 10))
    screen.blit(avoided_text, (10, 50))

# function to store the next obstacle in the variable
def find_next_obstacle():
    global next_obstacle
    for obstacle in obstacles:
        if obstacle.rect.x + obstacle.rect.width >= ball.rect.x:
            next_obstacle = obstacle
            break

#initialize assets
ball = Player("white", window.height * 0.075 , window.height * 0.075)
bot = Machine()
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
    if keys[pygame.K_SPACE]:
        ball.jump()

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

    # check for death and avoidance, and remove obstacles when they move out of the screen
    ball.check_avoidance()
    find_next_obstacle()

    for obstacle in obstacles[:]:
        if ball.rect.colliderect(obstacle.rect):
            collisions += 1
            obstacles.remove(obstacle)
            #bot.calculate_jump_distance()
        elif obstacle.rect.x < 0:
            obstacles.remove(obstacle)

    # render all obstacles
    for obstacle in obstacles:
        obstacle.update(dt)
        screen.blit(obstacle.image, obstacle.rect)
    
    # decide whether the bot will jump
    bot.jump()

    # render the player
    ball.gravity(dt)
    ball.update(dt)
    screen.blit(ball.image, ball.rect)

    # draw the floor
    pygame.draw.line(screen, "white", [0, floor_y], [window.width, floor_y], int(window.height * 0.005))

    # Display the number of collisions and avoidances
    display_text(screen, collisions, avoided)

    # flip() the display to print all changes in the screen
    pygame.display.flip()

    clock.tick(120)  # limits FPS to 60
    print(ball.rect.y)

pygame.quit()