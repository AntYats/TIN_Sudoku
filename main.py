from copy import deepcopy
from pickle import dump, load
from random import shuffle, randrange


class Game:
    """
    Sudoku game

    2 modes - solved py algorithm or by user

    General idea:

    Default board is two-dimensional array 9x9 with 0

    Steps:
    [1] Do permission to continue or to start a new game
    [2] If the game is continued just start user play function, If it is not do a permission request
    -> 1) How many cells will be available to fill -> (3) -> Draw board to solve 2) Check who will solve it - user or algo

    (3) Generate solvable board -> Save it to the solved_board variable
    [4] From generated board randomly delete n cells with check of existing solve
     -> Save it to the board variable
    [5] User should type row, col and value to fill the board. If it right, board will be saved to .pkl file
    [6] When the board is full the game is over.
    """

    def __init__(self):
        # default board is [81x81] array
        self.board = [[0] * 9 for _ in [0] * 9]
        self.solved_board = None
        self.mode = None

    def load_game(self):
        with open("savings.pkl", "rb") as file:
            self.board = load(file)
            self.solved_board = deepcopy(self.board)

            self.solve_board(self.solved_board)

            self.draw_board(self.board)

    def game_start(self):
        """"""
        game_status = int(input("Вы хотите продолжить игру - 1 или начать новую - 2 ?"))
        # Load saved game
        if game_status == 1:
            self.load_game()
            self.mode = "USER"
            self.user_play()
        # Create new game
        elif game_status == 2:
            game_mode = int(input("Вы хотите решить сами - 1 или пусть машина играет - 2 ?"))
            empty_cells = int(input("Как много клеток должно быть пропущено? "))
            # Start user mode
            if game_mode == 1:
                self.mode = "USER"
                self.generate_new_board(empty_cells)
                self.draw_board(self.board)
                self.user_play()
            # Start pc mode
            elif game_mode == 2:
                self.mode = "COMPUTER"
                self.generate_new_board(empty_cells)
                self.draw_board(self.board)

    def generate_new_board(self, k):
        """
        [1] To empty board add randomly few values
        [2] Solve this board
        [3] Randomly delete n cells
        """
        # Randomly fill board
        for _ in range(20):
            row = randrange(0, 9)
            col = randrange(0, 9)
            value = randrange(1, 10)

            if self.check_enter_valid(self.board, row, col, value):
                self.board[row][col] = value
        # Solve the board
        self.solve_board(self.board)
        # Save solved board to the variable
        self.solved_board = deepcopy(self.board)
        # Randomly delete k cells
        for _ in range(k):
            row = randrange(0, 9)
            col = randrange(0, 9)

            value = self.board[row][col]
            # Solve description by pc
            if self.mode == "COMPUTER":
                self.draw_board(self.board)
                print(f"Ставлю цифру {value} на {row + 1} ряд на {col + 1} место")

            self.board[row][col] = 0

    def check_empty_cell(self, board):
        """ Finding [row, col] of empty cell
            If there is empty cell no return None
        """
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return row, col
        return None, None

    def check_enter_valid(self, board, row, col, guess):
        """ Checking for valid value by sudoku rules
            [1] No such value in a row
            [2] No such value in a column
            [3] No such value in [3x3] block

            Returns True if value is valid, False otherwise
        """
        # Checking in row
        row_values = board[row]
        if guess in row_values:
            return False

        # Checking in column
        for r in range(9):
            if board[r][col] == guess:
                return False

        # Checking [3x3] block

        # Block starting cells
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if board[r][c] == guess:
                    return False
        # Every check didn't return False, so it is safe to put this guess
        return True

    def solve_board(self, board):
        """Backtracking algo"""

        # Finding cell to fill
        row, col = self.check_empty_cell(board)
           
        # When there are no clean cells the board is solved
        if row is None:
            return True

        # Finding number to fill in this cell
        for guess in range(1, 10):
            # Checking for valid number by rules
            if self.check_enter_valid(board, row, col, guess):
                board[row][col] = guess
                # Recursive call until board is solved
                if self.solve_board(board):
                    return True
            # If guess is wrong clean cell
            board[row][col] = 0
        # Algo didn't solve the board
        return False

    def user_play(self):
        """User play mode"""
        while self.check_empty_cell(self.board) != (None, None):
            # Input validation
            row, col, value = [None, None, None]
            while row is None:
                try:
                    row = int(input("Введите ряд в который хотите вставить цифру ")) - 1
                except ValueError:
                    row = None
                    print("Необходимо ввести числовое значение")
                else:
                    if not (row in range(0, 9)):
                        row = None
                        print("Необходимо ввести числовое значение")

            while col is None:
                try:
                    col = int(input("Введите колонку в которую хотите вставить цифру ")) - 1
                except ValueError:
                    col = None
                    print("Необходимо ввести числовое значение")
                else:
                    if not (col in range(0, 9)):
                        col = None
                        print("Цифра должна быть от 1 до 9")

            while value is None:
                try:
                    value = int(input("Введи значение цифры "))
                except ValueError:
                    value = None
                    print("Необходимо ввести числовое значение")
                else:
                    if not (value in range(1, 10)):
                        value = None
                        print("Цифра должна быть от 1 до 9")

            # Check for emptiness
            if self.board[row][col] == 0:
                # Check for compliance with the rules
                if value == self.solved_board[row][col]:
                    self.board[row][col] = value
                    # Save new board to .pkl file
                    with open("savings.pkl", "wb") as file:
                        dump(self.board, file)
                    self.draw_board(self.board)
                else:
                    # Value is incorrect -> cancel operation
                    print("Этой цифры здесь не может быть, попробуйте что-нибудь другое")
                    self.board[row][col] = 0
                    self.draw_board(self.board)
            else:
                print("Тут уже есть цифра")

        # Board is full -> victory!
        print("Игра закончена! Поздравляю!")
        return ""

    def draw_board(self, board):
        """Just printing board that is convenient to play"""
        print("---------------------")
        for i in range(len(board)):
            line = ""
            if i == 3 or i == 6:
                print("---------------------")
            for j in range(len(board[i])):
                if j == 3 or j == 6:
                    line += "| "
                line += str(board[i][j]) + " "
            print(line)
        print("---------------------")

game = Game()
game.game_start()
