"""
Content Cleaning and Assembly Script for Master White Paper
Cleans artifacts, removes duplicates, and assembles complete document.
"""

import os
import re

# === PATHS ===
BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
MASTER_REPORT_DIR = os.path.join(BASE_DIR, "report/master_report")

# Input files
PART_I_II_FILE = os.path.join(MASTER_REPORT_DIR, "20260118_01_Part_I_II.md")
PART_III_FILE = os.path.join(MASTER_REPORT_DIR, "20260118_02_Part_III.md")
PART_IV_FILE = os.path.join(MASTER_REPORT_DIR, "20260118_03_Part_IV.md")
PART_V_FILE = os.path.join(MASTER_REPORT_DIR, "20260118_04_Part_V.md")

# Fallback to refined if parts don't exist
REFINED_FILE = os.path.join(MASTER_REPORT_DIR, "20260118_Master_WhitePaper_Refined.md")

# Output
OUTPUT_CLEAN = os.path.join(MASTER_REPORT_DIR, "20260118_Master_WhitePaper_Clean.md")


def clean_content(text):
    """Clean various artifacts from the content."""
    
    # 1. Remove broken reference links (e.g., investor.zoetis+2​)
    text = re.sub(r'[a-zA-Z-]+\.[a-zA-Z-]+\+\d+\u200b?', '', text)
    
    # 2. Remove French text artifacts
    french_patterns = [
        r'Ajouter à la question de suivi\n?',
        r'Vérifier les sources\n?',
        r'PARAGRAPHE DE TRANSITION\n?',
    ]
    for pattern in french_patterns:
        text = re.sub(pattern, '', text)
    
    # 3. Remove raw S3/ppl-ai URLs
    text = re.sub(r'https://ppl-ai-file-upload\.s3\.amazonaws\.com[^\s\n]+\n?', '', text)
    
    # 4. Remove excessive blank lines (more than 2)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    # 5. Remove trailing whitespace on lines
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    
    # 6. Clean up spaced ellipses and weird unicode
    text = text.replace('\u200b', '')  # Zero-width space
    text = text.replace('​', '')  # Another zero-width
    
    # 7. Fix "¬µg" encoding issue -> "µg"
    text = text.replace('¬µg', 'µg')
    
    return text


def extract_part_iii_from_refined(refined_content):
    """Extract Part III content from refined file (starts at line 7)."""
    lines = refined_content.split('\n')
    
    # Find where Part III starts and Part IV starts
    part_iii_start = None
    part_iv_start = None
    
    for i, line in enumerate(lines):
        if re.match(r'^#+\s*III\.?\s+|^III\.\s+', line) or 'III. Market Structure' in line:
            if part_iii_start is None:
                part_iii_start = i
        if re.match(r'^#+\s*IV\.?\s+|^# IV\.|^---\s*$', line) and 'IV.' in line:
            if part_iii_start is not None and part_iv_start is None:
                part_iv_start = i
                break
    
    if part_iii_start is not None:
        if part_iv_start is not None:
            return '\n'.join(lines[part_iii_start:part_iv_start])
        else:
            return '\n'.join(lines[part_iii_start:])
    
    return None


def extract_part_iv_from_refined(refined_content):
    """Extract Part IV (Competitive Landscape) from refined file."""
    lines = refined_content.split('\n')
    
    part_iv_start = None
    part_v_start = None
    
    for i, line in enumerate(lines):
        if '# IV.' in line or 'IV. Mapping the Competitive Landscape' in line:
            if part_iv_start is None:
                part_iv_start = i
        # Find first occurrence of Part V or VI (transactions)
        if part_iv_start is not None and part_v_start is None:
            if re.match(r'^#+\s*(V|VI)\.?\s+', line) or 'Notable Transactions' in line:
                part_v_start = i
                break
    
    if part_iv_start is not None:
        if part_v_start is not None:
            return '\n'.join(lines[part_iv_start:part_v_start])
        else:
            return '\n'.join(lines[part_iv_start:])
    
    return None


def extract_part_v_first_occurrence(refined_content):
    """Extract first occurrence of Part V/VI (transactions) to avoid duplicates."""
    lines = refined_content.split('\n')
    
    part_v_start = None
    part_v_end = None
    
    for i, line in enumerate(lines):
        # Find VI. Notable Transactions (first occurrence)
        if part_v_start is None:
            if 'VI. Notable Transactions' in line or ('VI.' in line and 'Notable' in line):
                part_v_start = i
            elif 'V. Notable Transactions' in line:
                part_v_start = i
        # Find the duplicate (second occurrence starts with ---\n# V.)
        elif part_v_start is not None and part_v_end is None:
            if line.strip() == '---' and i < len(lines) - 1:
                # Check if next non-empty line starts a duplicate
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip():
                        if '# V. Notable' in lines[j] or 'V. Notable Transactions' in lines[j]:
                            part_v_end = i
                            break
                        break
    
    # If no duplicate marker found, take until References section
    if part_v_start is not None and part_v_end is None:
        for i in range(part_v_start, len(lines)):
            if lines[i].strip() == '---':
                # Check what follows
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip().startswith('# V.'):
                        part_v_end = i
                        break
                if part_v_end:
                    break
    
    if part_v_start is not None:
        if part_v_end is not None:
            content = '\n'.join(lines[part_v_start:part_v_end])
        else:
            content = '\n'.join(lines[part_v_start:])
        
        # Renumber VI to V if needed
        content = re.sub(r'^(#+\s*)VI\.', r'\1V.', content, flags=re.MULTILINE)
        content = re.sub(r'^VI\.', 'V.', content, flags=re.MULTILINE)
        
        return content
    
    return None


def read_file(path):
    """Read file content safely."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None


def build_master_document():
    """Assemble the complete master document from parts."""
    
    print("=" * 60)
    print("BUILDING CLEAN MASTER DOCUMENT")
    print("=" * 60)
    
    # Read refined file as primary source
    refined = read_file(REFINED_FILE)
    if not refined:
        print("ERROR: Cannot find refined file")
        return None
    
    # Read Part I & II
    part_i_ii = read_file(PART_I_II_FILE)
    if not part_i_ii:
        print("WARNING: Part I-II file not found, extracting from master...")
        # Fallback: could extract from 20260118_Master_WhitePaper.md
        master_full = read_file(os.path.join(MASTER_REPORT_DIR, "20260118_Master_WhitePaper.md"))
        if master_full:
            # Extract up to Part III
            lines = master_full.split('\n')
            end_idx = None
            for i, line in enumerate(lines):
                if '# 20260118_PartIII' in line or 'III. Market Structure' in line:
                    end_idx = i
                    break
            if end_idx:
                part_i_ii = '\n'.join(lines[:end_idx])
    
    if not part_i_ii:
        print("WARNING: Could not locate Part I-II content")
        part_i_ii = ""
    else:
        print(f"✓ Found Part I-II: {len(part_i_ii)} chars")
    
    # Extract Part III from refined
    part_iii = extract_part_iii_from_refined(refined)
    if part_iii:
        print(f"✓ Extracted Part III: {len(part_iii)} chars")
    else:
        print("WARNING: Could not extract Part III")
        part_iii = ""
    
    # Extract Part IV from refined
    part_iv = extract_part_iv_from_refined(refined)
    if part_iv:
        print(f"✓ Extracted Part IV: {len(part_iv)} chars")
    else:
        print("WARNING: Could not extract Part IV")
        part_iv = ""
    
    # Extract Part V (first occurrence only, not duplicate)
    part_v = extract_part_v_first_occurrence(refined)
    if part_v:
        print(f"✓ Extracted Part V: {len(part_v)} chars")
    else:
        print("WARNING: Could not extract Part V")
        part_v = ""
    
    # Build document with proper structure
    document_parts = []
    
    # Title
    document_parts.append("# Master White Paper: The Animal Nutraceutical Landscape (2024-2030)")
    document_parts.append("")
    document_parts.append("---")
    document_parts.append("")
    
    # Part I & II (clean the header if it has file reference)
    part_i_ii_clean = part_i_ii
    part_i_ii_clean = re.sub(r'^#\s*2026015_WhitePaper\.docx\s*\n?', '', part_i_ii_clean)
    document_parts.append(part_i_ii_clean.strip())
    document_parts.append("")
    document_parts.append("---")
    document_parts.append("")
    
    # Part III
    document_parts.append(part_iii.strip())
    document_parts.append("")
    document_parts.append("---")
    document_parts.append("")
    
    # Part IV
    document_parts.append(part_iv.strip())
    document_parts.append("")
    document_parts.append("---")
    document_parts.append("")
    
    # Part V
    document_parts.append(part_v.strip())
    
    # Combine
    full_document = '\n'.join(document_parts)
    
    # Clean the combined document
    print("\nCleaning content artifacts...")
    full_document = clean_content(full_document)
    
    # Remove any remaining raw URL dumps at the end
    # Find where proper references end and raw URLs begin
    lines = full_document.split('\n')
    cutoff = None
    for i, line in enumerate(lines):
        if line.strip().startswith('https://ppl-ai-') or line.strip().startswith('https://investor.') or line.strip().startswith('https://finance.'):
            if cutoff is None:
                # Check if this is a block of URLs
                url_count = 0
                for j in range(i, min(i+10, len(lines))):
                    if lines[j].strip().startswith('http'):
                        url_count += 1
                if url_count > 3:
                    cutoff = i
                    break
    
    if cutoff:
        print(f"  Removing raw URL block starting at line {cutoff}")
        full_document = '\n'.join(lines[:cutoff])
    
    # Final cleanup
    full_document = re.sub(r'\n{4,}', '\n\n\n', full_document)
    
    print(f"\n✓ Final document: {len(full_document)} chars, {len(full_document.split(chr(10)))} lines")
    
    return full_document


def main():
    document = build_master_document()
    
    if document:
        # Write clean output
        with open(OUTPUT_CLEAN, 'w', encoding='utf-8') as f:
            f.write(document)
        print(f"\n✓ Saved to: {OUTPUT_CLEAN}")
        
        # Summary stats
        lines = document.split('\n')
        h1_count = len([l for l in lines if l.startswith('# ')])
        h2_count = len([l for l in lines if l.startswith('## ')])
        h3_count = len([l for l in lines if l.startswith('### ')])
        figures = len(re.findall(r'!\[.*?\]\(.*?\)', document))
        
        print(f"\nDocument Statistics:")
        print(f"  H1 headings: {h1_count}")
        print(f"  H2 headings: {h2_count}")
        print(f"  H3 headings: {h3_count}")
        print(f"  Figure references: {figures}")
    else:
        print("ERROR: Failed to build document")


if __name__ == "__main__":
    main()
