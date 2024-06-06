import pygame
import chess
import sys
import random

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

# Map pieces to their image names
piece_map = {
    'r': 'r-b', 'n': 'n-b', 'b': 'b-b', 'q': 'q-b', 'k': 'k-b', 'p': 'p-b',
    'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K', 'P': 'P'
}

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
                screen.blit(PIECE_IMAGES[piece_map[piece_symbol]], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Function to handle a move
def handle_move(start_square, end_square):
    move = chess.Move(start_square, end_square)
    if move in board.legal_moves:
        board.push(move)
        return True
    return False

# Function to evaluate the board
def evaluate_board(board):
    # Simple evaluation function
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0

    material = sum([
        len(board.pieces(piece_type, chess.WHITE)) - len(board.pieces(piece_type, chess.BLACK))
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
    ])

    return material

# Function for the AI to select a move
def select_best_move(board):
    best_move = None
    best_value = -9999 if board.turn else 9999

    for move in board.legal_moves:
        board.push(move)
        board_value = evaluate_board(board)
        board.pop()

        if board.turn:
            if board_value > best_value:
                best_value = board_value
                best_move = move
        else:
            if board_value < best_value:
                best_value = board_value
                best_move = move

    return best_move

# Main game loop
running = True
selected_square = None
dragging = False
dragged_piece = None
dragged_piece_image = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not board.turn:  # If it's not the player's turn (i.e., AI's turn), ignore mouse input
                continue

            pos = pygame.mouse.get_pos()
            col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
            clicked_square = chess.square(col, 7 - row)
            
            if not dragging:
                if board.piece_at(clicked_square) is not None and board.piece_at(clicked_square).color == board.turn:
                    selected_square = clicked_square
                    dragging = True
                    dragged_piece = board.piece_at(clicked_square)
                    dragged_piece_image = PIECE_IMAGES[piece_map[dragged_piece.symbol()]]
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                pos = pygame.mouse.get_pos()
                col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                released_square = chess.square(col, 7 - row)
                if handle_move(selected_square, released_square):
                    selected_square = None
                dragging = False
                dragged_piece = None
                dragged_piece_image = None

    # Draw everything
    screen.fill(WHITE)
    draw_board()
    draw_pieces()

    if dragging and dragged_piece_image is not None:
        pos = pygame.mouse.get_pos()
        screen.blit(dragged_piece_image, (pos[0] - SQUARE_SIZE // 2, pos[1] - SQUARE_SIZE // 2))

    pygame.display.update()

    # AI Move
    if not board.turn:
        best_move = select_best_move(board)
        if best_move:
            board.push(best_move)



