import pygame
import sys
import time

#local imports
from games import *
from tree_search import TreeSearch

# Constants

GRID_SIZE = 4
WIDTH, HEIGHT = GRID_SIZE * 50, (GRID_SIZE + 1) * 50
TILE_SIZE = 50
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH // 8 , 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
pygame.font.init()
FONT = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Tile Puzzle")

# Initialize the game board
main_view = SlidingPuzzle(GRID_SIZE)

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
            print("Clicked on tile: ", row, col) # REMOVE LATER 
            moved = main_view.board.perform_action((row - main_view.board.emptyRow, col - main_view.board.emptyCol))
            if moved:
                print("Moved tile") # REMOVE LATER  
            col = mouse_x // BUTTON_SIZE
            if (row == GRID_SIZE) and (0 <= col < 4):
                ts = TreeSearch(main_view.board) # Initialize the tree search object
                sequence = []
                
                match col:
                    
                    case 0:
                        main_view.shuffle_board(50)
                    case 1:
                        print("Solving with BFS")
                        sequence = ts.BFS_solve()
                    case 2: 
                        print("Solving with A*")
                        sequence = ts.A_star_solve()
                    case 3:
                        print("Solving with IDA*")
                        sequence = ts.IDA_star_solve()
                    case _:
                        pass
                if sequence:
                    print("Recieved sequence: ", sequence) # REMOVE LATER
                    for move in sequence:
                        main_view.board.perform_action(move)

    # Draw the game board
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = main_view.board.grid[row][col]
            if tile != 0:
                pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                text = FONT.render(str(tile), True, WHITE)
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)

    # Draw buttons around the empty tile
    


    # Draw the buttons for the algorithms at the bottom of the screen, and the shuffle button using RED, BLUE, YELLOW, and GREEN
    BUTTON_SIZE = WIDTH // 4

    pygame.draw.rect(screen, RED,       (0              , GRID_SIZE * TILE_SIZE, BUTTON_SIZE, BUTTON_HEIGHT))
    pygame.draw.rect(screen, BLUE,      (BUTTON_SIZE    , GRID_SIZE * TILE_SIZE, BUTTON_SIZE, BUTTON_HEIGHT))
    pygame.draw.rect(screen, PURPLE,    (2 * BUTTON_SIZE, GRID_SIZE * TILE_SIZE, BUTTON_SIZE, BUTTON_HEIGHT))
    pygame.draw.rect(screen, GREEN,     (3 * BUTTON_SIZE, GRID_SIZE * TILE_SIZE, BUTTON_SIZE, BUTTON_HEIGHT))

    # Have the buttons display the names of the algorithms
    button_names = ["Shuffle", "BFS", "A*", "IDA*"]
    button_positions = [1, 3, 5, 7]
    button_colors = [RED, BLUE, PURPLE, GREEN]

    for name, position, color in zip(button_names, button_positions, button_colors):
        text = FONT.render(name, True, WHITE)
        text_rect = text.get_rect(center=(position * BUTTON_WIDTH, GRID_SIZE * TILE_SIZE + BUTTON_HEIGHT // 2))
        screen.blit(text, text_rect)

    # Link the buttons to the algorithms
    

    

    pygame.display.flip()
