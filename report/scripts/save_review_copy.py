
import os
from docx import Document

# Source file path (The visualized document created in the previous step)
SOURCE_FILE = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/Master_WhitePaper_Final_Visualized.docx"

print(f"Loading source document: {SOURCE_FILE}")
doc = Document(SOURCE_FILE)

# --- User Provided Request Logic ---
# Configuration
output_filename = "Whitepaper_v3_Final.docx" 
target_path = "/Users/celinecollin/Documents/review/" + output_filename

# 1. Ensure the directory exists
# Note: Using absolute path as requested. 
# Check if parent dir is accessible.
try:
    os.makedirs("/Users/celinecollin/Documents/review", exist_ok=True)
    print("Directory check: /Users/celinecollin/Documents/review (Ensured)")
except Exception as e:
    print(f"Directory creation warning: {e}")

# 2. Save the document
try: 
    doc.save(target_path) 
    print(f"SUCCESS: File saved to {target_path}") 
except Exception as e: 
    print(f"ERROR: Could not write to local path ({e}).") 
    print("Saving to default sandbox instead.") 
    doc.save(output_filename)
