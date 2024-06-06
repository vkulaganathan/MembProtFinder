# MembProtFinder
A tool to identify transmembrane proteins from a given list of gene or protein IDs.

<br></br>
**Usage**

``$ MembProtFinder.py [-h] --infile INFILE --infile-index-column INFILE_INDEX_COLUMN --givenIDs GIVENIDS --outfile OUTFILE [--TMcount] [--TMcoordinates] [--filter]``

 Options
- `-h`, `--help`: Show this help message and exit
- `--infile INFILE`: Input file containing gene or protein identifiers
- `--infile-index-column INFILE_INDEX_COLUMN`: Index of the column containing gene or protein identifiers in the input file (0-based)
- `--givenIDs GIVENIDS`: Type of identifiers to search for in the database
- `--outfile OUTFILE`: Output file with the results
- `--filter`: Filter out entries that are not transmembrane proteins

<br></br>
**Installation**

``$ pip install MembProtFinder``


