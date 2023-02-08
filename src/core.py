from typing import List, Literal, Tuple
import sys, os

"""  Core file - Power4 engine """

class Power4(object):
    _2DArray = List[List[int]]
    
    def __init__(self, cells_repr: Tuple[str] = (' ', '⬟', '⬠')) -> None:
        self.cells_repr = cells_repr
        self.arr = [[0] * 6 for _ in range(7)]
    
    def ask_player(self, player: int) -> int:
        column = int(input(f"[ {self.cells_repr[player]} ] On which column do you want to place a pawn ? "))
        assert column <= 7, 'Max column is 7.'
        running = True
        while running:
            if self.arr[column][0] != 0:
                column = int(input("--- The choosen column is full, please take another one : "))
                continue
            running = False 
        return column

    def update_grid(self, player: int) -> _2DArray:
        column = self.ask_player(player) - 1
        for i in range(1, len(self.arr)):
            line = -i
            if self.arr[column][line] != 0:
                continue
            self.arr[column][line] = player
            return self.arr
        return self.arr

    def format_grid(self) -> str:
        return ''.join(
            ' | '.join([self.cells_repr[self.arr[i][j]] for i in range(len(self.arr))])
            + '\n--------------------------\n'
            for j in range(len(self.arr) - 1)
        )

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
        incr = get_decr_in(list(reversed(self.arr)))
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
            if winner == 0: continue
            return winner
        return 0

    def end_game(self):
        winner = self.check_end()
        print(f'The game is over, {self.cells_repr[winner]}  won !')
        sys.exit(1)

    def shell_run(self) -> None:
        running = True
        i = 1
        while running:
            player = 1 if i % 2 == 0 else 2
            winner = self.check_end()
            if winner != 0:
                self.end_game()
            self.update_grid(player)
            i += 1
            self.clear()
            print(self.format_grid())

    @classmethod
    def clear(cls) -> None:
        os.system('cls') if os.name == 'nt' else os.system('clear')

if __name__ == '__main__':
    p4 = Power4()
    p4.run()