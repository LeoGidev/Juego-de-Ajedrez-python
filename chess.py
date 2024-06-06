import pygame
import chess
import chess.engine
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT // ROWS

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (200, 150, 100)
DARK_BROWN = (100, 75, 50)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Load images of pieces
PIECE_IMAGES = {}
pieces = ['r-b', 'n-b', 'b-b', 'q-b', 'k-b', 'p-b', 'R', 'N', 'B', 'Q', 'K', 'P']
for piece in pieces:
    PIECE_IMAGES[piece] = pygame.image.load(f'images/{piece}.png')

# Set up the board
board = chess.Board()

# Function to draw the board
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw the pieces
def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece is not None:
                piece_symbol = piece.symbol()
                screen.blit(PIECE_IMAGES[piece_symbol], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Function to handle a move
def handle_move(start_square, end_square):
    move = chess.Move(start_square, end_square)
    if move in board.legal_moves:
        board.push(move)
        return True
    return False

# Main game loop
running = True
selected_square = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
            clicked_square = chess.square(col, 7 - row)
            
            if selected_square is None:
                if board.piece_at(clicked_square) is not None and board.piece_at(clicked_square).color == board.turn:
                    selected_square = clicked_square
            else:
                if handle_move(selected_square, clicked_square):
                    selected_square = None
                else:
                    selected_square = clicked_square

    # Draw everything
    screen.fill(WHITE)
    draw_board()
    draw_pieces()
    pygame.display.update()
