# Jaarverslagen text mining
Text mining techniques, as stopword removal and [tf-idf](https://en.wikipedia.org/wiki/tf-idf), are used to extract the most important words from a PDF jaarverslag.

## Usage
Put English pdf files in the folder jaarverslagen/en and Dutch pdf files in jaarverslagen/nl. The script treats each language as an independent corpus with its own processing rules.

Execute the following scripts
```
python src/pdf_to_text.py
python src/text_mining_tf.py
python src/text_mining_tf-idf.py
```
Make sure docker is running to execute `pdf_to_text.py`.

The results (csv) of each jaarverslag is saved in data/en/tf and data/nl/tf. All these results, and the tf-idf of each word, are combined and saved in data/Alle_jaarverslagen.csv.
