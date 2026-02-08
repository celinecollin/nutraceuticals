import re
import os

BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
FILE_PATH = os.path.join(BASE_DIR, "report/master_report/Master_WhitePaper_Final.md")

def final_repair(content):
    # 1. Fix unclosed alert blocks [!IMPORTANT -> [!IMPORTANT]
    content = re.sub(r'\[!(IMPORTANT|NOTE|TIP|WARNING|CAUTION)\b(?![^\]]*\])', r'[!\1]', content)
    
    # 2. Fix headers that are just image tags without paths e.g. '### ![Title]'
    content = re.sub(r'^#+\s*!\[[^\]]*\]\s*$', '', content, flags=re.MULTILINE)
    
    # 3. Fix headers that have image tags but NO path and are followed by the real image
    # Example:
    # ###![Timeline]
    # ![Timeline](path)
    # Becomes just:
    # ![Timeline](path)
    # (The cleanup above handles the empty header part)

    # 4. Fix stray exclamation marks at the end of paragraphs/headers
    # The user added '!' as a separator sometimes
    content = re.sub(r'([a-zA-Z0-9.\)])!([#\s])', r'\1\n\2', content)
    content = re.sub(r'([a-zA-Z0-9.\)])!$', r'\1', content, flags=re.MULTILINE)

    # 5. Fix double part headers if any remain
    lines = content.split('\n')
    new_lines = []
    last_header = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('## I') or stripped.startswith('# I'):
            if stripped == last_header:
                continue
            last_header = stripped
        else:
            last_header = None
        new_lines.append(line)
    content = '\n'.join(new_lines)

    # 6. Ensure space after # in all headers
    content = re.sub(r'^(#+)([A-Za-z0-9])', r'\1 \2', content, flags=re.MULTILINE)

    return content

if __name__ == "__main__":
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            text = f.read()
        fixed = final_repair(text)
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print("Final Markdown repair complete.")
