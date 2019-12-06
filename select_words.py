"""Count term frequencies of words in a text file.

Note(!) It drops all words for which count = 1 to save disk space and speed up
processing.

"""

import pandas as pd
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from unicodedata import normalize


def select_words(wc, language):
    # Drop all words (is mostly garbage anyway) which only occur once
    wc = wc[wc["count"] > 1]

    # Remove stopwords
    not_a_stopword = set(wc.index) - set(stopwords.words(language))
    wc = wc.loc[not_a_stopword]

    # Sort
    wc.sort_values(by="tf", ascending=False, inplace=True)
    print("Words selected. Top 5", wc.head().index.to_list())
    return wc


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
