import timeit

import models
import models as m
import visualization
import Evolutionary_visualization
import EvolutionarySimulation

#example_game = m.PokemonGame(team1=[m.Types.GRASS, m.Types.WATER, m.Types.DARK],
#                             team2=[m.Types.GRASS, m.Types.WATER, m.Types.BUG])

test_team1 = [m.Types.NORMAL, m.Types.NORMAL]
test_team2 = [m.Types.NORMAL, m.Types.POISON]
m.staticWinnerWithNash(2)

print("here")

#for time in range(10):
#    generation = e.play_one_round()
#    players_over_time.append(generation)

#Evolutionary_visualization.visualize_typing_evolution(players_over_time)