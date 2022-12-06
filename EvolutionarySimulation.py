import models as m
import numpy as np

class EvolutionarySimulation():

    def __init__(self):
        self.team_size = 3
        self.player_list = self.initialize_players()
        self.num_players = len(self.player_list)
        self.score_list = np.zeros(self.num_players)

    # Generates teams of initial players. Right now it makes one of each combinations (including more types on the same team).
    # Might change to something else later. This was easier to implement.
    def initialize_players(self):
        #player_list = np.full((pow(18,3),self.team_size),m.Types.NORMAL)
        #i = 0
        #for mon1 in m.Types:
        #    for mon2 in m.Types:
        #        for mon3 in m.Types:
        #            player_list[i] = [mon1, mon2, mon3]
        #            i += 1

        player_list = np.array([[m.Types.GRASS, m.Types.WATER, m.Types.DARK],
                                [m.Types.GRASS, m.Types.WATER, m.Types.BUG],
                                [m.Types.FIRE, m.Types.STEEL, m.Types.BUG],
                                [m.Types.NORMAL, m.Types.PSYCHIC, m.Types.DRAGON],
                                [m.Types.DARK, m.Types.FIRE, m.Types.DARK],
                                [m.Types.STEEL, m.Types.ELECTRIC, m.Types.ICE]])
        return player_list

    # Let all players battle each other and evaluate score
    def play_game(self):
        for p1 in range(self.num_players):
            for p2 in range(p1):
                team1 = self.player_list[p1]
                team2 = self.player_list[p2]
                scores = m.battle(team1,team2,num_rounds=1)
                self.score_list[p1] += scores[0]
                self.score_list[p2] += scores[1]

    # Help method to find where to cut off a list.
    # Takes in a list sorted descending and returns an index of the first value that's lower than the break point (bp).
    def find_break_point(self,arr,bp,first,last):
        if arr[last-1] >= bp:
            return last
        if arr[first] >= bp > arr[first + 1]:
            return first+1
        mid = (first+last)//2
        if arr[mid] >= bp:
            return self.find_break_point(arr,bp,mid,last)  # Look to the right
        else:  # If arr[mid] < bp
            return self.find_break_point(arr,bp,first,mid)  # Look to the left

    # Give all players a chance to reconsider their teams based on their own and other players' score.
    def switch_pokemon(self, score_to_survive, trade_probability, mutation_probability):
        # Step 1: Sort out all players with a score < 0.
        scores_sorted = np.sort(self.score_list)[::-1]
        bp = self.find_break_point(scores_sorted,bp=score_to_survive,first=0,last=len(scores_sorted))
        surviving_scores = scores_sorted[0:bp]

        ascendingly_sorted_indices = np.argsort(self.score_list)
        ascendingly_sorted_teams = self.player_list[ascendingly_sorted_indices]
        surviving_teams = ascendingly_sorted_teams[(self.num_players-bp):self.num_players]
        surviving_teams = np.flip(surviving_teams)  # indices should now match with surviving_scores

        # Step 2: Make a new population with a distribution like proportional to their scores
        total_score = sum(surviving_scores)
        population_filled = 0
        for i in range(len(surviving_teams)):
            num_copies = round(self.num_players * surviving_scores[i] / total_score)
            self.player_list[population_filled:num_copies] = surviving_teams[i]
            population_filled += num_copies

        # Step 3: Possible trades.
        # TODO (But not necessary for the code to run)

        # Step 4: Possible "mutations". Each player has a probability for each of their Pokémon to be traded for another
        # one at random with uniform distribution.
        for i in range(self.num_players):
            for j in range(self.team_size):
                if np.random.rand() < mutation_probability:
                    self.player_list[i][j] = m.Types(np.random.randint(0,17))

    # Play the simulator for one generation and return the state. (To be called from outside)
    def play_one_round(self):
        self.play_game()
        self.switch_pokemon(0,0.0,0.0)
        return self.player_list


# --------- SOME LINES TO TEST THE METHODS ---------
#sim = EvolutionarySimulation()
#sim.play_one_round()




