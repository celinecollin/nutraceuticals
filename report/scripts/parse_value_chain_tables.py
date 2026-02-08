import re
import sys

input_file = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/temp_value_chain_source.txt"
output_file = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/tables_dump.md"

def parse_fixed_width(lines):
    tables = []
    current_lines = []
    
    for line in lines:
        if line.strip().startswith("Theme") or line.strip().startswith("Table III"):
            if current_lines:
                tables.append(process_table_chunk(current_lines))
                current_lines = []
            tables.append(f"## {line.strip()}")
        elif "Investment Thesis" in line:
            tables.append(f"*{line.strip()}*\n")
        else:
            current_lines.append(line)
            
    if current_lines:
        tables.append(process_table_chunk(current_lines))
        
    return tables

def process_table_chunk(lines):
    # Find separator line
    separator_idx = -1
    col_ranges = []
    
    for i, line in enumerate(lines):
        if re.match(r'^\s*[-]{3,}', line):
            separator_idx = i
            # determine ranges
            # e.g. "-------------- ------------"
            # find start/end of dashes
            matches = list(re.finditer(r'-+', line))
            col_ranges = [(m.start(), m.end()) for m in matches]
            break
            
    if separator_idx == -1:
        return ""
        
    # Headers are likely line i-1 (or i-2 if wrapped?)
    # Let's assume headers are i-1
    header_line_idx = separator_idx - 1
    # Check if there are multiple header lines (e.g. "Product\n(Commercial)")
    # Not trivial. Let's assume single line header or we can fix manually.
    
    headers = []
    for start, end in col_ranges:
        # Extend end slightly for header?
        h_text = lines[header_line_idx][start:end+1].strip() # +1 margin
        # Look above for more header text?
        if header_line_idx > 0 and len(lines[header_line_idx-1]) > start and lines[header_line_idx-1][start:end+1].strip():
             h_text = lines[header_line_idx-1][start:end+1].strip() + " " + h_text
        headers.append(h_text)
        
    # Identify rows
    rows = []
    current_row = [""] * len(headers)
    
    # Iterate lines AFTER separator
    for i in range(separator_idx + 1, len(lines)):
        line = lines[i]
        if not line.strip() or re.match(r'^\s*[-]{3,}', line):
            if any(current_row):
                 rows.append(current_row)
                 current_row = [""] * len(headers)
            continue
            
        # Parse cells
        is_new_row = False
        # Check first column
        start0, end0 = col_ranges[0]
        col0_text = line[start0:end0].strip()
        
        if col0_text:
            # New row
            if any(current_row):
                rows.append(current_row)
            current_row = [""] * len(headers)
            
        # Append content for all columns
        for col_idx, (start, end) in enumerate(col_ranges):
            # extend reading to next col start or end of line
            read_end = col_ranges[col_idx+1][0] if col_idx+1 < len(col_ranges) else len(line)
            cell_text = line[start:read_end].strip()
            if cell_text:
                if current_row[col_idx]:
                    current_row[col_idx] += " " + cell_text
                else:
                    current_row[col_idx] = cell_text
                    
    if any(current_row):
        rows.append(current_row)
        
    # Format markdown
    md = []
    md.append("| " + " | ".join(headers) + " |")
    md.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        # Clean specific chars
        clean_r = [c.replace("\n", " ") for c in r]
        md.append("| " + " | ".join(clean_r) + " |")
    
    return "\n".join(md) + "\n"

with open(input_file, 'r') as f:
    full_lines = f.readlines()
    
# Clean lines
fixed_lines = [l.replace('\t', '    ') for l in full_lines]

results = parse_fixed_width(fixed_lines)

with open(output_file, 'w') as f:
    for block in results:
        f.write(block + "\n")
