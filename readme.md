The rise and fall of genre differentiation in English-language fiction
======================================================================

[![DOI](https://zenodo.org/badge/296900027.svg)](https://zenodo.org/badge/latestdoi/296900027)

Code and metadata supporting a paper for Computational Humanities Research.

Authors: Aniruddha Sharma, Yuerong Hu, Peizhen Wu, Wenyi Shang, Shubhangi Singhal, and Ted Underwood.

This repository mostly contains metadata rather than raw word counts, etc. The raw data is also available, but it's mostly too large to fit in this repository, so we have pointed to it in a range of ways -- by providing ids that can be used to download HTRC extracted feature files, and links that can be used to download the vectors we produced from those files.

The code, metadata, and visualizations are divided into two directories that match the two experiments in the paper: **locexperiment** for the experiment based on Library of Congress genre and subject headings; **kirkusexperiment** for the experiment based on a topic model of book reviews from *Kirkus Reviews.*

The repository also makes available (in **kirkusreviewswordshuffled.tsv**) the texts of 19,000 short reviews of fiction scraped from *Kirkus Reviews*, paired with the volume IDs in HathiTrust for which they are reviews. Note that we have scrambled the word order of these reviews to avoid violating copyright.

