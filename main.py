import numpy as np


import timeit

import models
import models as m
import visualization
import Evolutionary_visualization
import EvolutionarySimulation

#example_game = m.PokemonGame(team1=[m.Types.GRASS, m.Types.WATER, m.Types.DARK],
#                             team2=[m.Types.GRASS, m.Types.WATER, m.Types.BUG])

example_game = m.PokemonGame(team1=[m.Types.GRASS, m.Types.WATER, m.Types.DARK],
                             team2=[m.Types.GRASS, m.Types.WATER, m.Types.BUG])

b_dict = m.getLookupDict(3)
test_team1 = [m.Types.NORMAL, m.Types.NORMAL, m.Types.NORMAL]
test_team2 = [m.Types.WATER, m.Types.GRASS, m.Types.FIGHT]
start = timeit.timeit()
print(m.lookupValue(test_team1, test_team2, b_dict))
end = timeit.timeit()
print("Elapsed time: " + str(end - start))
#e = EvolutionarySimulation.EvolutionarySimulation()
#generations = 10
#players_over_time = []
#players_over_time.append(Evolutionary_visualization.create_typing_distribution(np.array([e.player_list])))

#for time in range(10):
#    generation = e.play_one_round()
#    players_over_time.append(generation)

#Evolutionary_visualization.visualize_typing_evolution(players_over_time)