# Models and utilities for the pokemon games and likes go here
from enum import Enum
import numpy as np
import nashpy
import itertools
import json

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


pokemon_types = ["Nor", "Fir", "Wtr", "Ele", "Grs", "Ice",
                 "Fig", "Psn", "Gnd", "Fly", "Psy",
                 "Bug", "Rck", "Gst", "Drg", "Drk", "Stl", "Fry"]
pokemon_types_full = ["Normal", "Fire", "Water", "Electric", "Grass", "Ice",
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

possible_types = [Types.NORMAL, Types.FIRE, Types.WATER, Types.ELECTRIC, Types.GRASS, Types.ICE, Types.FIGHT,
                  Types.POISON, Types.GROUND,
                  Types.FLYING, Types.PSYCHIC, Types.BUG, Types.ROCK, Types.GHOST, Types.DRAGON, Types.DARK,
                  Types.STEEL, Types.FAIRY]


class PokemonGame():
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.team1_permutations = list(itertools.permutations(self.team1))
        self.team2_permutations = list(itertools.permutations(self.team2))
        self.utility_matrix = calculateUtilities(team1, team2)
        self.nash_eqs = calculateNash(self.utility_matrix)


def loadNashLookupDict():
    with open('dict.json') as json_file:
        nash_dict = json.load(json_file)

        return nash_dict


def getNashLookupDict(num):
    combinations = list(itertools.combinations_with_replacement(possible_types, num))
    nash_lookup = dict()
    for i in range(len(combinations)):
        for j in range(len(combinations)):
            nash_lookup[str([combinations[i], combinations[j]])] = deterministic_battle(combinations[i],
                                                                                        combinations[j])

    file_dump = json.dumps(nash_lookup)
    f = open("dict.json", "w")
    f.write(file_dump)
    return nash_lookup


# Gets huge lookup dictionary
def getLookupDict(num):
    combinations = list(itertools.combinations_with_replacement(possible_types, num))
    big_dict = dict()
    for i in range(len(combinations)):
        for j in range(len(combinations)):
            big_dict[str([combinations[i], combinations[j]])] = staticUtilityHelper(combinations[i], combinations[j])
    return big_dict


# Looks up value in dictionary
def lookupValue(team1, team2, dict):
    return dict[str([tuple(team1), tuple(team2)])]


# Calculate the utility matrix for all given permutations of a team
def calculateUtilities(team1, team2):
    team1_permutations = list(itertools.permutations(team1))
    team2_permutations = list(itertools.permutations(team2))
    utilities = np.zeros((len(team1_permutations), len(team1_permutations)), dtype='i,i')
    for i in range(len(team1_permutations)):
        for j in range(len(team2_permutations)):
            team1_effectiveness = np.zeros(len(team1))
            team2_effectiveness = np.zeros(len(team1))
            for k in range(len(team1)):
                team1_effectiveness[k] = type_chart[team1_permutations[i][k].value, team2_permutations[j][k].value]
                team2_effectiveness[k] = type_chart[team2_permutations[j][k].value, team1_permutations[i][k].value]

            utilities[i, j] = effectivenessToUtility(team1_effectiveness, team2_effectiveness)

    return utilities


# Converts from effectiveness from the type chart to utility
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


#Splits utilities for player into two matrices
def splitUtilities(utilities):
    m_len = int(np.sqrt(utilities.size))
    player1_utilities = np.zeros((m_len, m_len), dtype='i')
    player2_utilities = np.zeros((m_len, m_len), dtype='i')
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


#Converts the Types.NORMAL to an int representing index
def convertEnumToString(enums_permutations):
    string_permutations = np.zeros((len(enums_permutations), int(len(enums_permutations) / 2)), dtype=np.dtype('U100'))
    for i in range(len(enums_permutations)):
        current = enums_permutations[i]
        for j in range(len(current)):
            ind = current[j].value
            string_permutations[i, j] = pokemon_types[ind]

    return string_permutations

def staticWinnerWithNash(team_size):
    all_teams = list(itertools.combinations_with_replacement(possible_types, team_size))
    all_utilities = np.zeros(shape=(len(all_teams), len(all_teams), team_size))
    total_utilities = np.zeros(len(all_teams))
    nash_dict = loadNashLookupDict()
    for i in range(len(all_teams)):
        for j in range(len(all_teams)):
            all_utilities[i][j] = lookupValue(all_teams[i], all_teams[j], nash_dict)
    for k in range(len(all_utilities)):
        total_utilities[k] = sum(l for l, m in all_utilities[k])

    win_index = list(total_utilities).index(max(total_utilities))
    print("Winning team of " + str(team_size) + " in the static approach is:" + str(
        all_teams[win_index]) + " with an average utility of: " + str(max(total_utilities) / len(total_utilities)))
    runner_ups = [all_teams[i] for i in np.argsort(total_utilities)[-10:]]
    runner_ups_utilities = [total_utilities[i] for i in np.argsort(total_utilities)[-10:]]
    worst = [all_teams[i] for i in np.argsort(total_utilities)[0:10]]
    worst_utilities = [total_utilities[i] for i in np.argsort(total_utilities)[0:10]]

    print("Runner ups are: " + str(runner_ups[1]) + " and " + str(runner_ups[2]) + " with avg utilities of: " + str(
        runner_ups_utilities[1] / len(total_utilities))
          + " and " + str(runner_ups_utilities[2] / len(total_utilities)))
    print("Worst performing combinations were: " + str(worst[0]) + " and " + str(
        worst[1]) + " with avg utilities of: " + str(worst_utilities[0] / len(total_utilities))
          + " and " + str(worst_utilities[1] / len(total_utilities)))

    return all_teams[win_index]

# Determines static game winner depending on team size
def staticWinner(team_size):
    all_teams = list(itertools.combinations_with_replacement(possible_types, team_size))
    all_utilities = np.zeros((len(all_teams), len(all_teams)), dtype=('i,i'))
    total_utilities = np.zeros(len(all_teams))
    for i in range(len(all_teams)):
        for j in range(len(all_teams)):
            all_utilities[i][j] = staticUtilityHelper(all_teams[i], all_teams[j])

    for k in range(len(all_utilities)):
        total_utilities[k] = sum(l for l, m in all_utilities[k])

    win_index = list(total_utilities).index(max(total_utilities))
    print("Winning team of " + str(team_size) + " in the static approach is:" + str(
        all_teams[win_index]) + " with an average utility of: " + str(max(total_utilities) / len(total_utilities)))
    runner_ups = [all_teams[i] for i in np.argsort(total_utilities)[-10:]]
    runner_ups_utilities = [total_utilities[i] for i in np.argsort(total_utilities)[-10:]]
    worst = [all_teams[i] for i in np.argsort(total_utilities)[0:10]]
    worst_utilities = [total_utilities[i] for i in np.argsort(total_utilities)[0:10]]

    print("Runner ups are: " + str(runner_ups[1]) + " and " + str(runner_ups[2]) + " with avg utilities of: " + str(
        runner_ups_utilities[1] / len(total_utilities))
          + " and " + str(runner_ups_utilities[2] / len(total_utilities)))
    print("Worst performing combinations were: " + str(worst[0]) + " and " + str(
        worst[1]) + " with avg utilities of: " + str(worst_utilities[0] / len(total_utilities))
          + " and " + str(worst_utilities[1] / len(total_utilities)))

    return all_teams[win_index]


# Calculates utility given two teams
def staticUtilityHelper(team1, team2):
    team1_utilities = np.zeros(len(team1))
    team2_utilities = np.zeros(len(team2))
    for i in range(len(team1)):
        team1_utilities[i] = type_chart[team1[i].value][team2[i].value]
        team2_utilities[i] = type_chart[team2[i].value][team1[i].value]

    return effectivenessToUtility(team1_utilities, team2_utilities)


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
