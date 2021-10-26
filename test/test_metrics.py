from src.board import Board
from src.metrics import amt_groups_2_consecutive_markers, amt_groups_n_consecutive_markers_followed_by_marker, \
    blank_between_marker, amt_groups_n_consecutive_markers, two_or_more_markers_in_winnable_line


def test_amt_groups_n_consecutive_markers():
    board = Board(size=3)
    board.values = [["X", "X", "."],
                    ["X", "O", "O"],
                    ["O", "X", "X"]]
    result = amt_groups_2_consecutive_markers(board, "X")

    assert result == 3

def test_amt_groups_n_consecutive_markers_followed_by_marker():
    board = Board(size=3)
    board.values = [["X", "X", "."],
                    ["X", "O", "O"],
                    ["O", "X", "X"]]
    result = amt_groups_n_consecutive_markers_followed_by_marker(board, "X")

    assert result == 2


def test_blank_between_marker():
    board = Board(size=3)
    board.values = [["X", ".", "X"],
                    ["O", ".", "."],
                    ["X", "O", "X"]]
    result = blank_between_marker(board, "X")

    assert result == 3

def test_amt_groups_3_consecutive_markers():
    board = Board(size=3)
    board.values = [["X", "X", "."],
                    ["X", "O", "O"],
                    ["O", "X", "X"]]
    result = amt_groups_n_consecutive_markers(board=board, marker='X')
    assert result == 0

    board = Board(size=3)
    board.values = [["X", "X", "."],
                    ["X", "O", "O"],
                    ["X", "X", "X"]]
    result = amt_groups_n_consecutive_markers(board=board, marker='X')
    assert result == 2

    board = Board(size=3)
    board.values = [["X", "X", "."],
                    ["X", "X", "O"],
                    ["X", "X", "X"]]
    result = amt_groups_n_consecutive_markers(board=board, marker='X')
    assert result == 4


def test_amt_groups_5_consecutive_markers():
    board = Board(size=5)
    board.values = [["X", "X", ".", ".", "."],
                    ["X", "X", "O", ".", "."],
                    ["O", "X", "X", "X", "X"],
                    ["O", "X", "X", "X", "."],
                    ["O", "X", "X", ".", "X"]]
    result = amt_groups_n_consecutive_markers(board=board, marker='X')
    assert result ==2

def test_two_or_more_markers_in_winnable_line():
    board = Board(size=3)
    board.values = [["X", ".", "X"],
                    ["O", ".", "."],
                    ["X", "O", "X"]]

    result = two_or_more_markers_in_winnable_line(board, "X")
    assert result == 8

    result = two_or_more_markers_in_winnable_line(board, "O")
    assert result == 0

    board = Board(size=3)
    board.values = [[".", ".", "X"],
                    ["O", "O", "."],
                    ["X", "O", "X"]]

    result = two_or_more_markers_in_winnable_line(board, "X")
    assert result == 2

    result = two_or_more_markers_in_winnable_line(board, "O")
    assert result == 4

    board = Board(size=5)
    board.values = [["X", "X", "X", ".", "."],
                    ["O", "O", "O", ".", "."],
                    [".", ".", ".", "O", "O"],
                    ["O", "O", "X", ".", "."],
                    ["X", ".", "X", ".", "X"]]

    result = two_or_more_markers_in_winnable_line(board, "X")
    assert result == 6

    result = two_or_more_markers_in_winnable_line(board, "O")
    assert result == 5
