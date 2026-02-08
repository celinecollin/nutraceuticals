import os
import re
from pypdf import PdfReader

# Key files to process for Innovation Analysis
FILES = {
    "Zoetis": "Zoetis-2024-Annual-Report.pdf",
    "Virbac": "Annual_report_Virbac_2024.pdf",
    "Novonesis": "Novonesis_Annual_Report_2024.pdf",
    "Swedencare": "swedencare-half-year-report-2025.pdf", # Might be limited
    "Symrise": "250327-Symrise-Corporate-Report-2024.pdf", # Using full report for R&D details
    "Givaudan": "giv-2024-gcfr.pdf", # Full report 2024
    "DSM_Firmenich": "mission-driven-company-report-2023.pdf", # 2023 full report likely has better R&D breakdown than H1 press release
    "Roquette": "roquette-group-2024-annual-report.pdf",
    "ForFarmers": "250220_Annual-report-ForFarmers-2024.pdf"
}

BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/20260121_new input/Financial reports"

KEYWORDS_CLINICAL = ["clinical trial", "efficacy study", "scientific proof", "mode of action", "peer-reviewed", "in vivo", "in vitro", "pipeline"]

def extract_metrics(name, filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        print(f"[{name}] File not found: {path} (Check path)")
        return

    try:
        reader = PdfReader(path)
        print(f"\n--- {name} Analysis ---")
        
        # 1. Search for R&D Expenses (often in first 50 pages or financial tables)
        text_financial = ""
        # Scan pages likely to contain "Consolidated Income Statement" or "Key Figures"
        # usually first 20 pages or specific sections. We'll scan first 40 for now.
        for i in range(min(40, len(reader.pages))):
            text_financial += reader.pages[i].extract_text() + "\n"
            
        lines = text_financial.split('\n')
        
        print(">> Financials (R&D / Revenue Candidates):")
        rd_candidates = []
        for line in lines:
            # Look for lines with 'Research' AND numbers
            if ("Research and development" in line or "R&D" in line or "Innovation expenses" in line) and re.search(r'\d', line):
                 # Filter out short lines or table headers
                 if len(line) > 10 and len(line) < 150:
                    print(f"   {line.strip()}")
        
        # 2. Clinical Signal Strength (Keyword Frequency)
        # Scan specific sections or whole doc? Whole doc is safer for frequency.
        # To save time/memory, we might sample or just count based on the read pages so far 
        # but ideally we read the whole thing for "Signal".
        
        # Let's read more pages for the signal count, maybe up to 100
        text_full = text_financial
        for i in range(40, min(100, len(reader.pages))):
             text_full += reader.pages[i].extract_text() + "\n"
             
        print(">> Clinical Signal (Keyword Counts):")
        text_lower = text_full.lower()
        for kw in KEYWORDS_CLINICAL:
            count = text_lower.count(kw)
            if count > 0:
                print(f"   '{kw}': {count}")
                
    except Exception as e:
        print(f"Error reading {name}: {e}")

if __name__ == "__main__":
    for name, filename in FILES.items():
        extract_metrics(name, filename)
