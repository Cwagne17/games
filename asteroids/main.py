import pygame

pygame.init()

# Set the screen size to 1280x720 pixels
screen = pygame.display.set_mode((1280, 720))

# Set the window title to "Asteroids"
pygame.display.set_caption("Asteroids")

# Create a clock object to help control the frame rate
clock = pygame.time.Clock()
dt = 0

# Set the player's starting position to the center of the screen
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Load the background image and scale it to the screen size
background = pygame.image.load("assets/space_background.png")
background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

# Load the play icon (rocket) and scale it to 40x40 pixels
player = pygame.image.load("assets/rocket.svg")
player = pygame.transform.scale(player, (50, 50))

def renderScreen():
    # Set the background image to the screen
    screen.blit(background, (0, 0))

    # Set the player icon to the screen at the player's position
    screen.blit(player, player_pos)
 
def exit(event):
    pygame.quit()
    exit(0)

def keyUpAction(event):
    player_pos.y -= 300 * dt
    renderScreen()

def keyRightAction(event):
    player_pos.x += 300 * dt

def keydownAction(event):
    player_pos.y += 300 * dt

def keyLeftAction(event):
    player_pos.x -= 300 * dt

def keySpaceAction(event):
    print("Space")
    
eventhandler = {
    pygame.QUIT: exit,
    pygame.K_w: keyUpAction,
    pygame.K_d: keyRightAction,
    pygame.K_s: keydownAction,
    pygame.K_a: keyLeftAction,
    pygame.K_SPACE: keySpaceAction,
    pygame.KEYUP: keyUpAction,
}    

while True:
    renderScreen()
    
    for key in pygame.key.get_pressed():
        if key:
            eventhandler[key](key)
        
    # flip() the display to put your work on screen
    

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000