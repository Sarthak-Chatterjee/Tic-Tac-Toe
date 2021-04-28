class Node:

    def __init__(self, val=None):
        self.val = val
        self.next = {}


class Board:

    def __init__(self):
        self.table = [[' '] * 3 for _ in range(3)]
        self.available = {(col, row): True for col in range(3) for row in range(3)}
        self.winner = ''

    def put(self, col, row, sign):
        self.table[col][row] = sign
        self.available[(col, row)] = False

    def delete(self, move):
        self.table[move[0]][move[1]] = ' '
        self.available[move] = True
        self.winner = ''

    def __str__(self):
        return '\n' + '\n---------\n'.join(' | '.join(col) for col in self.table) + '\n'

    def finished(self):
        for col in range(3):
            if self.table[col][0] == self.table[col][1] == self.table[col][2] != ' ':
                self.winner = self.table[col][0]
                return True
        for row in range(3):
            if self.table[0][row] == self.table[1][row] == self.table[2][row] != ' ':
                self.winner = self.table[0][row]
                return True
        if self.table[0][0] == self.table[1][1] == self.table[2][2] != ' ' \
                or self.table[0][2] == self.table[1][1] == self.table[2][0] != ' ':
            self.winner = self.table[1][1]
            return True
        if not any(self.available.values()):
            return True
        return False


class Player:

    def __init__(self, sign):
        self.sign = sign

    def next_move(self):
        return divmod(int(input("enter a valid box number as shown above: ")) - 1, 3)

    def play(self, board):
        while True:
            row, col = self.next_move()
            if row > 2 or col > 2:
                print("Bad input: Invalid box number")
                continue
            if board.available[(row, col)]: break
            print("Bad input: Box is not empty")
        board.put(row, col, self.sign)
        return row, col


class Bot(Player):

    def __init__(self, sign):
        super().__init__(sign)
        self.solution = Node()

    def play(self, board):
        if not len(self.solution.next):
            self.solve(board)
        else:
            for move in self.solution.next:
                if not board.available[move.val]:
                    self.solution = move
                    break
        val = -2
        for move in self.solution.next:
            if board.available[move.val] and self.solution.next[move] > val:
                best_move = move
                val = self.solution.next[move]
        print("Opponent plays:", best_move.val[0] * 3 + best_move.val[1] + 1)
        self.solution = best_move
        board.put(*best_move.val, self.sign)

    def let(self, board, move, sign):
        wins = [-2, 2][sign == self.sign]
        col, row = move.val
        board.put(col, row, sign)
        if board.finished():
            if board.winner == self.sign:
                wins = 1
            elif board.winner == '':
                wins = 0
            else:
                wins = -1
            board.delete(move.val)
            return wins

        for col, row in board.available:
            if board.available[(col, row)]:
                new_move = Node((col, row))
                move.next[new_move] = self.let(board, new_move, ('X', 'O')[sign == 'X'])
                if sign == self.sign:
                    wins = min(wins, move.next[new_move])
                else:
                    wins = max(wins, move.next[new_move])

        board.delete(move.val)
        return wins

    def solve(self, board):
        for col, row in board.available:
            if board.available[(col, row)]:
                move = Node((col, row))
                self.solution.next[move] = self.let(board, move, 'O')


class Game:

    def __init__(self, board, player1, player2):
        print("boxes and their numbers:")
        print("\n---------\n".join((' | '.join(str(row * 3 + col + 1) for col in range(3)) for row in range(3))))
        self.board = board
        self.player1 = player1
        self.player2 = player2

    def proceed(self):
        move = self.player1.play(self.board)
        print(self.board)
        if self.board.finished():
            if self.board.winner == '':
                print("IT'S A DRAW!!!")
            elif type(self.player2) == Bot:
                print(f"YOU {('LOST', 'WON')[self.board.winner == self.player1.sign]}")
            else:
                print(f"PLAYER{(2, 1)[self.board.winner == self.player1.sign]} WINS")
            return
        self.player2.play(self.board)
        print(self.board)


while True:
    n = input("choose:    1. vs Computer    2. Two Players\nEnter the corresponding number: ")
    if n == '1':
        p2 = Bot('O')
    elif n == '2':
        p2 = Player('O')
    else:
        print("Wrong Input")
        continue
    game = Game(Board(), Player('X'), p2)
    while True:
        game.proceed()
        if game.board.finished():
            break
    if input("enter 'q' to quit, anything else to continue: ") == 'q': break
