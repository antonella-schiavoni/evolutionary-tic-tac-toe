import pickle
import random
from typing import Tuple

import numpy as np

from deap import base, creator, tools, algorithms

from src.agent import RandomAgent, AMOUNT_OF_FEATURES
from src.tateti import Agent, Board, Game


# creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Fitness", base.Fitness, weights=(1.0,-1.0)) # To be used only when the evaluation function is evaluate_moves_to_victory
# creator.create("Fitness", base.Fitness, weights=(-1.0,) # To be used only when the evaluation function is evaluate_loss_ratio_against_agent

creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()


# https://stackoverflow.com/questions/58745803/deap-make-fitness-of-an-individual-depend-on-entire-population
def evaluate_win_ratio_against_agent(individual, population) -> Tuple:
    """
    Makes an agent play against AMOUNT_OF_GAMES randomly selected agents from the population and return the win ratio
    """
    agent_1 = Agent(individual)
    wins = 0
    AMOUNT_OF_GAMES = 30

    if len(population) < AMOUNT_OF_GAMES:
        population_subset = population
    else:
        population_subset = random.sample(population, AMOUNT_OF_GAMES)

    for opponent_individual in population_subset:
        board = Board()
        agent_2 = Agent(opponent_individual)
        game = Game(agent_1=agent_1, agent_2=agent_2, board=board)
        winner = game.play()

        if winner and winner.id == agent_1.id:
            wins += 1

    return ((wins / AMOUNT_OF_GAMES),)

# Alternative fitness function
def evaluate_win_ratio_against_random_agent(individual) -> Tuple:
    """
    Makes an agent play against a RandomAgent and return the win ratio
    """
    agent_1 = Agent(individual)
    wins = 0
    AMOUNT_OF_GAMES = 30

    for i in range(AMOUNT_OF_GAMES):
        random_agent = RandomAgent()
        board = Board()
        game = Game(agent_1=agent_1, agent_2=random_agent, board=board)
        winner = game.play()

        if winner and winner.id == agent_1.id:
            wins += 1

    return ((wins / AMOUNT_OF_GAMES),)


# Alternative fitness function
def evaluate_loss_ratio_against_agent(individual, population) -> Tuple:
    """
    Makes an agent play against AMOUNT_OF_GAMES randomly selected agents from the population and return the loss ratio
    """
    agent_1 = Agent(individual)
    losses = 0
    AMOUNT_OF_GAMES = 30

    if len(population) < AMOUNT_OF_GAMES:
        population_subset = population
    else:
        population_subset = random.sample(population, AMOUNT_OF_GAMES)

    for opponent_individual in population_subset:
        board = Board()
        agent_2 = Agent(opponent_individual)
        game = Game(agent_1=agent_1, agent_2=agent_2, board=board)
        winner = game.play()

        if winner and winner.id == agent_2.id:
            losses += 1

    return ((losses / AMOUNT_OF_GAMES),)

# Alternative fitness function
def evaluate_moves_to_victory(individual, population) -> Tuple:
    """
    Makes an agent play against AMOUNT_OF_GAMES randomly selected agents from the population.
    Compute the number of moves it took the agent to win and also how many steps it took to defeat the opponent
    """
    agent_1 = Agent(individual)
    moves = 0
    wins = 0
    AMOUNT_OF_GAMES = 30

    if len(population) < AMOUNT_OF_GAMES:
        population_subset = population
    else:
        population_subset = random.sample(population, AMOUNT_OF_GAMES)

    for opponent_individual in population_subset:
        board = Board()
        agent_2 = Agent(opponent_individual)
        game = Game(agent_1=agent_1, agent_2=agent_2, board=board)
        winner = game.play()

        if winner and winner.id == agent_1.id:
            moves += agent_1.moves
            wins += 1

    return (wins/AMOUNT_OF_GAMES, moves/max(wins,1))


def main():
    """
    Run evolutionary algorithm
    """
    GENERATIONS = 50
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 500
    CXPB = 0.6
    MUTPB = 0.4

    toolbox.register("attr_float", random.random)
    toolbox.register(
        "individual",
        tools.initRepeat,
        creator.Individual,
        toolbox.attr_float,
        n=AMOUNT_OF_FEATURES,
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    pop = toolbox.population(n=POPULATION)

    toolbox.register("mate", tools.cxTwoPoint)
    # toolbox.register("mate", tools.cxOnePoint) alternative crossover method

    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.3)
    #toolbox.register("mutate", tools.mutPolynomialBounded, eta=10.0, low=0, up=1, indpb=0.3)

    #toolbox.register("select", tools.selTournament, tournsize=int(POPULATION / 10))
    toolbox.register("select", tools.selBest) #alternative selection method
    #toolbox.register("select", tools.selRoulette) # alternative selection method

    #toolbox.register("evaluate", evaluate_win_ratio_against_agent, population=pop)
    #toolbox.register("evaluate", evaluate_win_ratio_against_random_agent) # alternative evaluation method
    # toolbox.register("evaluate", evaluate_loss_ratio_against_agent, population=pop) # alternative evaluation method
    toolbox.register("evaluate", evaluate_moves_to_victory, population=pop) # alternative evaluation method

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min, axis=0)
    stats.register("avg", np.mean, axis=0)
    stats.register("max", np.max, axis=0)
    algorithms.eaMuPlusLambda(
        pop,
        toolbox,
        INDIVIDUALS_TO_SELECT,
        POPULATION,
        CXPB,
        MUTPB,
        GENERATIONS,
        stats,
        halloffame=hof,
        verbose=True,
    )

    return pop, stats, hof


if __name__ == "__main__":
    pop, log, hof = main()
    best_individual = list(hof[0])

    # Save best individual
    with open("src/best_individual.pkl", "wb") as cp_file:
        pickle.dump(best_individual, cp_file)

    # Force winner to play against an agent with random strategy
    print(f"The best individual is: {best_individual}")
    best_agent = Agent(best_individual)
    random_agent = RandomAgent()
    board = Board()

    game = Game(agent_1=best_agent, agent_2=random_agent, board=board, debug=True)
    print(f"Best Agent: {best_agent.marker}")
    print(f"Random Agent: {random_agent.marker}")
    winner = game.play()
    if not winner:
        print("Tie!")
    elif winner.id == best_agent.id:
        print(f"The winner is {winner.marker} (Best Agent)")
    else:
        print(f"The winner is {winner.marker} (Random Agent)")
        print(f"The winner's alphas are: {winner.alphas}")
