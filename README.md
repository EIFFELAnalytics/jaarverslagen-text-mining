# Jaarverslagen text mining
Text mining techniques, as [tf-idf](https://en.wikipedia.org/wiki/tf-idf), are used to extract the most important words from a PDF jaarverslag.

The output is, for each jaarverslag:
* A csv with all the unique words from the document, their count, term frequency (`tf`), document count and term frequency-inverse document frequency (`tf-idf`),

TODO: Currently PDF to text converting is not working for me (well) on Windows. Use a website for this (Google) and store the txt files in jaarverslag/en/ or /nl/.
