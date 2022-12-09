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
        self.nash_eqs = calculateNash(self.utility_matrix)


# Calculate the utility matrix for two given teams
def calculateUtilities(team1, team2):
    utilities = np.zeros((6, 6), dtype='i,i')
    team1_permutations = list(itertools.permutations(team1))
    team2_permutations = list(itertools.permutations(team2))
    for i in range(len(team1_permutations)):
        for j in range(len(team2_permutations)):
            team1_effectiveness = np.zeros(3)
            team2_effectiveness = np.zeros(3)
            for k in range(len(team1)):
                team1_mon = team1_permutations[i][k].value
                team2_mon = team2_permutations[j][k].value
                team2_effectiveness[k] = type_chart[team1_mon, team2_mon]
                team1_effectiveness[k] = type_chart[team2_mon, team1_mon]

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
def calculateNash(utilities):
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


# Perform a battle with random selections based on the nash_EQ and return the resulting score for each player
# Output: [scoreP1, scoreP2]
def probabilistic_battle(team1,team2,num_rounds):
    utility_matrix = calculateUtilities(team1, team2)
    nash_eqs = calculateNash(utility_matrix)
    num_nashes = len(nash_eqs)

    p1_pick = -1  # Initialized to -1 so that we will get an error if no pick is made
    p2_pick = -1
    scores = [0,0]

    if len(nash_eqs) == 0:
        # TODO: Can't think at the moment
        return [0,0]

    num_options = len(nash_eqs[0][0])  # Will probably always be 6
    for n in range(num_rounds):
        rP1 = np.random.rand()
        rP2 = np.random.rand()
        nash_index = np.random.randint(num_nashes)
        for k in range(num_options):
            mixed_k1 = nash_eqs[nash_index][0][k]
            mixed_k2 = nash_eqs[nash_index][1][k]
            if rP1 < mixed_k1:
                p1_pick = k
            else:
                rP1 -= mixed_k1
            if rP2 < mixed_k2:
                p2_pick = k
            else:
                rP2 -= mixed_k2

        scores[0] += utility_matrix[p1_pick][p2_pick][0]
        scores[1] += utility_matrix[p1_pick][p2_pick][1]
    scores[0] = scores[0]/num_rounds
    scores[1] = scores[1]/num_rounds

    return scores

# Calculating theoretical result as they would have been after an infinite amount of battles.
def deterministic_battle(team1,team2):
    utility_matrix = calculateUtilities(team1, team2)
    nash_eqs = calculateNash(utility_matrix)
    averaged_utilities = [0,0]  # [p1,p2]
    num_nashes = len(nash_eqs)
    if num_nashes == 0:
        # TODO: Can't think at the moment
        return [0,0]

    num_options = len(nash_eqs[0][0])  # Will probably always be 6

    for nash_index in range(num_nashes):
        for i in range(num_options):
            for j in range(num_options):
                #  I think this is the correct way to compute it
                averaged_utilities[0] += nash_eqs[nash_index][0][i] * nash_eqs[nash_index][1][j] * utility_matrix[i][j][0]
                averaged_utilities[1] += nash_eqs[nash_index][0][i] * nash_eqs[nash_index][1][j] * utility_matrix[i][j][1]

    averaged_utilities[0] = averaged_utilities[0] / num_nashes
    averaged_utilities[1] = averaged_utilities[1] / num_nashes

    return averaged_utilities
