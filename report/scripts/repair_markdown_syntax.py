import re
import os

BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
FILE_PATH = os.path.join(BASE_DIR, "report/master_report/Master_WhitePaper_Final.md")

def repair_markdown(content):
    # 1. Deduplicate major headers (I., II., etc.)
    # The user added several "## I. Definition..." in a row
    lines = content.split('\n')
    new_lines = []
    last_header = None
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('## I. ') or stripped.startswith('# I. '):
            if stripped == last_header:
                continue
            last_header = stripped
        else:
            last_header = None
        new_lines.append(line)
    
    content = '\n'.join(new_lines)

    # 2. Fix malformed image/caption syntax '!*Figure X...*' -> '*Figure X...*'
    # but ONLY if it's at the end of a header or paragraph and looks like a stray caption
    content = re.sub(r'(!\*Figure [^*]+\*)', r'\n\1', content)
    content = re.sub(r'([^!])(!\*Figure)', r'\1\n\2', content)
    content = re.sub(r'!(\*Figure [^*]+\*)', r'\1', content)

    # 3. Fix stray image syntax remnants '![]' or just '!' at end of lines
    content = re.sub(r'(!\[\])', r'', content)
    
    # 4. Fix headers without spaces e.g. '###![Title]' -> '### ![Title]'
    content = re.sub(r'^(#+)(!\[)', r'\1 \2', content, flags=re.MULTILINE)
    
    # 5. Fix headers that are just '#'
    content = re.sub(r'^#+\s*$', '', content, flags=re.MULTILINE)

    # 6. Ensure actual images are on their own lines
    content = re.sub(r'(!\[[^\]]*\]\([^)]+\))', r'\n\n\1\n\n', content)
    
    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

if __name__ == "__main__":
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            text = f.read()
        
        fixed_text = repair_markdown(text)
        
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(fixed_text)
        print("Markdown repaired successfully.")
    else:
        print(f"File not found: {FILE_PATH}")
