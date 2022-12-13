import numpy as np


import models as m
import visualization
import Evolutionary_visualization
import EvolutionarySimulation

#example_game = m.PokemonGame(team1=[m.Types.GRASS, m.Types.WATER, m.Types.DARK],
#                             team2=[m.Types.GRASS, m.Types.WATER, m.Types.BUG])

#print(example_game.utility_matrix)
#print(m.splitUtilities(example_game.utility_matrix))
m.staticWinner(2)

#e = EvolutionarySimulation.EvolutionarySimulation()
#generations = 10
#players_over_time = []
#players_over_time.append(Evolutionary_visualization.create_typing_distribution(np.array([e.player_list])))

#for time in range(10):
#    generation = e.play_one_round()
#    players_over_time.append(generation)

#Evolutionary_visualization.visualize_typing_evolution(players_over_time)