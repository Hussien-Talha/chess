# Import pygame and chess libraries
import pygame
import chess

# Define some colors and constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WIDTH = 800 # Width of the window
HEIGHT = 800 # Height of the window
FPS = 30 # Frames per second
SQUARE_SIZE = WIDTH // 8 # Size of each square on the board
PIECE_SIZE = SQUARE_SIZE // 2 # Size of each piece on the board
OFFSET = SQUARE_SIZE // 4 # Offset of each piece from the center of the square
MODE = "two-player" # Mode of the game: "two-player" or "one-player"
LEVEL = "random" # Level of the computer opponent: "random" or "minimax"

# Initialize pygame and create a window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

# Load the images of the pieces
pieces = {}
pieces["P"] = pygame.transform.scale(pygame.image.load("images/wp.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["N"] = pygame.transform.scale(pygame.image.load("images/wn.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["B"] = pygame.transform.scale(pygame.image.load("images/wb.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["R"] = pygame.transform.scale(pygame.image.load("images/wr.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["Q"] = pygame.transform.scale(pygame.image.load("images/wq.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["K"] = pygame.transform.scale(pygame.image.load("images/wk.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["p"] = pygame.transform.scale(pygame.image.load("images/bp.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["n"] = pygame.transform.scale(pygame.image.load("images/bn.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["b"] = pygame.transform.scale(pygame.image.load("images/bb.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["r"] = pygame.transform.scale(pygame.image.load("images/br.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["q"] = pygame.transform.scale(pygame.image.load("images/bq.png"), (PIECE_SIZE, PIECE_SIZE))
pieces["k"] = pygame.transform.scale(pygame.image.load("images/bk.png"), (PIECE_SIZE, PIECE_SIZE))

# Create a chess board object using the chess library
board = chess.Board()

# Define some variables to store the game state
selected_piece = None # The piece that is selected by the player
valid_moves = [] # The list of valid moves for the selected piece
move_history = [] # The list of moves made by both players
game_over = False # The flag that indicates if the game is over
winner = None # The winner of the game
result = None # The result of the game

# Define a function to draw the board and the pieces on the screen
def draw_board():
    # Draw a green border around the board
    pygame.draw.rect(screen, GREEN, (0, 0, WIDTH, HEIGHT))
    # Draw the squares on the board
    for row in range(8):
        for col in range(8):
            # Alternate the colors of the squares
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK
            # Draw each square
            pygame.draw.rect(screen, color, (SQUARE_SIZE * col + SQUARE_SIZE // 16,
                                             SQUARE_SIZE * row + SQUARE_SIZE // 16,
                                             SQUARE_SIZE - SQUARE_SIZE // 8,
                                             SQUARE_SIZE - SQUARE_SIZE // 8))
    # Draw the pieces on the board
    for row in range(8):
        for col in range(8):
            # Get the piece at each square
            piece = board.piece_at(chess.square(col, row))
            if piece is not None:
                # Get the image of the piece
                image = pieces[piece.symbol()]
                # Draw the image on the screen at the corresponding position
                screen.blit(image,
                            (SQUARE_SIZE * col + OFFSET,
                             SQUARE_SIZE * (7 - row) + OFFSET))

# Define a function to highlight the selected piece and its valid moves on the screen
def highlight_moves():
    global selected_piece, valid_moves
    # If a piece is selected
    if selected_piece is not None:
        # Get the row and column of the selected piece
        row, col = selected_piece
        # Highlight the square of the selected piece with yellow color
        pygame.draw.rect(screen, YELLOW, (SQUARE_SIZE * col + SQUARE_SIZE // 16,
                                          SQUARE_SIZE * row + SQUARE_SIZE // 16,
                                          SQUARE_SIZE - SQUARE_SIZE // 8,
                                          SQUARE_SIZE - SQUARE_SIZE // 8))
        # Highlight the squares of the valid moves with blue color
        for move in valid_moves:
            # Get the row and column of the target square
            row, col = move.to_square // 8, move.to_square % 8
            # Draw a blue circle on the center of the square
            pygame.draw.circle(screen, BLUE, (SQUARE_SIZE * col + SQUARE_SIZE // 2,
                                              SQUARE_SIZE * (7 - row) + SQUARE_SIZE // 2),
                               PIECE_SIZE // 4)

# Define a function to draw the move history on the screen
def draw_move_history():
    global move_history
    # Set the font and the color for the text
    font = pygame.font.SysFont("Arial", 32)
    color = RED
    # Draw a horizontal line to separate the board and the move history
    pygame.draw.line(screen, color, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), 4)
    # Draw a vertical line to separate the moves of white and black players
    pygame.draw.line(screen, color, (WIDTH // 2, HEIGHT - SQUARE_SIZE), (WIDTH // 2, HEIGHT), 4)
    # Draw the text "White" and "Black" on the top of each column
    text_white = font.render("White", True, color)
    text_black = font.render("Black", True, color)
    screen.blit(text_white, (WIDTH // 4 - text_white.get_width() // 2, HEIGHT - SQUARE_SIZE + 10))
    screen.blit(text_black, (WIDTH * 3 // 4 - text_black.get_width() // 2, HEIGHT - SQUARE_SIZE + 10))
    # Draw each move in the move history
    for i in range(len(move_history)):
        # Get the move and its notation
        move = move_history[i]
        notation = board.san(move)
        # Get the text of the move
        text_move = font.render(notation, True, color)
        # Get the position of the text based on the turn and the index of the move
        if i % 2 == 0: # White's turn
            x = WIDTH // 4 - text_move.get_width() // 2
            y = HEIGHT - SQUARE_SIZE + 50 + (i // 2) * text_move.get_height()
        else: # Black's turn
            x = WIDTH * 3 // 4 - text_move.get_width() // 2
            y = HEIGHT - SQUARE_SIZE + 50 + ((i - 1) // 2) * text_move.get_height()
        # Draw the text on the screen at the corresponding position
        screen.blit(text_move, (x, y))

# Define a function to draw the game over message on the screen
def draw_game_over():
    global winner, result
    # Set the font and the color for the text
    font = pygame.font.SysFont("Arial", 64)
    color = RED
    # Draw a semi-transparent black rectangle to cover the board
    s = pygame.Surface((WIDTH - SQUARE_SIZE, HEIGHT - SQUARE_SIZE))
    s.set_alpha(128)
    s.fill((0,0,0))
    screen.blit(s, (SQUARE_SIZE // 2,SQUARE_SIZE // 2))
    # Draw the game over message on the center of the screen
    if winner is not None: # There is a winner
        text = font.render(winner + " wins!", True, color)
    else: # There is no winner (draw or stalemate)
        text = font.render(result, True, color)
    screen.blit(text,
                (WIDTH // 2 - text.get_width() // 2,
                 HEIGHT // 2 - text.get_height() // 2))

# Define a function to get a random valid move for the computer opponent
def get_random_move():
    global board
    # Get all legal moves for the current board position
    legal_moves = list(board.legal_moves)
    # If there are no legal moves, return None
    if len(legal_moves) == 0:
        return None
    # Otherwise, choose a random move from the list and return it
    import random
    return random.choice(legal_moves)

# Define a function to get a minimax move for the computer opponent using alpha-beta pruning and a simple evaluation function
def get_minimax_move(depth, alpha, beta, is_maximizing):
    global board
    # If the depth is zero or the game is over, return the evaluation of the board position
    if depth == 0 or board.is_game_over():
        return None, evaluate_board()
    # If it is the maximizing player's turn (white)
    if is_maximizing:
        # Initialize the best move and the best score
        best_move = None
        best_score = -float("inf")
        # Loop through all legal moves
        for move in board.legal_moves:
            # Make the move on the board
            board.push(move)
            # Recursively get the score of the move using alpha-beta pruning
            _, score = get_minimax_move(depth - 1, alpha, beta, False)
            # Undo the move on the board
            board.pop()
            # Update the best move and the best score if the current score is higher
            if score > best_score:
                best_move = move
                best_score = score
            # Update the alpha value if the current score is higher
            alpha = max(alpha, score)
            # Prune the branch if alpha is greater than or equal to beta
            if alpha >= beta:
                break
        # Return the best move and the best score for the maximizing player
        return best_move, best_score
    # If it is the minimizing player's turn (black)
    else:
        # Initialize the best move and the best score
        best_move = None
        best_score = float("inf")
        # Loop through all legal moves
        for move in board.legal_moves:
            # Make the move on the board
            board.push(move)
            # Recursively get the score of the move using alpha-beta pruning
            _, score = get_minimax_move(depth - 1, alpha, beta, True)
            # Undo the move on the board
            board.pop()
            # Update the best move and the best score if the current score is lower
            if score < best_score:
                best_move = move
                best_score = score
            # Update the beta value if the current score is lower
            beta = min(beta, score)
            # Prune the branch if alpha is greater than or equal to beta
            if alpha >= beta:
                break
        # Return the best move and the best score for the minimizing player
        return best_move, best_score

# Define a function to evaluate the board position using a simple piece value heuristic
def evaluate_board():
    global board
    # Define a dictionary of piece values
    piece_values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0,
                    "p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": 0}
    # Initialize the total evaluation to zero
    evaluation = 0
    # Loop through all squares on the board
    for square in chess.SQUARES:
        # Get the piece at each square
        piece = board.piece_at(square)
        if piece is not None:
            # Add or subtract the piece value to/from the evaluation based on its color
            symbol = piece.symbol()
            value = piece_values[symbol]
            evaluation += value
    # Return the evaluation from white's perspective (positive means white is better, negative means black is better)
    return evaluation

# Define a function to make a move for the computer opponent based on its level (random or minimax)
def make_computer_move():
    global board, LEVEL, game_over, winner, result
    # If it is white's turn and one-player mode is selected and level is random or minimax 
    if board.turn == chess.WHITE and MODE == "one-player" and LEVEL in ["random", "minimax"]:
        # Get a move for the computer opponent based on its level 
        if LEVEL == "random":
            move = get_random_move()
        elif LEVEL == "minimax":
            move, _ = get_minimax_move(3, -float("inf"), float("inf"), True) # Use a depth of 3 for minimax search 
        # If there is a valid move 
        if move is not None:
            # Make the move on the board 
            board.push(move)
            # Add the move to the move history 
            move_history.append(move)
        else: 
            # If there is no valid move, set game over flag to True 
            game_over = True 
        # Check if the game is over 
        if board.is_game_over():
            # Set game over flag to True 
            game_over = True
            # Get the result of the game 
            result = board.result()
            # Declare the winner or the result 
            if result == "1-0":
                winner = "White"
            elif result == "0-1":
                winner = "Black"
            elif result == "1/2-1/2":
                result = "Draw"
            elif result == "*":
                result = "Stalemate"

# Define a function to handle the mouse events
def handle_mouse_events():
    global board, selected_piece, valid_moves, move_history, game_over, winner, result
    # Get the position of the mouse
    x, y = pygame.mouse.get_pos()
    # Get the row and column of the square that the mouse is on
    row = 7 - (y - SQUARE_SIZE // 2) // SQUARE_SIZE
    col = (x - SQUARE_SIZE // 2) // SQUARE_SIZE
    # If the mouse is clicked
    if pygame.mouse.get_pressed()[0]:
        # If a piece is not selected yet
        if selected_piece is None:
            # If there is a piece on the square that the mouse is on and it is the right color
            if board.piece_at(chess.square(col, row)) is not None and board.piece_at(chess.square(col, row)).color == board.turn:
                # Select the piece and get its valid moves
                selected_piece = (row, col)
                valid_moves = list(board.legal_moves)
                valid_moves = [move for move in valid_moves if move.from_square == chess.square(col, row)]
        # If a piece is already selected
        else:
            # If the mouse is on a different square than the selected piece
            if (row, col) != selected_piece:
                # Create a move object from the selected piece to the target square
                move = chess.Move.from_uci(chess.SQUARE_NAMES[chess.square(selected_piece[1], selected_piece[0])] +
                                           chess.SQUARE_NAMES[chess.square(col, row)])
                # If the move is valid
                if move in valid_moves:
                    # Make the move on the board
                    board.push(move)
                    # Add the move to the move history
                    move_history.append(move)
                    # Deselect the piece and reset its valid moves
                    selected_piece = None
                    valid_moves = []
                    # Check if the game is over
                    if board.is_game_over():
                        # Set game over flag to True
                        game_over = True
                        # Get the result of the game
                        result = board.result()
                        # Declare the winner or the result
                        if result == "1-0":
                            winner = "White"
                        elif result == "0-1":
                            winner = "Black"
                        elif result == "1/2-1/2":
                            result = "Draw"
                        elif result == "*":
                            result = "Stalemate"
                else: # If the move is not valid
                    # Deselect the piece and reset its valid moves
                    selected_piece = None
                    valid_moves = []

# Define a function to handle the keyboard events
def handle_keyboard_events():
    global MODE, LEVEL, board, move_history, game_over, winner, result
    # Get all pressed keys 
    keys = pygame.key.get_pressed()
    # If R key is pressed 
    if keys[pygame.K_r]:
        # Reset the mode, level, board, move history, game over flag, winner and result 
        MODE = "two-player"
        LEVEL = "random"
        board = chess.Board()
        move_history = []
        game_over = False 
        winner = None 
        result = None 
    # If M key is pressed 
    if keys[pygame.K_m]:
        # Toggle between two-player and one-player modes 
        if MODE == "two-player":
            MODE = "one-player"
        else:
            MODE = "two-player"
    # If L key is pressed 
    if keys[pygame.K_l]:
        # Toggle between random and minimax levels for one-player mode 
        if MODE == "one-player":
            if LEVEL == "random":
                LEVEL = "minimax"
            else:
                LEVEL = "random"

# Define a function to update the game logic 
def update():
    global game_over 
    # If the game is not over 
    if not game_over:
        # Make a move for the computer opponent based on its level 
        make_computer_move()

# Define a function to draw everything on the screen 
def draw():
    global game_over 
    # Draw the board and the pieces on the screen 
    draw_board()
    # Highlight the selected piece and its valid moves on the screen 
    highlight_moves()
    # Draw the move history on the screen
    # Define a function to draw everything on the screen 
def draw():
    global game_over 
    # Draw the board and the pieces on the screen 
    draw_board()
    # Highlight the selected piece and its valid moves on the screen 
    highlight_moves()
    # Draw the move history on the screen 
    draw_move_history()
    # If the game is over, draw the game over message on the screen 
    if game_over:
        draw_game_over()

# Define the main loop of the game 
running = True
while running:
    # Set the frame rate 
    clock.tick(FPS)
    # Handle the events 
    for event in pygame.event.get():
        # If the user quits, exit the loop 
        if event.type == pygame.QUIT:
            running = False
        # If the user clicks the mouse, handle the mouse events 
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_events()
        # If the user presses a key, handle the keyboard events 
        if event.type == pygame.KEYDOWN:
            handle_keyboard_events()
    # Update the game logic 
    update()
    # Draw everything on the screen 
    draw()
    # Update the display 
    pygame.display.flip()

# Quit pygame 
pygame.quit()
