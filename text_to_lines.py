"""Calculate word counts for 1 pdf file. The counts are then saved as a csv file.

Run with the following command:
$ python create_word_count.py [pdf_input] [csv_output]
Example:
$ python create_word_count.py data/jaarverslagen/MN_2017.pdf data/wount-counts/MN_2017.csv

Or import create_word_count from another script an run as a function.

"""

import sys
from pdf_to_text import pdf_to_text
from process_text import process_text
from count_words import count_words
from select_words import select_words, detect_language
import re
import pandas as pd
from unicodedata import normalize
from nltk.corpus import stopwords


def remove_stopwords(line):
    # Remove stopwords
    words = [w for w in line.split() if w not in stopwords.words('Dutch')]
    line = " ".join(words)
    return line


def process_line(text):
    # Convert to lowercase
    text = text.lower()

    # UTF-8 to ASCII (ë to e)
    text = normalize("NFD", text)
    text = text.encode("ascii", "ignore")
    text = text.decode("ascii")

    # Remove punctuation. Also replaces all whitespace with 1 space
    text = re.sub(r"[^A-z0-9]+", " ", text)

    # Remove stopwords
    text = remove_stopwords(text)


    # Tokenize with nltk
    #words = word_tokenize(text)

    # TODO: Stemming and/or lemmatization
    #print("Text processed to words:", words[:10])
    return text


def create_word_count(pdf_input, csv_output):
    # First extract text from pdf
    text = pdf_to_text(pdf_input)

    # Split on linebreaks
    lines = text.split("\n")

    # Replace all other whitespace with a single space
    lines = [process_line(line) for line in lines]


    df = pd.DataFrame(data=lines)

    df.to_csv(csv_output)

    print('E')
    


#if __name__ == "__main__":
    # Constants for debugging
    PDF_INPUT = "data/jaarverslagen/2017_MN.pdf"
    CSV_OUTPUT = "data/word-counts/2017_MN_text.csv"

    # Get CLI arguments if ran through CLI else use debug constants
    pdf_input = sys.argv[1] if len(sys.argv) > 1 else PDF_INPUT
    csv_output = sys.argv[2] if len(sys.argv) > 2 else CSV_OUTPUT

    # Run the process
    create_word_count(pdf_input, csv_output)


if __name__ == "__main__":
    TXT_INPUT = 'data/plain-txt/2018_Philips.txt'
    TXT_OUTPUT = 'data/2018_Philips_words.txt'

    with open(TXT_INPUT, 'r', encoding='ascii') as f:
        txt = f.read()

    txt = txt.lower()

    txt = re.sub('[^a-z\s]', '', txt)
    # Wat gebeurt hier met e-accent letters? Die worden dus weggegooit

    words = txt.split()

    words = '\n'.join(words)

    with open(TXT_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(words)

    print('Done')
