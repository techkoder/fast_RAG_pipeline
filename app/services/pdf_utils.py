import requests
from pypdf import PdfReader
from io import BytesIO
print("🔹 pdf_utils is getting loadded")

def download_pdf_text(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    reader = PdfReader(BytesIO(response.content))
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)
    return "\n".join(full_text)
