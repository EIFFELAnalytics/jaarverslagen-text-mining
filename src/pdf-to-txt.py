#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'src'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # PDF to text
# Part of project "Text mining jaarverslagen".
# 
# Use the kernel `tmj` which I've made in the virtual environment `~/venv/tmj`. This environment holds all the needed packages and so I can manage them without interfering with the system Python installation or other Python projects.

#%%
from os.path import join
import re


#%%
# Parameters
filename = 'AEGON_2017.pdf'
folder = '../jaarverslagen'
filename_no_extension = re.search('(.*)\.pdf', filename).group(1)
output_folder = join('../output', filename_no_extension)


#%%
# Parameters
filename = "Heineken_2017.pdf"
folder = "../jaarverslagen"
filename_no_extension = "Heineken_2017"
output_folder = "../output/Heineken_2017"


#%%
# Extract text (as bytes) from pdf
import textract
text = textract.process(join(folder, filename))
print(text.hex()[:100], '...\n')

# Textract encodes as UTF-8, so decode back to text before proceding
text = text.decode('utf-8')
print(text[:100], '...')

#%% [markdown]
# Maybe decompose to get rid of the accents? Nah

#%%
# Save as text
save_as = join(output_folder, filename_no_extension + '.txt')
with open(save_as, 'w+') as file:
    file.write(text)

print('Saved as:', save_as)


