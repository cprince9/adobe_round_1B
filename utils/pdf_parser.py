import pdfplumber

def extract_sections_from_pdf(file_path):
    sections = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                sections.append({
                    "heading": f"Page {i+1}",
                    "text": text.strip(),
                    "page_number": i+1
                })
    return sections
