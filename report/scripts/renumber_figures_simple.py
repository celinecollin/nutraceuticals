
import re

file_path = 'report/master_report/Master_WhitePaper_Final.md'

with open(file_path, 'r') as f:
    content = f.read()

def replacer(match):
    num = int(match.group(1))
    if num >= 6:
        return f"Figure {num - 1}"
    return match.group(0)

# Replace "Figure N" with "Figure N-1" for N >= 6
# This handles:
# - **Figure 6:**
# - (see Figure 6)
# - | Figure 6 |
new_content = re.sub(r'Figure\s+(\d+)', replacer, content)

with open(file_path, 'w') as f:
    f.write(new_content)

print("Renumbering complete.")
