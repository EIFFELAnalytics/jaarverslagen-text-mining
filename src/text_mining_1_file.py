"""
Calculate word term-frequency from a plain text file.
"""

#%%
from os.path import join
import pandas as pd
import re

#%%
# Count a list of words
def count_words(words):
    
    # Set up a dataframe with the counts
    df = (pd.Series(words).value_counts()
     .reset_index()
     .rename(columns={'index': 'word', 0: 'count'})
     .set_index('word')
    )

    # Calculate term frequency
    df['tf'] = df['count'] / df['count'].sum()
    return df

# Inspect a dataframe
def inspect_df(df):
    print(df.shape)
    try:
        display(df.head(10))
    except NameError:
        print(df.head(10))

#%%
"""
Does some language specific word processing. Returns a dataframe with the tf's.
If optional output_file is supplied, the df is also saved.
"""
def calculate_tf(input_file, language, output_file=None):
    
    # Read from file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
 
    # Tokenize with the Natural Language Toolkit (nltk)
    from nltk import word_tokenize
    words = word_tokenize(text)

    # Convert all to lowercase
    words = [w.lower() for w in words]

    # Remove punctuation
    words = [re.sub('[^A-Za-z]', '', w) for w in words]
    words = list(filter(None, words))

    # Remove stopwords
    from nltk.corpus import stopwords
    words = [w for w in words if w not in stopwords.words(language)]

    # TODO: Stemming and/or lemmatization

    # Calculate term-frequencies
    df = count_words(words)
    
    # Save if output file
    if output_file is not None:
        # TODO: makedirs
        df.to_csv(output_file)

    return df

#%%
# Press F5 to run
if __name__ == "__main__":

    # Parameters
    filename = '2017_Ten_Cate.txt'
    folder = 'data/en/plain-text/'
    language = 'english'
    output_folder = 'data/en/tf/'
    filename_no_extension = re.match('(.+)\.txt', filename).group(1)
    
    # Run with save
    #df = calculate_tf(join(folder, filename), 'English', join(output_folder, filename_no_extension + '.csv'))
    
    # Run without save
    df = calculate_tf(join(folder, filename), 'English', None)
    
    # Inspect
    inspect_df(df)

