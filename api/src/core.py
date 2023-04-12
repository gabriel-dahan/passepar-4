from typing import List, Literal, Tuple
import sys, os

"""  CORE file -  ENGINE """

class GameCore(object):
    _2DArray = List[List[int]]
    
    def __init__(self, array: _2DArray) -> None:
        self.arr = array
        self.col_arr = self.as_columns()

    def is_full(self):
        """ Renvoie un booléen indiquant si la grille est pleine ou non. """
        return all(0 not in set(line) for line in self.arr)

    def as_columns(self) -> _2DArray:
        """ Returns the game matrix as a list of columns (instead of lines). """
        new_arr = []
        for i in range(7):
            new_arr.append([self.arr[j][i] for j in range(len(self.arr))])
        return new_arr

    def get_y_pos(self, column_pos: int) -> int:
        """ Returns the position at which the new pawn should be in the chosen column. """
        column = self.col_arr[column_pos][::-1] # Get the choosen column and reverse it so its easier to deal with.
        for i, elem in enumerate(column):
            if elem != 0:
                continue
            return len(column) - 1 - i
        return -1
    
    def get_diagonals(self) -> _2DArray:
        """ Returns a list that contains every diagonal of the array. """
        def get_decr_in(arr):
            decr = []
            for i in range(3):
                decr.append([arr[column][column + i] for column in range(6 - i)])
                decr.append([arr[column + (3 - i)][column] for column in range(4 + i)])
            return decr
        decr = get_decr_in(self.col_arr)
        # Getting an increasing diagonal in an array is the same as getting a decreasing one in the inverse of that array.
        incr = get_decr_in(self.col_arr[::-1])
        return decr + incr 
    
    def check_end(self) -> Literal[0, 1, 2]:
        """ Checks every row, column and diagonal of the array, and returns 0, 1 or 2 depending on the winner (or tie). """
        if self.is_full():
            return 0
        columns_check = [self.check_in(column) for column in self.col_arr]
        rows_check = [self.check_in(row) for row in self.arr]
        diag_check = [self.check_in(diag) for diag in self.get_diagonals()]
        general_check = set(columns_check + rows_check + diag_check)
        for num in general_check:
            if num != 0:
                return num
        return 0
    
    @classmethod
    def check_in(cls, l: list) -> int:
        """ Checks whether a number appears 4 times in a row in a simple list. 
            Returns 0 if no one got 4 and 1 or 2 otherwise depending on the winner. """
        sequence = 1
        temp = 0
        for i in range(len(l)):
            temp = l[i]
            if (l[i + 1] if len(l) != i + 1 else 0) == temp:
                sequence += 1
            else:
                sequence = 1
            if sequence == 4:
                return temp
        return 0
    

""" --- SHELL VERSION OF THE GAME --- """
class ShellConnect4(object):
    _2DArray = List[List[int]]
    
    def __init__(self, array: _2DArray = None, cells_repr: Tuple[str] = (' ', '⬟', '⬠')) -> None:
        self.cells_repr = cells_repr
        self.arr = array or [[0] * 6 for _ in range(7)]

    def get_rows(self) -> _2DArray:
        return [
            [self.arr[i][j] for i in range(len(self.arr))] 
            for j in range(len(self.arr) - 1)
        ]

    def get_diagonals(self) -> _2DArray:
        def get_decr_in(arr):
            decr = []
            for i in range(3):
                decr.append([arr[column][column + i] for column in range(6 - i)])
                decr.append([arr[column + (3 - i)][column] for column in range(4 + i)])
            return decr
        decr = get_decr_in(self.arr)
        # Getting an increasing diagonal in an array is the same as getting a decreasing one in the inverse of that array.
        incr = get_decr_in(self.arr[::-1])
        return decr + incr
    
    @classmethod
    def check_in(cls, l: list) -> int:
        """ 
            Checks whether a number appears 4 times in a row in a simple list. 
            Returns 0 if no one got 4 and 1 or 2 otherwise depending on the winner.
        """
        sequence = 1
        temp = 0
        for i in range(len(l)):
            temp = l[i]
            if (l[i + 1] if len(l) != i + 1 else 0) == temp:
                sequence += 1
            else:
                sequence = 1
            if sequence == 4:
                return temp
        return 0

    def check_end(self) -> Literal[0, 1, 2]:
        columns_check = [self.check_in(column) for column in self.arr]
        rows_check = [self.check_in(row) for row in self.get_rows()]
        diag_check = [self.check_in(diag) for diag in self.get_diagonals()]
        general_check = columns_check + rows_check + diag_check
        for winner in general_check:
            if winner == 0: 
                continue
            return winner
        return 0

    def update_grid(self, player: int) -> _2DArray:
        column = self.ask_player(player)
        print(column)
        for i in range(1, len(self.arr)):
            line = -i
            if self.arr[column][line] != 0:
                continue
            self.arr[column][line] = player
            return self.arr
        return self.arr

    def run(self, clear: bool = True) -> None:
        running = True
        i = 1
        while running:
            player = 1 if i % 2 == 0 else 2
            winner = self.check_end()
            if winner != 0:
                self.end_game()
            self.update_grid(player)
            i += 1
            if clear:
                self.clear()
            print(self.format_grid())

    def ask_player(self, player: int) -> int:
        column = input(f"[ {self.cells_repr[player]} ] On which column do you want to place a pawn ? ")
        while not self.represents_int(column) or column not in [str(c) for c in range(1, 8)]:
            column = input(f"[ {self.cells_repr[player]} ] Wrong, must be between 1 and 7, try again : ")
        column = int(column) - 1
        running = True
        while running:
            if self.arr[column][0] != 0:
                column = int(input("--- The choosen column is full, please take another one : "))
                continue
            running = False 
        return column

    def format_grid(self) -> str:
        return ''.join(
            ' | '.join([self.cells_repr[self.arr[i][j]] for i in range(len(self.arr))])
            + '\n--------------------------\n'
            for j in range(len(self.arr) - 1)
        )

    def end_game(self):
        winner = self.check_end()
        print(f'The game is over, {self.cells_repr[winner]}  won !')
        sys.exit(1)

    @classmethod
    def clear(cls) -> None:
        os.system('cls') if os.name == 'nt' else os.system('clear')

    @classmethod
    def represents_int(cls, val) -> bool:
        try:
            int(val)
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    gc = GameCore([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 2, 1, 2, 0], [0, 0, 2, 2, 2, 1, 0], [0, 0, 1, 2, 2, 1, 1]])
    print(gc.as_columns())