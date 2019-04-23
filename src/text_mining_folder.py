"""
Calculates term frequency-inverse document frequency from a collection of plain text files.
"""

#%%
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
# Calculate term frequencies of all text files in a folder
def calculate_tf_folder(folder, language, output_folder=None):
    
    # Find txt files
    filenames = [f for f in sorted(listdir(folder)) if re.match('.+\.txt', f)]
    print('Number of files found:', len(filenames))

    # Initialize dataframe and loop over all files
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
            language,
            output_file
        )
        
        # Append to totals dataframe
        df = df.append(df_1)

    return df

# Load the data from all TF files
def read_tf_csv_from_folder(folder):

    # Find all csv files
    filenames = [f for f in sorted(listdir(folder)) if re.match('.+\.csv', f)]
    print('Number of files found:', len(filenames))

    # Initialize dataframe and read each csv
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
import numpy as np
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
# Press F5 to run
if __name__ == '__main__':

    # Optional: (Re-)calculate tf for each document
    calculate_tf_folder('data/nl/plain-text/', 'Dutch', 'data/nl/tf/')

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
