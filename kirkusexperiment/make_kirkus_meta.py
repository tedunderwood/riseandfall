import pandas as pd

meta = pd.read_csv('mallet80metadata4experiment2.tsv', sep = '\t')

volume = pd.read_csv('/Users/tunder/Dropbox/python/noveltmmeta/metadata/volumemeta.tsv', sep = '\t', low_memory = False, index_col = 'docid')

dates = []

for docid in meta.docid:
    if docid not in volume.index:
        docid = docid.replace('.$b', '.b')
    if docid not in volume.index:
        docid = docid.replace('.b', '.$b')
    if docid not in volume.index:
        print('error', docid)
        continue

    date = volume.at[docid, 'latestcomp']
    if pd.isnull(date):
        print('dateerror')
        sys.exit(0)
    else:
        dates.append(int(date))

meta['date'] = dates

meta = meta.loc[~meta.index.duplicated(keep='first')]

meta.to_csv('genremetadata4kirkusdeltas.tsv', sep = '\t', index = False)
