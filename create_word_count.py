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


def create_word_count(pdf_input, csv_output):
    # First extract text from pdf
    text = pdf_to_text(pdf_input)

    # Text processing
    words = process_text(text)

    # Language detection
    language = detect_language(words)

    # Count words
    wc = count_words(words)

    # Select some words, such as no stopwords and only >1 occurences
    wc = select_words(wc, language)

    # Save as CSV
    wc.to_csv(csv_output, index=True)
    print("Word count saved as:", csv_output)


if __name__ == "__main__":
    # Constants for debugging
    PDF_INPUT = "data/jaarverslagen/2017_MN.pdf"
    CSV_OUTPUT = "data/word-counts/2017_MN.csv"

    # Get CLI arguments if ran through CLI else use debug constants
    pdf_input = sys.argv[1] if len(sys.argv) > 1 else PDF_INPUT
    csv_output = sys.argv[2] if len(sys.argv) > 2 else CSV_OUTPUT

    # Run the process
    create_word_count(pdf_input, csv_output)
