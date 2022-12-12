import timeit

import models
import models as m
import visualization

example_game = m.PokemonGame(team1=[m.Types.GRASS, m.Types.WATER, m.Types.DARK],
                             team2=[m.Types.GRASS, m.Types.WATER, m.Types.BUG])

b_dict = m.getLookupDict(3)
test_team1 = [m.Types.NORMAL, m.Types.NORMAL, m.Types.NORMAL]
test_team2 = [m.Types.WATER, m.Types.GRASS, m.Types.FIGHT]
start = timeit.timeit()
print(m.lookupValue(test_team1, test_team2, b_dict))
end = timeit.timeit()
print("Elapsed time: " + str(end - start))
