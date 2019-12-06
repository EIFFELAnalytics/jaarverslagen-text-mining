"""Text mining term frequencies.

Calculates the word term frequency from a plain text file and stores the
results in a CSV.

Note(!) It drops all words for which count = 1 to save disk space and speed up
processing.

"""
import os
from os.path import join
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import glob
from pdf_to_text import stopwatch


def inspect_df(df):
    print(df.shape)
    try:
        display(df.head(10))
    except NameError:
        print(df.head(10))


def calculate_tf(input_filename, output_filename=None, language=None):
    """Calculates term-frequency of an input txt file. It does some language
    specific word processing. It returns a dataframe with the tf's and
    optionally stores that df in output_file.

    Args:
        input_filename: Path and filename of input text file.
        output_filename (optional): Path and filename of output CSV. If None,
        the output will not be saved.
        language (optional): Removes language specific stopwords. If None,
        stopwords from all languages will be removed.

    """

    # Read from file
    with open(input_filename, "r", encoding="utf-8") as f:
        text = f.read()

    # Tokenize with the Natural Language Toolkit (nltk)
    words = word_tokenize(text)

    # Convert all to lowercase
    words = [w.lower() for w in words]

    # Remove punctuation
    words = [re.sub("[^A-Za-z]", "", w) for w in words]
    words = list(filter(None, words))

    # TODO: Stemming and/or lemmatization

    # Get word counts and term frequencies
    df = count_words(words)

    # Remove stopwords now. Do this after counting because it's way faster.
    no_stopwords = set(df.index) - set(stopwords.words(language))
    df = df.loc[no_stopwords]

    # Sort
    df.sort_values(by="tf", ascending=False, inplace=True)

    # Optionally save as output_file
    if output_filename is not None:
        # TODO: makedirs
        df.to_csv(output_filename, index=True)

    return df


def count_words(words: list) -> pd.DataFrame:
    """Returns all unique words, counts and term frequency."""

    # Set up a dataframe with the counts
    df = (
        pd.Series(words)
        .value_counts()
        .reset_index()
        .rename(columns={"index": "word", 0: "count"})
        .set_index("word")
    )

    # Drop all words which only occur once (!)
    df = df[df["count"] > 1]

    # Calculate term frequency
    df["tf"] = df["count"] / df["count"].sum()
    return df


def derive_csv_filename(txt_filename):
    """Translate ./data/*/plain-text/input.txt to ./data/*/tf/output.csv"""
    first = re.sub(r"plain\-text", "tf", txt_filename)
    second = re.sub(r"\.txt", ".csv", first)
    return second


def extract_language(filename):
    """Extract language (en/nl) from ./data/*/..."""
    # Mapping dictionary
    map = {"en": "English", "nl": "Dutch"}
    return map[filename.split(os.sep)[1]]


@stopwatch
def main():
    # Search ./data/*/plain-text/ for txt files
    txts = glob.glob("data/*/plain-text/*.txt")

    # Derive corresponding output CSV filenames and languages
    csvs = list(map(derive_csv_filename, txts))
    languages = list(map(extract_language, txts))

    # Run with save
    for txt, csv, language in zip(txts, csvs, languages):
        print(txt, "\n>", csv)
        # Calculate term frequency for each text file
        calculate_tf(txt, csv, language)


if __name__ == "__main__":
    main()
