# Jaarverslagen text mining
Dit script prepareert jaarverslagen van bedrijven en organisaties (PDF) om ze in een wordcloud (Power BI) te visualiseren.

Term-frequency en [tf-idf](https://en.wikipedia.org/wiki/tf-idf) worden berekend. Irrelevante woorden (bekende [stopwoorden](https://www.nltk.org/book/ch02.html#wordlist-corpora) en woorden die slechts 1 keer voorkomen) worden niet meegenomen in de tellingen.


## Gebruik
Zet de PDF jaarverslagen in data/jaarverslagen (maak deze folder aan als het nog niet bestaat). Engelse en Nederlandse jaarverslagen zijn toegestaan.

Zorg dat docker aanstaat en draai de volgende commando's:  

1. `python pdf_to_text.py` Converteert alle PDF's naar txt's.
1. `python count_words.py` Telt de woorden van alle txt's en slaat ze op in csv's.
1. `python prepare_for_sharepoint.py` Combineert alle csv's in 1 grote csv Alle_jaarverslagen.csv - Die kan opgeslagen worden op [SharePoint](https://eiffelnl.sharepoint.com/sites/eif-finance-brainstorm) via Teams.

Het Power BI dashboard Wordcloud_jaarverslagen.pbix haalt de dataset van SharePoint.
