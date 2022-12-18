import timeit

import matplotlib.pyplot as plt
import models as m
import visualization
import Evolutionary_visualization
import EvolutionarySimulation

#example_game = m.PokemonGame(team1=[m.Types.GRASS, m.Types.WATER, m.Types.DARK],
#                             team2=[m.Types.GRASS, m.Types.WATER, m.Types.BUG])

#test_team1 = [m.Types.NORMAL, m.Types.NORMAL]
#test_team2 = [m.Types.NORMAL, m.Types.POISON]
#m.staticWinnerWithNash(2)

es = EvolutionarySimulation.EvolutionarySimulation(team_size=2, population_size=5*18, survival_limit=0.8,
                                                   trade_prob=0.4, transfer_prob=0.05)
players_over_time = []
ev = Evolutionary_visualization.EvolutionaryVisualization(es.player_list)

for time in range(1,200):
    generation = es.play_one_round()
    #players_over_time.append(generation)
    ev.update_line(time,generation)

plt.show()


