from PyPDF2 import PdfReader

class Reader:
    def reader(self, pdf_name):
        reader = PdfReader(f"{pdf_name}")
        page = reader.pages[0]
        text = page.extract_text()
        return text

 