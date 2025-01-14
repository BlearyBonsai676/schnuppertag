import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# Player settings
player_width = 30
player_height = 30
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 10
player_stunned = False
player_invincible = False

# Ball settings
ball_radius = 20
ball_speed = 5
ball_list = []

# Blaster settings
blaster_width = 20
blaster_height = 30
blaster_speed = 20
blaster_list = []
blaster_cooldown = 200  # Cooldown in milliseconds
last_shot_time = 0

# Kamehameha settings
kamehameha_width = player_width * 10  # Increased width
kamehameha_height = SCREEN_HEIGHT  # Height of the beam
kamehameha_speed = 20
kamehameha_active = False
kamehameha_charging = False
kamehameha_cooldown = 5000  # Cooldown in milliseconds
kamehameha_duration = 4000  # Duration in milliseconds
kamehameha_charge_time = 2000  # Charge time in milliseconds
last_kamehameha_time = 0

# Genkidama settings
genkidama_radius = 20  # Initial radius
genkidama_max_radius = 100  # Maximum radius
genkidama_speed = 10
genkidama_active = False
genkidama_charging = False
genkidama_cooldown = 10000  # Cooldown in milliseconds
genkidama_charge_time = 3000  # Charge time in milliseconds
genkidama_traveling = False
genkidama_exploding = False
last_genkidama_time = 0
genkidama_x = 0
genkidama_y = 0

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Balls")

# Clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if not player_stunned:
        if keys[pygame.K_LEFT] and player_x - player_speed > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_speed < SCREEN_WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_shot_time > blaster_cooldown:
            blaster_list.append([player_x + player_width // 2 - blaster_width // 2, player_y])
            last_shot_time = pygame.time.get_ticks()
        if keys[pygame.K_k] and pygame.time.get_ticks() - last_kamehameha_time > kamehameha_cooldown:
            kamehameha_charging = True
            last_kamehameha_time = pygame.time.get_ticks()
            player_stunned = True
            player_invincible = True
        if keys[pygame.K_g] and pygame.time.get_ticks() - last_genkidama_time > genkidama_cooldown:
            genkidama_charging = True
            last_genkidama_time = pygame.time.get_ticks()
            player_stunned = True
            player_invincible = True

    # Add new balls
    if random.randint(1, 20) == 1:
        ball_x = random.randint(0, SCREEN_WIDTH - ball_radius * 2)
        ball_list.append([ball_x, -ball_radius * 2])

    # Move balls
    for ball in ball_list:
        ball[1] += ball_speed

    # Move blasters
    for blaster in blaster_list:
        blaster[1] -= blaster_speed

    # Remove off-screen balls and blasters
    ball_list = [ball for ball in ball_list if ball[1] < SCREEN_HEIGHT]
    blaster_list = [blaster for blaster in blaster_list if blaster[1] > 0]

    # Handle Kamehameha charging and activation
    if kamehameha_charging and pygame.time.get_ticks() - last_kamehameha_time > kamehameha_charge_time:
        kamehameha_charging = False
        kamehameha_active = True
        last_kamehameha_time = pygame.time.get_ticks()

    if kamehameha_active and pygame.time.get_ticks() - last_kamehameha_time > kamehameha_duration:
        kamehameha_active = False
        player_stunned = False
        player_invincible = False

    # Handle Genkidama charging and activation
    if genkidama_charging and pygame.time.get_ticks() - last_genkidama_time > genkidama_charge_time:
        genkidama_charging = False
        genkidama_traveling = True
        genkidama_x = player_x + player_width // 2
        genkidama_y = player_y - genkidama_radius

    if genkidama_traveling:
        genkidama_y -= genkidama_speed
        if genkidama_y <= SCREEN_HEIGHT // 2:
            genkidama_traveling = False
            genkidama_exploding = True
            last_genkidama_time = pygame.time.get_ticks()

    if genkidama_exploding:
        explosion_time = pygame.time.get_ticks() - last_genkidama_time
        radius = genkidama_max_radius + explosion_time * 2  # Increase radius over time
        pygame.draw.circle(screen, LIGHT_BLUE, (genkidama_x, genkidama_y), int(radius))
        ball_list.clear()
        for i in range(10):  # More beams for Genkidama
            beam_end_x = random.randint(0, SCREEN_WIDTH)
            beam_end_y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.line(screen, LIGHT_BLUE, (genkidama_x, genkidama_y), (beam_end_x, beam_end_y), 12)  # Increase beam thickness to 12
        if explosion_time > 3000:  # Clear the move after 3 seconds
            genkidama_exploding = False
            player_stunned = False
            player_invincible = False

    # Check for collisions
    for ball in ball_list:
        if not player_invincible and (player_x < ball[0] + ball_radius * 1.5 < player_x + player_width or player_x < ball[0] + ball_radius * 0.5 < player_x + player_width) and \
           (player_y < ball[1] + ball_radius * 1.5 < player_y + player_height or player_y < ball[1] + ball_radius * 0.5 < player_y + player_height):
            running = False

    # Check for blaster-ball collisions
    for blaster in blaster_list:
        for ball in ball_list:
            if (ball[0] < blaster[0] < ball[0] + ball_radius * 2) and (ball[1] < blaster[1] < ball[1] + ball_radius * 2):
                ball_list.remove(ball)
                blaster_list.remove(blaster)
                break

    # Check for Kamehameha-ball collisions
    if kamehameha_active:
        for ball in ball_list:
            if (player_x < ball[0] + ball_radius * 2 < player_x + player_width):
                ball_list.remove(ball)

    # Draw everything
    screen.fill(WHITE)
    for ball in ball_list:
        pygame.draw.circle(screen, RED, (ball[0] + ball_radius, ball[1] + ball_radius), ball_radius)
    for blaster in blaster_list:
        pygame.draw.rect(screen, YELLOW, (blaster[0], blaster[1], blaster_width, blaster_height))
    if kamehameha_charging:
        pygame.draw.circle(screen, BLUE, (player_x + player_width // 2, player_y - 20), 10)
        for i in range(5):
            pygame.draw.line(screen, LIGHT_BLUE, (player_x + player_width // 2, player_y - 20), (random.randint(0, SCREEN_WIDTH), 0), 2)
    if kamehameha_active:
        for y in range(SCREEN_HEIGHT):
            width = kamehameha_width + (y // -10)  # Increase width as y increases
            pygame.draw.rect(screen, DARK_BLUE, (player_x + player_width // 2 - width // 2, y, width, 1))
    if genkidama_charging:
        charge_time = pygame.time.get_ticks() - last_genkidama_time
        radius = genkidama_radius + (genkidama_max_radius - genkidama_radius) * (charge_time / genkidama_charge_time)
        pygame.draw.circle(screen, LIGHT_BLUE, (player_x + player_width // 2, player_y - radius), int(radius))
        for i in range(10):  # More beams for Genkidama
            pygame.draw.line(screen, LIGHT_BLUE, (player_x + player_width // 2, player_y - radius), (random.randint(0, SCREEN_WIDTH), 0), 2)
    if genkidama_traveling or genkidama_exploding:
        pygame.draw.circle(screen, LIGHT_BLUE, (genkidama_x, genkidama_y), genkidama_max_radius)
        for i in range(10):  # More beams for Genkidama
            beam_end_x = random.randint(0, SCREEN_WIDTH)
            beam_end_y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.line(screen, LIGHT_BLUE, (genkidama_x, genkidama_y), (beam_end_x, beam_end_y), 12)  # Increase beam thickness to 12
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))  # Draw player last

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
