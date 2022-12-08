import models
import models as m
import visualization

example_game = m.PokemonGame(team1=[m.Types.GRASS, m.Types.WATER, m.Types.DARK],
                             team2=[m.Types.GRASS, m.Types.WATER, m.Types.BUG])

print(example_game.utility_matrix)
print(m.splitUtilities(example_game.utility_matrix))
models.staticWinner(2)
