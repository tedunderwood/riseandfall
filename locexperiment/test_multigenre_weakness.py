import pandas as pd
import csv

weirdvols = pd.read_csv('taggedparts/all2remove.tsv', sep = '\t')
weirdvols = set(weirdvols.loc[weirdvols.remove != 'n', 'docid'])
print(len(weirdvols))

# LOAD vectors

existingdocids = set()

# The first column is docid, the rest are floats
# for a particular word, scaled by idf.

with open('delta_matrix_loc2.tsv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        if fields[0] == 'docid':
            continue   # that's the header
        existingdocids.add(fields[0])

numgenresfordoc = dict()

with open('filtered_meta_4loc2.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        r = row['remove']
        if len(r) > 1:
            print(r)
            continue

        docid = row['docid']
        if docid in weirdvols:
            continue

        if docid not in existingdocids:
            docid = docid.replace('.$b', '.b')
            if docid not in existingdocids:
                print('skip')
                continue

        genrestring = row['exp_genres']
        genreset = genrestring.split('|')

        numgenresfordoc[docid] = len(genreset)

results = pd.read_csv('annotated_loc2_delta_results3.tsv', sep = '\t')

errors = 0

outrows = []

enrichedrows = []

for idx, row in results.iterrows():
    docA = row['firstdoc']
    docB = row['genrematch']

    if docA not in numgenresfordoc or docB not in numgenresfordoc:
        errors += 1
        continue

    numgenres = numgenresfordoc[docA] + numgenresfordoc[docB]

    randdiff = row['fullrandomdist'] - row['ingenredist']
    otherdiff = row['othergenredist'] - row['ingenredist']

    outrows.append([numgenres, randdiff, otherdiff, row['meandate'], row['ingenredist']])

    row['numgenres'] = numgenres

    enrichedrows.append(row)

print(errors)

with open('multigenre_weakness.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('numgenres\tranddiff\totherdiff\tmeandate\tingenredist\n')
    for o in outrows:
        f.write('\t'.join([str(x) for x in o]) + '\n')

enriched = pd.DataFrame(enrichedrows)

enriched.to_csv('enriched_results.tsv', sep = '\t', index = False)

