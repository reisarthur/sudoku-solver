import copy
import random

class Sudoku:

    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)] # initialize 2d-array 9x9 with zeros
        self.possibilities = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)] # initialize 2d-array 9x9 with a list [1-9]


    def create_board(self, boardArray):
        for r in range(9):
            for c in range(9):
                v = boardArray[r][c]
                if v != 0:
                    self.put(r,c,v)


    def put(self, row, col, value):
        self.board[row][col] = value # update board
        self.possibilities[row][col] = [] # update possibilities (remove all)
        for (r,c) in self.get_idx_pairs_at_row(row):
            self.remove_possibility(r, c, value) # remove value from possibilities at same row
        for (r,c) in self.get_idx_pairs_at_column(col):
            self.remove_possibility(r, c, value) # remove value from possibilities at same column
        for (r,c) in self.get_idx_pairs_at_square(row, col):
            self.remove_possibility(r, c, value) # remove value from possibilities at same square
        return True

    def remove_possibility(self, row, col, value):
        if value in self.possibilities[row][col]:
            self.possibilities[row][col].remove(value)


    def print(self):
        self.print_board()
        self.print_possibilities()

    def print_board(self):
        for row in self.board:
            for value in row:
                if value == 0:
                    print("_", end=" ")
                else:
                    print(value, end=" ")
            print()

    def print_possibilities(self):
        for row in self.possibilities:
            for element in row:
                print(element, end=" ")
            print()


    def get_all_idx_pairs(self):
        pairsList = []
        for r in range(9):
            for c in range(9):
                pairsList.append((r, c))
        return pairsList

    def get_all_idx_rows(self):
        pairsList = []
        for row in range(9):
            pairsList.append(self.get_idx_pairs_at_row(row))
        return pairsList

    def get_all_idx_columns(self):
        pairsList = []
        for col in range(9):
            pairsList.append(self.get_idx_pairs_at_column(col))
        return pairsList

    def get_all_idx_squares(self):
        pairsList = []
        for row in [0,3,6]:
            for col in [0,3,6]:
                pairsList.append(self.get_idx_pairs_at_square(row, col))
        return pairsList

    def get_idx_pairs_at_row(self, row):
        pairsList = []
        for col in range(9):
            pairsList.append((row, col))
        return pairsList

    def get_idx_pairs_at_column(self, col):
        pairsList = []
        for row in range(9):
            pairsList.append((row, col))
        return pairsList

    def get_idx_pairs_at_square(self, row, col):
        pairsList = []
        for r in range(3):
            for c in range(3):
                pairsList.append(((row // 3) * 3 + r, (col // 3) * 3 + c))
        return pairsList

    def get_value_array_from_idx_pairs(self, pairsList):
        values = []
        for (r,c) in pairsList:
            values.append(self.board[r][c])
        return values


    def check_everything(self):
        while self.check_single_possibilities() or self.check_single_possible_placements():
            pass

    def check_single_possibilities(self):
        for (r,c) in self.get_all_idx_pairs():
            if len(self.possibilities[r][c]) == 1:
                return self.put(r,c,self.possibilities[r][c][0])

    def check_single_possible_placements(self):
        for value in range(9):
            for pairsList in (self.get_all_idx_rows() + self.get_all_idx_columns() + self.get_all_idx_squares()):
                if self.check_value_at_pairs_list(pairsList, value): 
                    return True

    def check_value_at_pairs_list(self, pairsList, value):
        occurrences = 0
        for (r,c) in pairsList:
            if value in self.possibilities[r][c]:
                occurrences += 1
                (rIdx, cIdx) = (r, c)
        if (occurrences == 1):
            return self.put(rIdx, cIdx, value)


    def is_incorrect(self):
        return self.is_incorrect_row() or self.is_incorrect_column() or self.is_incorrect_square() or self.is_incorrect_out_possibilities()

    def is_incorrect_row(self):
        for pairsList in self.get_all_idx_squares():
            values = self.get_value_array_from_idx_pairs(pairsList)
            if self.contains_repeated(values):
                print(f"Row {pairsList[0][0]} Not Correct!")
                return True
        return False

    def is_incorrect_column(self):
        for pairsList in self.get_all_idx_columns():
            values = self.get_value_array_from_idx_pairs(pairsList)
            if self.contains_repeated(values):
                print(f"Column {pairsList[0][1]} Not Correct!")
                return True
        return False

    def is_incorrect_square(self):
        for pairsList in self.get_all_idx_squares():
            values = self.get_value_array_from_idx_pairs(pairsList)
            if self.contains_repeated(values):
                print(f"Square {pairsList[0]} Not Correct!")
                return True
        return False

    def is_incorrect_out_possibilities(self):
        for (r,c) in self.get_all_idx_pairs():
            if self.board[r][c] == 0 and len(self.possibilities[r][c]) == 0:
                print(f"Run Out Of Possibilities on {(r,c)}!")
                return True
        return False


    def check_completed_board(self):
        for (r,c) in self.get_all_idx_pairs():
            if self.board[r][c] == 0 or len(self.possibilities[r][c]) > 0:
                # print("Board Not Completed!")
                return False
        return True
    
    
    def contains_repeated(self, arr):
        non_zero_values = [x for x in arr if x != 0]
        return len(non_zero_values) != len(set(non_zero_values))
    
    
    def contains_all_numbers(self, arr):
        if len(arr) != 9:
            return False
        if not all(1 <= num <= 9 for num in arr):
            return False
        if len(set(arr)) != 9:
            return False
        return True


    def get_remaining_possibilities(self):
        remaining = []
        for (r,c) in self.get_all_idx_pairs():
            for v in self.possibilities[r][c]:
                remaining.append((r,c,v))
        return remaining


def create_branch(sdk: Sudoku, moves):
    sdk_alt = None
    sdk_alt = Sudoku()
    sdk_alt.board = copy.deepcopy(sdk.board)
    sdk_alt.possibilities = copy.deepcopy(sdk.possibilities)
    (r,c,v) = random.choice(sdk_alt.get_remaining_possibilities())
    sdk_alt.put(r,c,v)
    sdk_alt.check_everything()
    # sdk_alt.print()
    moves.append((r,c,v))
    if sdk_alt.is_incorrect():
        return (False, moves)
    if sdk_alt.check_completed_board():
        return (True, moves)
    return create_branch(sdk_alt, moves)
