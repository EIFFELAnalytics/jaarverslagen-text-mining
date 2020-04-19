"""Prepare for upload to SharePoint/Teams.

Combine all CSV files with the word counts. 

Also add tf-idf. See: https://en.wikipedia.org/wiki/tf-idf

"""

import numpy as np
import pandas as pd
from os.path import join, basename
import glob


def read_from_folder(folder):
    # Read all CSV's in folder - ** means also find files in subfolders
    csvs = glob.glob(join(folder, "**.csv"))

    # Initialize an empty list and read each CSV
    li = []
    for csv in csvs:
        # Read 1
        print("Reading:", csv)
        df_1 = pd.read_csv(csv)

        # Add the filename as a column
        df_1["filename"] = basename(csv)

        # Append to list
        li.append(df_1)

    # Concat all df's into 1 big one
    df = pd.concat(li, ignore_index=True)
    return df


def calculate_idf(df):
    """ df must have the following columns:
    * filename
    * word
    """
    # N: total number of documents
    N = len(set(df["filename"]))

    # Group by word and count the number of documents
    idf = (
        df.groupby(by="word", as_index=False)
        .size()
        .reset_index(name="document_count")
        .set_index("word")
    )

    # Calculate idf from the document count. Formula: https://en.wikipedia.org/wiki/tf-idf#Inverse_document_frequency_2
    idf["idf"] = np.log(N / idf["document_count"])
    return idf


if __name__ == "__main__":
    # Read and combine all CSVs
    df = read_from_folder("data/word-counts/")

    # Calculate idf for all words in this corpus
    idf = calculate_idf(df)

    # Join idf's with the tf's dataframe
    df = df.merge(idf, how="left", left_on="word", right_index=True)

    # Multiply tf * idf = tf-idf
    df["tf-idf"] = df["tf"] * df["idf"]
    df["count-idf"] = round(df["count"] * df["idf"])

    # Save
    df.to_csv("data/Alle_jaarverslagen.csv", index=False)
    print("Saved in ./data/Alle_jaarverslagen.csv")
    print(df.shape)
    print(df.head())
