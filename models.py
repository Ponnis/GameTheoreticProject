# Models and utilities for the pokemon games and likes go here
from enum import Enum
import numpy as np
import nashpy


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
    utilities = np.random.rand(6, 6)

    return utilities


# Calculate the mixed nash for a given zero-sum game
def calculateNash(pokemon_game):
    utilities = pokemon_game.utility_matrix
    nash_game = nashpy.Game(utilities)
    nash_EQs = nash_game.support_enumeration()
    return list(nash_EQs)

# Perform a battle with selections based on the nash_EQ and return the resulting score for each player
# Output: [scoreP1, scoreP2]
def battle(pokemon_game,num_rounds):
    p1_pick = -1
    p2_pick = -1
    scores = [0,0]
    num_options = len(pokemon_game.nash_eqs[0][0])
    for n in range(num_rounds):
        rP1 = np.random.rand()
        rP2 = np.random.rand()
        for k in range(num_options):
            mixed_k1 = pokemon_game.nash_eqs[0][0][k]
            mixed_k2 = pokemon_game.nash_eqs[0][1][k]
            if rP1 < mixed_k1:
                p1_pick = k
            else:
                rP1 -= mixed_k1
            if rP2 < mixed_k2:
                p2_pick = k
            else:
                rP2 -= mixed_k2

        print(scores[0])
        scores[0] += pokemon_game.utility_matrix[p1_pick][p2_pick][0]
        scores[1] += pokemon_game.utility_matrix[p1_pick][p2_pick][1]
    scores[0] = scores[0]/num_rounds
    scores[1] = scores[1]/num_rounds

    return scores


