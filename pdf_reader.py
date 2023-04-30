import PyPDF2
import pdfplumber
import pdf2image
from PIL import Image
import pytesseract
import itertools

# Function to extract tables from a PDF page
def extract_tables_from_page(pdf_path, page):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        pdf_page = pdf.pages[page]
        tables = pdf_page.extract_tables()
    return tables

pdf_path = "Duolingo Hebrew Vocab.pdf"
page_number = 3  # Change the page number as needed

def flatten(iterable):
   out = []
   for i in iterable:
      if [hasattr(i,'__iter__'):]
         out.extend(flatten(i))
      else:
         out.append(i)
   return out

for i in range(3, 76):
    tables = extract_tables_from_page(pdf_path, i)
    for table in tables:
        print(table)
        print(flatten(table))

