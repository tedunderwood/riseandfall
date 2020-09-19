import pandas as pd
import glob

paths = glob.glob('taggedparts/*4*.tsv')
print(paths)

toremove = set()
taggedby = dict()

for p in paths:
    name = p.split('4')[1].replace('.tsv', '')
    print(name)
    df = pd.read_csv(p, sep = '\t', index_col = 'docid')
    for idx, row in df.iterrows():
        if not pd.isnull(row.remove) and row.remove.lower().startswith('y'):
            toremove.add(idx)
            if idx not in taggedby:
                taggedby[idx] = []
            taggedby[idx].append(name)

print(toremove)
meta = pd.read_csv('filtered_meta_4loc2.tsv', sep = '\t', index_col = 'docid')

weirdones = meta.loc[toremove, : ]

def concat_tags(idx):
    global taggedby
    return ' | '.join(taggedby[idx])

weirdones = weirdones.assign(taggedby = weirdones.index.map(concat_tags))

weirdones.to_csv('taggedparts/all2remove.tsv', sep = '\t', index_label = 'docid')
