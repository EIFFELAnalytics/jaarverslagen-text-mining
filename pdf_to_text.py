"""Convert pdf to plain text.

Uses https://hub.docker.com/r/arjobsen/pdftotext so make sure docker is running.

"""

import subprocess


def pdf_to_text(input_pdf, output_txt):
    # Convert input.pdf to output.txt
    with open(input_pdf, "r") as input:
        with open(output_txt, "w") as output:
            # TODO: Catch docker errors. Or with CompletedProcess return maybe?
            subprocess.run(
                "docker run --rm -i arjobsen/pdftotext", stdin=input, stdout=output
            )
    return 0


if __name__ == "__main__":
    # Run a test. TODO later: Look into (unit) testing
    test_input = "data/jaarverslagen/2018_Philips.pdf"
    test_output = "data/plain-txt/2018_Philips.txt"
    pdf_to_text(test_input, test_output)
