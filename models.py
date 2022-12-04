# Models and utilities for the pokemon games and likes go here
from enum import Enum
import numpy as np
import nashpy
import itertools


class Types(Enum):
    NORMAL = 0
    FIRE = 1
    WATER = 2
    ELECTRIC = 3
    GRASS = 4
    ICE = 5
    FIGHT = 6
    POISON = 7
    GROUND = 8
    FLYING = 9
    PSYCHIC = 10
    BUG = 11
    ROCK = 12
    GHOST = 13
    DRAGON = 14
    DARK = 15
    STEEL = 16
    FAIRY = 17


pokemon_types = ["Normal", "Fire", "Water", "Electric", "Grass", "Ice",
                 "Fighting", "Poison", "Ground", "Flying", "Psychic",
                 "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]

# Can be indexed like type_chart
type_chart = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 2, 0, 1, 1, 1 / 2, 1],
                       [1, 1 / 2, 1 / 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1 / 2, 1, 1 / 2, 1, 2, 1],
                       [1, 2, 1 / 2, 1, 1 / 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1 / 2, 1, 1, 1],
                       [1, 1, 2, 1 / 2, 1 / 2, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1 / 2, 1, 1, 1],
                       [1, 1 / 2, 2, 1, 1 / 2, 1, 1, 1 / 2, 2, 1 / 2, 1, 1 / 2, 2, 1, 1 / 2, 1, 1 / 2, 1],
                       [1, 1 / 2, 1 / 2, 1, 2, 1 / 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1 / 2, 1],
                       [2, 1, 1, 1, 1, 2, 1, 1 / 2, 1, 1 / 2, 1 / 2, 1 / 2, 2, 0, 1, 2, 2, 1 / 2],
                       [1, 1, 1, 1, 2, 1, 1, 1 / 2, 1 / 2, 1, 1, 1, 1 / 2, 1 / 2, 1, 1, 0, 2],
                       [1, 2, 1, 2, 1 / 2, 1, 1, 2, 1, 0, 1, 1 / 2, 2, 1, 1, 1, 2, 1],
                       [1, 1, 1, 1 / 2, 2, 1, 2, 1, 1, 1, 1, 2, 1 / 2, 1, 1, 1, 1 / 2, 1],
                       [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1 / 2, 1, 1, 1, 1, 0, 1 / 2, 1],
                       [1, 1 / 2, 1, 1, 2, 1, 1 / 2, 1 / 2, 1, 1 / 2, 2, 1, 1, 1 / 2, 1, 2, 1 / 2, 1 / 2],
                       [1, 2, 1, 1, 1, 2, 1 / 2, 1, 1 / 2, 2, 1, 2, 1, 1, 1, 1, 1 / 2, 1],
                       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1 / 2, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1 / 2, 0],
                       [1, 1, 1, 1, 1, 1, 1 / 2, 1, 1, 1, 2, 1, 1, 2, 1, 1 / 2, 1, 1 / 2],
                       [1, 1 / 2, 1 / 2, 1 / 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1 / 2, 2],
                       [1, 1 / 2, 1, 1, 1, 1, 2, 1 / 2, 1, 1, 1, 1, 1, 1, 2, 2, 1 / 2, 1]])


class PokemonGame():
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.utility_matrix = calculateUtilities(team1, team2)
        self.nash_eqs = calculateNash(self)


# Calculate the utility matrix for two given teams
def calculateUtilities(team1, team2):
    utilities = np.zeros((6, 6), dtype='i,i')
    print(list(range(3)))
    team1_permutations = list(itertools.permutations(team1))
    team2_permutations = list(itertools.permutations(team2))
    print(team2_permutations[0][0].value)
    print(team2_permutations)
    for i in range(len(team1_permutations)):
        for j in range(len(team2_permutations)):
            team1_effectiveness = np.zeros(3)
            team2_effectiveness = np.zeros(3)
            for k in range(3):
                team2_effectiveness[k] = type_chart[team1_permutations[i][k].value, team2_permutations[j][k].value]
                team1_effectiveness[k] = type_chart[team2_permutations[j][k].value, team1_permutations[i][k].value]

            utilities[i, j] = effectivenessToUtility(team1_effectiveness, team2_effectiveness)

    return utilities


def effectivenessToUtility(team1_utilities, team2_utilities):
    p1_utility = 0
    p2_utility = 0

    for i in range(len(team1_utilities)):
        diff = team1_utilities[i] - team2_utilities[i]
        if diff > 0:
            p1_utility += 1
            p2_utility -= 1
        if diff < 0:
            p2_utility += 1
            p1_utility -= 1

    return p1_utility, p2_utility

def splitUtilities(utilities):
    player1_utilities = np.zeros((6, 6), dtype='i')
    player2_utilities = np.zeros((6, 6), dtype='i')
    for i in range(len(utilities)):
        for j in range(len(utilities)):
            player1_utilities[i, j] = utilities[i, j][0]
            player2_utilities[i, j] = utilities[i, j][1]

    return player1_utilities, player2_utilities


# Calculate the mixed nash for a given zero-sum game
def calculateNash(pokemon_game):
    utilities = pokemon_game.utility_matrix
    A, B = splitUtilities(utilities)
    nash_game = nashpy.Game(A, B)
    nash_EQs = nash_game.support_enumeration()

    return list(nash_EQs)


# def calculateNash2(game):
# for every row
# for every column
# Check player 1, can a better move be made?
# Check player 2, can a better move be made?
# if neither:
# nash eq
# else:
# not nash eq

# OR

# start with player 1
# mark indices where it has the highest utility in a row
# now player 2
# mark indices where it has the highest utility in a column
# match indices , if match, that is a nash eq.


# Perform a battle with selections based on the nash_EQ and return the resulting score for each player
# Output: [scoreP1, scoreP2]
def battle(pokemon_game):
    scores = [0, 0]
    return scores
