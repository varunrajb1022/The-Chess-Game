class Board:
    def __init__(self):
        self.matrix = [[None for _ in range(8)] for _ in range(8)]

    def initial_pos(self):
        # Initial pawn position
        for i in range(8):
            self.matrix[1][i] = Pawn('w')
            self.matrix[6][i] = Pawn('b')

        # Initial piece positions
        back_rank_white = [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')]
        back_rank_black = [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')]

        self.matrix[0] = back_rank_white
        self.matrix[7] = back_rank_black


class Pawn:
    def __init__(self, color):
        self.color = color
        self.id = 'p'

    def valid_move(self, start_x, start_y, end_x, end_y, board):
        direction = 1 if self.color == 'w' else -1

        # Move one square forward
        if start_y == end_y and end_x == start_x + direction and board.matrix[end_x][end_y] == None:
            return True
        
        # Initial double forward 
        if start_y == end_y and end_x == start_x + 2*direction and board.matrix[end_x][end_y] == None and  (start_x == 1 or start_x == 6):
            return True

        # Capture move
        if end_x == start_x + direction and abs(start_y - end_y) == 1:
            target_piece = board.matrix[end_x][end_y]
            if target_piece and target_piece.color != self.color:
                return True
        return False


    def have_checked(self, board, start_x, start_y):
        directions =  [[1, -1], [1, 1]] if self.color == 'w' else [[-1, -1], [-1, 1]]
        for i in directions:
            r, c = start_x + i[0], start_y + i[1]
            if r in range(len(board.matrix)) and c in range(len(board.matrix[0])):
                if board.matrix[r][c] is not None and board.matrix[r][c].id == 'k' and board.matrix[r][c].color != self.color:
                    return True
        return False

    def get_valid_moves(self, start_x, start_y, board):
        valid_moves = set()
        for end_x in range(8):
            for end_y in range(8):
                if self.valid_move(start_x, start_y, end_x, end_y, board):
                    valid_moves.add((end_x, end_y))
        return valid_moves

class Queen:
    def __init__(self,color):
        self.color = color
        self.id = 'q'

    def valid_move(self, start_x, start_y, end_x, end_y, board):
        directions = [[1,1], [1,-1], [-1,1], [-1,-1], [1,0], [0,1], [-1,0], [0,-1]]
        target = board.matrix[end_x][end_y]
        for i in directions:
            r, c = start_x, start_y
            while r+i[0] in range(len(board.matrix)) and c+i[1] in range(len(board.matrix[0])):
                r+=i[0]
                c+=i[1]
                if r == end_x and c == end_y:
                    if target is None:
                        return True
                    # Check Capture
                    elif target.color!= self.color:
                        return True

                # If something is in the way, stop
                elif board.matrix[r][c] is not None:
                    break
        return False


    def have_checked(self, board, start_x, start_y):
        directions = [[1,1], [1,-1], [-1,1], [-1,-1], [1,0], [0,1], [-1,0], [0,-1]]
        for i in directions:
            r, c = start_x, start_y
            while r+i[0] in range(len(board.matrix)) and c+i[1] in range(len(board.matrix[0])):
                r+=i[0]
                c+=i[1]
                if board.matrix[r][c] is not None:
                    if board.matrix[r][c].id == 'k' and board.matrix[r][c].color != self.color:
                        return True
                    else:
                        break
        return False
    
    def get_valid_moves(self, start_x, start_y, board):
        valid_moves = set()
        for end_x in range(8):
            for end_y in range(8):
                if self.valid_move(start_x, start_y, end_x, end_y, board):
                    valid_moves.add((end_x, end_y))
        return valid_moves



class King:
    def __init__(self,color):
        self.color = color
        self.id = 'k'
        self.move = False

    def valid_move(self, start_x, start_y, end_x, end_y, board, mt = 'n'):
        directions = [[1,1], [1,-1], [-1,1], [-1,-1], [1,0], [0,1], [-1,0], [0,-1]]
        target = board.matrix[end_x][end_y]
        for i in directions:
            if start_x + i[0] == end_x and start_y + i[1] == end_y:
                if target is None:
                    return True
                # Check Capture
                elif target.color!= self.color:
                    return True
        
        
        if self.color == 'w' and (start_x == 0 and start_y == 4) and (end_x == 0 and end_y == 6) and board.matrix[0][5] is None and board.matrix[0][6] is None and board.matrix[0][7] is not None and board.matrix[0][7].id == 'r' and self.move == False and board.matrix[0][7].move == False and mt == 'n':
            for i in range(len(board.matrix)):
                for j in range(len(board.matrix[0])):
                    if board.matrix[i][j] and board.matrix[i][j].color!=self.color:
                        valid_moves = board.matrix[i][j].get_valid_moves(i,j,board)
                        if (0,6) in valid_moves or (0,7) in valid_moves:
                            return False
                        else:
                            continue     
            board.matrix[0][5] = board.matrix[0][7]
            board.matrix[0][7] = None
            self.move = True
            return True
        
        elif self.color == 'w' and (start_x == 0 and start_y == 4) and (end_x == 0 and end_y == 2) and board.matrix[0][3] is None and board.matrix[0][2] is None and board.matrix[0][0] is not None and board.matrix[0][0].id == 'r' and self.move == False and board.matrix[0][0].move == False and mt == 'n':
            for i in range(len(board.matrix)):
                for j in range(len(board.matrix[0])):
                    if board.matrix[i][j] and board.matrix[i][j].color!=self.color:
                        valid_moves = board.matrix[i][j].get_valid_moves(i,j,board)
                        if (0,3) in valid_moves or (0,2) in valid_moves:
                            return False
                        else:
                            continue 
            board.matrix[0][3] = board.matrix[0][0]
            board.matrix[0][0] = None 
            self.move = True
            return True

        elif self.color == 'b' and (start_x == 7 and start_y == 4) and (end_x == 7 and end_y == 6) and board.matrix[7][5] is None and board.matrix[7][6] is None and board.matrix[7][7] is not None and board.matrix[7][7].id == 'r' and self.move == False and board.matrix[7][7].move == False and mt == 'n':
            for i in range(len(board.matrix)):
                for j in range(len(board.matrix[0])):
                    if board.matrix[i][j] and board.matrix[i][j].color!=self.color:
                        valid_moves = board.matrix[i][j].get_valid_moves(i,j,board)
                        if (7,5) in valid_moves or (7,6) in valid_moves:
                            return False
                        else:
                            continue 
            board.matrix[7][5] = board.matrix[7][7]
            board.matrix[7][7] = None
            self.move = True
            return True
        
        elif self.color == 'b' and (start_x == 7 and start_y == 4) and (end_x == 7 and end_y == 2) and board.matrix[7][3] is None and board.matrix[7][2] is None and board.matrix[7][0] is not None and board.matrix[7][0].id == 'r' and self.move == False and board.matrix[7][0].move == False and mt == 'n':
            for i in range(len(board.matrix)):
                for j in range(len(board.matrix[0])):
                    if board.matrix[i][j] and board.matrix[i][j].color!=self.color:
                        valid_moves = board.matrix[i][j].get_valid_moves(i,j,board)
                        if (7,3) in valid_moves or (7,2) in valid_moves:
                            return False
                        else:
                            continue 
            board.matrix[7][3] = board.matrix[7][0]
            board.matrix[7][0] = None 
            self.move = True
            return True

        else:
            return False

    def have_checked(self, board, start_x, start_y):
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [0, 1], [-1, 0], [0, -1]]

        for direction in directions:
            r, c = start_x + direction[0], start_y + direction[1]
            if r in range(len(board.matrix)) and c in range(len(board.matrix[0])):
                target = board.matrix[r][c]
                if target and target.id == 'k' and target.color != self.color:
                    return True
        return False
    
    def get_valid_moves(self, start_x, start_y, board):
        valid_moves = set()
        for end_x in range(8):
            for end_y in range(8):
                if self.valid_move(start_x, start_y, end_x, end_y, board, 'castle'):
                    valid_moves.add((end_x, end_y))
        return valid_moves
            

    

class Rook:
    def __init__(self,color):
        self.color = color
        self.id = 'r'
        self.move = False

    def valid_move(self, start_x, start_y, end_x, end_y, board):
        directions = [[1,0], [0,1], [-1,0], [0,-1]]
        target = board.matrix[end_x][end_y]
        for i in directions:
            r , c = start_x , start_y
            while r+i[0] in range(len(board.matrix)) and c+i[1] in range(len(board.matrix[0])):
                r+=i[0]
                c+=i[1]
                if r == end_x and c == end_y:
                    if target is None:
                        return True
                    # Check Capture
                    elif target.color!=self.color:
                        return True
                # If something is in the way, stop
                elif board.matrix[r][c] is not None:
                    break
        return False


    def have_checked(self, board, start_x, start_y):
        directions = [[1,0], [0,1], [-1,0], [0,-1]]
        for i in directions:
            r, c = start_x, start_y
            while r+i[0] in range(len(board.matrix)) and c+i[1] in range(len(board.matrix[0])):
                r+=i[0]
                c+=i[1]
                if board.matrix[r][c] is not None:
                    if board.matrix[r][c].id == 'k' and board.matrix[r][c].color != self.color:
                        return True
                    else:
                        break
        return False

    def get_valid_moves(self, start_x, start_y, board):
        valid_moves = set()
        for end_x in range(8):
            for end_y in range(8):
                if self.valid_move(start_x, start_y, end_x, end_y, board):
                    valid_moves.add((end_x, end_y))
        return valid_moves
    

class Knight:
    def __init__(self,color):
        self.color = color
        self.id = 'n'
    
    def valid_move(self, start_x, start_y, end_x, end_y, board):
        directions = [[1,2], [-1,2], [1, -2], [-1,-2], [2,1], [2,-1], [-2,1], [-2,-1]]
        target = board.matrix[end_x][end_y]
        for i in directions:
            r , c = start_x , start_y
            while r+i[0] in range(len(board.matrix)) and c+i[1] in range(len(board.matrix[0])):
                r+=i[0]
                c+=i[1]
                if r == end_x and c == end_y:
                    if target is None:
                        return True
                    # Check Capture
                    elif target.color!=self.color:
                        return True

        return False

    
    def have_checked(self, board, start_x, start_y):
        directions = [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
        for i in directions:
            r, c = start_x + i[0], start_y + i[1]
            if r in range(len(board.matrix)) and c in range(len(board.matrix[0])):
                target = board.matrix[r][c]
                if target is not None and target.id == 'k' and target.color != self.color:
                    return True
        return False

    def get_valid_moves(self, start_x, start_y, board):
        valid_moves = set()
        for end_x in range(8):
            for end_y in range(8):
                if self.valid_move(start_x, start_y, end_x, end_y, board):
                    valid_moves.add((end_x, end_y))
        return valid_moves


class Bishop:
    def __init__(self,color):
        self.color = color
        self.id = 'b'
    
    def valid_move(self, start_x, start_y, end_x, end_y, board):
        directions = [[1,1], [1,-1], [-1,1], [-1,-1]]
        target = board.matrix[end_x][end_y]
        for i in directions:
            r, c = start_x, start_y
            while r+i[0] in range(len(board.matrix)) and c+i[1] in range(len(board.matrix[0])):
                r+=i[0]
                c+=i[1]
                if r == end_x and c == end_y:
                    if target is None:
                        return True
                    # Check Capture
                    elif target.color!= self.color:
                        return True

                # If something is in the way, stop
                elif board.matrix[r][c] is not None:
                    break

        return False

    def have_checked(self, board, start_x, start_y):
        directions = [[1,1], [1,-1], [-1,1], [-1,-1]]
        for i in directions:
            r, c = start_x, start_y
            while r+i[0] in range(len(board.matrix)) and c+i[1] in range(len(board.matrix[0])):
                r+=i[0]
                c+=i[1]
                if board.matrix[r][c] is not None:
                    if board.matrix[r][c].id == 'k' and board.matrix[r][c].color != self.color:
                        return True
                    else:
                        break
        return False

    
    def get_valid_moves(self, start_x, start_y, board):
        valid_moves = set()
        for end_x in range(8):
            for end_y in range(8):
                if self.valid_move(start_x, start_y, end_x, end_y, board):
                    valid_moves.add((end_x, end_y))
        return valid_moves


    
