"""Pdf to text.

Converts all pdf files in jaarverslagen/en and jaarverslagen/nl to plain text
files and saves these in data/en/plain-text and data/nl/plain-text.

Make sure to launch docker before running this script.

"""
import glob
import re
import subprocess
import os
from os.path import join
import time
from functools import wraps


def pdf_to_text(pdf_filename, txt_filename):
    """Convert a PDF to plain text.

    This function uses my docker container from
    https://hub.docker.com/r/arjobsen/pdftotext which executes pdftotext from
    poppler-utils.

    """
    with open(pdf_filename, 'r') as input:
        with open(txt_filename, 'w') as output:
            # TODO: Catch docker errors. Or with CompletedProcess return?
            subprocess.run(
                'docker run --rm -i arjobsen/pdftotext',
                stdin=input,
                stdout=output
            )
    return 0


def derive_txt_filename(pdf_filename):
    # Split by the OS path separator
    filename_parts = pdf_filename.split(os.sep)
    # Translate ./jaarverslagen/*/input.pdf to ./data/*/plain-text/output.txt
    return join(
        'data',
        filename_parts[1],
        'plain-text',
        re.sub(r'\.pdf', '.txt', filename_parts[-1])
    )


def stopwatch(func):
    """Decorator which times the duration of the function it wraps."""
    @wraps(func)
    def inner(*args, **kwargs):
        t0 = time.time()
        func(*args, **kwargs)
        print('Done in %.1f seconds' % (time.time() - t0))
    return inner


@stopwatch
def main():
    # List all pdf's in jaarverslagen
    pdfs = glob.glob('jaarverslagen/**/*.pdf', recursive=True)
    txts = list(map(derive_txt_filename, pdfs))

    for pdf, txt in zip(pdfs, txts):
        print(pdf, '\n>', txt)
        # Convert the pdf to text. This saves the file to disk immediately
        pdf_to_text(pdf, txt)
        # break  # <- Useful breakpoint for debugging


if __name__ == "__main__":
    main()
