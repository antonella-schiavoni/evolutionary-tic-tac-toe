from src.board import Board


def test_is_finished():
    board = Board(size=3)
    board.values = [["X", "X", "O"],
                    ["X", "O", "X"],
                    ["X", "O", "X"]]

    result = board.is_finished()
    assert result == True

    board.values = [[".", "X", "O"],
                    ["X", "O", "X"],
                    ["X", "O", "."]]
    result = board.is_finished()
    assert result == False

    board.values = [["X", ".", "O"],
                    ["X", "O", "X"],
                    ["X", ".", "."]]
    result = board.is_finished()
    assert result == True

def test_is_not_finished():
    board = Board(size=3)
    board.values = [["X", "X", "O"],
                    [".", "O", "."],
                    [".", ".", "O"]]

    result = board.is_finished()
    assert result == False

    board = Board(size=5)
    board.values = [["X", "X", "X", ".", "."],
                    ["O", "O", "O", ".", "."],
                    [".", ".", ".", ".", "."],
                    [".", ".", ".", ".", "."],
                    [".", ".", ".", ".", "."]]

    result = board.is_finished()
    assert result == False

def test_initialize_values_3():
    board = Board(size=3)
    board._initialize_values()

    assert len(board.values) == 3
    for row in board.values:
        assert ['.', '.', '.'] == row


def test_initialize_values_5():
    board = Board(size=5)
    board._initialize_values()

    assert len(board.values) == 5
    for row in board.values:
        assert ['.', '.', '.', '.', '.'] == row

def test_get_empty_boxes():
    board = Board(size=3)
    board.values = [["X", ".", "."],
                    ["X", "O", "."],
                    ["O", ".", "."]]
    result = board.get_empty_boxes()
    assert len(result) == 5


def test_who_won():
    board = Board(size=3)
    board.values = [["X", "X", "O"],
                    ["X", "O", "X"],
                    ["X", "O", "X"]]
    result = board.who_won()
    assert result == "X"

    board.values = [["O", "X", "O"],
                    ["X", "O", "O"],
                    ["X", "O", "X"]]
    result = board.who_won()
    assert result == "-"

    board.values = [["X", "X", "O"],
                    ["X", "X", "O"],
                    ["O", "O", "X"]]
    result = board.who_won()
    assert result == "X"

    board.values = [["X", "X", "O"],
                    ["X", "O", "O"],
                    ["O", "O", "X"]]
    result = board.who_won()
    assert result == "O"
