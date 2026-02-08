#!/usr/bin/env python3
"""
Fix all figure formatting issues in the markdown.
"""

import re
import os

BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
INPUT_MD = os.path.join(BASE_DIR, "report/master_report/Master_WhitePaper_Final.md")
OUTPUT_MD = os.path.join(BASE_DIR, "report/master_report/Master_WhitePaper_Final.md")
FIGURES_DIR = os.path.join(BASE_DIR, "report/master_report/figures")

def fix_figures(content):
    """Fix all broken figure markdown syntax."""
    
    # 1. Fix duplicate path patterns: ![caption](path1)(path2) -> ![caption](path2)
    # Keep the second path as it's usually the intended one
    content = re.sub(
        r'!\[([^\]]*)\]\([^)]+\)\(([^)]+)\)',
        r'![\1](\2)',
        content
    )
    
    # 2. Remove the bad Venn diagram - replace with a more useful table/figure
    content = re.sub(
        r'!\[The Nutraceutical Landscape\]\(figures/Venn_Nutraceuticals\.png\)\n\*[^*]+\*\n*',
        '',
        content
    )
    
    # 3. Fix orphaned image syntax remnants
    content = re.sub(r'\(figures/[^)]+\.png\)\s*\n', '\n', content)
    
    # 4. Ensure figures are on their own lines with proper spacing
    content = re.sub(r'([.!?])\s*!\[', r'\1\n\n![', content)
    
    # 5. Remove stray brackets after figure captions
    content = re.sub(r'\*\.\s*\]\s*\n', '*\n\n', content)
    content = re.sub(r'\.\s*\]\s*\n', '.\n', content)
    
    return content

def insert_early_figures(content):
    """Insert useful figures early in the document."""
    
    # Insert US vs EU table after I.2 intro
    insert1 = '''
![US vs EU Regulatory Comparison](figures/Table_US_vs_EU.png)

*Figure I.1: Key regulatory differences between US and EU animal nutraceutical frameworks.*

'''
    content = content.replace(
        'I.2. Regulatory Landscape by Region\n\nI.2.1.',
        f'I.2. Regulatory Landscape by Region\n\n{insert1}I.2.1.'
    )
    
    # Insert regulatory timeline after UK section
    insert2 = '''

![Regulatory Evolution Timeline](figures/Timeline_Regulations.png)

*Figure I.2: Timeline of major regulatory developments in animal nutraceuticals (2020-2026).*

'''
    content = content.replace(
        'I.3. Scope of Analysis',
        f'{insert2}I.3. Scope of Analysis'
    )
    
    # Insert functional matrix at start of Part II
    insert3 = '''

![Species-Functional Matrix](figures/Matrix_Species_Functional.png)

*Figure II.1: Mapping functional needs across companion and production animal species.*

'''
    content = content.replace(
        'II. Functional Segmentation, Use Cases',
        f'{insert3}II. Functional Segmentation, Use Cases'
    )
    
    # Insert efficacy matrix in II.1
    insert4 = '''

![Ingredient Efficacy Landscape](figures/Matrix_Efficacy.png)

*Figure II.2: Evidence levels and market positioning of key mobility ingredients.*

'''
    content = content.replace(
        'II.2. Gut Health and Microbiome',
        f'{insert4}II.2. Gut Health and Microbiome'
    )
    
    # Insert probiotics share chart
    insert5 = '''

![Feed Probiotics Market Share](figures/Figure5_Probiotics_Share.png)

*Figure II.3: Feed probiotics market distribution by species (2024).*

'''
    content = content.replace(
        'II.3. Immunity and Resilience',
        f'{insert5}II.3. Immunity and Resilience'
    )
    
    return content

def clean_duplicate_figures(content):
    """Remove duplicate figure insertions."""
    lines = content.split('\n')
    seen_figures = set()
    result = []
    skip_until_blank = False
    
    for i, line in enumerate(lines):
        # Check if this is a figure line
        fig_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
        if fig_match:
            fig_path = fig_match.group(2)
            if fig_path in seen_figures:
                # Skip this figure and its caption
                skip_until_blank = True
                continue
            seen_figures.add(fig_path)
        
        if skip_until_blank:
            if line.strip() == '':
                skip_until_blank = False
            continue
        
        result.append(line)
    
    return '\n'.join(result)

def main():
    print("=" * 60)
    print("FIXING FIGURE FORMATTING")
    print("=" * 60)
    
    with open(INPUT_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Read {len(content)} characters")
    
    # Count figures before
    before_count = len(re.findall(r'!\[', content))
    print(f"Figures before cleanup: {before_count}")
    
    print("Fixing broken figure syntax...")
    content = fix_figures(content)
    
    print("Inserting early figures...")
    content = insert_early_figures(content)
    
    print("Removing duplicates...")
    content = clean_duplicate_figures(content)
    
    # Count figures after
    after_count = len(re.findall(r'!\[', content))
    print(f"Figures after cleanup: {after_count}")
    
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {len(content)} characters")
    
    print("=" * 60)
    print("✓ COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
