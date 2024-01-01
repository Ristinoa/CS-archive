'''graph.py'''

'''Author: A.J. Ristino'''

'''A simple program for creating basic scatterplots for use in
    webapp development'''

import pandas as pd
import albums.csv as albums
from matplotlib import pyplot as plt

pl.style.use('seaborn')

data = pd.read_csv(albums)
rankings = data[0]
numratings = data[5]

plt.scatter(numratings, rankings, edgecolor='black', linewidth=1, alpha=0.75)

plt.title('Ranking (1 - 5000) vs number of ratings')
plt.xlabel('Number of ratings')
plt.ylabel('Ranking')


