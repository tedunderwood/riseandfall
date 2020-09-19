import random, os, sys
from collections import Counter

import string, csv
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from scipy.spatial.distance import cosine

# GET METADATA

# It would probably be simpler if I had written this to use a pandas dataframe,
# but I didn't; I'm using aligned numpy vectors. The reasons lie in the possibility
# of overlapping genre assignments in the LoC version of this code.

results = pd.read_csv('kirkus_delta_results.tsv', sep = '\t')

allgenres = list(set(results['genre']))
print(len(allgenres))

meta = pd.read_csv('genremetadata4kirkusdeltas.tsv', sep = '\t', index_col = 'docid', dtype = {'Dominant_Topic': object})
meta = meta.loc[~meta.index.duplicated(keep='first')]

bydecade = meta.groupby((meta.date//10)*10)

decadeprevalence = dict()

for decade, df in bydecade:
    print(decade)
    if decade < 1935:
        continue
    allbooks = len(df)
    for g in allgenres:
        if g not in decadeprevalence:
            decadeprevalence[g] = []
        thisgenre = df.loc[df['Dominant_Topic'] == str(g), : ]
        thisgenrect = len(thisgenre)
        decadeprevalence[g].append((decade, thisgenrect/allbooks))

allprevalence = []

for g in allgenres:
    decadeprevalence[g].sort()
    decadeprevalence[g] = [x[1] for x in decadeprevalence[g]]
    allprevalence.extend(decadeprevalence[g])

results = pd.read_csv('kirkus_delta_results.tsv', sep = '\t')

bydecade = results.groupby((results.meandate//10)*10)

decademeandiffs = dict()

for decade, df in bydecade:
    allbooks = len(df)
    for g in allgenres:
        if g not in decademeandiffs:
            decademeandiffs[g] = []
        thisgenre = df.loc[df['genre'] == g, : ]
        if len(thisgenre) < 1:
            decademeandiffs[g].append((decade, float('nan')))
        else:
            decademeandiffs[g].append((decade, np.mean(thisgenre.othergenrediff)))

allmeandiffs = []

for g in allgenres:
    decademeandiffs[g].sort()
    decademeandiffs[g] = [x[1] for x in decademeandiffs[g]]
    allmeandiffs.extend(decademeandiffs[g])

allprevalence = np.array(allprevalence)
allmeandiffs = np.array(allmeandiffs)
allprevalence = allprevalence[~np.isnan(allmeandiffs)]
allmeandiffs = allmeandiffs[~np.isnan(allmeandiffs)]

print(pearsonr(allprevalence, allmeandiffs))




