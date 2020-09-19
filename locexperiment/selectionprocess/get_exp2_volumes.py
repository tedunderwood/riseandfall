# This code gets the volumes for experiment 2, filtering them for
# appropriate size.
import pandas as pd
import SonicScrewdriver as utils
import os, sys, random

import numpy as np

from sklearn.preprocessing import StandardScaler


from htrc_features import FeatureReader

meta = pd.read_csv('genre_assignments_4loc2.tsv', sep = '\t')

allselected = meta.docid.tolist()

random.shuffle(allselected)

missing = set()
idmapper = dict()

for anid in allselected:

    path, postfix = utils.pairtreepath(anid, '/Volumes/TARDIS/work/ef/fic/')
    totalpath = path + postfix + '/' + utils.clean_pairtree(anid) + '.json.bz2'

    if not os.path.isfile(totalpath):
        if '$' in anid:
            newid = anid.replace('uc1.b', 'uc1.$b')
        else:
            newid = anid.replace('uc1.$b', 'uc1.b')

        path, postfix = utils.pairtreepath(newid, '/Volumes/TARDIS/work/ef/fic/')
        totalpath = path + postfix + '/' + utils.clean_pairtree(newid) + '.json.bz2'
        if os.path.isfile(totalpath):
            idmapper[anid] = totalpath
        else:
            missing.add(anid)
    else:
        idmapper[anid] = totalpath

print("Found: ", len(idmapper))
print("Missing: ", len(missing))
print()

from collections import Counter

import csv
import numpy as np
from collections import Counter

# BUILD TRANSLATORS.

# We want to translate ocr errors and American spellings
# to the correct British spelling when possible.

translator = dict()

with open('../../bpo/gethathimatches/CorrectionRules.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

with open('../../bpo/gethathimatches/VariantSpellings.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

print('Translators built.')

paths = list(set(idmapper.values()))

# The following code is borrowed from Yuerong Hu, and also uses HTRC Feature Reader, by
# Peter Organisciak.

def get_token_counts(vol,hat,tail):
    df_tl = vol.tokenlist().reset_index()# convert to dataframe
    df_tl = df_tl[df_tl['section']=='body']#get rid of header and footer; keep only body
    page_count=df_tl['page'].tolist()[-1]# get total page number
    page_hat=round(page_count*hat)# find the 15% page
    page_tail=page_count-round(page_count*tail)# find the "counter-5%" page
    df_tl=df_tl[df_tl['page'].between(page_hat, page_tail, inclusive=False)] # locate the pages in between
    series_tl=df_tl.groupby(["token"]).size()# group the tokens across pages
    new_df_tl = series_tl.to_frame().reset_index() # convert to df
    return new_df_tl

docfreqs = Counter()
termfreqs = dict()
ctr = 0
alldoclengths = dict()

fr = FeatureReader(paths)
for vol in fr.volumes():
    ctr += 1
    if ctr % 100 == 1:
        print(ctr)

    output = get_token_counts(vol,0.15,0.05)
    docid = str(vol.id)
    doclength = 0

    thesewords = Counter()

    for row in output.itertuples(index = False):
        if pd.isnull(row[0]):
            continue
        word = row[0].lower().strip('.",')

            # we're lowercasing everything and also
            # stripping certain kinds of punctuation that
            # may be glued to the word without really
            # changing its meaning

        if len(word) < 2 and not word.isalpha():
            continue

            # we don't want to include punctuation marks in our vocabulary

        if word in translator:
            word = translator[word]

            # we correct ocr errors and convert to British spelling

        thesewords[word] = int(row[1])      # the raw count of this token in this document

    # increment document frequencies

    for w, count in thesewords.items():
        docfreqs[w] += 1
        doclength += count
        # note that these are document frequencies, so only increment by 1
        # not by the term frequency (count) in the document

    # also create a dictionary entry in termfreqs, where the key is
    # a docid, and the value is a Counter of term frequencies

    termfreqs[docid] = thesewords
    alldoclengths[docid] = doclength

# MAKE VOCABULARY OF 2500 MOST COMMON WORDS

vocab = docfreqs.most_common(2500)

with open('loc2_vocabulary.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('word\tdocfreq\n')
    for word, docfreq in vocab:
        f.write(word + '\t' + str(docfreq) + '\n')

vocabwords = [x[0] for x in vocab]

def truncate(freqs, wordlimit):
    text = []
    for k, v in freqs.items():
        text.extend([k] * v)
    random.shuffle(text)

    newfreqs = Counter()

    assert len(text) > wordlimit

    for w in text[0: wordlimit]:
        newfreqs[w] += 1

    return newfreqs

# MAKE A MATRIX OF TF-IDF VALUES

dictforpandas = dict()
tooshort = list()

for docid, wordfreqs in termfreqs.items():

    doclength = alldoclengths[docid]

    if doclength < 11000:
        tooshort.append(docid.replace(':', '+').replace('/', '='))
        continue
    elif doclength > 60000:
        wordfreqs = truncate(wordfreqs, 60000)

    termvector = np.zeros(2500)
    for idx, word in enumerate(vocabwords):
        if word in wordfreqs:
            termvector[idx] = wordfreqs[word]

    docid = docid.replace(':', '+').replace('/', '=')
    dictforpandas[docid] = termvector

outdf = pd.DataFrame.from_dict(newdict, orient = 'index', columns = vocabwords)

scaler = StandardScaler()
scaler.fit(outdf)

scaled_features = scaler.transform(outdf)

outdf = pd.DataFrame(scaled_features, index = outdf.index, columns = outdf.columns)

outdf.to_csv('delta_matrix_loc2.tsv', sep = '\t', index_label = 'docid')

# meta = meta.set_index('docid')
outmeta = meta.drop(tooshort)
outmeta.to_csv('filtered_meta_4loc2.tsv', sep = '\t', index_label = 'docid')

