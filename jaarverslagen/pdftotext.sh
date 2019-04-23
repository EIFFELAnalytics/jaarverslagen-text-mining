#!/bin/bash
for f in ./en/*.pdf
do
	echo $f
	pdftotext $f
done
