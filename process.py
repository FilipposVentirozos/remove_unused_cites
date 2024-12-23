import zipfile
import os

def extract_zip(zip_path, extract_to):
    """
    Extracts a zip file to a specified directory.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted zip file to {extract_to}")

def read_bib_files(directory):
    """
    Reads and prints the contents of all .bib files in a directory.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".bib"):
                file_path = os.path.join(root, file)
                print(f"Reading {file_path}...")
                with open(file_path, 'r') as bib_file:
                    bibs = bib_file.read()
                    print(bibs)
                print("-" * 40)  # Just a separator for readability

if __name__ == "__main__":
    zip_path = '/Users/filippos.ventirozos/Library/CloudStorage/OneDrive-AutoTraderGroupPlc/Projects/remove_unused_cites/data/RR.zip'  # Specify your zip file path
    extract_to = '/Users/filippos.ventirozos/Library/CloudStorage/OneDrive-AutoTraderGroupPlc/Projects/remove_unused_cites/data'  # Specify your extraction directory

    extract_zip(zip_path, extract_to)
    read_bib_files(extract_to)


