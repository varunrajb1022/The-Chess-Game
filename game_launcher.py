import pygame
from board_and_pieces import Board

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

# Load piece images
piece_images = {
    'wp': pygame.image.load('images\White\Pawn.png'),
    'bp': pygame.image.load('images\Black\Pawn.png'),
    'wr': pygame.image.load('images\White\Rook.png'),
    'br': pygame.image.load('images\Black\Rook.png'),
    'wn': pygame.image.load('images\White\Knight.png'),
    'bn': pygame.image.load('images\Black\Knight.png'),
    'wb': pygame.image.load('images\White\Bishop.png'),
    'bb': pygame.image.load('images\Black\Bishop.png'),
    'wq': pygame.image.load('images\White\Queen.png'),
    'bq': pygame.image.load('images\Black\Queen.png'),
    'wk': pygame.image.load('images\White\King.png'),
    'bk': pygame.image.load('images\Black\King.png')
}

# Resize images to fit on the board squares
for key in piece_images:
    piece_images[key] = pygame.transform.scale(piece_images[key], (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen, board):
    for row in range(ROWS):
        for col in range(COLS):
            draw_row = ROWS - 1 - row
            color = LIGHT_COLOR if (draw_row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Draw pieces
            piece = board.matrix[draw_row][col]
            if piece is not None:
                piece_key = f"{piece.color}{piece.id}"
                screen.blit(piece_images[piece_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_under_mouse(pos):
    x, y = pos
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    return 7 - row, col

# Initialize board with pieces
chess_board = Board()
chess_board.initial_pos()

# Main loop
running = True
selected_tile = None
end_tile = None
turn = 'w'
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_under_mouse(pygame.mouse.get_pos())
            if selected_tile:
                end_tile = (row, col)
                piece = chess_board.matrix[selected_tile[0]][selected_tile[1]]

                if piece is not None and piece.color == turn:
                    if piece.valid_move(selected_tile[0], selected_tile[1], row, col, chess_board):
                        chess_board.matrix[end_tile[0]][end_tile[1]] = piece
                        chess_board.matrix[selected_tile[0]][selected_tile[1]] = None
                        turn = 'b' if turn == 'w' else 'w'
                selected_tile = None
            else:
                selected_tile = (row, col) if chess_board.matrix[row][col] is not None else None
            

    # Draw the board and pieces
    draw_board(screen, chess_board)

    pygame.display.flip()

pygame.quit()