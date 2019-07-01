"""Text mining process to calculate term frequency-inverse document frequency.

This module builds on text_mining_tf.py and requires CSV files with term
frequencies in ./data/*/tf/. These files are read and used to calculate tf-idf
for the whole corpus (language specific).

"""

import numpy as np
import pandas as pd
import re
from os import listdir
from os.path import join, isdir, basename
import os
import glob
from pdf_to_text import stopwatch
from text_mining_tf import inspect_df


def read_and_append_csvs(csvs):
    """Read a bunch of CSV's, append and return them as 1 dataframe."""

    # Initialize an empty list and read each CSV
    li = []
    for csv in csvs:
        # Read 1
        print('Reading:', csv)
        df_1 = pd.read_csv(csv)

        # Add the filename as a colmun
        df_1['filename'] = basename(csv)

        # Append to list
        li.append(df_1)

    df = pd.concat(li, axis=0, ignore_index=True)
    return df


def calculate_idf(df):
    """Calculate idf from a dataframe with the following columns:
    * filename
    * word
    * term frequency

    """
    # N: total number of documents
    N = len(set(df['filename']))

    # Group by word and count the number of documents
    idf = (
        df.groupby(by='word', as_index=False).size()
        .reset_index(name='document_count')
        .set_index('word')
    )

    # Calculate idf from the document count. Formula:
    # https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Inverse_document_frequency_2
    idf['idf'] = np.log(N/idf['document_count'])
    return idf


@stopwatch
def main():
    # Search ./data/ for the different corpora (en/nl) we have to deal with
    corpora = [d for d in listdir('./data/') if isdir(join('./data', d))]

    li = []
    for corpus in corpora:
        # Read all CSV's in ./data/*/tf/
        csvs = glob.glob(join('data', corpus, 'tf', '*.csv'))
        tfs_corpus = read_and_append_csvs(csvs)

        idf = calculate_idf(tfs_corpus)

        # Join idf's with the tf's dataframe
        tfs_corpus = tfs_corpus.merge(
            idf,
            how='left',
            left_on='word',
            right_index=True
        )

        # Multiply tf * idf = tf-idf
        tfs_corpus['tf-idf'] = tfs_corpus['tf'] * tfs_corpus['idf']

        tfs_corpus['corpus'] = corpus
        li.append(tfs_corpus)

    # Concat to 1 large dataframe
    df = pd.concat(li, axis=0, ignore_index=True)
    df.to_csv('data/Alle_jaarverslagen.csv', index=False)
    inspect_df(df)


if __name__ == "__main__":
    main()
