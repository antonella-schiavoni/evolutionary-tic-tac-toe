# Tic Tac Toe - Genetic Algorithm

This project consists of several scripts that are used to run the evolutionary algorithm to train an Agent to play tic tac toe. The main goal is to beat a Random Agent which will select an empty box randomly.

## Set up

In order to run this project, you should be located in folder named `3`. It's highly advised that all the commands mentioned in this file are run from this folder.

- Create a new virtual environment
- Install requirements: `pip install -r src/requirements.txt`

## How to run?

```
python -m src.ai_agent_vs_random_agent
```

This script makes the best ai agent saved in the pickle play against a random agent. This is an example of the output:

AI Agent: X
Random Agent: O
```
['.', '.', '.']
['.', '.', '.']
['.', '.', '.']
---------------
['.', '.', '.']
['.', 'X', '.']
['.', '.', '.']
---------------
['.', '.', 'O']
['.', 'X', '.']
['.', '.', '.']
---------------
['.', '.', 'O']
['.', 'X', '.']
['X', '.', '.']
---------------
['.', '.', 'O']
['.', 'X', '.']
['X', '.', 'O']
---------------
['X', '.', 'O']
['.', 'X', '.']
['X', '.', 'O']
---------------
['X', 'O', 'O']
['.', 'X', '.']
['X', '.', 'O']
---------------
['X', 'O', 'O']
['X', 'X', '.']
['X', '.', 'O']
```
The winner is X (AI Agent)
The winner's alphas are: [0.49507123359744676, 0.9018762640396896, 0.7417790044938776, 0.44483942180345415, 0.05025689895808372, 0.6402559306820909]

```
python -m src.ai_agent_vs_random_agent -g 100
```

This script makes the best ai agent saved in the pickle play against a random agent g amount of times.

To play in a bigger board , for example in a 5x5 board, you should execute the following command:

```
python -m src.ai_agent_vs_random_agent -s 5
```

You can also make an Agent play against itself. To do this, execute this command:

```
python -m src.ai_agent_vs_random_agent -a
```

## How to train?

Inside the `src/genetic_algorithm.py` there's all the logic necesary to train an Agent to play tic tac toe. To run this, execute this command:

```
python -m src.genetic_algorithm
```

## Evolutionary Tools 

### Selection

For this project, we used three different selection methods

- tools.selTournament with the tournsize parameter equals to int(POPULATION / 10)
- tools.selBest
- tools.selRoulette

### Mutation

The mutation methods that we experimented with are:

- tools.mutGaussian
- tools.mutPolynomialBounded

### Crossover

For the crossover, we experimented with:

- tools.cxTwoPoint
- tools.cxOnePoint


For a more detailed explanation of each of the genetic features mentionned above, please visit to this page: https://deap.readthedocs.io/en/master/api/tools.html

### Fitness

#### evaluate_win_ratio_against_agent()

Makes an agent play against AMOUNT_OF_GAMES randomly selected agents from the population and return the win ratio

#### evaluate_win_ratio_against_random_agent()

Makes an agent play against a RandomAgent and return the win ratio

#### evaluate_loss_ratio_against_agent()

Makes an agent play against AMOUNT_OF_GAMES randomly selected agents from the population and return the loss ratio

#### evaluate_moves_to_victory()

Makes an agent play against AMOUNT_OF_GAMES randomly selected agents from the population.
Compute the number of moves it took the agent to win and also how many steps it took to defeat the opponent


## Experiment Results

### Experiment 1

Configuration:

    GENERATIONS = 30
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 100
    CXPB = 0.5
    MUTPB = 0.5

    Mate: cxTwoPoint
    Mutate: mutGaussian
    Selection: selTournament
    Evaluate: evaluate_win_ratio_against_random_agent
    Fitness: creator.create("Fitness", base.Fitness, weights=(1.0,))

Result:

	The AI Agent played against the Random Agent 100 times
	The AI Agent won 95 times (succes_rate=0.95)
	The Random Agent won 5 times (succes_rate=0.05)
	There were 0 ties


### Experiment 2

Configuration:

    GENERATIONS = 30
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 100
    CXPB = 0.5
    MUTPB = 0.5

    Mate: cxTwoPoint
    Mutate: mutGaussian
    Selection: selTournament
    Evaluate: evaluate_loss_ratio_against_agent
    Fitness: creator.create("Fitness", base.Fitness, weights=(-1.0,)

Result:

	The AI Agent played against the Random Agent 100 times
	The AI Agent won 47 times (succes_rate=0.47)
	The Random Agent won 51 times (succes_rate=0.51)
	There were 2 ties


### Experiment: 3

Configuration:

    GENERATIONS = 30
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 100
    CXPB = 0.5
    MUTPB = 0.5

    Mate: cxTwoPoint
    Mutate: mutGaussian
    Selection: selTournament
    Evaluate: evaluate_moves_to_victory
    Fitness: creator.create("Fitness", base.Fitness, weights=(1.0,-1.0))

Result:

	The AI Agent played against the Random Agent 100 times
	The AI Agent won 71 times (succes_rate=0.71)
	The Random Agent won 29 times (succes_rate=0.29)
	There were 0 ties


### Experiment: 4

Configuration:

    GENERATIONS = 30
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 100
    CXPB = 0.5
    MUTPB = 0.5

    Mate: cxTwoPoint
    Mutate: mutGaussian
    Selection: selTournament
    Evaluate: evaluate_win_ratio_against_agent
    Fitness: creator.create("Fitness", base.Fitness, weights=(1.0,))


Result:

	The AI Agent played against the Random Agent 100 times
	The AI Agent won 64 times (succes_rate=0.64)
	The Random Agent won 33 times (succes_rate=0.33)
	There were 3 ties


### Experiment: 5

Configuration:

    GENERATIONS = 30
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 100
    CXPB = 0.5
    MUTPB = 0.5

    Mate: cxTwoPoint
    Mutate: mutGaussian
    Selection: selBest
    Evaluate: evaluate_moves_to_victory
    Fitness: creator.create("Fitness", base.Fitness, weights=(1.0,-1.0))

Result:

	The AI Agent played against the Random Agent 100 times
	The AI Agent won 82 times (succes_rate=0.82)
	The Random Agent won 18 times (succes_rate=0.18)
	There were 0 ties


### Experiment: 6

Configuration:

    GENERATIONS = 30
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 100
    CXPB = 0.5
    MUTPB = 0.5

    Mate: cxTwoPoint
    Mutate: mutGaussian
    Selection: selRoulette
    Evaluate: evaluate_moves_to_victory
    Fitness: creator.create("Fitness", base.Fitness, weights=(1.0,-1.0))

Result:

	The AI Agent played against the Random Agent 100 times
	The AI Agent won 60 times (succes_rate=0.6)
	The Random Agent won 38 times (succes_rate=0.38)
	There were 2 ties


### Experiment: 7

Configuration:

	GENERATIONS = 30
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 100
    CXPB = 0.5
    MUTPB = 0.5

    Mate: cxOnePoint
    Mutate: mutGaussian
    Selection: selBest
    Evaluate: evaluate_moves_to_victory
    Fitness: creator.create("Fitness", base.Fitness, weights=(1.0,-1.0))

Result:

	The AI Agent played against the Random Agent 100 times
	The AI Agent won 78 times (succes_rate=0.78)
	The Random Agent won 22 times (succes_rate=0.22)
	There were 0 ties


### Experiment: 8

Configuration:

	GENERATIONS = 30
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 100
    CXPB = 0.5
    MUTPB = 0.5

	Mate: cxTwoPoint
    Mutate: mutPolynomialBounded
    Selection: selBest
    Evaluate: evaluate_moves_to_victory
    Fitness: creator.create("Fitness", base.Fitness, weights=(1.0,-1.0))

Result:

	The AI Agent played against the Random Agent 100 times
	The AI Agent won 43 times (succes_rate=0.43)
	The Random Agent won 45 times (succes_rate=0.45)
	There were 12 ties
	
### Experiment: 9 (Best)

Configuration:

    GENERATIONS = 50
    INDIVIDUALS_TO_SELECT = 10
    POPULATION = 500
    CXPB = 0.6
    MUTPB = 0.4

	Mate: cxTwoPoint
    Mutate: mutGaussian
    Selection: selBest
    Evaluate: evaluate_moves_to_victory
    Fitness: creator.create("Fitness", base.Fitness, weights=(1.0,-1.0))

Result:

    The AI Agent played against the Random Agent 100 times
    The AI Agent won 95 times (succes_rate=0.95)
    The Random Agent won 5 times (succes_rate=0.05)
    There were 0 ties


