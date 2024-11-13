# Document Similarity Analysis

This project is a Python script designed to compute pairwise similarity scores between documents based on their content. By leveraging **TF-IDF vectors** and **cosine similarity**, the script analyzes each document and returns the similarity scores for the top document pairs.

## Features
- **Document Preprocessing**: Extracts `<TITLE>` and `<TEXT>` from each document, normalizes cases, and tokenizes alphanumeric characters.
- **Token Dictionary Generation**: Builds a dictionary of tokens to token IDs for efficient indexing.
- **TF-IDF Calculation**: Computes TF-IDF vectors for each document using term frequency and inverse document frequency (IDF).
- **Cosine Similarity**: Calculates cosine similarity between document vectors to identify and rank document pairs by similarity.
- **Efficient Document Handling**: Reads and consolidates all documents into a single file for streamlined processing.

## Requirements
- **Python 3.x**
- **Standard Python Libraries**: `sys`, `os`, `time`, `math`

## Setup
1. **Clone this repository** to your local machine.
2. **Ensure all document files** are in a single folder, each containing the document `<DOCNO>`, `<TITLE>`, and `<TEXT>` tags.

## Usage
Run the script from the command line, providing the path to the document folder as an argument:
```bash
python main.py /path/to/document_folder
