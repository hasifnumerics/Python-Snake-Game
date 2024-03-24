import pygame
import random

# Initialize Pygame
pygame.init()

# Game Display Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20
NUM_CELLS_WIDTH = SCREEN_WIDTH // CELL_SIZE
NUM_CELLS_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
COLOR_BACKGROUND = (10, 10, 10)
COLOR_FOOD = (255, 0, 0)
COLOR_SNAKE = (0, 255, 0)
COLOR_TEXT = (255, 255, 255)
TEXT_SIZE = 24
MARGIN = 20  # Margin from the edges for the play area

# Setup Pygame Screen
display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Classic Snake Game")
game_font = pygame.font.Font(None, TEXT_SIZE)
game_clock = pygame.time.Clock()

# Defining snake class
class Serpent:
    def __init__(self):
        self.segments = [(
            random.randint(MARGIN // CELL_SIZE, NUM_CELLS_WIDTH - MARGIN // CELL_SIZE - 1),
            random.randint(MARGIN // CELL_SIZE, NUM_CELLS_HEIGHT - MARGIN // CELL_SIZE - 1))]
        self.current_direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.is_growing = False

    def update_position(self):
        x, y = self.segments[0]
        if self.current_direction == "UP":
            next_head = (x, (y - 1) % NUM_CELLS_HEIGHT)
        elif self.current_direction == "DOWN":
            next_head = (x, (y + 1) % NUM_CELLS_HEIGHT)
        elif self.current_direction == "LEFT":
            next_head = ((x - 1) % NUM_CELLS_WIDTH, y)
        else:  # RIGHT
            next_head = ((x + 1) % NUM_CELLS_WIDTH, y)

        self.segments.insert(0, next_head)
        if not self.is_growing:
            self.segments.pop()
        else:
            self.is_growing = False

    def grow(self):
        self.is_growing = True

    def render(self):
        for part in self.segments:
            pygame.draw.rect(display_screen, COLOR_SNAKE, (part[0] * CELL_SIZE, part[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Defining Food Class
class Nutrient:
    def __init__(self):
        self.position = self.new_position()

    def new_position(self):
        return (
            random.randint(MARGIN // CELL_SIZE, NUM_CELLS_WIDTH - MARGIN // CELL_SIZE - 1),
            random.randint(MARGIN // CELL_SIZE, NUM_CELLS_HEIGHT - MARGIN // CELL_SIZE - 1))

    def render(self):
        pygame.draw.rect(display_screen, COLOR_FOOD, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Game Initiate
player_snake = Serpent()
game_food = Nutrient()
player_score = 0
game_duration = 2  # Game time in seconds
elapsed_time = 0

# Main Game Loop
game_active = True
while game_active:
    display_screen.fill(COLOR_BACKGROUND)
    pygame.draw.rect(display_screen, COLOR_TEXT, (MARGIN, MARGIN, SCREEN_WIDTH - 2*MARGIN, SCREEN_HEIGHT - 2*MARGIN), 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_snake.current_direction != "DOWN":
                player_snake.current_direction = "UP"
            elif event.key == pygame.K_DOWN and player_snake.current_direction != "UP":
                player_snake.current_direction = "DOWN"
            elif event.key == pygame.K_LEFT and player_snake.current_direction != "RIGHT":
                player_snake.current_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and player_snake.current_direction != "LEFT":
                player_snake.current_direction = "RIGHT"

    player_snake.update_position()

    # Check for collisions
    if player_snake.segments[0] in player_snake.segments[1:]:
        game_active = False

    # Check boundary collision
    x_head, y_head = player_snake.segments[0]
    if x_head < MARGIN // CELL_SIZE or x_head >= NUM_CELLS_WIDTH - MARGIN // CELL_SIZE or y_head < MARGIN // CELL_SIZE or y_head >= NUM_CELLS_HEIGHT - MARGIN // CELL_SIZE:
        game_active = False

    # Check if the snake eats the food
   
    if player_snake.segments[0] == game_food.position:
        player_snake.grow()
        game_food.position = game_food.new_position()
        player_score += 1

    # Update and check game time
    elapsed_time += game_clock.get_rawtime() / 1000  # Convert milliseconds to seconds
    if elapsed_time >= game_duration:
        game_active = False

    # Rendering the snake and food
    player_snake.render()
    game_food.render()

    # Display score on the screen
    score_display = game_font.render(f"Score: {player_score}", True, COLOR_TEXT)
    display_screen.blit(score_display, (10, 10))

    # Display remaining game time
    remaining_time = max(game_duration - elapsed_time, 0)
    time_display = game_font.render(f"Time Left: {remaining_time:.1f}", True, COLOR_TEXT)
    display_screen.blit(time_display, (SCREEN_WIDTH - 170, 10))

    pygame.display.flip()
    game_clock.tick(10)

# Display game over message
game_over_display = game_font.render("Game Over", True, COLOR_TEXT)
final_score_display = game_font.render(f"Final Score: {player_score}", True, COLOR_TEXT)
display_screen.blit(game_over_display, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 24))
display_screen.blit(final_score_display, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))
pygame.display.flip()

pygame.time.wait(3000)  # Wait for 3 seconds before closing

pygame.quit()
