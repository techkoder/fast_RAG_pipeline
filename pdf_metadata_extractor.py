import sys
import os
from datetime import datetime
import re
import fitz  # PyMuPDF

def extract_pdf_metadata(pdf_path):
    metadata = {}
    try:
        doc = fitz.open(pdf_path)
        metadata['pages'] = doc.page_count

        # Extract full text
        full_text = ""
        for page in doc:
            text = page.get_text()
            if text:
                full_text += text + "\n"

        # Word count
        words = re.findall(r'\b\w+\b', full_text)
        metadata['words'] = len(words)

        # Section detection heuristics
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

        doc.close()
    except Exception as e:
        print(f"Error processing file {pdf_path}: {e}")
        return None

    return metadata

def write_metadata_to_file(metadata, output_path="meta_data.txt"):
    with open(output_path, "w", encoding="utf-8") as f:  # 'w' overwrites file each time

        f.write(f"Number of Pages: {metadata.get('pages', 'N/A')}\n")
        f.write(f"Number of Words: {metadata.get('words', 'N/A')}\n")
        f.write(f"Number of Sections: {metadata.get('sections', 'N/A')}\n")


def main():
    pdf_path = r"C:\Users\Dell\Desktop\indian_constitution.pdf"  # 🔁 Replace with actual path

    if not os.path.isfile(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    metadata = extract_pdf_metadata(pdf_path)
    if metadata is None:
        print("Failed to extract metadata.")
        sys.exit(1)

    write_metadata_to_file(metadata)
    print("Metadata written to meta_data.txt")

if __name__ == '__main__':
    main()
