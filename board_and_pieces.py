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
                if board.matrix[r][c] is not None:
                    break


class King:
    def __init__(self,color):
        self.color = color
        self.id = 'k'
    def valid_move(self, start_x, start_y, end_x, end_y, board):
        directions = [[1,1], [1,-1], [-1,1], [-1,-1], [1,0], [0,1], [-1,0], [0,-1]]
        target = board.matrix[end_x][end_y]
        for i in directions:
            if start_x + i[0] == end_x and start_y + i[1] == end_y:
                if target is None:
                    return True
                # Check Capture
                elif target.color!= self.color:
                        return True
    

class Rook:
    def __init__(self,color):
        self.color = color
        self.id = 'r'

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


class Knight:
    def __init__(self,color):
        self.color = color
        self.id = 'n'
    
    def valid_move(self, start_x, start_y, end_x, end_y, board):
        if (abs(end_x - start_x) == 1 and abs(end_y - start_y) == 2) or (abs(end_x - start_x) == 2 and abs(end_y - start_y) == 1):
            # Check Capture
            target_piece = board.matrix[end_x][end_y] 
            if target_piece is None:
                return True
            elif target_piece.color!=self.color:
                return True


class Bishop:
    def __init__(self,color):
        self.color = color
        self.id = 'b'
    
    def __str__(self):
        return self.id.upper() if self.color == 'w' else self.id.lower()
    
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
                if board.matrix[r][c] is not None:
                    break


    
