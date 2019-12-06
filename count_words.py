"""Count term frequencies of words in a text file.

Note(!) It drops all words for which count = 1 to save disk space and speed up
processing.

"""

import pandas as pd


def count_words(words: list) -> pd.DataFrame:
    # Set up a dataframe with the counts
    df = (
        pd.Series(words)
        .value_counts()
        .reset_index()
        .rename(columns={"index": "word", 0: "count"})
        .set_index("word")
    )

    # Calculate term frequency
    df["tf"] = df["count"] / df["count"].sum()

    # Sort
    df.sort_values(by="tf", ascending=False, inplace=True)
    print("Words counted. Top 5:", df.head().index.to_list())
    return df


if __name__ == "__main__":
    pass
