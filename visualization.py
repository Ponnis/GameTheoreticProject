# Plots and all the likes goes here
import seaborn as sns
from matplotlib import pyplot as plt

import models

# Plotting a basic type chart
fig, ax = plt.subplots()
ax = sns.heatmap(models.type_chart, annot=models.type_chart, fmt='', cmap="Greens",
                 xticklabels=models.pokemon_types, yticklabels=models.pokemon_types)
print(models.Types.DRAGON.value)
plt.title("Type interaction chart", size=18, color="#b30000")
plt.show()
