"""Count term frequencies of words in a text file.

Note(!) It drops all words for which count = 1 to save disk space and speed up
processing.

"""

import re
from nltk import word_tokenize
from unicodedata import normalize


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
    print("Text processed to words:", words[:10])
    return words


if __name__ == "__main__":
    # Just run a test
    from pdf_to_text import pdf_to_text

    text = pdf_to_text("data/jaarverslagen/2018_Philips.pdf")
    # print(text)
    words = process_text(text)
    # print(words)
