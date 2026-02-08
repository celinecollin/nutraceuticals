
import re

file_path = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/Master_WhitePaper_Final.md"

def clean_content():
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    
    # regex for Bold Headers with numbers: **1. Title** or **A. Title** or **I.1.1. Title**
    # We want to keep the ** and ** but remove the number.
    # Group 1: **
    # Group 2: Numbering (to remove)
    # Group 3: Rest of text
    
    # Pattern 1: **1. Title** or **1.1 Title**
    # Note: re.sub is easier if we match the whole line or specific bold blocks.
    # Let's target lines starting with **
    
    for line in lines:
        stripped = line.strip()
        
        # SKIP Main Headers (Part I, I.1, etc) which rely on #
        if stripped.startswith('#'):
             new_lines.append(line)
             continue
        
        # 1. Convert Ordered Lists to Bullets
        # Match "1. " at start of line (allowing for indentation)
        if re.match(r'^\s*[0-9]+\.\s+', line):
            # Replace digit+dot+space with "* "
            # Keep indentation
            line = re.sub(r'(^\s*)[0-9]+\.\s+', r'\1* ', line)
        
        # 2. Clean Bold Headers
        # Look for **[Number/Letter]. space
        if stripped.startswith('**'):
            # Check if it starts with a number/letter pattern inside the bold
            # Patterns:
            # 1. **1. Text**
            # 2. **A. Text**
            # 3. **I.2.3. Text** (The flattened sub-sub-sections)
            # 4. **1.1 Text**
            
            # We strictly want to avoid stripping legitimate things? 
            # User said "no numbers or letters except bulletpoints for parts...".
            # So strip them all.
            
            # Remove "1. " or "1.1 " or "A. " or "I.2.1 " inside **...**
            # We search for ** match, then sub inside it?
            
            def replacer(match):
                content = match.group(1) # Content inside **...**
                # Remove leading numbering
                # Regex: Start of string, (Digits dots | Letters dots), space
                # Catch "I.2.3. " -> (IVX0-9.]+)\s+
                cleaned = re.sub(r'^([0-9]+\.|[A-Z]\.|[IVX]+\.[0-9]+(\.[0-9]+)?\.?)\s+', '', content)
                return f"**{cleaned}**"

            # Apply to line (handling potential trailing ** or .**)
            # The line might be `**1. Title.**` (We added dots in previous script)
            # Regex for bold block
            line = re.sub(r'\*\*(.+?)\*\*', replacer, line)
            
        new_lines.append(line)

    with open(file_path, 'w') as f:
        f.writelines(new_lines)
    
    print("Cleaned numbering from bold headers and lists.")

if __name__ == "__main__":
    clean_content()
