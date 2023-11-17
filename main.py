import pygame
import sys
import random

# Constants

GRID_SIZE = 4
WIDTH, HEIGHT = GRID_SIZE * 100, (GRID_SIZE + 1) * 100
TILE_SIZE = 100
BUTTON_SIZE = TILE_SIZE // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

# Initialize Pygame
pygame.init()
pygame.font.init()
FONT = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Tile Puzzle")

# Initialize game board
grid = [[i + j * GRID_SIZE + 1 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
grid[GRID_SIZE - 1][GRID_SIZE - 1] = 0  # Empty tile
empty_row, empty_col = GRID_SIZE - 1, GRID_SIZE - 1


# Shuffle the board randomly
def shuffle_board():
    global empty_row, empty_col
    tile_numbers = list(range(1, GRID_SIZE * GRID_SIZE))
    random.shuffle(tile_numbers)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if tile_numbers:
                grid[row][col] = tile_numbers.pop(0)
            else:
                grid[row][col] = 0
                empty_row, empty_col = row, col

def check_win():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != row * GRID_SIZE + col + 1:
                return False
    return True

# TODO: Add a function to check if the tile puzzle is solvable
# https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
def check_solvable():
    pass

def generate_solvable_board():
    while not check_solvable():
        shuffle_board()
    return grid

#TODO: Add a function to solve the puzzle using BFS
def BFS_solve():
    pass

#TODO: Add a function to solve the puzzle using A*
def A_star_solve():
    pass

#TODO: Add a function to solve the puzzle using IDA*
def IDA_star_solve():
    pass

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row = mouse_y // TILE_SIZE
            col = mouse_x // TILE_SIZE
            if (
                abs(row - empty_row) + abs(col - empty_col) == 1
                and 0 <= row < GRID_SIZE
                and 0 <= col < GRID_SIZE
            ):
                # Swap the clicked tile with the empty tile
                grid[row][col], grid[empty_row][empty_col] = grid[empty_row][empty_col], grid[row][col]
                empty_row, empty_col = row, col
            elif (GRID_SIZE < row < GRID_SIZE + 1):
                match col:

                    case 0:
                        generate_solvable_board()
                    case 1:
                        BFS_solve()
                    case 2: 
                        A_star_solve()
                    case 3:
                        IDA_star_solve()
                    case _:
                        pass

    # Draw the game board
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = grid[row][col]
            if tile != 0:
                pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                text = FONT.render(str(tile), True, WHITE)
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)

    # Draw buttons around the empty tile
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        row, col = empty_row + dr, empty_col + dc
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, GREY, (col * TILE_SIZE + 2, row * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4))
            text = FONT.render(str(grid[row][col]), True, WHITE)
            text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
            screen.blit(text, text_rect)

    pygame.display.flip()
