import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Ball dimensions
BALL_SIZE = 10

# Paddle positions
left_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball position and velocity
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Paddle velocity
right_paddle_velocity = 0

# Game loop
running = True
clock = pygame.time.Clock()

# Difficulty settings
difficulties = {
    "easy": {"ball_speed": 3, "paddle_speed": 4, "npc_speed": 2},
    "medium": {"ball_speed": 6, "paddle_speed": 6, "npc_speed": 3},
    "hard": {"ball_speed": 9, "paddle_speed": 8, "npc_speed": 4},
    "godly": {"ball_speed": 50, "paddle_speed": 20, "npc_speed": 500}
}

# Start screen
def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Select Difficulty", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    font = pygame.font.Font(None, 50)
    easy_text = font.render("1. Easy", True, WHITE)
    medium_text = font.render("2. Medium", True, WHITE)
    hard_text = font.render("3. Hard", True, WHITE)
    godly_text = font.render("4. Godly", True, WHITE)

    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(godly_text, (WIDTH // 2 - godly_text.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()

    selected_difficulty = None
    while selected_difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_difficulty = "easy"
                elif event.key == pygame.K_2:
                    selected_difficulty = "medium"
                elif event.key == pygame.K_3:
                    selected_difficulty = "hard"
                elif event.key == pygame.K_4:
                    selected_difficulty = "godly"
    return selected_difficulty

# Main game loop
difficulty = start_screen()
ball_velocity = [random.choice([-difficulties[difficulty]["ball_speed"], difficulties[difficulty]["ball_speed"]]), 
                 random.choice([-difficulties[difficulty]["ball_speed"], difficulties[difficulty]["ball_speed"]])]
paddle_speed = difficulties[difficulty]["paddle_speed"]
npc_speed = difficulties[difficulty]["npc_speed"]

# Scoreboard
left_score = 0
right_score = 0
font = pygame.font.Font(None, 74)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                right_paddle_velocity = -paddle_speed
            elif event.key == pygame.K_DOWN:
                right_paddle_velocity = paddle_speed
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                right_paddle_velocity = 0

    # Move paddles
    right_paddle.y += right_paddle_velocity

    # NPC movement for left paddle
    if left_paddle.centery < ball.centery:
        left_paddle.y += npc_speed
    elif left_paddle.centery > ball.centery:
        left_paddle.y -= npc_speed

    # Keep paddles on screen
    left_paddle.y = max(min(left_paddle.y, HEIGHT - PADDLE_HEIGHT), 0)
    right_paddle.y = max(min(right_paddle.y, HEIGHT - PADDLE_HEIGHT), 0)

    # Move ball
    ball.x += ball_velocity[0]
    ball.y += ball_velocity[1]

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_velocity[1] = -ball_velocity[1]

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_velocity[0] = -ball_velocity[0]

    # Ball out of bounds
    if ball.left <= 0:
        right_score += 1
        ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
        ball_velocity = [random.choice([-difficulties[difficulty]["ball_speed"], difficulties[difficulty]["ball_speed"]]), 
                         random.choice([-difficulties[difficulty]["ball_speed"], difficulties[difficulty]["ball_speed"]])]
    elif ball.right >= WIDTH:
        left_score += 1
        ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
        ball_velocity = [random.choice([-difficulties[difficulty]["ball_speed"], difficulties[difficulty]["ball_speed"]]), 
                         random.choice([-difficulties[difficulty]["ball_speed"], difficulties[difficulty]["ball_speed"]])]

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw scores
    left_text = font.render(str(left_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(right_text, (3 * WIDTH // 4 - right_text.get_width() // 2, 20))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()