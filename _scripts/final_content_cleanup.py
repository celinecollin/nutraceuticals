#!/usr/bin/env python3
"""
Final Content Cleanup Script
Fixes all identified issues in the markdown content.
"""

import re
import os

BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
INPUT_MD = os.path.join(BASE_DIR, "report/master_report/Master_WhitePaper_Final.md")
OUTPUT_MD = os.path.join(BASE_DIR, "report/master_report/Master_WhitePaper_Final.md")

# Enhanced Executive Summary
NEW_EXEC_SUMMARY = '''# Master White Paper: The Animal Nutraceutical Landscape (2024-2030)

---

## Executive Summary

The global animal nutraceutical market stands at a critical inflection point, driven by two powerful secular trends: the "humanization" of companion animals and the post-antibiotic transition in livestock production. This whitepaper provides a comprehensive strategic analysis of a **$6+ billion industry** projected to reach **$10-14 billion by 2030-2035**.

### Key Findings

**Market Structure**
- The pet nutraceutical segment ($5.8-6.2B) commands premium valuations (15-20x EBITDA) driven by recurring revenue models and "wellness premium" pricing
- Livestock feed additives ($7-8B) operate on thinner margins (3-10% EBITDA) but benefit from regulatory tailwinds as antibiotic alternatives gain mandatory status
- The market exhibits a clear "two-speed" dynamic: pet brands are trophy assets; livestock feed is essential infrastructure

**Competitive Landscape**
- Top 5 players (Zoetis, Merck, DSM-Firmenich, Cargill, Novonesis) control ~55% of global feed additive market
- Clinical differentiation drives 20-40% price premiums (Nutramax's Dasuquin, DSM's Bovaer)
- E-commerce disruption (Chewy, Amazon) is compressing traditional veterinary channel margins by 100-200 bps

**Investment Themes**
- **Science as moat**: Companies with peer-reviewed efficacy data command sustained pricing power
- **Regulatory de-risking**: The Innovative FEED Act (US) and EU harmonization are shortening approval timelines
- **ESG integration**: Methane-reduction additives (Bovaer, 3-NOP) are becoming strategic procurement requirements

**Regional Dynamics**
- North America leads with 48% of global pet supplement revenue ($2.26B)
- Europe shows cat-dominant demographics (127M cats vs 104M dogs) with stricter regulatory frameworks
- Asia-Pacific represents the fastest-growing opportunity, driven by rising pet ownership in China and India

---

## I. Definition, Scope and Structural Dynamics

'''

def clean_content(content):
    """Apply all content cleaning operations."""
    
    # 1. Remove source.name tags anywhere in text
    content = re.sub(r'[a-zA-Z-]+\.[a-zA-Z-]+\+\d+\u200b?', '', content)
    content = re.sub(r'\.[a-zA-Z-]+\+\d+', '.', content)
    
    # 2. Remove citation brackets [1], [2][3], etc.
    content = re.sub(r'\[\d+\]', '', content)
    
    # 3. Clean orphaned brackets
    content = re.sub(r'\s*\]\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*\[\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\s+\]', '', content)
    content = re.sub(r'\[\s+', '', content)
    
    # 4. Remove zero-width spaces and invisible chars
    content = content.replace('\u200b', '')
    content = content.replace('\u200c', '')
    content = content.replace('\u200d', '')
    content = content.replace('\ufeff', '')
    
    # 5. Clean multiple blank lines (max 2)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # 6. Clean multiple spaces
    content = re.sub(r'  +', ' ', content)
    
    # 7. Clean space before punctuation
    content = re.sub(r'\s+([.,;:!?])', r'\1', content)
    
    # 8. Clean trailing source references in reference section
    # Format: "Title (Date).source.name" -> "Title (Date)."
    content = re.sub(r'\)\.[a-zA-Z-]+$', ').', content, flags=re.MULTILINE)
    content = re.sub(r'"\.[a-zA-Z-]+$', '".', content, flags=re.MULTILINE)
    
    # 9. Remove lines that are just source references
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip lines that are just domain references
        if re.match(r'^[a-zA-Z-]+\.[a-zA-Z-]+(\.[a-zA-Z-]+)?$', stripped):
            continue
        # Skip empty source references
        if re.match(r'^[a-zA-Z-]+\+\d+$', stripped):
            continue
        cleaned_lines.append(line)
    content = '\n'.join(cleaned_lines)
    
    return content

def replace_executive_summary(content):
    """Replace the executive summary with enhanced version."""
    # Find the start of the document and replace up to Part I
    pattern = r'^# Master White Paper.*?(?=## I\. |I\.1\. Terminology)'
    
    # Check if we can find the pattern
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    if match:
        content = content[:match.start()] + NEW_EXEC_SUMMARY + content[match.end():]
    else:
        # Fallback: prepend the new summary
        content = NEW_EXEC_SUMMARY + content
    
    return content

def ensure_figure_embeds(content):
    """Ensure figure references are proper markdown image embeds."""
    # Convert [INSERT FIGURE X: Title] to proper embeds if figure exists
    figure_map = {
        'Figure 1': 'figures/Figure1_Pet_Ownership.png',
        'Figure 2': 'figures/Figure2_EU_Pet_Pop.png',
        'Figure 3': 'figures/Figure3_EU_Growth.png',
        'Figure 4': 'figures/Figure4_Regional_Market.png',
        'Figure 5': 'figures/Figure5_Probiotics_Share.png',
        'Figure 6': 'figures/Figure6_Poultry_HPAI.png',
        'Figure 7': 'figures/Figure7_Swine_Decline.png',
        'Figure 8': 'figures/Figure8_Cattle_Region.png',
        'Figure 9': 'figures/Figure9_Livestock_Trends.png',
        'Figure 10': 'figures/Figure10_Aqua_v_Capture.png',
    }
    
    for fig_name, fig_path in figure_map.items():
        # Replace [INSERT FIGURE X: ...] with proper embed
        pattern = rf'\[INSERT {fig_name.upper()}[^\]]*\]'
        replacement = f'![{fig_name}]({fig_path})'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def break_dense_paragraphs(content):
    """Break up very long paragraphs for readability."""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Skip headers and short lines
        if line.startswith('#') or len(line) < 500:
            result.append(line)
            continue
        
        # For very long paragraphs, try to break at sentence boundaries
        if len(line) > 800:
            # Find good break points (after periods followed by caps)
            sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', line)
            if len(sentences) > 2:
                # Group into 2-3 sentence chunks
                chunks = []
                current = []
                for sent in sentences:
                    current.append(sent)
                    if len(' '.join(current)) > 400:
                        chunks.append(' '.join(current))
                        current = []
                if current:
                    chunks.append(' '.join(current))
                
                # Add chunks as separate paragraphs
                for chunk in chunks:
                    result.append(chunk)
                    result.append('')  # blank line
                continue
        
        result.append(line)
    
    return '\n'.join(result)

def clean_references_section(content):
    """Clean up the references section to be properly formatted."""
    # Find references section
    ref_match = re.search(r'(## References\n)(.*?)$', content, re.DOTALL)
    if not ref_match:
        return content
    
    before_refs = content[:ref_match.start()]
    refs_header = ref_match.group(1)
    refs_content = ref_match.group(2)
    
    # Clean each reference line
    ref_lines = refs_content.strip().split('\n')
    cleaned_refs = []
    ref_num = 1
    
    for line in ref_lines:
        line = line.strip()
        if not line:
            continue
        
        # Remove trailing source domains
        line = re.sub(r'\.[a-zA-Z-]+$', '.', line)
        line = re.sub(r'\.[a-zA-Z-]+\.[a-zA-Z-]+$', '.', line)
        
        # Clean up formatting
        line = line.strip('.')
        if line:
            cleaned_refs.append(f'{ref_num}. {line}.')
            ref_num += 1
    
    new_refs = refs_header + '\n'.join(cleaned_refs) + '\n'
    return before_refs + new_refs

def main():
    print("=" * 60)
    print("FINAL CONTENT CLEANUP")
    print("=" * 60)
    
    # Read input
    with open(INPUT_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Read {len(content)} characters from input")
    
    # Apply all cleanups
    print("Cleaning content artifacts...")
    content = clean_content(content)
    
    print("Replacing executive summary...")
    content = replace_executive_summary(content)
    
    print("Ensuring figure embeds...")
    content = ensure_figure_embeds(content)
    
    print("Breaking dense paragraphs...")
    content = break_dense_paragraphs(content)
    
    print("Cleaning references section...")
    content = clean_references_section(content)
    
    # Final cleanup pass
    content = clean_content(content)
    
    # Write output
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {len(content)} characters to output")
    
    print("=" * 60)
    print(f"✓ COMPLETE: {OUTPUT_MD}")
    print("=" * 60)

if __name__ == "__main__":
    main()
