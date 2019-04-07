#Make generate_all_legal_moves quicker!

from chessPieces import *
import pygame
import sys #For sys.exit()
from chessPlayer_tree import *

def get_player_positions(board, player):
    """
    Takes in the board as a list and player (10 for white, 20 for black).
    Returns a list of all the positions that the player has pieces on.
    """
    positions = []
    for spot in range(len(board)):
        piece = board[spot]
        if piece != 0:
            if piece.opponent != player:
                positions += [spot]
    return positions

def board_state(board, player):
    """
    Takes in the board as a list and player (10 for white, 20 for black).
    Evaluates the board state and returns as a float.
    """
    #Values corresponding to positions on board
    wKing = [2,3,1,0,0,1,3,2,2,2,0,0,0,0,2,2,-1,-2,-2,-2,-2,-2,-2,-1,-2,-3,-3,-4,-4,-3,-3,-2,-3,-4,-4,-5,-5,-4,-4,-3,-3,-4,-4,-5,-5,-4,-4,-3,-3,-4,-4,-5,-5,-4,-4,-3,-3,-4,-4,-5,-5,-4,-4,-3]
    bKing = [-3,-4,-4,-5,-5,-4,-4,-3,-3,-4,-4,-5,-5,-4,-4,-3,-3,-4,-4,-5,-5,-4,-4,-3,-3,-4,-4,-5,-5,-4,-4,-3,-2,-3,-3,-4,-4,-3,-3,-2,-1,-2,-2,-2,-2,-2,-2,-1,2,2,0,0,0,0,2,2,2,3,1,0,0,1,3,2]
    wQueen = [-2,-1,-1,-0.5,-0.5,-1,-1,-2,-1,0,0,0,0,0.5,0,-1,-1,0,0.5,0.5,0.5,0.5,0.5,-1,-0.5,0,0.5,0.5,0.5,0.5,0,0,-0.5,0,0.5,0.5,0.5,0.5,0,-0.5,-1,0,0.5,0.5,0.5,0.5,0,-1,-1,0,0,0,0,0,0,-1,-2,-1,-1,-0.5,-0.5,-1,-1,-2]
    bQueen = [-2,-1,-1,-0.5,-0.5,-1,-1,-2,-1,0,0,0,0,0,0,-1,-1,0,0.5,0.5,0.5,0.5,0,-1,-0.5,0,0.5,0.5,0.5,0.5,0,-0.5,-0.5,0,0.5,0.5,0.5,0.5,0,0,-1,0,0.5,0.5,0.5,0.5,0.5,-1,-1,0,0,0,0,0.5,0,-1,-2,-1,-1,-0.5,-0.5,-1,-1,-2]
    wRook = [0,0,0,0.5,0.5,0,0,0,-0.5,0,0,0,0,0,0,-0.5,-0.5,0,0,0,0,0,0,-0.5,-0.5,0,0,0,0,0,0,-0.5,-0.5,0,0,0,0,0,0,-0.5,-0.5,0,0,0,0,0,0,-0.5,0.5,1,1,1,1,1,1,0.5,0,0,0,0,0,0,0,0]
    bRook = [0,0,0,0,0,0,0,0,0.5,1,1,1,1,1,1,0.5,-0.5,0,0,0,0,0,0,-0.5,-0.5,0,0,0,0,0,0,-0.5,-0.5,0,0,0,0,0,0,-0.5,-0.5,0,0,0,0,0,0,-0.5,-0.5,0,0,0,0,0,0,-0.5,0,0,0,0.5,0.5,0,0,0]
    wBishop = [-2,-1,-1,-1,-1,-1,-1,-2,-1,0.5,0,0,0,0,0.5,-1,-1,1,1,1,1,1,1,-1,-1,0,1,1,1,1,0,-1,-1,0.5,0.5,1,1,0.5,0.5,-1,-1,0,0.5,1,1,0.5,0,-1,-1,0,0,0,0,0,0,-1,-2,-1,-1,-1,-1,-1,-1,-2]
    bBishop = [-2,-1,-1,-1,-1,-1,-1,-2,-1,0,0,0,0,0,0,-1,-1,0,0.5,1,1,0.5,0,-1,-1,0.5,0.5,1,1,0.5,0.5,-1,-1,0,1,1,1,1,0,-1,-1,1,1,1,1,1,1,-1,-1,0.5,0,0,0,0,0.5,-1,-2,-1,-1,-1,-1,-1,-1,-2]
    wKnight = [-5,-4,-3,-3,-3,-3,-4,-5,-4,-2,0,0.5,0.5,0,-2,-4,-3,0.5,1,1.5,1.5,1,0.5,-3,-3,0,1.5,2,2,1.5,0,-3,-3,0.5,1.5,2,2,1.5,0.5,-3,-3,0,1,1.5,1.5,1,0,-3,-4,-2,0,0,0,0,-2,-4,-5,-4,-3,-3,-3,-3,-4,-5]
    bKnight = [-5,-4,-3,-3,-3,-3,-4,-5,-4,-2,0,0,0,0,-2,-4,-3,0,1,1.5,1.5,1,0,-3,-3,0.5,1.5,2,2,1.5,0.5,-3,-3,0,1.5,2,2,1.5,0,-3,-3,0.5,1,1.5,1.5,1,0.5,-3,-4,-2,0,0.5,0.5,0,-2,-4,-5,-4,-3,-3,-3,-3,-4,-5]
    wPawn = [0,0,0,0,0,0,0,0,0.5,1,1,-2,-2,1,1,0.5,0.5,-0.5,-1,0,0,-1,-0.5,0.5,0,0,0,2,2,0,0,0,0.5,0.5,1,2.5,2.5,1,0.5,0.5,1,1,2,3,3,2,1,1,5,5,5,5,5,5,5,5,0,0,0,0,0,0,0,0]
    bPawn = [0,0,0,0,0,0,0,0,5,5,5,5,5,5,5,5,1,1,2,3,3,2,2,1,0.5,0.5,1,2.5,2.5,1,0.5,0.5,0,0,0,2,2,0,0,0,0.5,-0.5,-1,0,0,-1,-0.5,0.5,0.5,1,1,-2,-2,1,1,0.5,0,0,0,0,0,0,0,0]

    score = 0
    positions = get_player_positions(board, player)
    if player == 10:
        opponent = 20
        oppPositions = get_player_positions(board, opponent)
        for p in positions:    
            piece = type(board[p])
            if piece == Pawn:
                score = score + 1 + wPawn[p]
            if piece == Knight:
                score = score + 3 + wKnight[p]
            if piece == Bishop:
                score = score + 3 + wBishop[p]
            if piece == Rook:
                score = score + 5 + wRook[p]
            if piece == Queen:
                score = score + 9 + wQueen[p]
            if piece == King:
                score = score + 200 + wKing[p]
        for p in oppPositions:    
            piece = type(board[p])
            if piece == Pawn:
                score = score - 1 - bPawn[p]
            if piece == Knight:
                score = score - 3 - bKnight[p]
            if piece == Bishop:
                score = score - 3 - bBishop[p]
            if piece == Rook:
                score = score - 5 - bRook[p]
            if piece == Queen:
                score = score - 9 - bQueen[p]
            if piece == King:
                score = score - 200 - bKing[p]
    else:
        opponent = 10
        oppPositions = get_player_positions(board, opponent)
        for p in positions:    
            piece = type(board[p])
            if piece == Pawn:
                score = score + 1 + bPawn[p]
            if piece == Knight:
                score = score + 3 + bKnight[p]
            if piece == Bishop:
                score = score + 3 + bBishop[p]
            if piece == Rook:
                score = score + 5 + bRook[p]
            if piece == Queen:
                score = score + 9 + bQueen[p]
            if piece == King:
                score = score + 200 + bKing[p]
        for p in oppPositions:    
            piece = type(board[p])
            if piece == Pawn:
                score = score - 1 - wPawn[p]
            if piece == Knight:
                score = score - 3 - wKnight[p]
            if piece == Bishop:
                score = score - 3 - wBishop[p]
            if piece == Rook:
                score = score - 5 - wRook[p]
            if piece == Queen:
                score = score - 9 - wQueen[p]
            if piece == King:
                score = score - 200 - wKing[p]
    return score

def generate_all_legal_moves(board, player):
    """
    Takes in the board as a list and player (10 for white, 20 for black).
    Returns all possible moves for the player as a list of 2-lists.
    """
    all_pieces = get_player_positions(board, player)
    #Find the king
    king_position = -1
    for piece in all_pieces:
        if type(board[piece]) == King:
            king_position = piece
            break
    legal_moves = []
    if king_position == -1:
        return legal_moves
    for a in all_pieces:
        moves = (board[a]).get_moves(board)
        if a != king_position:
            for m in moves:
                temp = board[m]
                board[m] = board[a]
                board[a] = 0
                if check_checker(board, king_position, player) == False:
                    legal_moves += [[a, m]]
                board[a] = board[m]
                board[m] = temp
        else:
            #Moving the king
            for m in moves:
                temp = board[m]
                board[m] = board[a]
                board[a] = 0
                if check_checker(board, m, player) == False:
                    legal_moves += [[a, m]]
                board[a] = board[m]
                board[m] = temp
    return legal_moves

def position_to_coor(position, square_dim):
    """
    Used to convert the mouse input into which square is being clicked on.
    Takes in a position as a float and the side length of a square.
    Returns which square is being clicked on as a tuple of (row, column).
    """
    #Get position and convert to coordinate on board
    x = (7 - (position % 8)) * square_dim
    y = (7 - (position // 8)) * square_dim
    return (x, y)

def gameplay():
    """
    Runs chess and return True upon exiting.
    """
    player = "White"
    screen_dim = 640

    pygame.init() #Start pygame
    screen = pygame.display.set_mode((screen_dim, screen_dim)) #Opens a window

    #Load pictures to use - use .convert() so that it draws faster
    chess_board = pygame.image.load("Media\\board.png").convert()
    selected_piece = pygame.image.load("Media\\green_box.png").convert()
    possible_move = pygame.image.load("Media\\green_circle_small.png").convert_alpha()

    #Create and draw the board
    selected = False #Boolean that shows if a piece has been clicked
    square_dim = screen_dim // 8
    board = [Rook(0, 10, square_dim), Knight(1, 10, square_dim), Bishop(2, 10, square_dim),\
             King(3, 10, square_dim), Queen(4, 10, square_dim), Bishop(5, 10, square_dim),\
             Knight(6, 10, square_dim), Rook(7, 10, square_dim), Pawn(8, 10, square_dim),\
             Pawn(9, 10, square_dim), Pawn(10, 10, square_dim), Pawn(11, 10, square_dim),\
             Pawn(12, 10, square_dim), Pawn(13, 10, square_dim), Pawn(14, 10, square_dim),\
             Pawn(15, 10, square_dim), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Pawn(48, 20, square_dim),\
             Pawn(49, 20, square_dim), Pawn(50, 20, square_dim), Pawn(51, 20, square_dim),\
             Pawn(52, 20, square_dim), Pawn(53, 20, square_dim), Pawn(54, 20, square_dim),\
             Pawn(55, 20, square_dim), Rook(56, 20, square_dim), Knight(57, 20, square_dim),\
             Bishop(58, 20, square_dim), King(59, 20, square_dim), Queen(60, 20, square_dim),\
             Bishop(61, 20, square_dim), Knight(62, 20, square_dim), Rook(63, 20, square_dim)]
    screen.blit(chess_board, (0, 0))
    for piece in board:
        if piece != 0:
            screen.blit(piece.img, (position_to_coor(piece.position, square_dim)))
    pygame.display.update() #Updates the screen
    ai_turn = False
    #Run the game
    if player == "White":
        while True:
            #If it is the computer's turn
            if ai_turn == True:
                print("thinking")
                ai_turn = False
                state, ai_move = (chess_player(board, 20))
                #If no possible moves
                if state == False:
                    print("Game over")
                    break
                #AI makes a move
                board[ai_move[0]].set_position(board, ai_move[1])
                print("My move is", ai_move[1])
                #Pawn promotion
                for i in range(0,8,1):
                    if type(board[i]) == Pawn:
                        board[i] = Queen(i, 20, square_dim)
                #Redraw the board
                screen.blit(chess_board, (0, 0))
                for piece in board:
                        if piece != 0:
                            screen.blit(piece.img, (position_to_coor(piece.position, square_dim)))
                #If the player has no possible moves, ie. checkmate
                possible_moves = generate_all_legal_moves(board, 10)
                if len(possible_moves) == 0:
                    print("Game over")
                    break
            for event in pygame.event.get(): #Opens a list of every event
                #User clicks the red X to exit
                if event.type == pygame.QUIT: #Means the user clicked the red X
                    pygame.quit() #Shut down pygame and closes window
                    sys.exit() #Shuts down the program
                #Mouse is clicked
                if event.type == pygame.MOUSEBUTTONUP and selected == False:
                    x, y = pygame.mouse.get_pos() #Gets position of mouse
                    col = 7 - (x // square_dim)
                    row = 7 - (y // square_dim)
                    pos = row * 8 + col
                    if (board[pos]) != 0:
                        #Shade positions that are possible moves
                        if (board[pos]).opponent == 20:
                            screen.blit(selected_piece, (position_to_coor(pos, square_dim)))
                            screen.blit((board[pos]).img, (position_to_coor(pos, square_dim)))
                            #Generate all legal moves
                            moves = []
                            #Find the king
                            all_pieces = get_player_positions(board, 10)
                            king_position = -1
                            for piece in all_pieces:
                                if type(board[piece]) == King:
                                    king_position = piece
                                    break
                            if pos != king_position:
                                for i in (board[pos]).get_moves(board):
                                    temp = board[i]
                                    board[i] = board[pos]
                                    board[pos] = 0
                                    if check_checker(board, king_position, 10) == False:
                                        moves += [i]
                                        coor = position_to_coor(i, square_dim)
                                        screen.blit(possible_move, coor)
                                    board[pos] = board[i]
                                    board[i] = temp
                            else:
                                #Moving the king
                                for i in (board[pos]).get_moves(board):
                                    temp = board[i]
                                    board[i] = board[pos]
                                    board[pos] = 0
                                    if check_checker(board, i, 10) == False:
                                        moves += [i]
                                        coor = position_to_coor(i, square_dim)
                                        screen.blit(possible_move, coor)
                                    board[pos] = board[i]
                                    board[i] = temp
                            selected = True
                            #Restart the while loop
                            continue
                #Mouse is clicked the second time (when a piece has been
                #selected)
                if event.type == pygame.MOUSEBUTTONUP and selected == True:
                    x, y = pygame.mouse.get_pos()
                    col = 7 - (x // square_dim)
                    row = 7 - (y // square_dim)
                    move_pos = row * 8 + col
                    #If the move is legal, move it
                    if move_pos in moves:
                        (board[pos]).set_position(board, move_pos)
                        ai_turn = True
                    #Pawn promotion
                    for i in range(56,64,1):
                        if type(board[i]) == Pawn:
                            board[i] = Queen(i, 10, square_dim)
                    #Redraw the board
                    screen.blit(chess_board, (0, 0))
                    for piece in board:
                        if piece != 0:
                            screen.blit(piece.img, (position_to_coor(piece.position, square_dim)))
                    selected = False
                    #Restart the while loop
                    continue
            pygame.display.update()
        #After the game has ended, allow the user to still exit the program
        #via clicking the red 'X'
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        return True
    
def chess_player(board, player):
    """
    This is the AI.
    Takes in the board as a list and player (10 for white, 20 for black).
    Returns the state of the game as a boolean where True indicates the AI can
    make a move and False indicates it cannot, and its move if the state is
    True.
    """
    simulation_board = list(board)
    if player == 10:
        opponent = 20
    else:
        opponent = 10
    all_moves = generate_all_legal_moves(board, player)
    possibilities = maxHeap()

    #Just for one level deep
    if len(all_moves) >= 1:
        for move in all_moves:
            temp = simulation_board[move[1]]
            simulation_board[move[1]] = simulation_board[move[0]]
            simulation_board[move[0]] = 0
            value = board_state(simulation_board, player)
            possibilities.add_child(move, value)
            simulation_board[move[0]] = simulation_board[move[1]]
            simulation_board[move[1]] = temp
        return [True, possibilities.get_max()[0]]
    else:
        return [False, all_moves]

if __name__ == "__main__":
    gameplay()
