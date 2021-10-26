import pickle
import argparse
from src.agent import RandomAgent, Agent
from src.tateti import Board, Game


def _show_results(winner, ai_agent, show_alphas=False) -> None:
    """
    Helper function that prints the result, along with the winners, or tie if it's the case
    """
    if not winner:
        print("Tie!")
    elif winner.id == ai_agent.id:
        print(f"The winner is {winner.marker} (AI Agent)")
        if show_alphas:
            print(f"The winner's alphas are: {winner.alphas}")
    else:
        print(f"The winner is {winner.marker} (Random Agent)")
        if show_alphas:
            print(f"The winner's alphas are: {winner.alphas}")


def main(size: int, games: int, agents=False):
    """
    Load the best individual and play against the random agent
    """

    with open("src/best_individual.pkl", "rb") as cp_file:
        best_individual = pickle.load(cp_file)

    ai_agent = Agent(best_individual)
    random_agent = Agent(best_individual) if agents else RandomAgent()

    if games == 1:
        board = Board(size=size)
        game = Game(agent_1=ai_agent, agent_2=random_agent, board=board, debug=True)

        print(f"AI Agent: {ai_agent.marker}")
        if agents:
            print(f"AI Agent 2: {random_agent.marker}")
        else:
            print(f"Random Agent: {random_agent.marker}")

        winner = game.play()
        _show_results(winner, ai_agent, show_alphas=True)
    else:
        for i in range(games):
            print(f"Match {i}")
            board = Board(size=size)
            game = Game(agent_1=ai_agent, agent_2=random_agent, board=board)
            winner = game.play()
            board.pretty_print_board()
            _show_results(winner, ai_agent)
            print("---------------")
        print("")
        if agents:
            print(f"The AI Agent played against the AI Agent 2 {games} times")
        else:
            print(f"The AI Agent played against the Random Agent {games} times")
        print(
            f"The AI Agent won {ai_agent.wins} times (succes_rate={ai_agent.wins/games})"
        )
        print(
            f"The Random Agent won {random_agent.wins} times (succes_rate={random_agent.wins/games})"
        )
        if agents:
            print(
                f"The AI Agent 2 won {random_agent.wins} times (succes_rate={random_agent.wins/games})"
            )
        else:
            print(
                f"The Random Agent won {random_agent.wins} times (succes_rate={random_agent.wins/games})"
            )
        print(f"There were {ai_agent.ties} ties")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", type=int, help="Board size", default=3)
    parser.add_argument("-g", "--games", type=int, help="Amount of games", default=1)
    parser.add_argument("-a", "--agents", help="Game between 2 AI Agents", action='store_true')

    args = parser.parse_args()
    main(size=args.size, games=args.games, agents=args.agents)