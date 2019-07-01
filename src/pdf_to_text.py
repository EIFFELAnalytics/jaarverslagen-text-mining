import glob
import re
import subprocess
import os
from os.path import join
import time


def pdf_to_text(pdf_filename, txt_filename):
    """Converts PDF to plain text.
    
    Use my docker container (https://hub.docker.com/r/arjobsen/pdftotext)
    which executes pdftotext from poppler-utils.

    """
    with open(pdf_filename, 'r') as input:
        with open(txt_filename, 'w') as output:
            subprocess.run(
                'docker run --rm -i arjobsen/pdftotext',
                stdin=input,
                stdout=output
            )
    return 0


def derive_txt_filename(pdf_filename):
    # Split by the OS path separator
    path_and_filename = pdf_filename.split(os.sep)
    # Translate ./jaarverslagen/NL/input.pdf to ./data/NL/plain-text/output.txt
    return join(
        'data',
        path_and_filename[1],
        'plain-text',
        re.sub(r'\.pdf', '.txt', path_and_filename[-1])
    )


if __name__ == "__main__":
    # Set the timer
    t0 = time.time()

    # Find all PDF files in jaarverslagen
    pdfs = glob.glob('jaarverslagen/**/*.pdf', recursive=True)
    for pdf in pdfs:
        # Derive the path and filename of output.txt
        txt = derive_txt_filename(pdf)
        # Show
        print(pdf, '\n>', txt)
        # Convert pdf to text. This saves the file to disk immediately
        pdf_to_text(pdf, txt)

    # Stop the timer
    print('Done in %.1f seconds' % (time.time() - t0))
