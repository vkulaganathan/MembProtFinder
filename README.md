# MembProtFinder
A tool to identify transmembrane proteins from a given list of gene or protein IDs.


**Usage**

``$ MembProtFinder [-h] --infile INFILE --infile-index-column INFILE_INDEX_COLUMN --givenIDs GIVENIDS --outfile OUTFILE [--TMcount] [--TMcoordinates] [--filter]``

 Options
- `-h`, `--help`: Show this help message and exit
- `--infile INFILE`: Input file containing gene or protein identifiers
- `--infile-index-column INFILE_INDEX_COLUMN`: Index of the column containing gene or protein identifiers in the input file (0-based)
- `--givenIDs GIVENIDS`: Type of identifiers to search for in the database
- `--outfile OUTFILE`: Output file with the results
- `--filter`: Filter out entries that are not transmembrane proteins

**Example**

Input File
| Genes | 
|---|
| ENSG00000075624 |
| ENST00000275493 |
| ENSG00000141510 |
| ENST00000342462 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |
| ENSG00000184895 |

Output File
| Genes | Gene Name | Transmembrane Protein? | Transmembrane_Helices_Count | Transmembrane_Helices_Positions |
|---|---|---|---|---|
| ENST00000275493	| EGFR	| True	| 1	| TM1: TRANSMEM 646..668 |
| ENST00000342462	| TMPPE	| True	| 5	| TM1: TRANSMEM 7..27 <br> TM2: TRANSMEM 43..63 <br> TM3: TRANSMEM 87..107 <br> TM4: TRANSMEM 114..134 <br> TM5: TRANSMEM 162..182 |




**Installation**

``$ pip install MembProtFinder``


