"""Convert pdf to plain text.

This uses https://hub.docker.com/r/arjobsen/pdftotext so make sure docker is running. The container 
uses pdftotext from poppler-utils.

Valid encoding (-enc) arguments are: Latin1, UTF-8, ASCII7. See https://linux.die.net/man/5/xpdfrc.
For all other arguments see https://www.mankier.com/1/pdftotext.

"""

import subprocess
import os


def pdf_to_text(input_pdf, output_txt):
    # Convert input.pdf to output.txt
    with open(input_pdf, "r") as file_in:
        with open(output_txt, "w") as file_out:
            subprocess.run(
                # Run a container, attach stdin stdout and optionally give pdftotext arguments
                "docker run --rm -i arjobsen/pdftotext -enc ASCII7",
                shell=True,
                # Pass the files from the host to the container
                stdin=file_in,
                stdout=file_out,
                text=True,
                check=True,
            )


if __name__ == "__main__":
    # Press F5 (Visual Studio Code) to convert all jaarverslagen to text
    input_folder = "data/jaarverslagen"
    output_folder = "data/plain-txt"
    for pdf in os.listdir(input_folder):
        txt = pdf[:-4] + ".txt"
        pdf_to_text(os.path.join(input_folder, pdf), os.path.join(output_folder, txt))
        print(f"{pdf} converted to {txt}")

        # For testing, create a breakpoint here
        pass
