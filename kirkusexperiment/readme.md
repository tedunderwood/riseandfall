Experiment on a topic model of Kirkus Reviews
=============================================

The files here were used to measure the coherence of groups of books associated with a single "genre-like" topic in a model of book reviews from *Kirkus Reviews.*

Results of the topic model
--------------------------

For the code used to produce the topic model, see [https://github.com/Yuerong2/Kirkus_topic_modeling](https://github.com/Yuerong2/Kirkus_topic_modeling)

Some of the relevant output here:

**genre_80_mallet_categories_for_20c_exp.csv** lists all eighty topics from the model, with additional labels in the ```possible_genres``` column where we decided the topic was "genre-like."

**genremetadata4kirkusdeltas.tsv** has genre categories for all volumes actually used in the experiment; these are volumes with genre-like topics.

**random_metadata_4kirkus.tsv** is a random sample of volumes to provide a fully-random baseline.

Code used in the experiment
---------------------------

**make_kirkus_deltas.py** creates normalized word vectors to be used in subsequent stages of processing. We refer to those vectors as "deltas" not because they reflect a change, but because they're standardized using Burrows' Delta. For the rationale guiding that choice, see

    S. Evert, T. Proisl, F. Jannidis, I. Reger, S. Pielstr ̈om, C. Sch ̈och, T. Vitt, Understandingand  explaining  Delta  measures  for  authorship  attribution,   Digital  Scholarship  in  theHumanities 31 (2017).

You will not be able to run **make_kirkus_deltas.py**, as it stands, on your own machine, because it points to extracted-feature files downloaded from HathiTrust Research Center. Those files are too bulky to include in a git repo; so is the matrix of word vectors *produced* by this script. To reproduce our process entirely from scratch, you could download the extracted-feature files from HTRC and edit the script to point to them. Alternatively, here's a Dropbox link to the matrix of vectors we produced: https://www.dropbox.com/s/pknr0co37pzmaax/delta_matrix_4kirkus.tsv?dl=0

**measure_kirkus_distances.py** is arguably the central script for this experiment; it actually does the random selection of pairs of books and measures distances.

Results of the experiment
-------------------------

The central file here is **kirkus_delta_results_uncut.tsv**. Again, "delta" just specifies that vectors were standardized with Burrows' delta. "Uncut" is a modifier we added to mean, essentially, "latest version of."

Most of the columns are self-explanatory, but note that the "difference" columns ```fullrandomdiff``` and ```othergenrediff```, which might look like results to be visualized, *are not actually used.* Instead, in the visualization scripts, we use a Fishers z-transform on the cosine distances before subtracting them.

visualization
--------------

This subfolder has R scripts used for visualization, and the jpgs they produced.

