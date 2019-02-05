# Jaarverslagen text mining
Text mining techniques, as [TF-IDF](https://en.wikipedia.org/wiki/tf-idf), are used to extract the most important words from a PDF jaarverslag.

The output is, for each jaarverslag:
* a CSV with all the unique words from the document, their count, term frequency (`tf`), document count and term frequency-inverse document frequency (`tf-idf`),
* and an image of a word cloud.

Sometimes output can be generated for in-between steps. See the filename (of the CSV and the image) for which text mining step that output belongs to.

## Notebook setup
You'll find all notebooks in `./src`.

### File list preparation
Some text mining steps are language dependend. And the script is not able (yet) to determine the language of the jaarverslag. So this should be done with the help of a human.

Run `prepare_file_list.ipynb`. This will view the files in the input folder and create a CSV with a list of all found jaarverslagen. Now you should open that list (e.g. in Excel) and fill in the `language` column with `english` or `dutch`.

Note: the script won't remove already known values.

### The runbook
The main notebook to use is the runbook. It will read the file list and loop over the text mining steps by calling other notebooks. It uses `papermill` for that.