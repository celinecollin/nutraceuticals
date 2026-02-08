
import re

file_path = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/Master_WhitePaper_Final.md"

with open(file_path, 'r') as f:
    lines = f.readlines()

print("--- DOCUMENT MAP ---")
for i, line in enumerate(lines):
    line = line.strip()
    if line.startswith("# "):
        print(f"LINE {i+1}: HEADER: {line}")
    elif line.startswith("!["):
        print(f"LINE {i+1}: FIGURE: {line}")
    elif line.startswith("*Figure"):
        print(f"LINE {i+1}: CAPTION: {line}")
