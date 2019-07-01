"""
Calculates term frequency-inverse document frequency from a collection of plain text files.
"""

#%%
import numpy as np
import pandas as pd
import re
from os.path import join
from os import listdir
try:
    from text_mining_1_file import calculate_tf, inspect_df
except ModuleNotFoundError:
    # Jupyter also needs the folder
    from src.text_mining_1_file import calculate_tf, inspect_df


#%%
def calculate_tf_folder(folder, output_folder=None, language=None):
    """Calculates term frequencies for all text files in a folder.

    Basically runs calculate_tf from module text_mining_1_file for all text 
    files it can find in `folder` and stores the output CSV's in output_folder.

    Also returns a dataframe of all appended output CSV's.

    """
    # Find all txt files in folder
    filenames = [f for f in sorted(listdir(folder)) if re.match('.+\.txt', f)]
    print('Number of files found:', len(filenames))

    # Initialize an empty dataframe and loop over all files
    df = pd.DataFrame()
    for filename in filenames:
        print('Processing:', filename)

        # Save in output folder or not?
        if output_folder is not None:
            output_file = join(output_folder, filename[:-4] + '.csv')
        else:
            output_file = None

        # Analyse the text file and calculate term frequency for each word
        df_1 = calculate_tf(
            join(folder, filename),
            output_file,
            language,
        )
        
        # Append to totals dataframe
        df = df.append(df_1)

    return df


def read_tf_csv_from_folder(folder):
    """Read all CSV's from a folder, append and return them and 1 dataframe."""
    # Find all CSV files in `folder`
    filenames = [f for f in sorted(listdir(folder)) if re.match('.+\.csv', f)]
    print('Number of files found:', len(filenames))

    # Initialize dataframe and read each CSV
    df = pd.DataFrame()
    for filename in filenames:
        # Read 1
        df_1 = pd.read_csv(join(folder, filename))
        
        # Add the filename as a colmun
        df_1['filename'] = filename
        
        # Append to totals dataframe
        df = df.append(df_1)
    
    return df


# Calculate idf from a dataframe with
# * filename
# * word
# * term frequency
def calculate_idf(df):
    # N: total number of documents
    N = len(set(df['filename']))

    # Group by word and count the occurence of filename
    idf = (df.groupby(by='word', as_index=False)['filename']
            .count()
            .rename(columns={'filename': 'document_count'})
            .set_index('word')
        )

    # Calculate idf from the document count
    # See formula: https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Inverse_document_frequency_2
    idf['idf'] = np.log(N/idf['document_count'])
    return idf


#%%
if __name__ == '__main__':
    # Calculate tf for each document
    # This step be skipped if the text files haven't changed
    calculate_tf_folder('data/nl/plain-text/', 'data/nl/tf/', 'dutch')

    # Read the pre-calculated tf's
    df = read_tf_csv_from_folder('data/nl/tf/')

    # Calculate idf's for each word in the entire corpus of documents
    idf = calculate_idf(df)

    # Join idf's with the tf's
    df = df.merge(idf, how='left', left_on='word', right_index=True)

    # Multiply tf * idf = tf-idf
    df['tf-idf'] = df['tf'] * df['idf']

    # Split and save as individual CSVs
    for filename in set(df['filename']):
        (
            df[df['filename'] == filename]
            .drop(columns='filename')
            .sort_values(by='tf-idf', ascending=False)
            .to_csv(join('data/nl/tf-idf', filename), index=False)
        )

    # Also save as 1 large CSV
    df.to_csv('data/nl/tf-idf/Alle_jaarverslagen.csv')
    inspect_df(df)
