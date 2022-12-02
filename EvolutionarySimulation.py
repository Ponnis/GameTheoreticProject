import models as m
import numpy as np

class EvolutionarySimulation():

    def __init__(self):
        self.team_size = 3
        self.player_list = self.initialize_players()
        self.num_players = len(self.player_list)
        self.score_list = np.zeros(self.num_players)
        self.game = m.PokemonGame(None,None)

    # Generates teams of initial players. Right now it makes one of each combinations (including more types on the same team).
    # Might change to something else later. This was easier to implement.
    def initialize_players(self):
        player_list = np.zeros((180,self.team_size))
        i = 0
        for mon1 in m.Types:
            for mon2 in m.Types:
                for mon3 in m.Types:
                    player_list[i] = [mon1.value, mon2.value, mon3.value]
                    i += 1

        return player_list

    # Let all players battle each other and evaluate score
    def play_game(self):
        for p1 in range(self.num_players):
            for p2 in range(p1):
                self.game.team1 = self.player_list[p1]
                self.game.team2 = self.player_list[p2]
                self.game.utility_matrix = m.calculateUtilities(self.game.team1,self.game.team2)
                self.game.nash_eqs = m.calculateNash(self.game)
                scores = m.battle(self.game)
                self.score_list[p1] += scores[0]
                self.score_list[p2] += scores[1]

    # Give all players a chance to reconsider their teams based on their own and other players' score.
    def switch_pokemon(self):
        # Step 1: Sort out all players with a score < 0.
        # Step 2: Make a new population with a distribution like ??
        # Step 3: Possible trades.
        # Step 4: Possible "mutations"
        return None

    # Play the simulator for one generation and return the state. (To be called from outside)
    def play_one_round(self):
        # TODO:
        return None


sim = EvolutionarySimulation()
print(sim.player_list)

