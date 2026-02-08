import os
import re
from pypdf import PdfReader

# Key files to process
FILES = {
    "Zoetis": "Zoetis-2024-Annual-Report.pdf",
    "Novonesis": "Novonesis_Annual_Report_2024.pdf",
    "Virbac": "Annual_report_Virbac_2024.pdf",
    "Swedencare": "swedencare-half-year-report-2025.pdf",
    "HandH": "H&H Group 9M 2025 media release_ENG(2025.11.18-07_36_26).pdf",
    "Balchem": "Balchem-2024-Annual-Report-Final.pdf",
    "Symrise": "251028-Symrise-Financial-Information-9M-2025.pdf",
    "Givaudan": "giv-2025-nine-month-sales-en.pdf",
    "DSM_Firmenich": "press-release-dsm-firmenich-h1-report-20250731.pdf",
    "Petco": "Petco Reports Third Quarter 2025 Financial Results.pdf",
    "SHV_Nutreco": "SHV-Annual-Report-2023-online.pdf",
    "Roquette": "roquette-group-2024-annual-report.pdf",
    "ForFarmers": "250220_Annual-report-ForFarmers-2024.pdf",
    "BioAtla": "BioAtla Reports Fourth Quarter and Full Year 2022 Financial Results and Highlights Recent Progress.pdf",
    "Smithfield": "March 25, 2025 - 10-K_ Annual report [Section 13 and 15(d), not S-K Item 405] _ Smithfield Foods, Inc. (SFD).pdf"
}

BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/20260121_new input/Financial reports"

def extract_financials(name, filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        print(f"[{name}] File not found: {path}")
        return

    try:
        reader = PdfReader(path)
        print(f"\n--- {name} ({filename}) ---")
        
        # Scan first 10 pages for high-level numbers
        text = ""
        for i in range(min(15, len(reader.pages))):
            text += reader.pages[i].extract_text() + "\n"
            
        # Regex for Revenue/Sales usually followed by currency
        # Looking for patterns like "Revenue $8,544" or "Revenue ... 8,544"
        
        # Simple extraction of lines containing key terms
        lines = text.split('\n')
        keywords = ["Revenue", "Net Sales", "Total Income", "EBITDA", "Growth"]
        
        count = 0
        for line in lines:
            if any(k.lower() in line.lower() for k in keywords):
                # Filter for lines that likely contain numbers
                if re.search(r'\d', line):
                    print(line.strip())
                    count += 1
                if count > 15: # Limit output
                    break
                    
    except Exception as e:
        print(f"Error reading {name}: {e}")

if __name__ == "__main__":
    for name, filename in FILES.items():
        extract_financials(name, filename)
