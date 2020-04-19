"""Count term frequencies of words in a text file.

Note(!) It drops all words for which count = 1 to save disk space and speed up
processing.

"""

import pandas as pd
import os
from os.path import join
import re
from nltk.corpus import stopwords


def process_text(text):
    text = text.lower()
    text = re.sub(r"\W", " ", text)
    # TODO: Stemming or lemmatization
    return text


def count_words(words: list) -> pd.DataFrame:
    # Set up a dataframe with the counts
    df = (
        pd.Series(words)
        .value_counts()
        .reset_index()
        .rename(columns={"index": "word", 0: "count"})
        .set_index("word")
    )

    # Also calculate term frequency
    df["tf"] = df["count"] / df["count"].sum()
    return df


if __name__ == "__main__":
    # Press F5 (Visual Studio Code) to count words in all text files
    input_folder = "data/plain-txt"
    output_folder = "data/word-counts"
    for txt in os.listdir(input_folder):
        # Read the text file
        with open(join(input_folder, txt), "r", encoding="ascii") as f:
            text = f.read()

        # Process text
        text = process_text(text)

        # Split text into words
        words = text.split()
        print(
            f"Words found: {len(words)} - Unique words found: {len(set(words))} - ",
            end="",
        )

        # Count
        counts = count_words(words)

        # Drop irrelevant words - do this after count because it's faster
        counts = counts[counts["count"] > 1]
        not_a_stopword = (
            set(counts.index)
            - set(stopwords.words("English"))
            - set(stopwords.words("Dutch"))
        )
        counts = counts.loc[not_a_stopword]

        # Sort
        counts.sort_values(by="count", ascending=False, inplace=True)
        print("Top 5 words: ", counts.head().index.to_list())

        # Save to disk
        csv = txt[:-4] + ".csv"
        counts.to_csv(join(output_folder, csv))
        print(f"{txt} word counts stored in {csv}")

        # For testing, create a breakpoint here
        pass
