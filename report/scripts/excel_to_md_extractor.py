
import os
import openpyxl
from datetime import datetime

INPUT_DIR = "report/20260121_new input"
OUTPUT_FILE = "report/source_material/20260121_New_Input_Consolidated.md"

def ensure_dir_exists(path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def clean_cell_value(val):
    if val is None:
        return ""
    s = str(val).strip()
    return s.replace("|", "&#124;").replace("\n", "<br>")

def process_file(filepath, writer):
    filename = os.path.basename(filepath)
    print(f"Processing {filename}...")
    
    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)
    except Exception as e:
        writer.write(f"\n> **Error reading file {filename}:** {e}\n\n")
        print(f"Error reading {filename}: {e}")
        return

    writer.write(f"# File: {filename}\n\n")

    for sheetname in wb.sheetnames:
        print(f"  Sheet: {sheetname}")
        writer.write(f"## Sheet: {sheetname}\n\n")
        
        sheet = wb[sheetname]
        rows = list(sheet.values)
        
        if not rows:
            writer.write("> *Sheet is empty*\n\n")
            continue

        # Convert to MD table
        # 1. Inspect columns to find max width or just print carefully
        # We assume first row *might* be header, or just print all as table
        
        # Filter out empty rows at the end or completely empty rows
        cleaned_rows = []
        for row in rows:
            # Check if row has any content
            if any(cell is not None and str(cell).strip() != "" for cell in row):
                cleaned_rows.append(row)
        
        if not cleaned_rows:
             writer.write("> *Sheet is empty or blank*\n\n")
             continue

        # Determine number of columns based on the max length of any row
        # (Sometimes rows vary in length in values, though usually consistent in sheet)
        # But openpyxl 'values' property usually returns tuples of same length for the used range.
        # Let's check max length just in case.
        max_cols = 0
        for row in cleaned_rows:
            if len(row) > max_cols:
                max_cols = len(row)
                
        if max_cols == 0:
            continue

        # Header Row
        header = cleaned_rows[0]
        header_line = "| " + " | ".join([f"**{clean_cell_value(c)}**" for c in header]) + " |"
        writer.write(header_line + "\n")
        
        # Separator Row
        sep_line = "| " + " | ".join(["---"] * len(header)) + " |"
        writer.write(sep_line + "\n")
        
        # Data Rows
        # (Handling varying lengths if any, though header len usually sets the table width)
        # We will pad rows to match header length or truncate? 
        # Standard MD tables need consistent column count.
        # We will iterate row by row. If a row is shorter/longer, we adjust to header length.
        
        header_len = len(header)
        
        count = 0
        for row in cleaned_rows[1:]:
            row_vals = list(row)
            # Pad or Trim
            if len(row_vals) < header_len:
                row_vals += [""] * (header_len - len(row_vals))
            elif len(row_vals) > header_len:
                row_vals = row_vals[:header_len]
                
            line = "| " + " | ".join([clean_cell_value(c) for c in row_vals]) + " |"
            writer.write(line + "\n")
            
            count += 1
            if count > 5000: # Safety limit for massive files
                writer.write("\n> *...[Truncated after 5000 rows]...*\n")
                break
        
        writer.write("\n")

def main():
    ensure_dir_exists(OUTPUT_FILE)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Consolidated Input Source Material\n")
        f.write(f"Generated on: {datetime.now()}\n")
        f.write(f"Source Directory: `{INPUT_DIR}`\n\n")
        
        if not os.path.exists(INPUT_DIR):
            f.write("Error: Input directory not found.\n")
            return

        files = sorted([x for x in os.listdir(INPUT_DIR) if x.endswith(".xlsx") and not x.startswith("~$")])
        
        if not files:
            f.write("No .xlsx files found in input directory.\n")
            return

        for filename in files:
            filepath = os.path.join(INPUT_DIR, filename)
            process_file(filepath, f)

    print(f"Done. Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
