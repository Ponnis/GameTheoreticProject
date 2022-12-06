# Plots and all the likes goes here
import seaborn as sns
from matplotlib import pyplot as plt

import models


# plot a given game

def plotGame(game):
    # Plots a heatmap for both players
    sns.cubehelix_palette(as_cmap=True)
    p1_u, p2_u = models.splitUtilities(game.utility_matrix)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.get_shared_y_axes().join(ax2)
    x_labels_rough = models.convertEnumToString(game.team1_permutations)
    x_labels = [[",".join([str(x) for x in m]) for m in x_labels_rough]][0]
    y_labels_rough = models.convertEnumToString(game.team2_permutations)
    y_labels = [[",".join([str(x) for x in m]) for m in y_labels_rough]][0]
    g1 = sns.heatmap(p1_u, annot=p1_u, fmt='', xticklabels=x_labels,
                     yticklabels=y_labels, ax=ax1, cbar=False)
    g2 = sns.heatmap(p2_u, annot=p2_u, fmt='', yticklabels=x_labels,
                     xticklabels=y_labels, ax=ax2)

    plt.show()


# Plotting a basic type chart
fig, ax = plt.subplots()
ax = sns.heatmap(models.type_chart, annot=models.type_chart, fmt='', cmap="Greens",
                 xticklabels=models.pokemon_types, yticklabels=models.pokemon_types)
print(models.Types.DRAGON.value)
plt.title("Type interaction chart", size=18, color="#b30000")
plt.show()
