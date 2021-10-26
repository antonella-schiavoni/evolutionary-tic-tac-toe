import numpy as np
from typing import List, Tuple

SIZE = 3


class Board:
    """
    Class that represents the tic tac toe board
    """

    def __init__(self, size: int = None):
        self.steps = 0
        self.size = size or SIZE
        self.values = self._initialize_values()

    def _initialize_values(self) -> List[List]:
        """
        Initialize the board to prepare it for the game.
        All boxes are initialized with '.' meaning that the box is empty
        """
        result = []
        for _ in range(self.size):
            result.append(["." for _ in range(self.size)])
        return result

    def get_empty_boxes(self) -> List[Tuple[int, int]]:
        """
        Return the coordinates in which there are empty boxes
        """
        results = []
        for id_row, row in zip(range(self.size), self.values):
            index_at = [index for index, element in enumerate(row) if element == "."]
            if index_at:
                for id in index_at:
                    results.append((id_row, id))
        return results

    def who_won(self) -> str:
        """
        Analyze the board for SIZE consecutive X or O.
        Return a string with "X" or "O" depending on who won the match.
        """

        board_transposed = list(map(list, zip(*self.values)))
        for row, row_transposed in zip(self.values, board_transposed):

            if len(set(row)) == 1 and row[0] in ["X", "O"]:
                return row[0]  # Somebody won

            if len(set(row_transposed)) == 1 and row_transposed[0] in ["X", "O"]:
                return row_transposed[0]  # Somebody won

        # Add check for diagonals
        diag_1 = np.array(self.values).diagonal()
        if len(set(diag_1)) == 1 and diag_1[0] in ["X", "O"]:
            return diag_1[0]  # Somebody won

        diag_2 = np.fliplr(np.array(self.values)).diagonal()
        if len(set(diag_2)) == 1 and diag_2[0] in ["X", "O"]:
            return diag_2[0]  # Somebody won

        # If we reach this point, it means it's a tie
        return "-"

    def is_finished(self) -> bool:
        """
        Checks if the board is finished or not by seeing if there is a
        winner already or if it still has empty  boxes
        """

        return self.who_won() != "-" or not self.has_empty_boxes()

    def has_empty_boxes(self) -> bool:
        """
        If there is a "." in any part of the board it'll return True
        False otherwise
        """

        for row in self.values:
            if "." in row:
                return True
        return False

    def pretty_print_board(self):
        """
        Print the board human readable
        """
        for i in range(self.size):
            print(self.values[i])
