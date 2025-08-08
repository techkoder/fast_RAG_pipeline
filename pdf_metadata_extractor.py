import sys
import os
from datetime import datetime
import re

import PyPDF2
import pdfplumber

def extract_pdf_metadata(pdf_path):
    metadata = {}
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            metadata['pages'] = len(reader.pages)

            # Extract text using pdfplumber for better text extraction
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"

            # Word count (splitting by whitespace)
            words = re.findall(r'\b\w+\b', full_text)
            metadata['words'] = len(words)

            # Section detection heuristics
            # Look for lines that look like section headings:
            # Patterns include:
            # 1. Numbered sections: "1. Introduction", "2.1 Subsection"
            # 2. All caps lines (likely headings)
            # 3. "Chapter" followed by number
            sections = set()
            lines = full_text.splitlines()
            section_pattern = re.compile(r'^\s*(Chapter\s+\d+|[0-9]+(\.[0-9]+)*\s+.+|[IVXLCDM]+\.\s+.+|[A-Z\s]{3,})$')
            for line in lines:
                line = line.strip()
                if section_pattern.match(line):
                    sections.add(line)
            metadata['sections'] = len(sections)

            # File info
            metadata['file_name'] = os.path.basename(pdf_path)
            metadata['processed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        print(f"Error processing file {pdf_path}: {e}")
        return None

    return metadata

def write_metadata_to_file(metadata, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("PDF METADATA EXTRACTION REPORT\n")
        f.write("========================================\n\n")
        f.write(f"File Name: {metadata.get('file_name', 'N/A')}\n")
        f.write(f"Number of Pages: {metadata.get('pages', 'N/A')}\n")
        f.write(f"Number of Words: {metadata.get('words', 'N/A')}\n")
        f.write(f"Number of Sections: {metadata.get('sections', 'N/A')}\n")
        f.write(f"Processed At: {metadata.get('processed_at', 'N/A')}\n")
        f.write("\n========================================\n")

def main():
    pdf_path = "/your/path/to/input.pdf"

    if not os.path.isfile(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    metadata = extract_pdf_metadata(pdf_path)
    if metadata is None:
        print("Failed to extract metadata.")
        sys.exit(1)

    output_file = os.path.splitext(pdf_path)[0] + "_metadata.txt"
    write_metadata_to_file(metadata, output_file)
    print(f"Metadata written to {output_file}")

if __name__ == '__main__':
    main()
