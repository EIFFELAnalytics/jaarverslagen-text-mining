
# See https://automatetheboringstuff.com/chapter13/
import PyPDF2
pdf_file_obj = open('jaarverslagen/nl/Kramp_2017.pdf', 'rb')
reader = PyPDF2.PdfFileReader(pdf_file_obj)

# Run through all pages
plain_text = ''
print('Number of pages:', reader.numPages)
for page in range(reader.numPages):

    # Read 1 page and append to all text
    page_obj = reader.getPage(page)
    plain_text += page_obj.extractText()

# Close
pdf_file_obj.close()

# Encode as UTF-8
#plain_text = plain_text.encode('utf-8')

# Verbose
print('Length of text (characters):', len(plain_text))
print('First 100 characters:\n', plain_text[:100])

# Save as
with open('jaarverslagen/plain-text/nl/Kramp_2017.txt', 'w+', encoding='utf-8') as file:
    file.write(plain_text)
