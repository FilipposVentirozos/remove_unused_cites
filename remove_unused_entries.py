import os
import re
import json
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


def parse_bib_file(directory):
    """
    Parses a .bib file and returns a dictionary of bib entries.
    """
    all_bib_entries = dict()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".bib"):
                file_path = os.path.join(root, file)
                print(f"Reading {file_path}...")
                with open(file_path, 'r') as bib_file:
                    bib_database = bibtexparser.load(bib_file)
                    all_bib_entries = all_bib_entries | bib_database.entries_dict

    return all_bib_entries


def find_used_references(directory):
    """
    Finds and returns a set of all citation keys used in a .tex file.
    """
    used_references = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".tex"):
                # Pattern to match \cite, \citep, \citet, \citealp, and similar commands
                citation_pattern = re.compile(r'\\cite(?:t|p|author|year|yearpar|alp)?\{([^}]+)\}')
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as tex_file:
                    content = tex_file.read()
                    matches = citation_pattern.findall(content)
                    for match in matches:
                        # Citations might be comma-separated for multiple references or even given as \cite{ref1,ref2}
                        used_references.update([ref.strip() for ref in match.split(',')])
    return used_references


def filter_bib_entries(bib_entries, used_references):
    """
    Filters the bib_entries to only include those that are used.
    """
    return {key: value for key, value in bib_entries.items() if key in used_references}


def write_dict_to_bib_file(entries_dict, output_file_path):
    """
    Writes a dictionary of BibTeX entries to a .bib file.
    
    :param entries_dict: Dictionary of BibTeX entries, where keys are the citation keys.
    :param output_file_path: Path to the output .bib file.
    """
    # Create a BibDatabase object
    db = BibDatabase()
    
    # Convert the dictionary entries to a list of dictionaries
    db.entries = [entry for entry in entries_dict.values()]
    
    # Use BibTexWriter to write the BibDatabase to a file
    writer = BibTexWriter()
    with open(output_file_path, 'w') as bibfile:
        bibfile.write(writer.write(db))


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Remove unused citations from BibTeX files')
    parser.add_argument('--input-dir', '-i', default='./data/', 
                        help='Directory containing .bib and .tex files (default: ./data/)')
    parser.add_argument('--output', '-o', default='./data/output.bib',
                        help='Output path for filtered .bib file (default: ./data/output.bib)')
    
    args = parser.parse_args()
    
    directory = os.path.abspath(args.input_dir)
    output_path = os.path.abspath(args.output)
    
    if not os.path.exists(directory):
        print(f"Error: Directory {directory} does not exist")
        exit(1)

    print(f"Processing files in: {directory}")
    print("Parsing bib files...")
    bib_entries = parse_bib_file(directory=directory)
    print(f"Found {len(bib_entries)} bib entries")
    
    print("Finding used references...")
    used_references = find_used_references(directory=directory)
    print(f"Found {len(used_references)} used references: {sorted(used_references)}")
    
    print("Filtering entries...")
    filtered_entries = filter_bib_entries(bib_entries, used_references)
    print(f"Filtered to {len(filtered_entries)} entries")
    
    print("Writing output file...")
    write_dict_to_bib_file(filtered_entries, output_path)

    print(f"Filtered .bib file has been written to {output_path}")