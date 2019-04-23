# Jaarverslagen text mining
Text mining techniques, as [tf-idf](https://en.wikipedia.org/wiki/tf-idf), are used to extract the most important words from a PDF jaarverslag.

The results are, for each jaarverslag:
* A csv file with all the unique words from the document, their raw count, term frequency (`tf`), document count and term frequency-inverse document frequency (`tf-idf`),

## Pdf to text
Converting PDF to plain text currently isn't working out for me on Windows. Better just find a online converter or use pdftotext from [poppler-utils](https://manpages.debian.org/jessie/poppler-utils/pdftotext.1.en.html) on Linux. 
