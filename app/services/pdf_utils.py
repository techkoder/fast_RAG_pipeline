import requests
import fitz  # PyMuPDF
import docx
import extract_msg
from io import BytesIO
from pathlib import Path

def extract_text_from_pdf(file_stream: BytesIO) -> str:
    doc = fitz.open(stream=file_stream, filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

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

def download_pdf_text(url: str) -> str:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    file_stream = BytesIO(response.content)
    lower_url = url.lower()

    if ".pdf" in lower_url:
        return extract_text_from_pdf(file_stream)
    elif ".docx" in lower_url:
        return extract_text_from_docx(file_stream)
    elif ".msg" in lower_url or ".eml" in lower_url:
        return extract_text_from_email(file_stream)
    else:
        raise ValueError("Unsupported file type. Only .pdf, .docx, .msg, and .eml are supported.")
