"""Count term frequencies of words in a text file.

Note(!) It drops all words for which count = 1 to save disk space and speed up
processing.

"""

import pandas as pd
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from unicodedata import normalize


def count_term_freq(input_txt, output_csv=None):
    # Read text file
    with open(input_txt, "r", encoding="utf-8") as f:
        text = f.read()

    # Text processing and word separation
    words = process_text(text)

    # Detect language (Dutch or English)
    language = detect_language(words)

    # Get word counts and term frequencies
    df = count_words(words)

    # Now remove stopwords. Do this after counting because it's way faster!
    not_a_stopword = set(df.index) - set(stopwords.words(language))
    df = df.loc[not_a_stopword]

    # Sort
    df.sort_values(by="tf", ascending=False, inplace=True)

    # Optionally save as output_csv
    if output_csv is not None:
        # TODO: makedirs
        df.to_csv(output_csv, index=True)
        print("Saved as:", output_csv)


def process_text(text):
    # Convert to lowercase
    text = text.lower()

    # UTF-8 to ASCII (ë to e)
    text = normalize("NFD", text)
    text = text.encode("ascii", "ignore")
    text = text.decode("ascii")

    # Remove punctuation
    text = re.sub(r"[^A-z]", " ", text)

    # Tokenize with nltk
    words = word_tokenize(text)

    # TODO: Stemming and/or lemmatization

    return words


def count_words(words: list) -> pd.DataFrame:
    # Set up a dataframe with the counts
    df = (
        pd.Series(words)
        .value_counts()
        .reset_index()
        .rename(columns={"index": "word", 0: "count"})
        .set_index("word")
    )

    # Drop all words (is mostly garbage anyway) which only occur once (!)
    df = df[df["count"] > 1]

    # Calculate term frequency
    df["tf"] = df["count"] / df["count"].sum()
    return df


def detect_language(words):
    # Can be Dutch or English
    nl_stopwords = stopwords.words("Dutch")
    en_stopwords = stopwords.words("English")

    # Count all words from text recognized as NL or EN stopwords
    nl_words = len([w for w in words if w in nl_stopwords])
    en_words = len([w for w in words if w in en_stopwords])

    # Guess
    threshold = 2
    if nl_words > en_words * threshold:
        print("Language detected: Dutch")
        return "Dutch"
    elif en_words > nl_words * threshold:
        print("Language detected: English")
        return "English"
    else:
        raise Exception("Language not detected as Dutch nor English")


if __name__ == "__main__":
    # Just run a test
    count_term_freq(
        "data/plain-txt/2018_Philips.txt", "data/term-freq/2018_Philips.csv"
    )
