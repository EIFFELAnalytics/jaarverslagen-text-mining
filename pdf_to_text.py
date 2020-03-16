"""Convert pdf to plain text.

Uses https://hub.docker.com/r/arjobsen/pdftotext so make sure docker is running.

Encoding (-enc) values: Latin1, UTF-8, ASCII7
See https://linux.die.net/man/5/xpdfrc

"""

import subprocess


def pdf_to_text(input_pdf, output_txt=None):
    # Convert input.pdf to output.txt or return as string
    with open(input_pdf, "r") as file_in:
        if output_txt:
            # Write to text file
            with open(output_txt, "w") as file_out:
                CompletedProcess = subprocess.run(
                    "docker run --rm -i arjobsen/pdftotext -enc ASCII7",
                    stdin=file_in,
                    stdout=file_out,
                )
                print(input_pdf, "converted to\n", output_txt)
        else:
            # Capture output and return as a string
            CompletedProcess = subprocess.run(
                "docker run --rm -i arjobsen/pdftotext -enc ASCII7",
                stdin=file_in,
                capture_output=True,
                encoding="ascii",
            )
            print(input_pdf, "converted to text:", CompletedProcess.stdout[:20], "...")

    # Check for errors in docker container
    if CompletedProcess.returncode != 0:
        # Note: this doesn't show docker-not-running errors
        raise Exception(CompletedProcess.stderr)

    return CompletedProcess.stdout


if __name__ == "__main__":
    # Press F5 to run this test
    test_input = "data/jaarverslagen/2018_Philips.pdf"
    test_output = "data/plain-txt/2018_Philips.txt"
    s = pdf_to_text(test_input, test_output)
    print(s)
