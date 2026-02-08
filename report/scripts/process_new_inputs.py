import os
import glob
# import pandas as pd # CAUSING BINARY ERROR
from docx import Document
import openpyxl
import datetime
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

INPUT_DIR = "report/20260121_new input"
OUTPUT_FILE = "report/source_material/20260125_New_Input_Consolidated.md"

def extract_docx(filepath):
    """Extract text from a .docx file."""
    try:
        doc = Document(filepath)
        text = []
        for para in doc.paragraphs:
            if para.text.strip():
                if para.style.name.startswith('Heading'):
                    text.append(f"### {para.text}")
                else:
                    text.append(para.text)
        return "\n\n".join(text)
    except Exception as e:
        # Fallback if python-docx not installed or fails
        return f"Error reading .docx {filepath}: {str(e)}"

def extract_xlsx(filepath):
    """Extract all sheets from an .xlsx file using openpyxl (No Pandas)."""
    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)
        output = []
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            output.append(f"#### Sheet: {sheet_name}")
            
            rows = list(ws.rows)
            if not rows:
                output.append("(Empty Sheet)")
                continue
            
            # Simple Markdown Table Converter
            # 1. Get headers
            headers = [str(cell.value or "") for cell in rows[0]]
            
            # 2. Separator
            separator = ["---"] * len(headers)
            
            # 3. Data
            data_rows = []
            for row in rows[1:]:
                row_vals = [str(cell.value or "").replace("\n", " ").replace("|", "/") for cell in row]
                data_rows.append(row_vals)
                
            # Construct Table string
            tbl_lines = []
            tbl_lines.append("| " + " | ".join(headers) + " |")
            tbl_lines.append("| " + " | ".join(separator) + " |")
            for dr in data_rows:
                tbl_lines.append("| " + " | ".join(dr) + " |")
                
            output.append("\n".join(tbl_lines))
            
        return "\n\n".join(output)
    except Exception as e:
        return f"Error reading .xlsx {filepath}: {str(e)}"

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Error: Directory '{INPUT_DIR}' not found.")
        return

    # Ensure output dir exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    files = sorted(glob.glob(os.path.join(INPUT_DIR, "*")))
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Consolidated Input from {INPUT_DIR}\n")
        f.write(f"Generated on: {datetime.datetime.now()}\n\n")

        for filepath in files:
            filename = os.path.basename(filepath)
            # Skip temp files
            if filename.startswith("~$"):
                continue
                
            print(f"Processing {filename}...")
            
            f.write(f"\n\n{'='*50}\n")
            f.write(f"## FILE: {filename}\n")
            f.write(f"{'='*50}\n\n")

            if filename.endswith(".docx"):
                content = extract_docx(filepath)
                f.write(content)
            elif filename.endswith(".xlsx"):
                content = extract_xlsx(filepath)
                f.write(content)
            else:
                f.write(f"(Skipping file type: {filename})")
            
            f.write("\n")

    print(f"\nSuccess! Consolidated output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
