
from pypdf import PdfReader
import os

path = "report/format example old report/WP_Data_Centres_01_2026.pdf"

try:
    reader = PdfReader(path)
    text = ""
    # Read first 3 pages
    for i in range(min(3, len(reader.pages))):
        text += reader.pages[i].extract_text() + "\n\n"
    print(text)
except Exception as e:
    print(e)
