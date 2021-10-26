from src.agent import Agent, AMOUNT_OF_FEATURES
from src.board import Board


def test_make_move():
    agent = Agent()
    agent.marker = "X"
    board = Board(size=3)
    result = agent.make_move(board, (1, 1))

    assert result.values[1][1] == "X"

def test_first_move_is_center():
    alphas = [1] * AMOUNT_OF_FEATURES
    agent = Agent(alphas)
    agent.marker = "X"
    board = Board(size=3)
    result = agent.next_move(board)

    assert result == (1, 1)

    board = Board(size=5)
    result = agent.next_move(board)
    agent.make_move(board, result)
    board.pretty_print_board()

    assert result == (2, 2)