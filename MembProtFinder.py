import pandas as pd
import argparse
from pysqlcipher3 import dbapi2 as sqlite
import configparser
from tqdm import tqdm

def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def attach_index_file(conn, index_file):
    if index_file:
        with open(index_file, 'r') as f:
            sql = f.read()
            conn.executescript(sql)

def get_columns_to_search(givenIDs):
    givenIDs = givenIDs.lower()  # Convert givenIDs to lowercase for case-insensitive comparison
    
    if givenIDs == 'uniprot':
        return ['`Entry`', '`Entry Name`']
    elif givenIDs == 'ensembl':
        return ['`Ensembl`']
    elif givenIDs == 'entrez':
        return ['`GeneID`']
    elif givenIDs == 'hgnc':
        return ['`HGNC`']
    elif givenIDs == 'pharmgkb':
        return ['`PharmGKB`']        
    elif givenIDs == 'kegg':
        return ['`KEGG`']
    elif givenIDs == 'mane':
        return ['`MANE-Select`']
    elif givenIDs == 'ucsc':
        return ['`UCSC`']
    elif givenIDs == 'symbol':
        return ['`Gene Names (primary)`', '`Gene Names (synonym)`']
    else:
        print(f"Invalid givenIDs: {givenIDs}")
        return []

import argparse

def main(args=None):
    # If args is None, parse command line arguments
    if args is None:
        parser = argparse.ArgumentParser(description="Process gene or protein identifiers and check for transmembrane helices.")
        parser.add_argument('--infile', required=True, help="Input file containing gene or protein identifiers")
        parser.add_argument('--infile-index-column', type=int, required=True, help="Index of the column containing gene or protein identifiers in the input file (0-based)")
        parser.add_argument('--givenIDs', required=True, help="Type of identifiers to search for in the database")
        parser.add_argument('--outfile', required=True, help="Output file with the results")
        parser.add_argument('--TMcount', action='store_true', help="Include Transmembrane Helix Count in the output")
        parser.add_argument('--TMcoordinates', action='store_true', help="Include Transmembrane Helices Positions in the output")
        parser.add_argument('--filter', action='store_true', help="Filter out entries that do not contain Transmembrane Helix ")
        args = parser.parse_args()

    # The rest of your main function code goes here
    # Read configuration
    config = read_config()
    password = config['database']['password']
    table_name = config['database']['table_name']
    index_file = config['database'].get('index_file', '')  # Get the path to the index file (if provided)

    # Connect to the encrypted SQLite database
    conn = sqlite.connect('TMdatabase_encrypted.db', check_same_thread=False, timeout=10, isolation_level=None)
    c = conn.cursor()

    # Enable decryption
    c.execute(f"PRAGMA key = '{password}';")

    # Check if the database connection is valid
    try:
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    except sqlite.Error as e:
        print(f"An error occurred: {e}")
        conn.close()
        return

    # Attach the index file
    attach_index_file(conn, index_file)

    # Read the input file
    input_df = pd.read_csv(args.infile, compression='gzip' if args.infile.endswith('.gz') else None)
    identifiers = input_df.iloc[:, args.infile_index_column]

    # Filter out duplicate identifiers
    unique_identifiers = identifiers.drop_duplicates()

    # Get the columns to search in the database
    columns_to_search = get_columns_to_search(args.givenIDs)

    # Open the output file in append mode
    with open(args.outfile, 'w') as f_out:
        # Write the header to the output file
        header = [input_df.columns[args.infile_index_column], 'Gene Name', 'Transmembrane Protein?']
        if args.TMcount:
            header.append('Transmembrane_Helices_Count')
        if args.TMcoordinates:
            header.append('Transmembrane_Helices_Positions')
        f_out.write('\t'.join(header) + '\n')

        # Initialize a set to keep track of processed identifiers
        processed_identifiers = set()

        # Process each unique identifier with progress tracking
        for idx, identifier in tqdm(unique_identifiers.items(), desc="Processing identifiers", total=len(unique_identifiers)):
            if identifier in processed_identifiers:
                continue  # Skip if already processed

            # Mark this identifier as processed
            processed_identifiers.add(identifier)

            # Query the database for 'Gene Names (primary)' column
            query = f"SELECT `Gene Names (primary)` FROM {table_name} WHERE (" + " OR ".join([f"{col} LIKE ?" for col in columns_to_search]) + ")"
            search_pattern = f"{identifier}%"  # This will match any identifier starting with the given identifier
            c.execute(query, [search_pattern] * len(columns_to_search))
            result = c.fetchone()

            # Extract gene name if result is found
            if result:
                gene_name = result[0].rstrip(';') if result[0] else ""
            else:
                gene_name = ""  # If no result found, gene name is empty

            # Prepare the output row
            output_row = [identifier, gene_name, False]

            # Process each identifier for additional information
            query = f"SELECT * FROM {table_name} WHERE (" + " OR ".join([f"{col} LIKE ?" for col in columns_to_search]) + ")"
            search_pattern = f"{identifier}%"  # This will match any identifier starting with the given identifier
            c.execute(query, [search_pattern] * len(columns_to_search))
            result = c.fetchone()
            
            if result:
                # Map column names to their respective indices
                column_names = [desc[0] for desc in c.description]
                col_idx_map = {col_name: idx for idx, col_name in enumerate(column_names)}

                output_row[2] = True  # Set 'Transmembrane Protein?' to True
                if args.TMcount and 'Transmembrane_Helices_Count' in col_idx_map:
                    output_row.append(result[col_idx_map['Transmembrane_Helices_Count']])
                else:
                    output_row.append("")
                if args.TMcoordinates and 'Transmembrane_Helices_Positions' in col_idx_map:
                    output_row.append(result[col_idx_map['Transmembrane_Helices_Positions']])
                else:
                    output_row.append("")
            else:
                if args.TMcount:
                    output_row.append("")
                if args.TMcoordinates:
                    output_row.append("")

            # Write the row to the output file if --filter is not set or 'Transmembrane Protein?' is True
            if not args.filter or output_row[2]:
                f_out.write('\t'.join(map(str, output_row)) + '\n')
                f_out.flush()  # Ensure immediate write to file

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()

