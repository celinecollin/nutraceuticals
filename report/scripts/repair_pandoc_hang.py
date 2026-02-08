
import os

input_path = "report/master_report/Master_WhitePaper_Final_preprocessed.md"
output_path = "report/master_report/Master_WhitePaper_Final_repaired.md"

with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

processed_lines = []
in_appendix = False
table_replaced = False

for line in lines:
    if "Appendices" in line:
        in_appendix = True
        processed_lines.append(line)
        continue
    
    if in_appendix and "| Company | Country" in line:
        processed_lines.append("\n\n**[Full Appendix Table Omitted due to formatting complexity. Please refer to the PDF or Markdown source.]**\n\n")
        table_replaced = True
        processed_lines.append("| Company | Country | Category | ... |\n")
        processed_lines.append("|---|---|---|---|\n")
        processed_lines.append("| See Source | - | - | - |\n")
        continue

    if in_appendix and table_replaced and line.strip().startswith('|'):
        continue # Skip the table rows
        
    processed_lines.append(line)

with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(processed_lines)

print(f"Repaired file saved to {output_path}")
