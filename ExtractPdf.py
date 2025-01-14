from PyPDF2 import PdfReader

def extract_text_from_pdf():
    with open("resume.pdf", 'rb') as file:
        reader = PdfReader(file)
        # Get the number of pages
        num_pages = len(reader.pages)
        text = ""
        # Iterate over each page and extract text
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()        
    # print(text)
    return text
# extract_text_from_pdf()