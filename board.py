class Board:
    EMPTY = ' '
    BLACK = {"pawn": u'⚪', "king": u'⬜'}
    WHITE = {"pawn": u'⚫', "king": u'⬛'}

    def __init__(self, rows=8, columns=8, depth=3):
        self.columns = columns
        self.rows = rows
        self.depth = depth
        self.board = [[self.EMPTY for _ in range(columns)] for _ in range(rows)]
        self.turn = self.WHITE
        self.jump = False
        self.game_won = False
        for i in range(1, 4):
            if i % 2 == 0:
                for num, val in list(enumerate(self.board[i - 1]))[::2]:
                    self.board[i - 1][num] = self.BLACK['pawn']
                for num, val in list(enumerate(self.board[rows - i]))[1::2]:
                    self.board[rows - i][num] = self.WHITE['pawn']
            else:
                for num, val in list(enumerate(self.board[i - 1]))[1::2]:
                    self.board[i - 1][num] = self.BLACK['pawn']
                for num, val in list(enumerate(self.board[rows - i]))[::2]:
                    self.board[rows - i][num] = self.WHITE['pawn']

    def __str__(self):
        # This prints the numbers at the top of the Game Board
        # Prints the top of the game board in unicode
        lines = ['    ' + '   '.join(map(str, range(1, self.columns + 1))), u'  ╭' + (u'───┬' * (self.columns - 1)) + u'───╮']
        # Print the boards rows
        for num, row in enumerate(self.board[:-1]):
            lines.append(chr(num + 65) + u' │ ' + u' │ '.join(row) + u' │')
            lines.append(u'  ├' + (u'───┼' * (self.columns - 1)) + u'───┤')

        # Print the last row
        lines.append(chr(self.rows + 64) + u' │ ' + u' │ '.join(self.board[-1]) + u' │')

        # Prints the final line in the board
        lines.append(u'  ╰' + (u'───┴' * (self.columns - 1)) + u'───╯')
        return '\n'.join(lines)

    def is_valid_selection(self, row, col):
        # check if the player chose their piece
        piece = self.board[row][col]
        if piece in self.turn.values() or piece in self.turn.values():
            return True
        print("This is not your piece")
        return False

    def is_valid_move(self, row, col, target_row, target_col):
        # check if the move is ok - not on another piece, not outside of range etc.
        if not self.square_within_board(target_row, target_col):
            print("Move outside of the board")
            return False
        elif self.board[target_row][target_col] != self.EMPTY:
            print("You can't land on another piece")
            return False
        elif self.board[row][col] == self.turn['pawn']:
            return self.is_valid_move_pawn(row, col, target_row, target_col)
        elif self.board[row][col] == self.turn['king']:
            return self.is_valid_move_king(row, col, target_row, target_col)
        return True

    def is_valid_move_pawn(self, row, col, target_row, target_col):
        switch = -1 if self.turn == self.WHITE else 1
        if row - target_row == -switch * 1 and abs(col - target_col) == 1:
            return True
        elif (row - target_row == -switch * 2 and col - target_col == -2) and self.board[row + switch * 1][col + 1] in self.get_opponent().values():  # jump forward right
            self.jump = True
            return True
        elif (row - target_row == -switch * 2 and col - target_col == 2) and self.board[row + switch * 1][col - 1] in self.get_opponent().values():  # jump forward left
            self.jump = True
            return True
        elif (row - target_row == switch * 2 and col - target_col == -2) and self.board[row + -switch * 1][col + 1] in self.get_opponent().values():  # jump backward right
            self.jump = True
            return True
        elif (row - target_row == switch * 2 and col - target_col == -2) and self.board[row + -switch * 1][col - 1] in self.get_opponent().values():  # jump backward left
            self.jump = True
            return True
        print("This is not a valid pawn move")
        return False

    def check_king_jump(self, row, col, target_row, target_col):
        pieces = set()
        for r in range(min(row, target_row) + 1, max(row, target_row)):
            for c in range(min(col, target_col) + 1, max(col, target_col)):
                if self.board[r][c] in self.get_opponent().values():
                    pieces.add(self.board[r][c])
        if self.turn['pawn'] in pieces or self.turn['king'] in pieces:
            return False
        elif len(pieces) > 1:
            return False

    def is_valid_king_jump(self, row, col, target_row, target_col):
        if self.check_king_jump(row, col, target_row, target_col):
            print("It is not a valid king jump")
            return False
        else:
            self.jump = True
            return True

    def is_valid_move_king(self, row, col, target_row, target_col):
        if row == target_row or col == target_col:
            print("King cannot move horizontally")
            return False
        elif (target_row - row) != (target_col - col):
            print("King cannot move with slope other than 1")
            return False
        else:
            return self.is_valid_king_jump(row, col, target_row, target_col)

    def get_opponent(self):
        if self.turn == self.WHITE:
            return self.BLACK
        else:
            return self.WHITE

    def switch_turn(self):
        self.turn = self.get_opponent()

    def check_win(self):
        remaining_enemy_pieces = 0
        for row in self.board:
            remaining_enemy_pieces += row.count(self.get_opponent()['pawn'])
            remaining_enemy_pieces += row.count(self.get_opponent()['king'])
        if remaining_enemy_pieces == 0:
            self.game_won = self.turn

    def get_jumps(self, row: int, col: int) -> list:
        if self.board[row][col] == self.BLACK['pawn'] or self.board[row][col] == self.WHITE['pawn']:
            return self.get_jumps_pawn(row, col)
        elif self.board[row][col] == self.BLACK['king'] or self.board[row][col] == self.WHITE['king']:
            return self.get_jumps_king(row, col)
        else:
            return []

    def get_jumps_pawn(self, row, col):
        jumps = []
        options = ['fr', 'fl', 'br', 'bl']
        for opt in options:
            jumped = self.get_jump(row, col, opt)
            dest = self.get_jump(*jumped, opt)
            if self.square_within_board(*jumped) and self.square_within_board(*dest):
                if self.board[jumped[0]][jumped[1]] in self.get_opponent().values() \
                        and self.board[dest[0]][dest[1]] == self.EMPTY:
                    jumps.append(dest)
        return jumps


    def get_jumps_king(self, row, col):
        jumps = []
        squares_sets = self.get_king_diagonals(row, col, fr=True, fl=True, br=True, bl=True)
        for s in squares_sets:
            for sq in s:
                if self.check_king_jump(row, col, *sq):
                    jumps.append(s)
        return jumps

    def get_king_diagonals(self, row, col, fr=False, fl=False, br=False, bl=False):
        s_fr = set()
        s_fl = set()
        s_br = set()
        s_bl = set()
        r = row
        c = col
        while self.square_within_board(r, c) and br:  # backwards right
            s_br.add((r, c))
            r += 1
            c += 1
        r = row
        c = col
        while self.square_within_board(r, c) and fl:  # forward left
            s_fl.add((r, c))
            r -= 1
            c -= 1
        r = row
        c = col
        while self.square_within_board(r, c) and bl:  #backward left
            s_bl.add((r, c))
            r += 1
            c -= 1
        r = row
        c = col
        while self.square_within_board(r, c) and fr:  # forward right
            s_fr.add((r, c))
            r -= 1
            c += 1
        s_fr.remove((row, col))
        s_fl.remove((row, col))
        s_br.remove((row, col))
        s_bl.remove((row, col))
        return s_fr, s_fl, s_br, s_bl

    def square_within_board(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.columns:
            return False
        else:
            return True

    @staticmethod
    def get_jump(row, col, direction):
        if direction == "fr":
            return row - 1, col + 1
        elif direction == 'fl':
            return row - 1, col - 1
        elif direction == 'br':
            return row + 1, col + 1
        elif direction == 'bl':
            return row + 1, col - 1

    def player_move(self, row, col, target_row, target_col):
        self.board[target_row][target_col] = self.board[row][col]
        self.board[row][col] = self.EMPTY
        if (target_row == 0 and self.turn == self.WHITE) or (target_row == 7 and self.turn == self.BLACK):
            self.board[target_row][target_col] = self.turn['king']
        self.check_win()
        if not self.game_won:
            if self.jump:
                for r in range(min(row, target_row) + 1, max(row, target_row)):
                    for c in range(min(col, target_col) + 1, max(col, target_col)):
                        if self.board[r][c] in self.get_opponent().values():
                            self.board[r][c] = self.EMPTY
                print(self)
                return True
            else:
                self.switch_turn()
                print(self)
                return False
        print(self)
        return False
