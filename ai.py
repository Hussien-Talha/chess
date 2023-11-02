# Importing the chess library
import chess

# Importing the random library
import random

# Defining a simple evaluation function that assigns a score to each piece
def evaluate(board):
    # Initializing the score to zero
    score = 0
    # Looping through all the pieces on the board
    for piece in chess.PIECES:
        # Adding the value of the piece multiplied by the number of pieces of that type for white
        score += len(board.pieces(piece, chess.WHITE)) * get_piece_value(piece)
        # Subtracting the value of the piece multiplied by the number of pieces of that type for black
        score -= len(board.pieces(piece, chess.BLACK)) * get_piece_value(piece)
    # Returning the score
    return score

# Defining a function that returns the value of a piece according to a simple scheme
def get_piece_value(piece):
    # Using a dictionary to store the values
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    # Returning the value of the piece from the dictionary
    return piece_values[piece]

# Defining the minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    # Checking if the depth limit is reached or the game is over
    if depth == 0 or board.is_game_over():
        # Returning the evaluation of the board and None as the best move
        return evaluate(board), None
    # Initializing the best move to None
    best_move = None
    # If it is the maximizing player's turn (white)
    if maximizing_player:
        # Initializing the best score to negative infinity
        best_score = float("-inf")
        # Looping through all the legal moves
        for move in board.legal_moves:
            # Making a copy of the board
            board_copy = board.copy()
            # Pushing the move on the copy
            board_copy.push(move)
            # Recursively calling minimax on the copy with reduced depth, updated alpha and beta, and flipped player
            score, _ = minimax(board_copy, depth - 1, alpha, beta, False)
            # Updating the best score and best move if needed
            if score > best_score:
                best_score = score
                best_move = move
            # Updating alpha if needed
            alpha = max(alpha, best_score)
            # Pruning if alpha is greater than or equal to beta
            if alpha >= beta:
                break
        # Returning the best score and best move for white
        return best_score, best_move
    # If it is the minimizing player's turn (black)
    else:
        # Initializing the best score to positive infinity
        best_score = float("inf")
        # Looping through all the legal moves
        for move in board.legal_moves:
            # Making a copy of the board
            board_copy = board.copy()
            # Pushing the move on the copy
            board_copy.push(move)
            # Recursively calling minimax on the copy with reduced depth, updated alpha and beta, and flipped player
            score, _ = minimax(board_copy, depth - 1, alpha, beta, True)
            # Updating the best score and best move if needed
            if score < best_score:
                best_score = score
                best_move = move
            # Updating beta if needed
            beta = min(beta, best_score)
            # Pruning if alpha is greater than or equal to beta
            if alpha >= beta:
                break
        # Returning the best score and best move for black
        return best_score, best_move

# Defining a function that returns a random move among the moves with the highest score
def get_best_move(board, depth, maximizing_player):
    # Getting the score and move from minimax
    score, move = minimax(board, depth, float("-inf"), float("inf"), maximizing_player)
    # Initializing a list of moves with the same score
    moves = [move]
    # Looping through all the legal moves
    for move in board.legal_moves:
        # Making a copy of the board
        board_copy = board.copy()
        # Pushing the move on the copy
        board_copy.push(move)
        # Getting the score of the move from evaluate
        move_score = evaluate(board_copy)
        # If the score is equal to the best score
        if move_score == score:
            # Adding the move to the list of moves
            moves.append(move)
    # Returning a random choice among the moves
    return random.choice(moves)

# Defining the main function
def main():
    # Creating a new board
    board = chess.Board()
    # Printing the board
    print(board)
    # Printing a welcome message
    print("Welcome to Chess AI!")
    # Asking the user to choose a side
    side = input("Choose your side (white or black): ")
    # Validating the input
    while side not in ["white", "black"]:
        print("Invalid input. Please enter white or black.")
        side = input("Choose your side (white or black): ")
    # Setting the maximizing player flag according to the side
    if side == "white":
        maximizing_player = True
    else:
        maximizing_player = False
    # Setting the depth limit to 3 (can be changed)
    depth = 3
    # Looping until the game is over
    while not board.is_game_over():
        # If it is the user's turn
        if board.turn == maximizing_player:
            # Asking the user to enter a move in UCI format
            move = input("Enter your move: ")
            # Validating the input
            while not chess.Move.from_uci(move) in board.legal_moves:
                print("Invalid move. Please enter a legal move in UCI format.")
                move = input("Enter your move: ")
            # Pushing the move on the board
            board.push(chess.Move.from_uci(move))
            # Printing the board
            print(board)
        # If it is the AI's turn
        else:
            # Printing a message
            print("AI is thinking...")
            # Getting the best move from get_best_move
            move = get_best_move(board, depth, not maximizing_player)
            # Pushing the move on the board
            board.push(move)
            # Printing the board and the move
            print(board)
            print("AI played", move)
    # Printing the game result
    print("Game over.")
    print(board.result())

# Calling the main function
if __name__ == "__main__":
    main()
