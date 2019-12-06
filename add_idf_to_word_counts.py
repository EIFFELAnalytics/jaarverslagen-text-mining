"""Add term frequency-inverse document frequency to existing word count csv files.

See: https://en.wikipedia.org/wiki/Tf-idf

"""

import numpy as np
import pandas as pd
from os.path import join, basename
import glob


# The folder to read the csv's from
FOLDER = "data/word-counts/"


def read_from_folder(folder):
    """Read a bunch of CSV's, append and return them as 1 dataframe."""

    # Read all CSV's in folder
    # ** means also find files in subfolders
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

    # Concat all df's into 1
    # Needs sort= to suppress warning
    df = pd.concat(li, axis=0, ignore_index=True, sort=False)
    return df


def calculate_idf(df):
    """Calculate idf from a dataframe with the following columns:
    * filename
    * word
    * term frequency

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

    # Calculate idf from the document count. Formula:
    # https://en.wikipedia.org/wiki/Tf-idf#Inverse_document_frequency_2
    idf["idf"] = np.log(N / idf["document_count"])
    return idf


if __name__ == "__main__":
    # Read and combine all CSVs
    df = read_from_folder(FOLDER)

    # Calculate idf for all words in this corpus
    idf = calculate_idf(df)

    # Join idf's with the tf's dataframe
    df = df.merge(idf, how="left", left_on="word", right_index=True)

    # Multiply tf * idf = tf-idf
    df["tf-idf"] = df["tf"] * df["idf"]

    # Save
    df.to_csv("data/Alle_jaarverslagen.csv", index=False)
    print("Saved in ./data/Alle_jaarverslagen.csv")
    print(df.shape)
    print(df.head())
