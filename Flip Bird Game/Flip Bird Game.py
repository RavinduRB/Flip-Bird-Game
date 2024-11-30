import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Game variables
gravity = 0.5
bird_y = HEIGHT // 2
bird_x = 50
bird_velocity = 0
bird_radius = 15

pipe_width = 60
pipe_gap = 150
pipe_speed = 3
pipes = []
score = 0
font = pygame.font.SysFont("Arial", 24)

# Function to create pipes
def create_pipe():
    pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
    pipes.append({
        "x": WIDTH,
        "top": pipe_height,
        "bottom": pipe_height + pipe_gap
    })

# Initial pipes
for _ in range(3):
    create_pipe()

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -8  # Bird jump

    # Bird physics
    bird_velocity += gravity
    bird_y += bird_velocity

    # Draw bird
    pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)

    # Move pipes
    for pipe in pipes:
        pipe["x"] -= pipe_speed

    # Remove pipes off-screen and add new ones
    if pipes[0]["x"] < -pipe_width:
        pipes.pop(0)
        create_pipe()
        score += 1

    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))
        pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], pipe_width, HEIGHT - pipe["bottom"]))

    # Collision detection
    for pipe in pipes:
        if (bird_x + bird_radius > pipe["x"] and bird_x - bird_radius < pipe["x"] + pipe_width):
            if bird_y - bird_radius < pipe["top"] or bird_y + bird_radius > pipe["bottom"]:
                running = False  # End game on collision

    # Check if bird hits the ground or ceiling
    if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
        running = False

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

pygame.quit()
