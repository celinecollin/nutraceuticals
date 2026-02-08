
import re

input_path = "report/master_report/Master_WhitePaper_Final.md"
output_path = "report/master_report/Master_WhitePaper_Final.md"

with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

processed_lines = []
in_appendix = False
table_started = False

for line in lines:
    if "Appendices" in line or "| Company | Country" in line:
        in_appendix = True
    
    if in_appendix:
        # Check if it looks like a table row (starts with |)
        if line.strip().startswith('|'):
            table_started = True
            processed_lines.append(line)
        elif table_started:
            if line.strip() == "":
                # Skip blank lines inside the table in appendix
                continue
            else:
                # If we hit a non-blank, non-table line, strictly speaking the table ended.
                # But looking at the file, it seems the blank lines are accidental spacers.
                # We will append non-table lines (like comments) but usually it is just blank lines.
                processed_lines.append(line)
        else:
            processed_lines.append(line)
    else:
        processed_lines.append(line)

with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(processed_lines)

print(f"Cleaned table in {output_path}")
