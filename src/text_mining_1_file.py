"""Text mining process of 1 file.

Calculates the word term frequency from a plain text file and stores the
results in a CSV.

"""

#%%
from os.path import join
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import time


#%%
def count_words(words: list) -> pd.DataFrame:
    """Returns all unique words, counts and term frequency."""
    
    # Set up a dataframe with the counts
    df = (pd.Series(words).value_counts()
    .reset_index()
    .rename(columns={'index': 'word', 0: 'count'})
    .set_index('word')
    )

    # Calculate term frequency
    df['tf'] = df['count'] / df['count'].sum()
    return df


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
    with open(input_filename, 'r', encoding='utf-8') as f:
        text = f.read()
 
    # Tokenize with the Natural Language Toolkit (nltk)
    words = word_tokenize(text)

    # Convert all to lowercase
    words = [w.lower() for w in words]

    # Remove punctuation
    words = [re.sub('[^A-Za-z]', '', w) for w in words]
    words = list(filter(None, words))

    # TODO: Stemming and/or lemmatization

    # Get word counts and term frequencies
    df = count_words(words)

    # Remove stopwords now. This is way faster than looping through all words
    # because I can use set difference.
    no_stopwords = set(df.index) - set(stopwords.words(language))
    df = df.loc[no_stopwords]

    # Sort
    df.sort_values(by='tf', ascending=False, inplace=True)
    
    # Optionally save as output_file
    if output_filename is not None:
        # TODO: makedirs
        df.to_csv(output_filename)

    return df

#%%
if __name__ == "__main__":
    # Parameters
    input_filename = 'data/en/plain-text/2017_Philips.txt'
    output_filename = 'data/en/tf/2017_Philips.csv'
    language = 'english'

    # Set the timer
    t0 = time.time()
    
    # Run with save
    df = calculate_tf(input_filename, output_filename, language='english')
    
    # Run without save
    #df = calculate_tf(input_filename, 'english')
    
    # Inspect
    inspect_df(df)

    # Stop the timer
    print('Done in %.1f seconds' % (time.time() - t0))

