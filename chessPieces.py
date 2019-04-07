#Ctr+] to indent, Ctr+[ to unindent

import pygame

def position_checker(board, position):
    """
    Takes in the board as a list and a position as an index of the board.
    Returns -10 is the position is not in the board, 0 if the position is empty,
    10 if the position has a white piece, and 20 if the position has a black
    piece.
    """
    if position < 0 or position > 63:
        return -10
    piece = board[position]
    if piece == 0:
        return 0
    if piece.opponent == 20:
        return 10
    else:
        return 20

def check_checker(board, position, player):
    """
    Takes in the board as a list, a position as an index of the board, and the
    player, where 10 is white and 20 is black.
    Returns True if the position is in threat, otherwise, False.
    """
    column = position%8
    #Check against Pawns
    if player == 10:
        opponent = 20
        if column != 7:
            if position_checker(board, position+9) == opponent:
                if type(board[position+9]) == Pawn:
                    return True
        if column != 0:
            if position_checker(board, position+7) == opponent:
                if type(board[position+7]) == Pawn:
                    return True
    else:
        opponent = 10
        if column != 0:
            if position_checker(board, position-9) == opponent:
                if type(board[position-9]) == Pawn:
                    return True
        if column != 7:
            if position_checker(board, position-7) == opponent:
                if type(board[position-7]) == Pawn:
                    return True
    piece = board[position]
    #Check against Knights
    board[position] = Knight(position, player, 0)
    moves = (board[position]).get_moves(board)
    board[position] = piece
    for m in moves:
        if type(board[m]) == Knight:
            if (board[m]).opponent == player:
                return True
    #Check against Bishops
    board[position] = Bishop(position, player, 0)
    moves = (board[position]).get_moves(board)
    board[position] = piece
    for m in moves:
        if type(board[m]) == Bishop or type(board[m]) == Queen:
            if (board[m]).opponent == player:
                return True

    #Check against Rooks
    board[position] = Rook(position, player, 0)
    moves = (board[position]).get_moves(board)
    board[position] = piece
    for m in moves:
        if type(board[m]) == Rook or type(board[m]) == Queen:
            if (board[m]).opponent == player:
                return True
    #Check against Kings
    column = position % 8
    row = position // 8
    if column != 0:
        move = position - 1
        if position_checker(board, move) == opponent:
            if type(board[move]) == King:
                return True
        move = position + 7
        if position_checker(board, move) == opponent:
            if type(board[move]) == King:
                return True
        move = position - 9
        if position_checker(board, move) == opponent:
            if type(board[move]) == King:
                return True
    if column != 7:
        move = position + 1
        if position_checker(board, move) == opponent:
            if type(board[move]) == King:
                return True
        move = position - 7
        if position_checker(board, move) == opponent:
            if type(board[move]) == King:
                return True
        move = position + 9
        if position_checker(board, move) == opponent:
            if type(board[move]) == King:
                return True
    if row != 0:
        move = position - 8
        if position_checker(board, move) == opponent:
            if type(board[move]) == King:
                return True
    if row != 7:
        if position_checker(board, move) == opponent:
            if type(board[move]) == King:
                return True
    return False

class Pawn:
    
    def __init__(self, position, player, size):
        """
        Takes in a position as an index of the board, player where 10 is white
        and 20 is black, and the float size of the side length of the sprite of
        the pawn.
        Initializes the position of the pawn to position, a boolean to keep
        track if the pawn has moved or not, the color of the pawn, and the
        pawn's sprite.
        """
        self.position = position
        #Keep track of if the pawn can move two spaces forward
        self.moved = False
        #Set up the appropriate sprite
        if player == 10:
            self.opponent = 20
            #Use .convert_alpha() so that all images have pixel by pixel
            #transparency
            img = pygame.image.load("Media\\WhitePawn.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        else:
            self.opponent = 10
            img = pygame.image.load("Media\\BlackPawn.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
            
    def set_position(self, board, position):
        """
        Takes in the board as a list, and position as an index of the board.
        Sets the position of the pawn to that of position and updates the board.
        Returns True upon successful completion.
        """
        self.moved = True
        board[position] = board[self.position]
        board[self.position] = 0
        self.position = position
        return True

    def get_moves(self, board):
        """
        Takes in the board as a list.
        Returns all possible moves the pawn can make as a list of moves where
        each integer is a possible spot the pawn can move to corresponding to
        the index of the board.
        """
        moves = []
        #White pawn
        if self.opponent == 20:
            move = self.position + 8
            if position_checker(board, move) == 0:
                moves += [move]
                if self.moved == False:
                    if position_checker(board, move+8) == 0:
                        moves += [move+8]
            column = self.position % 8
            if column != 7:
                move = self.position + 9
                if position_checker(board, move) == 20:
                    moves += [move]
            if column != 0:
                move = self.position + 7
                if position_checker(board, move) == 20:
                    moves += [move]
        #Black pawn
        if self.opponent == 10:
            move = self.position - 8
            if position_checker(board, move) == 0:
                moves += [move]
                if self.moved == False:
                    if position_checker(board, move-8) == 0:
                        moves += [move-8]
            column = self.position % 8
            if column != 7:
                move = self.position - 7
                if position_checker(board, move) == 20:
                    moves += [move]
            if column != 0:
                move = self.position - 9
                if position_checker(board, move) == 20:
                    moves += [move]
        return moves


class Knight:
    
    def __init__(self, position, player, size):
        """
        Takes in a position as an index of the board, player where 10 is white
        and 20 is black, and the float size of the side length of the sprite of
        the knight.
        Initializes the position of the knight to position, the color of the
        knight, and the knight's sprite.
        """
        self.position = position
        if player == 10:
            self.opponent = 20
            img = pygame.image.load("Media\\WhiteKnight.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        else:
            self.opponent = 10
            img = pygame.image.load("Media\\BlackKnight.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        
    def set_position(self, board, position):
        """
        Takes in the board as a list, and position as an index of the board.
        Sets the position of the knight to that of position and updates the
        board.
        Returns True upon successful completion.
        """
        board[position] = board[self.position]
        board[self.position] = 0
        self.position = position
        return True

    def get_moves(self, board):
        """
        Takes in the board as a list.
        Returns all possible moves the knight can make as a list of moves where
        each integer is a possible spot the knight can move to corresponding to
        the index of the board.
        """
        column = self.position % 8
        row = self.position // 8
        moves = []
        if column != 0:
            move = self.position + 15
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                moves += [move]
            move = self.position - 17
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                moves += [move]
        if column != 7:
            move = self.position + 17
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                moves += [move]
            move = self.position - 15
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                moves += [move]
        if row != 0:
            if column != 0 and column != 1:
                move = self.position - 10
                piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                    moves += [move]
            if column != 7 and column != 6:
                move = self.position - 6
                piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                    moves += [move]
        if row != 7:
            if column != 0 and column != 1:
                move = self.position + 6
                piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                    moves += [move]
            if column != 6 and column != 7:
                move = self.position + 10
                piece = position_checker(board, move)
                if piece == 0 or piece == self.opponent:
                    moves += [move]
        return moves


class Bishop:
    
    def __init__(self, position, player, size):
        """
        Takes in a position as an index of the board, player where 10 is white
        and 20 is black, and the float size of the side length of the sprite of
        the bishop.
        Initializes the position of the bishop to position, the color of the
        bishop, and the bishop's sprite.
        """
        self.position = position
        if player == 10:
            self.opponent = 20
            img = pygame.image.load("Media\\WhiteBishop.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        else:
            self.opponent = 10
            img = pygame.image.load("Media\\BlackBishop.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        
    def set_position(self, board, position):
        """
        Takes in the board as a list, and position as an index of the board.
        Sets the position of the bishop to that of position and updates the
        board.
        Returns True upon successful completion.
        """
        board[position] = board[self.position]
        board[self.position] = 0
        self.position = position
        return True

    def get_moves(self, board):
        """
        Takes in the board as a list.
        Returns all possible moves the bishop can make as a list of moves where
        each integer is a possible spot the bishop can move to corresponding to
        the index of the board.
        """
        moves = []
        row = self.position // 8
        column = self.position % 8
        if row > column:
            times = 7-row
        else:
            times = 7-column
        move = self.position
        for i in range(0, times, 1):
            move += 9
            piece_type = position_checker(board, move)
            if piece_type == 0:
                moves += [move]
            elif piece_type == self.opponent:
                moves += [move]
                break
            else:
                break
        rtimes = 7-row
        if rtimes < column:
            times = rtimes
        else:
            times = column
        move = self.position
        for i in range(0,times,1):
            move += 7
            piece_type = position_checker(board, move)
            if piece_type == 0:
                moves += [move]
            elif piece_type == self.opponent:
                moves += [move]
                break
            else:
                break
        ctimes = 7-column
        if row < ctimes:
            times = row
        else:
            times = ctimes
        move = self.position
        for i in range(0,times,1):
            move -= 7
            piece_type = position_checker(board, move)
            if piece_type == 0:
                moves += [move]
            elif piece_type == self.opponent:
                moves += [move]
                break
            else:
                break
        if row < column:
            times = row
        else:
            times = column
        move = self.position
        for i in range(0,times,1):
            move -= 9
            piece_type = position_checker(board, move)
            if piece_type == 0:
                moves += [move]
            elif piece_type == self.opponent:
                moves += [move]
                break
            else:
                break
        return moves


class Rook:
    
    def __init__(self, position, player, size):
        """
        Takes in a position as an index of the board, player where 10 is white
        and 20 is black, and the float size of the side length of the sprite of
        the rook.
        Initializes the position of the rook to position, a boolean to keep
        track if the rook has moved or not, the color of the rook, and the
        rook's sprite.
        """
        self.position = position
        if player == 10:
            self.opponent = 20
            img = pygame.image.load("Media\\WhiteRook.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        else:
            self.opponent = 10
            img = pygame.image.load("Media\\BlackRook.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        #Keep track if the rook can castle
        self.moved = False
        
    def set_position(self, board, position):
        """
        Takes in the board as a list, and position as an index of the board.
        Sets the position of the rook to that of position and updates the
        board.
        Returns True upon successful completion.
        """
        board[position] = board[self.position]
        board[self.position] = 0
        self.position = position
        self.moved = True
        return True

    def get_moves(self, board):
        """
        Takes in the board as a list.
        Returns all possible moves the rook can make as a list of moves where
        each integer is a possible spot the rook can move to corresponding to
        the index of the board.
        """
        moves = []
        column = self.position % 8
        move = self.position
        while True:
            move += 8
            piece_type = position_checker(board, move)
            if piece_type == 0:
                moves += [move]
            elif piece_type == self.opponent:
                moves += [move]
                break
            else:
                break
        move = self.position
        times = 7-column
        for i in range(0, times, 1):
            move += 1
            piece_type = position_checker(board, move)
            if piece_type == 0:
                moves += [move]
            elif piece_type == self.opponent:
                moves += [move]
                break
            else:
                break
        move = self.position
        for i in range(0, column, 1):
            move -= 1
            piece_type = position_checker(board, move)
            if piece_type == 0:
                moves += [move]
            elif piece_type == self.opponent:
                moves += [move]
                break
            else:
                break
        move = self.position
        while True:
            move -= 8
            piece_type = position_checker(board, move)
            if piece_type == 0:
                moves += [move]
            elif piece_type == self.opponent:
                moves += [move]
                break
            else:
                break
        return moves


class Queen(Bishop, Rook):

    def __init__(self, position, player, size):
        """
        Takes in a position as an index of the board, player where 10 is white
        and 20 is black, and the float size of the side length of the sprite of
        the queen.
        Initializes the position of the queen to position, the color of the
        queen, and the queen's sprite.
        """
        self.position = position
        if player == 10:
            self.opponent = 20
            img = pygame.image.load("Media\\WhiteQueen.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        else:
            self.opponent = 10
            img = pygame.image.load("Media\\BlackQueen.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        
    def set_position(self, board, position):
        """
        Takes in the board as a list, and position as an index of the board.
        Sets the position of the queen to that of position and updates the
        board.
        Returns True upon successful completion.
        """
        board[position] = board[self.position]
        board[self.position] = 0
        self.position = position
        return True

    def get_moves(self, board):
        """
        Takes in the board as a list.
        Returns all possible moves the queen can make as a list of moves where
        each integer is a possible spot the queen can move to corresponding to
        the index of the board.
        """
        return Bishop.get_moves(self, board) + Rook.get_moves(self, board)


class King:

    def __init__(self, position, player, size):
        """
        Takes in a position as an index of the board, player where 10 is white
        and 20 is black, and the float size of the side length of the sprite of
        the king.
        Initializes the position of the king to position, a boolean to keep
        track if the king has moved or not, the color of the king, and the
        king's sprite.
        """
        self.position = position
        self.player = player
        if player == 10:
            self.opponent = 20
            img = pygame.image.load("Media\\WhiteKing.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        else:
            self.opponent = 10
            img = pygame.image.load("Media\\BlackKing.png").convert_alpha()
            self.img = pygame.transform.scale(img, (size, size))
        self.moved = False
        
    def set_position(self, board, position):
        """
        Takes in the board as a list, and position as an index of the board.
        Sets the position of the king to that of position and updates the
        board.
        Returns True upon successful completion.
        """
        #King has not moved
        if self.moved == False:
            #White king
            if self.opponent == 20:
                #King side castle
                if position == 1:
                    if type(board[0]) == Rook:
                        if (board[0]).opponent == 20:
                            (board[0]).set_position(board, 2)
                #Queen side castle
                if position == 5:
                    if type(board[7]) == Rook:
                        if (board[7]).opponent == 20:
                            (board[7]).set_position(board, 4)
            #Black king
            if self.opponent == 10:
                #King side castle
                if position == 57:
                    if type(board[56]) == Rook:
                        if (board[56]).opponent == 10:
                            (board[56]).set_position(board, 58)
                #Queen side castle
                if position == 61:
                    if type(board[63]) == Rook:
                        if (board[63]).opponent == 10:
                            (board[63]).set_position(board, 60)
            self.moved = True
        board[position] = board[self.position]
        board[self.position] = 0
        self.position = position
        return True

    def get_moves(self, board):
        """
        Takes in the board as a list.
        Returns all possible moves the king can make as a list of moves where
        each integer is a possible spot the king can move to corresponding to
        the index of the board.
        """
        column = self.position % 8
        row = self.position // 8
        moves = []
        if column != 0:
            move = self.position - 1
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                if check_checker(board, move, self.player) == False:
                    moves += [move]
            move = self.position + 7
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                if check_checker(board, move, self.player) == False:
                    moves += [move]
            move = self.position - 9
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                if check_checker(board, move, self.player) == False:
                    moves += [move]
        if column != 7:
            move = self.position + 1
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                if check_checker(board, move, self.player) == False:
                    moves += [move]
            move = self.position - 7
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                if check_checker(board, move, self.player) == False:
                    moves += [move]
            move = self.position + 9
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                if check_checker(board, move, self.player) == False:
                    moves += [move]
        if row != 0:
            move = self.position - 8
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                if check_checker(board, move, self.player) == False:
                    moves += [move]
        if row != 7:
            move = self.position + 8
            piece = position_checker(board, move)
            if piece == 0 or piece == self.opponent:
                if check_checker(board, move, self.player) == False:
                    moves += [move]
        #Castling
        if self.moved == False:
            if self.player == 10:
                if type(board[0]) == Rook:
                    if (board[0]).moved == False:
                        if board[1] == 0:
                            if board[2] == 0:
                                if check_checker(board, 1, self.player) == False:
                                    if check_checker(board, 2, self.player) == False:
                                        if check_checker(board, 3, self.player) == False:
                                            moves += [1]
                if type(board[7]) == Rook:
                    if (board[7]).moved == False:
                        if board[4] == 0:
                            if board[5] == 0:
                                if board[6] == 0:
                                    if check_checker(board, 4, self.player) == False:
                                        if check_checker(board, 5, self.player) == False:
                                            if check_checker(board, 6, self.player) == False:
                                                if check_checker(board, 3, self.player) == False:
                                                    moves += [5]
            if self.player == 20:
                if type(board[56]) == Rook:
                    if (board[56]).moved == False:
                        if board[57] == 0:
                            if board[58] == 0:
                                print(board)
                                if check_checker(board, 57, self.player) == False:
                                    if check_checker(board, 58, self.player) == False:
                                        if check_checker(board, 59, self.player) == False:
                                            moves += [57]
                if type(board[63]) == Rook:
                    if (board[63]).moved == False:
                        if board[60] == 0:
                            if board[61] == 0:
                                if board[62] == 0:
                                    if check_checker(board, 60, self.player) == False:
                                        if check_checker(board, 61, self.player) == False:
                                            if check_checker(board, 62, self.player) == False:
                                                if check_checker(board, 59, self.player) == False:
                                                    moves += [61]
        return moves
