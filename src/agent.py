import copy
import uuid
import random
import numpy as np
from typing import Tuple

from src.board import Board
from src.metrics import (
    amt_groups_n_consecutive_markers,
    amt_groups_n_consecutive_markers_followed_by_marker,
    two_or_more_markers_in_winnable_line,
    is_marker_in_center,
)

AMOUNT_OF_FEATURES = 6


def get_a_uuid() -> str:
    """
    Generate a unique id
    """
    return str(uuid.uuid4().fields[-1])[:5]


class Agent:
    def __init__(self, alphas=None):
        self.id = get_a_uuid()
        self._marker = ""
        self.wins = 0
        self.loss = 0
        self.ties = 0
        self.moves = 0
        self.alphas = alphas or [random.uniform(0, 1) for _ in range(7)]

    @property
    def marker(self) -> str:
        return self._marker

    @marker.setter
    def marker(self, marker: str) -> None:
        self._marker = marker

    def evaluate_board(self, board: Board) -> float:
        """
        Given a board, calculate and return the score

        Some thoughts: If player is playing
        """
        opponent_marker = "X" if self.marker == "O" else "O"

        consecutive_marker_followed_by_opponent_marker = (
            amt_groups_n_consecutive_markers_followed_by_marker(board, self.marker)
        )
        consecutive_opponent_marker_followed_by_marker = (
            amt_groups_n_consecutive_markers_followed_by_marker(board, opponent_marker)
        )

        two_or_more_markers_in_winnable_line(board, self.marker)
        two_or_more_markers_in_winnable_line(board, opponent_marker)

        result = (
            self.alphas[0] * amt_groups_n_consecutive_markers(board, self.marker)
            + self.alphas[1] * consecutive_marker_followed_by_opponent_marker
            + self.alphas[2] * consecutive_opponent_marker_followed_by_marker
            + self.alphas[3] * two_or_more_markers_in_winnable_line(board, self.marker)
            + self.alphas[4]
            * two_or_more_markers_in_winnable_line(board, opponent_marker)
            + self.alphas[5] * is_marker_in_center(board, self.marker)
        )

        return result

    def make_move(self, board: Board, position: Tuple) -> Board:
        """
        Put the agent's marker in the position on the board
        """
        self.moves += 1
        row = position[0]
        column = position[1]
        board.values[row][column] = self.marker

        return board

    def next_move(self, board: Board) -> Tuple[int, int]:
        """
        Takes a board and returns the number of row and column of the next move.
        If there are no empty boxes, it means the game is finished
        """
        boards = []
        scores = []
        empty_boxes = board.get_empty_boxes()

        for coordinates in empty_boxes:
            board_copy = copy.deepcopy(board)
            board_copy = self.make_move(board_copy, coordinates)
            boards.append(board_copy)
            scores.append(self.evaluate_board(board_copy))

        if empty_boxes:
            idx_highest_score = scores.index(max(scores))
            # best_board = boards[idx_highest_score]
            best_coordinates = empty_boxes[idx_highest_score]
        else:
            best_coordinates = (-1, -1)

        return best_coordinates

    def reset_moves(self)->None:
        self.moves = 0


class RandomAgent(Agent):
    """
    RandomAgent class plays tic tac toe randomly
    """

    def __init__(self):
        super().__init__()

    def next_move(self, board: Board) -> Tuple[int, int]:
        """
        Takes a board and returns the number of row and column of the next move.
        If there are no empty boxes, it means the game is finished
        """
        boards = []
        scores = []
        empty_boxes = board.get_empty_boxes()

        for coordinates in empty_boxes:
            board_copy = copy.deepcopy(board)
            board_copy = self.make_move(board_copy, coordinates)
            boards.append(board_copy)
            scores.append(np.random.binomial(1, 0.5))

        if empty_boxes:
            idx_highest_score = scores.index(max(scores))
            best_coordinates = empty_boxes[idx_highest_score]
        else:
            best_coordinates = (-1, -1)

        return best_coordinates
