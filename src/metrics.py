from typing import Tuple
import numpy as np
from itertools import groupby
from collections import Counter


def all_equal(iterable) -> bool:
    """
    Verify if all the element of the iterable are equals
    """
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def amt_groups_n_consecutive_markers(board, marker: str) -> int:
    """
    Counts the number of n consecutive markers in the board.
    n is the board size.
    """

    def _process_rows(row):
        result = []
        for i in range(board.size):
            result.append(row[i:])
        return result

    result = []
    for row in board.values:
        process_rows = _process_rows(row)
        result.extend(list(zip(*process_rows)))

    board_transposed = list(map(list, zip(*board.values)))
    for row in board_transposed:
        process_rows = _process_rows(row)
        result.extend(list(zip(*process_rows)))

    # Add check for diagonals
    diag_1 = np.array(board.values).diagonal()
    result.extend(list(zip(*_process_rows(diag_1))))

    diag_2 = np.fliplr(np.array(board.values)).diagonal()
    result.extend(list(zip(*_process_rows(diag_2))))

    counter = Counter(result)

    total = 0
    for key, value in counter.items():
        if all_equal(key) and key[0] == marker:
            total += value

    return total


def amt_groups_2_consecutive_markers(board, marker: str) -> int:
    """
    Counts the number of 2 consecutive markers in the board.
    """
    result = []
    for row in board.values:
        result.extend(list(zip(row, row[1:])))

    board_transposed = list(map(list, zip(*board.values)))
    for row in board_transposed:
        result.extend(list(zip(row, row[1:])))

    # Add check for diagonals
    diag_1 = np.array(board.values).diagonal()
    result.extend(list(zip(diag_1, diag_1[1:])))

    diag_2 = np.fliplr(np.array(board.values)).diagonal()
    result.extend(list(zip(diag_2, diag_2[1:])))

    counter = Counter(result)

    total = 0
    for key, value in counter.items():
        if key[0] == key[1] and key[0] == marker:
            total += value

    return total


def amt_groups_n_consecutive_markers_followed_by_marker(board, marker: str) -> int:
    """
    Amount of groups with 2 consecutive marker followed by opponent marker
    """
    result = []
    for row in board.values:
        result.extend(list(zip(row, row[1:], row[2:])))

    board_transposed = list(map(list, zip(*board.values)))
    for row in board_transposed:
        result.extend(list(zip(row, row[1:], row[2:])))

    # Add check for diagonals
    diag_1 = np.array(board.values).diagonal()
    result.extend(list(zip(diag_1, diag_1[1:], diag_1[2:])))

    diag_2 = np.fliplr(np.array(board.values)).diagonal()
    result.extend(list(zip(diag_2, diag_2[1:], diag_2[2:])))

    counter = Counter(result)
    total = 0
    for key, value in counter.items():
        if (key[0] == key[1] != key[2] and key[2] != "." and key[0] == marker) or (
                key[0] != key[1] == key[2] and key[0] != "." and key[1] == marker):
            total += value

    return total


def blank_between_marker(board, marker: str) -> int:
    """
    Amount of blank boxes between marker
    """
    result = []
    for row in board.values:
        result.extend(list(zip(row, row[1:], row[2:])))

    board_transposed = list(map(list, zip(*board.values)))
    for row in board_transposed:
        result.extend(list(zip(row, row[1:], row[2:])))

    # Add check for diagonals
    diag_1 = np.array(board.values).diagonal()
    result.extend(list(zip(diag_1, diag_1[1:], diag_1[2:])))

    counter = Counter(result)

    total = 0
    for key, value in counter.items():
        if key[0] == key[2] != key[1] and key[1] == "." and key[0] == marker:
            total += value

    return total


def is_marker_in_center(board, marker: str) -> int:
    """
    Checks if the marker is placed in center
    """
    if board.size % 2 != 0:
        center = board.size // 2
        return 1 if board.values[center][center] == marker else 0
    return 0


def _get_diagonals(board) -> Tuple:
    """
    Return both diagonals element
    """
    board_values = np.array(board.values)
    diag_1 = board_values.diagonal()
    diag_2 = np.fliplr(board_values).diagonal()
    return diag_1, diag_2


def _get_opponent_marker(marker) -> str:
    """
    Returns the opponent marker
    """
    return "X" if marker == "O" else "O"


def _is_line_winnable(list, marker) -> bool:
    """
    Returns a bool indicating if the opponent's marker is in the list
    """
    return _get_opponent_marker(marker) not in list


def _amount_of_markers_in_winnable_line(list, marker) -> int:
    """
    Counts the number of markers in a winnable line
    """
    result = 0
    markers_amount_in_list = 0
    for cell in list:
        if cell == marker:
            markers_amount_in_list += 1

    if (markers_amount_in_list > 1 and _is_line_winnable(list, marker)):
        result += markers_amount_in_list
    return result


def two_or_more_markers_in_winnable_line(board, marker: str):
    """
    Counts the number markers that are in the same line, but only if
    there are at least 2 and if it's a winnable line. This means that
    the line can contain empty boxes but not an opponent marker.
    A line can be a row, a column or any  of both diagonals.
    """
    result = 0
    board_transposed = list(map(list, zip(*board.values)))
    for row, column in zip(board.values, board_transposed):
        result += _amount_of_markers_in_winnable_line(row, marker)
        result += _amount_of_markers_in_winnable_line(column, marker)

    diag_1, diag_2 = _get_diagonals(board)
    result += _amount_of_markers_in_winnable_line(diag_1, marker)
    result += _amount_of_markers_in_winnable_line(diag_2, marker)

    return result
