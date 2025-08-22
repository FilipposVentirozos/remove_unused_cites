# Remove Unused Citations

A Python tool to clean up academic bibliography files by removing unused citations from BibTeX files. This tool analyzes LaTeX (.tex) files to identify which citations are actually used and creates a filtered bibliography containing only the referenced entries.

## Features

- Extracts and processes BibTeX (.bib) files from directories or archives
- Scans LaTeX (.tex) files for citation references (supports `\cite`, `\citep`, `\citet`, `\citealp`, etc.)
- Creates filtered bibliography files with only used citations
- Configurable input/output paths via command line arguments

## Requirements

Install the required dependencies:

```bash
pip install bibtexparser
```

## Usage

### Main Citation Removal Tool

Remove unused citations from your bibliography:

```bash
# Basic usage (uses default ./data/ directory)
python remove_unused_entries.py

# Specify custom input directory and output file
python remove_unused_entries.py --input-dir /path/to/your/files --output /path/to/output.bib

# Short form
python remove_unused_entries.py -i /path/to/files -o output.bib
```

**Options:**
- `--input-dir`, `-i`: Directory containing .bib and .tex files (default: `./data/`)
- `--output`, `-o`: Output path for filtered .bib file (default: `./data/output.bib`)

### Archive Processing Tool

Extract and examine BibTeX files from zip archives:

```bash
# Extract zip file and read .bib contents
python process.py --zip-path /path/to/archive.zip --extract-to /path/to/extract/

# Short form
python process.py -z archive.zip -e ./extracted/
```

**Options:**
- `--zip-path`, `-z`: Path to the zip file to extract (required)
- `--extract-to`, `-e`: Directory to extract files to (default: `./data/`)

## How It Works

1. **Parse Bibliography Files**: Scans all `.bib` files in the input directory and extracts bibliography entries
2. **Find Used References**: Analyzes all `.tex` files to find citation commands and extract referenced keys
3. **Filter Entries**: Keeps only bibliography entries that are actually cited in the LaTeX files
4. **Generate Output**: Creates a new `.bib` file with only the used citations

## Supported Citation Commands

The tool recognizes these LaTeX citation commands:
- `\cite{key}`
- `\citep{key}` (parenthetical citations)
- `\citet{key}` (textual citations)
- `\citealp{key}` (author-less parenthetical)
- Multiple citations: `\cite{key1,key2,key3}`

## Example

```bash
# Place your .bib and .tex files in the data/ directory
mkdir data
cp your_bibliography.bib data/
cp your_paper.tex data/

# Run the tool
python remove_unused_entries.py

# Check the output
cat data/output.bib
```

This will create `data/output.bib` containing only the citations referenced in your `.tex` files.