import random
import logging
import argparse
from src.agent import Agent
from src.board import Board



class Game:
    """
    Class that simulates the tic tac toe game
    """

    def __init__(self, agent_1: Agent, agent_2: Agent, board: Board, debug=False):
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.board = board
        self.debug = debug
        self.set_markers()

        self.agent_1.reset_moves()
        self.agent_2.reset_moves()

    @property
    def players(self):
        return [self.agent_1, self.agent_2]

    def set_markers(self):
        """
        Sets players markers. Player 1 always plays with X, while 2 plays with O
        """
        self.agent_1.marker = "X"
        self.agent_2.marker = "O"

    def play(self):
        """
        Two players compete against each other. Until the game is finished, agent_1 makes a move using "x",
        agent_2 makes a move using "o", then the status of the board is check returning the agent that won the match.
        """

        # Determine randomly who starts playing the game
        active_player, next_active_player = (
            (self.agent_1, self.agent_2)
            if random.random() > 0.5
            else (self.agent_2, self.agent_1)
        )

        while not self.board.is_finished():
            if self.debug:
                self.board.pretty_print_board()
                print("---------------")

            position = active_player.next_move(self.board)
            if position == (
                    -1,
                    -1,
            ):  # if position is (-1,-1), then there are no available moves to do
                break

            logging.debug(
                f"Next Coordinate for marker {active_player.marker} is: {position}"
            )
            active_player.make_move(self.board, position)

            active_player, next_active_player = next_active_player, active_player

        if self.debug:
            self.board.pretty_print_board()

        logging.debug(
            f"Players id: agent 1 is {self.agent_1.id} & agent 2 is {self.agent_2.id}"
        )

        result = self.board.who_won()
        winner = None
        if result == self.agent_1.marker:
            winner = self.agent_1
            self.agent_1.wins += 1
        elif result == self.agent_2.marker:
            winner = self.agent_2
            self.agent_2.wins += 1
        else:
            self.agent_1.ties += 1
            self.agent_2.ties += 1

        logging.debug(
            f"{self.board.values[0]} \n{self.board.values[1]}\n{self.board.values[2]}"
        )

        return winner


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        help="Print lots of debugging statements",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.DEBUG,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    board = Board()
    agent_1 = Agent()
    agent_2 = Agent()
    game = Game(agent_1=agent_1, agent_2=agent_2, board=board)
    winner = game.play()
