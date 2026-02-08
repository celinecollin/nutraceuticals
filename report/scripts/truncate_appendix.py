
import re

input_path = "report/master_report/Master_WhitePaper_Final.md"
output_path = "report/master_report/Master_WhitePaper_Final.md"

with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

processed_lines = []
in_appendix = False
table_started = False
rows_kept = 0
MAX_ROWS = 10

for line in lines:
    if "Appendices" in line or "| Company | Country" in line:
        in_appendix = True
    
    if in_appendix:
        if line.strip().startswith('|'):
            if not table_started:
                table_started = True
                processed_lines.append(line) # Header
                continue
            
            # Check if it's separator line
            if '---' in line:
                processed_lines.append(line)
                continue
            
            # Data row
            if rows_kept < MAX_ROWS:
                processed_lines.append(line)
                rows_kept += 1
            elif rows_kept == MAX_ROWS:
                processed_lines.append("| ... | ... | ... | ... | ... | ... |\n")
                processed_lines.append("\n**[Table truncated for PDF generation stability. Full data available in supplementary materials.]**\n")
                rows_kept += 1 # Stop adding
        else:
            # Non-table line in appendix
            processed_lines.append(line)
    else:
        processed_lines.append(line)

with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(processed_lines)

print(f"Truncated table in {output_path}")
