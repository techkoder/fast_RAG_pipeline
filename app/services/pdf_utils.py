import fitz
import docx
import extract_msg
from io import BytesIO
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import asyncio
import httpx
import re
from datetime import datetime

# === Metadata Extractor ===
def extract_pdf_metadata_from_stream(file_stream: BytesIO):
    metadata = {}
    try:
        doc = fitz.open(stream=file_stream, filetype="pdf")
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

        metadata['processed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        doc.close()
    except Exception as e:
        print(f"Error processing PDF stream: {e}")
        return None

    return metadata

def write_metadata_to_file(metadata, output_path="storage/meta_data.txt"):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Number of Pages: {metadata.get('pages', 'N/A')}\n")
        f.write(f"Number of Words: {metadata.get('words', 'N/A')}\n")
        f.write(f"Number of Sections: {metadata.get('sections', 'N/A')}\n")
        f.write(f"Processed At: {metadata.get('processed_at', 'N/A')}\n")

# === Extractors ===
def extract_text_from_pdf(file_stream: BytesIO) -> str:
    doc = fitz.open(stream=file_stream, filetype="pdf")

    # Extract text
    def get_text(page): return page.get_text()
    with ThreadPoolExecutor() as executor:
        texts = list(executor.map(get_text, doc))
    full_text = "\n".join(texts)

    # Extract and write metadata
    file_stream.seek(0)  # Reset stream before passing to metadata extractor
    metadata = extract_pdf_metadata_from_stream(file_stream)
    if metadata:
        write_metadata_to_file(metadata)

    return full_text

def extract_text_from_docx(file_stream: BytesIO) -> str:
    doc = docx.Document(file_stream)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_email(file_stream: BytesIO) -> str:
    tmp_path = Path("temp_email.msg")
    tmp_path.write_bytes(file_stream.read())
    msg = extract_msg.Message(str(tmp_path))
    text = msg.body
    tmp_path.unlink(missing_ok=True)
    return text

# === Async Download Function ===
async def async_download_to_bytesio(url: str) -> BytesIO:
    buffer = BytesIO()
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url) as response:
            response.raise_for_status()
            async for chunk in response.aiter_bytes():
                buffer.write(chunk)
    buffer.seek(0)
    return buffer

# === Async Extractor for use in FastAPI or Jupyter ===
async def download_pdf_text_async(url: str) -> str:
    print(f"Downloading (async) from {url}")
    file_stream = await async_download_to_bytesio(url)
    lower_url = url.lower()

    if ".pdf" in lower_url:
        return extract_text_from_pdf(file_stream)
    elif ".docx" in lower_url:
        return extract_text_from_docx(file_stream)
    elif ".msg" in lower_url or ".eml" in lower_url:
        return extract_text_from_email(file_stream)
    else:
        raise ValueError("Unsupported file type. Only .pdf, .docx, .msg, and .eml are supported.")

# === Sync Wrapper for use in scripts ===
def download_pdf_text(url: str) -> str:
    if asyncio.get_event_loop().is_running():
        raise RuntimeError(
            "download_pdf_text() cannot be used in an async context. "
            "Use await download_pdf_text_async(url) instead."
        )
    return asyncio.run(download_pdf_text_async(url))
