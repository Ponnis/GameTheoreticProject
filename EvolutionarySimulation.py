import models as m
import numpy as np

class EvolutionarySimulation():

    def __init__(self,team_size,population_size, survival_limit, trade_prob, transfer_prob):
        self.team_size = team_size
        self.num_players = population_size
        self.survival_limit = survival_limit
        self.trade_prob = trade_prob
        self.transfer_prob = transfer_prob
        self.player_list = self.initialize_players()
        self.score_list = np.zeros(self.num_players)
        self.nash_dict = m.loadNashLookupDict()

    # Generates teams of initial players. Right now it makes one of each combinations (including more types on the same team).
    # Might change to something else later. This was easier to implement.
    def initialize_players(self):
        # The following code generates one team per possible combination. They are now commented out as that would be an
        # absolute runtime mess.
        #player_list = np.full((pow(18,3),self.team_size),m.Types.NORMAL)
        #i = 0
        #for mon1 in m.Types:
        #    for mon2 in m.Types:
        #        for mon3 in m.Types:
        #            player_list[i] = [mon1, mon2, mon3]
        #            i += 1

        #player_list = np.array([[m.Types.GRASS, m.Types.WATER, m.Types.DARK],
        #                        [m.Types.GRASS, m.Types.WATER, m.Types.BUG],
        #                        [m.Types.FIRE, m.Types.STEEL, m.Types.BUG],
        #                        [m.Types.NORMAL, m.Types.PSYCHIC, m.Types.DRAGON],
        #                        [m.Types.DARK, m.Types.FIRE, m.Types.DARK],
        #                        [m.Types.STEEL, m.Types.ELECTRIC, m.Types.ICE]])

        num_per_comb = self.num_players // 18
        player_list = np.full((18*num_per_comb,self.team_size),m.Types.NORMAL)
        i = 0  # Lmao
        for mon in m.Types:
            player_list[i*num_per_comb:(i+1)*num_per_comb] = np.full(self.team_size,mon)
            i += 1

        return player_list

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
        # (This part can be further speed optimized, but I got tired of googling syntaxes)
        scores_sorted = np.sort(self.score_list)[::-1]
        bp = self.find_break_point(scores_sorted,bp=score_to_survive,first=0,last=len(scores_sorted))  # bp == number of survivors
        surviving_scores = scores_sorted[0:bp]

        ascendingly_sorted_indices = np.argsort(self.score_list)
        ascendingly_sorted_teams = self.player_list[ascendingly_sorted_indices]
        surviving_teams = ascendingly_sorted_teams[(self.num_players-bp):self.num_players]
        surviving_teams = np.flip(surviving_teams)  # indices should now match with surviving_scores

        # Step 2: Make a new population with a distribution like proportional to their scores
        total_score = sum(surviving_scores) + (-score_to_survive+1)*bp
        population_filled = 0
        for i in range(len(surviving_teams)):
            num_copies = round(self.num_players * (surviving_scores[i] - score_to_survive + 1) / total_score)
            self.player_list[population_filled:num_copies] = surviving_teams[i]
            population_filled += num_copies

        # Step 3: Possible trades or "mutations".
        for i in range(self.num_players):
            for j in range(self.team_size):
                # Each player has a probability to trade away pokémon on the team with corresponding one of
                # another random player.
                if np.random.rand() < trade_probability:
                    player_to_trade_with = np.random.randint(self.num_players)
                    copied_mon = self.player_list[i][j]
                    self.player_list[i][j] = self.player_list[player_to_trade_with][j]
                    self.player_list[player_to_trade_with][j] = copied_mon

                # They also have a probability for each of their Pokémon to be switched out for another
                # one at random with uniform distribution over types.
                if np.random.rand() < mutation_probability:
                    self.player_list[i][j] = m.Types(np.random.randint(0,18))

    # Let all players battle each other and evaluate score
    def play_game(self):
        for p1 in range(self.num_players):
            for p2 in range(p1):
                team1 = self.player_list[p1]
                team2 = self.player_list[p2]
                scores = m.lookupValue(team1, team2, self.nash_dict)
                self.score_list[p1] += scores[0]
                self.score_list[p2] += scores[1]

    # Play the simulator for one generation and return the state. (To be called from outside)
    def play_one_round(self):
        self.play_game()
        self.switch_pokemon(self.survival_limit,self.trade_prob,self.transfer_prob)
        return self.player_list.copy()


# --------- SOME LINES TO TEST THE METHODS -----------
#sim = EvolutionarySimulation()
#for gen in range(10):
#    sim.play_one_round()
#    print(sim.player_list)



