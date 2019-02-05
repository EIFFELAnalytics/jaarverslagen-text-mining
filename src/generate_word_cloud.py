# Takes in a pandas Series with the words as Index and the frequencies as values
def generate_word_cloud(series):
    # Initialize the word cloud
    from wordcloud import WordCloud
    wc = WordCloud(
        font_path='/usr/share/fonts/gsfonts/NimbusSansNarrow-Bold.otf',\
        max_words=100,\
        background_color='white',\
        colormap='Blues',\
        margin=10
    )

    # Convert all to uppercase
    SERIES = series.copy()
    SERIES.index = SERIES.index.str.upper()

    # Create the word cloud
    wordcloud = wc.generate_from_frequencies(SERIES)
    
    # Show it
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    # Return the word cloud to maybe save it
    return wordcloud