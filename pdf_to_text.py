"""Convert pdf to plain text.

Uses https://hub.docker.com/r/arjobsen/pdftotext so make sure docker is running.

"""

import subprocess


def pdf_to_text(input_pdf, output_txt=None):
    # Convert input.pdf to output.txt or return as string
    with open(input_pdf, "r") as file_in:
        if output_txt:
            with open(output_txt, "w") as file_out:
                # Write to text file
                CompletedProcess = subprocess.run(
                    "docker run --rm -i arjobsen/pdftotext",
                    stdin=file_in,
                    stdout=file_out,
                )
                print(input_pdf, "converted to\n", output_txt)
        else:
            # Capture output and use encoding to return as a string
            CompletedProcess = subprocess.run(
                "docker run --rm -i arjobsen/pdftotext",
                stdin=file_in,
                capture_output=True,
                encoding="utf-8",
            )
            print(input_pdf, "converted to text:", CompletedProcess.stdout[:20], "...")

    # Check for errors
    if CompletedProcess.returncode != 0:
        raise Exception(CompletedProcess.stderr)

    return CompletedProcess.stdout


if __name__ == "__main__":
    # Press F5 to run this test
    # TODO later: Look into (unit) testing
    test_input = "data/jaarverslagen/2018_Philips.pdf"
    test_output = "data/plain-txt/2018_Philips.txt"
    s = pdf_to_text(test_input)  # , test_output)
    # print(s)
