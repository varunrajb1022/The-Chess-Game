import pygame
from board_and_pieces import Board
import copy


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
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, draw_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # Draw pieces
            piece = board.matrix[row][col]
            if piece is not None:
                piece_key = f"{piece.color}{piece.id}"
                screen.blit(piece_images[piece_key], (col * SQUARE_SIZE, draw_row * SQUARE_SIZE))
    

def get_square_under_mouse(pos):
    x, y = pos
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    return 7 - row, col


def kingsafe(board, turn, start_x, start_y, end_x, end_y):
    board_copy = Board()
    for i in range(len(board.matrix)):
        for j in range(len(board.matrix[i])):
            board_copy.matrix[i][j] = board.matrix[i][j]

    piece = board_copy.matrix[start_x][start_y]
    Flag = True

    if piece and piece.valid_move(start_x, start_y, end_x, end_y, board):
        board_copy.matrix[end_x][end_y] = piece
        board_copy.matrix[start_x][start_y] = None
        if incheck(board_copy, turn):
            Flag = False
    return Flag
    
    
def incheck(board, turn):
    for i in range(len(board.matrix)):
        for j in range(len(board.matrix[0])):
            if board.matrix[i][j] and board.matrix[i][j].id != 'k' and board.matrix[i][j].color!=turn and board.matrix[i][j].have_checked(board, i, j):
                return True
    return False


def check_mated(board, turn):
    turn = 'b' if turn == 'w' else 'w'
    for i in range(len(board.matrix)):
        for j in range(len(board.matrix[0])):
            if board.matrix[i][j] and board.matrix[i][j].color==turn:
                valid_moves = board.matrix[i][j].get_valid_moves(i,j,board)
                for k in valid_moves:
                    if kingsafe(board, turn, i, j, k[0], k[1]):
                        return False
    return True



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
                    # Check if it's a valid move
                    if piece.valid_move(selected_tile[0], selected_tile[1], row, col, chess_board):
                        if kingsafe(chess_board, turn, selected_tile[0], selected_tile[1], row, col):
                            chess_board.matrix[end_tile[0]][end_tile[1]] = piece
                            chess_board.matrix[selected_tile[0]][selected_tile[1]] = None
                            if piece.id == 'r' or piece.id == 'k':
                                piece.move = True
                            if check_mated(chess_board, turn):
                                print('Checkmate')
                            else:
                                turn = 'b' if turn == 'w' else 'w'
                        else:
                            print("King will be left vulnerable")

                selected_tile = None
            else:
                selected_tile = (row, col) if chess_board.matrix[row][col] is not None else None

    # Draw the board and pieces
    draw_board(screen, chess_board)

    pygame.display.flip()

pygame.quit()