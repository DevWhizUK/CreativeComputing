import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200  # Increased width
SCREEN_HEIGHT = 800  # Increased height
TILE_SIZE = 20  # Reduced tile size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

# Player class
class Player:
    def __init__(self, x, y, maze):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = BLUE
        self.maze = maze

    def move(self, dx, dy):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Calculate grid position
        grid_x = new_x // TILE_SIZE
        grid_y = new_y // TILE_SIZE

        # Check if new position is within bounds and not a wall
        if 0 <= grid_x < len(self.maze[0]) and 0 <= grid_y < len(self.maze):
            if self.maze[grid_y][grid_x] == 0:
                self.rect.x = new_x
                self.rect.y = new_y

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Maze generation function
def generate_maze(width, height, difficulty):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve_passages(cx, cy):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                if (dx, dy) == (1, 0) or (dx, dy) == (-1, 0):
                    if nx + dx >= 0 and nx + dx < width and maze[ny][nx + dx] == 1:
                        maze[cy][cx] = 0
                        maze[ny][nx] = 0
                        maze[ny][nx + dx] = 0
                        carve_passages(nx + dx, ny)
                if (dx, dy) == (0, 1) or (dx, dy) == (0, -1):
                    if ny + dy >= 0 and ny + dy < height and maze[ny + dy][nx] == 1:
                        maze[cy][cx] = 0
                        maze[ny][nx] = 0
                        maze[ny + dy][nx] = 0
                        carve_passages(nx, ny + dy)

    carve_passages(0, 0)
    return maze

# Draw the maze
def draw_maze(surface, maze):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(surface, BLACK, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Main function
def main():
    clock = pygame.time.Clock()
    performance_metrics = []

    def calculate_difficulty():
        if not performance_metrics:
            return 0.5  # Default difficulty
        avg_time = sum([m['time'] for m in performance_metrics]) / len(performance_metrics)
        avg_moves = sum([m['moves'] for m in performance_metrics]) / len(performance_metrics)
        return min(max((avg_time + avg_moves) / 200, 0.1), 1.0)

    while True:
        difficulty = calculate_difficulty()
        maze = generate_maze(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE, difficulty)
        player = Player(TILE_SIZE // 2, TILE_SIZE // 2, maze)
        goal_rect = pygame.Rect((SCREEN_WIDTH // TILE_SIZE - 1) * TILE_SIZE, (SCREEN_HEIGHT // TILE_SIZE - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        start_time = time.time()
        moves = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player.move(-TILE_SIZE, 0)
                moves += 1
            if keys[pygame.K_d]:
                player.move(TILE_SIZE, 0)
                moves += 1
            if keys[pygame.K_w]:
                player.move(0, -TILE_SIZE)
                moves += 1
            if keys[pygame.K_s]:
                player.move(0, TILE_SIZE)
                moves += 1

            screen.fill(WHITE)
            draw_maze(screen, maze)
            player.draw(screen)
            pygame.draw.rect(screen, GREEN, goal_rect)

            if player.rect.colliderect(goal_rect):
                end_time = time.time()
                performance_metrics.append({
                    'time': end_time - start_time,
                    'moves': moves
                })
                print("You reached the goal!")
                running = False

            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    main()
