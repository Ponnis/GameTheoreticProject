import unittest
import models
import numpy as np


class MainTest(unittest.TestCase):

    # zero sum game test case
    def testCalculateNash(self):
        utility_matrix = np.array([[3, -4], [-2, 3]])

        team_1 = [models.Types.BUG, models.Types.ICE, models.Types.ICE]
        team_2 = [models.Types.BUG, models.Types.ICE, models.Types.ICE]
        game = models.PokemonGame(team_1, team_2)

        # replace matrix for testing purposes
        game.utility_matrix = utility_matrix
        nash_EQs = models.calculateNash(game)

        expected_nash = np.array([5/12, 7/12])

        first_nash = nash_EQs[0][0]

        self.assertEqual(first_nash, expected_nash)  # add assertion here


if __name__ == '__main__':
    unittest.main()
