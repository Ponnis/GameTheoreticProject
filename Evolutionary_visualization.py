import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import models as m

class EvolutionaryVisualization:
    def __init__(self,initial_generation):
        typing_distribution = create_typing_distribution([initial_generation])
        self.hl = []
        for typing_index in range(len(typing_distribution[0])):
            self.hl.append(plt.plot(0, typing_distribution[0][typing_index]))
            self.hl[typing_index][0].set_color(m.type_colors[typing_index])
        plt.draw()
        plt.pause(0.01)  # is necessary for the plot to update for some reason
        #plt.axis([0, 20, 0, 0.4])
        plt.legend(m.pokemon_types_full)
        #plt.show()

    def update_line(self, gen, new_data):
        new_data = create_typing_distribution([new_data])
        for type_index in range(len(new_data[0])):
            self.hl[type_index][0].set_xdata(np.append(self.hl[type_index][0].get_xdata(), gen))
            self.hl[type_index][0].set_ydata(np.append(self.hl[type_index][0].get_ydata(), new_data[0][type_index]))
        plt.draw()
        plt.pause(0.01)
        plt.axis([0, gen, 0, 0.4])


def visualize_generations(players_over_time):

    unique_teams = dict()
    counter = 0

    # record all the unique teams over the course of the algorithm
    for time in range(len(players_over_time)):
        for team in range(len(players_over_time[time])):
            specific_team = tuple(players_over_time[time][team])
            if(specific_team not in unique_teams):
                unique_teams[specific_team] = counter
                counter += 1

    probability_matrix = np.zeros((len(players_over_time), len(unique_teams.keys())))

    for time in range(len(players_over_time)):
        for team in range(len(players_over_time[time])):
            specific_team = tuple(players_over_time[time][team])
            index = unique_teams[specific_team]

            probability_matrix[time][index] += 1/len(players_over_time[time])

    for x in range(len(probability_matrix[0])):
        plt.plot(range(len(players_over_time)), probability_matrix[:,x])

    plt.show()

def create_typing_distribution(players_over_time):
    generations = len(players_over_time)
    total_mons = len(players_over_time[0]) * len(players_over_time[0][0])
    distribution_matrix = np.zeros((generations, 18))
    for time in range(generations):
        for team in players_over_time[time]:
            for mon in team:
                distribution_matrix[time][mon.value] += 1 / total_mons

    return distribution_matrix

def visualize_typing_evolution(players_over_time):
    distribution_matrix = create_typing_distribution(players_over_time)

    for x in range(len(distribution_matrix[0])):
        plt.plot(range(len(players_over_time)), distribution_matrix[:, x])
        plt.legend(m.pokemon_types_full)

    plt.show()









    # fig = plt.figure()
    # l, = plt.plot([], [], 'k-')
    #
    # l.set_data()


if __name__ == '__main__':

    teams = [[m.Types.GRASS, m.Types.WATER, m.Types.DARK],\
               [m.Types.GRASS, m.Types.WATER, m.Types.BUG],\
               [m.Types.FIRE, m.Types.STEEL, m.Types.BUG],\
               [m.Types.NORMAL, m.Types.PSYCHIC, m.Types.DRAGON],\
               [m.Types.DARK, m.Types.FIRE, m.Types.DARK],\
               [m.Types.STEEL, m.Types.ELECTRIC, m.Types.ICE]]

    artificial_data = []

    for i in range(100):
        artificial_data.append([])
        for j in range(100):
            index = np.random.randint(0, 6)
            artificial_data[i].append(teams[index])

    visualize_generations(artificial_data)




