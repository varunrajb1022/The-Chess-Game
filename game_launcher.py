import pygame
from board_and_pieces import Board, Queen, Bishop, Knight, Rook
import copy


# Initialize Pygame
pygame.init()


# Screen dimensions and colors
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)


# For displaying game state
font = pygame.font.Font(None, 36)


# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50
BUTTON_X, BUTTON_Y = 750, 750  

flip_button_image = pygame.image.load('images/Flip.png')  #
flip_button_image = pygame.transform.scale(flip_button_image, (50, 50)) 
flipped = True


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

# Draw the flip button
def draw_flip_button(screen):
    screen.blit(flip_button_image, (BUTTON_X, BUTTON_Y))

# Draw stalemate text
def draw_stalemate(screen):
    text_surface = font.render("Stalemate!", True, (255, 255, 255))
    outline_text_surface = font.render("Stalemate!", True, (0, 0, 0)) 

    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    
    center_x = (WIDTH // 2) - (text_width // 2)
    center_y = (HEIGHT // 2) - (text_height // 2) 
    offset = 1  
    screen.blit(outline_text_surface, (center_x - offset, center_y - offset)) 
    screen.blit(outline_text_surface, (center_x + offset, center_y - offset))  
    screen.blit(outline_text_surface, (center_x - offset, center_y + offset))  
    screen.blit(outline_text_surface, (center_x + offset, center_y + offset))  
    screen.blit(text_surface, (center_x, center_y))

# Draw Checkmate text
def draw_checkmate(screen, turn):
    if turn == 'w':
        text_surface = font.render("White Wins!", True, (255, 255, 255))
        outline_text_surface = font.render("White Wins!", True, (0, 0, 0))  
        king_image = piece_images['wk']
    else:  
        text_surface = font.render("Black Wins!", True, (255, 255, 255))
        outline_text_surface = font.render("Black Wins!", True, (0, 0, 0))  
        king_image = piece_images['bk']  

    king_image = pygame.transform.scale(king_image, (100, 100))

    text_width = text_surface.get_width()
    text_height = text_surface.get_height()

    center_x = (WIDTH // 2) - (text_width // 2)
    center_y = (HEIGHT // 2) - (text_height // 2) + 50

    king_x = (WIDTH // 2) - (king_image.get_width() // 2)
    king_y = center_y - king_image.get_height()   

    screen.blit(king_image, (king_x, king_y))

    offset = 1  
    screen.blit(outline_text_surface, (center_x - offset, center_y - offset)) 
    screen.blit(outline_text_surface, (center_x + offset, center_y - offset))  
    screen.blit(outline_text_surface, (center_x - offset, center_y + offset))  
    screen.blit(outline_text_surface, (center_x + offset, center_y + offset))  

    screen.blit(text_surface, (center_x, center_y))


# Draw the board
def draw_board(screen, board, flipped):
    for row in range(ROWS):
        for col in range(COLS):
            draw_row = ROWS - 1 - row if flipped else row # Check if the board is flipped
            if flipped:
                color = LIGHT_COLOR if (draw_row + col) % 2 == 0 else DARK_COLOR  
            else:
                color = DARK_COLOR if (draw_row + col) % 2 == 0 else LIGHT_COLOR
                
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, draw_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board.matrix[row][col]
            if piece is not None:
                piece_key = f"{piece.color}{piece.id}"
                piece_row = ROWS - 1 - row if flipped else row
                piece_col = col
                screen.blit(piece_images[piece_key], (piece_col * SQUARE_SIZE, piece_row * SQUARE_SIZE))


# Get the position of the square that was clicked
def get_square_under_mouse(pos, flipped):
    x, y = pos
    col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
    if flipped:
        row = ROWS - 1 - row
    return row, col


# Check if the king is safe
def kingsafe(board, turn, start_x, start_y, end_x, end_y):
    board_copy = Board()
    for i in range(len(board.matrix)):
        for j in range(len(board.matrix[i])):
            board_copy.matrix[i][j] = board.matrix[i][j]

    piece = board_copy.matrix[start_x][start_y]
    if piece and piece.valid_move(start_x, start_y, end_x, end_y, board):
        board_copy.matrix[end_x][end_y] = piece
        board_copy.matrix[start_x][start_y] = None
        if incheck(board_copy, turn):
            board_copy = None
            return False
    board_copy = None
    return True
    

# Check if the king is under attack(helper for kingsafe)
def incheck(board, turn):
    # Iterate through all the pieces
    for i in range(len(board.matrix)):
        for j in range(len(board.matrix[0])):
            if board.matrix[i][j] and board.matrix[i][j].id != 'k' and board.matrix[i][j].color!=turn and board.matrix[i][j].have_checked(board, i, j):
                return True
    return False


# Check if the king cannot excape the attack(if checkmated)
def check_mated(board, turn):
    turn = 'b' if turn == 'w' else 'w'
    # Iterate through all the pieces
    for i in range(len(board.matrix)):
        for j in range(len(board.matrix[0])):
            if board.matrix[i][j] and board.matrix[i][j].color==turn:
                valid_moves = board.matrix[i][j].get_valid_moves(i,j,board)
                for k in valid_moves:
                    if kingsafe(board, turn, i, j, k[0], k[1]):
                        return False
    return True


# Render Pawn Promotion UI
def show_promotion_ui(screen, piece_color):
    width, height = 320, 100
    x, y = (screen.get_width() - width) // 2, (screen.get_height() - height) // 2

    pygame.draw.rect(screen, DARK_COLOR, (x, y, width, height))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 2)  

    # Load promotion piece images based on color
    promotion_images = {
        'q': piece_images[f'{piece_color}q'],
        'r': piece_images[f'{piece_color}r'],
        'b': piece_images[f'{piece_color}b'],
        'n': piece_images[f'{piece_color}n']
    }

    piece_names = ['q', 'r', 'b', 'n']
    buttons = []
    spacing = (width - (4 * 70)) // 5  

    for i, piece in enumerate(piece_names):
        img = pygame.transform.scale(promotion_images[piece], (70, 70))
        button_x = x + spacing * (i + 1) + (70 * i)
        button_y = y + (height - img.get_height()) // 2
        screen.blit(img, (button_x, button_y))

        buttons.append((pygame.Rect(button_x, button_y, img.get_width(), img.get_height()), piece))

    return buttons


# Initialize board with pieces
chess_board = Board()
chess_board.initial_pos()


# Main loop
running = True
selected_tile = None
end_tile = None
turn = 'w'
checkmate = False
stalemate = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if BUTTON_X <= mouse_pos[0] <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_pos[1] <= BUTTON_Y + BUTTON_HEIGHT:
                flipped = not flipped
            else:
                # Handle board interactions
                row, col = get_square_under_mouse(pygame.mouse.get_pos(), flipped)
                if selected_tile:
                    end_tile = (row, col)
                    piece = chess_board.matrix[selected_tile[0]][selected_tile[1]]

                    if piece is not None and piece.color == turn:
                        # Check if it's a valid move
                        if piece.valid_move(selected_tile[0], selected_tile[1], row, col, chess_board):
                            if kingsafe(chess_board, turn, selected_tile[0], selected_tile[1], row, col):
                                if piece.id == 'p':
                                    if (piece.color == 'w' and end_tile[0] == 7) or (piece.color == 'b' and end_tile[0] == 0):
                                        promotion_ui_active = True
                                        promotion_buttons = show_promotion_ui(screen, piece.color)
                                        pygame.display.flip()
                                        # Pawn promotion logic
                                        while promotion_ui_active:
                                            for e in pygame.event.get():
                                                if e.type == pygame.QUIT:
                                                    running = False
                                                    promotion_ui_active = False
                                                elif e.type == pygame.MOUSEBUTTONDOWN:
                                                    mouse_pos = pygame.mouse.get_pos()
                                                    for button, promo_option in promotion_buttons:
                                                        if button.collidepoint(mouse_pos):
                                                            if promo_option == 'q':
                                                                piece = Queen(piece.color)
                                                            elif promo_option == 'r':
                                                                piece = Rook(piece.color)
                                                            elif promo_option == 'b':
                                                                piece = Bishop(piece.color)
                                                            elif promo_option == 'n':
                                                                piece = Knight(piece.color)
                                                            promotion_ui_active = False

                                chess_board.matrix[end_tile[0]][end_tile[1]] = piece
                                chess_board.matrix[selected_tile[0]][selected_tile[1]] = None
                                # Imposing Castle rule(if the rook or the king has moved before, then you cannot castle)
                                if piece.id == 'r' or piece.id == 'k':
                                    piece.move = True
                                # Call check_mated
                                if check_mated(chess_board, turn):
                                    if not incheck(chess_board, 'b' if turn == 'w' else 'w'):
                                        turn = 'b' if turn == 'w' else 'w'
                                        stalemate = True
                                    else:
                                        turn = 'b' if turn == 'w' else 'w'
                                        checkmate = True
                                else:
                                    turn = 'b' if turn == 'w' else 'w'

                    selected_tile = None
                else:
                    selected_tile = (row, col) if chess_board.matrix[row][col] is not None else None

    # Draw the board and pieces
    draw_board(screen, chess_board, flipped)
    draw_flip_button(screen)
    if checkmate:
        draw_checkmate(screen, 'b' if turn == 'w' else 'w')
    if stalemate:
        draw_stalemate(screen)

    pygame.display.flip()

pygame.quit()