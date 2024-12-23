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
                # Pattern to match \cite, \citep, \citet, and similar commands
                citation_pattern = re.compile(r'\\cite[t|p|author|year|yearpar]*\{([^}]+)\}')
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
    directory = "/Users/filippos.ventirozos/Library/CloudStorage/OneDrive-AutoTraderGroupPlc/Projects/remove_unused_cites/data/"  # Path to your .bib file
    # tex_path = "/Users/filippos.ventirozos/Library/CloudStorage/OneDrive-AutoTraderGroupPlc/Projects/remove_unused_cites/data/acl_latex.tex"  # Path to your .tex file
    output_path = "/Users/filippos.ventirozos/Library/CloudStorage/OneDrive-AutoTraderGroupPlc/Projects/remove_unused_cites/data/output.bib"  # Path for the new .bib file

    bib_entries = parse_bib_file(directory=directory)
    used_references = find_used_references(directory=directory)
    filtered_entries = filter_bib_entries(bib_entries, used_references)
    write_dict_to_bib_file(filtered_entries, output_path)

    print(f"Filtered .bib file has been written to {output_path}")