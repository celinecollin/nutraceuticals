
import re
import os

input_path = "report/master_report/Master_WhitePaper_Final.md"
output_path = "report/master_report/Master_WhitePaper_Final_fixed.md"

with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
for i, line in enumerate(lines):
    # Check if this line is the start of a table
    # Pattern: Line starts with | (pipe) and previous line was NOT a table row/blank
    if line.strip().startswith('|'):
        # Check previous line
        if i > 0:
            prev_line = lines[i-1].strip()
            # If previous line acts as content (not blank, not a separator)
            if prev_line and not prev_line.startswith('|') and not prev_line.startswith('<!--'):
                # We found a table starting immediately after text (e.g. caption)
                # Insert a blank line
                fixed_lines.append("\n")
                print(f"Fixing table at line {i+1} (inserted blank line).")
    
    # Also check specific issue with Line 176 "II. Functional Segmentation..."
    # If it looks like a header but missing markdown
    if line.strip().startswith("II. Functional Segmentation") and not line.strip().startswith("#"):
         fixed_lines.append("\n## " + line.lstrip()) # Convert to Header 2 for consistency? 
         # Wait, "II." might be Part II. But it's in Part I.
         # Numbering consistency: Part I is "I.1, I.2".
         # Maybe this was meant to be distinct. 
         # Let's bold it instead to avoid structural confusion.
         # fixed_lines.append("\n**" + line.strip() + "**\n")
         # Actually, looking at the user request "Systematically correct errors".
         # Let's just fix the tables first. 
         # I will rely on the printed output to manually verify line 176 fix in next step if needed.
         # For now, just pass.
         pass

    fixed_lines.append(line)

with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f"Fixed Markdown saved to {output_path}")
