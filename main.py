import models as m

example_game = m.PokemonGame(team1=[m.Types.DRAGON, m.Types.DRAGON, m.Types.DRAGON],
                             team2=[m.Types.ICE, m.Types.FAIRY, m.Types.FAIRY])
print(example_game.utility_matrix)
print(example_game.nash_eqs)
