"""
Clean Markdown Generator - Creates properly formatted markdown with figures.
"""

import os
import re

BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
INPUT_FILE = os.path.join(BASE_DIR, "report/master_report/20260118_Master_WhitePaper.md")
OUTPUT_FILE = os.path.join(BASE_DIR, "report/master_report/20260118_Master_WhitePaper_Clean.md")

# Figure Mappings: placeholder text -> actual figure file
FIGURE_MAP = {
    "Household Pet Ownership Rate by Region": ("Figure1_Pet_Ownership.png", "Household Pet Ownership Rate by Region (2023)"),
    "Pet Population in Europe by Species": ("Figure2_EU_Pet_Pop.png", "Pet Population in Europe by Species (2023)"),
    "Growth of Cat and Dog Populations": ("Figure3_EU_Growth.png", "Population Growth: Cats vs Dogs in Europe (2018–2023)"),
    "Regional Market Size for Pet Nutraceuticals": ("Figure4_Regional_Market.png", "Regional Market Size for Pet Nutraceuticals (2024E)"),
    "Feed Probiotics Market Share by Species": ("Figure5_Probiotics_Share.png", "Feed Probiotics Market by Species (2024)"),
    "Global Poultry Production": ("Figure6_Poultry_HPAI.png", "Poultry Production vs HPAI Impact"),
    "European Swine Herd Decline": ("Figure7_Swine_Decline.png", "European Swine Herd Contraction (2014–2024)"),
    "De-Ruminization": ("Figure9_Livestock_Trends.png", "The De-Ruminization of Europe: Livestock Trends"),
    "Aquaculture vs Capture": ("Figure10_Aqua_v_Capture.png", "The Blue Transformation: Aquaculture Overtakes Capture"),
    "Format Popularity by Species": ("Figure11_Formats.png", "Nutraceutical Format Preferences by Species"),
    "Preventive Health Wallet": ("Figure12_Wallet.png", "Preventive Health Spending Allocation"),
    "Consumer Segmentation by WTP": ("Figure13_Segmentation.png", "Consumer Segmentation: The Pareto Effect"),
    "Psychological Factors Influencing WTP": ("Figure14_Psychology.png", "Psychological Drivers of Willingness-to-Pay"),
    "Mobility Supplement Market Evolution": ("Figure15_Mobility_Evo.png", "Mobility Supplement Premiumization (2015–2030)"),
    "Senior & Pre-Senior Pet Market": ("Figure16_Senior_Growth.png", "Senior Pet Market Growth Opportunity"),
    "Value Chain Mapping": ("Figure17_Value_Chain.png", "Value Chain: From Molecule to Market"),
    "Pet Supplement Channel Economics": ("Figure18_Channel_Economics.png", "Channel Economics: Margin Erosion Over Time"),
    "Value Waterfall": ("Figure19_Value_Waterfall.png", "Value Capture: Livestock vs Pet Economics"),
    "Risk/Reward Map": ("Figure20_Risk_Reward.png", "Risk/Reward Map: Segment Analysis"),
    "Pharma Encroachment Funnel": ("Figure21_Pharma_Funnel.png", "Pharma Encroachment: The Customer Funnel"),
    "Regulatory Framework": ("Table_US_vs_EU.png", "Comparative Regulatory Landscape: US vs EU"),
    "Timeline": ("Timeline_Regulations.png", "Regulatory Timeline: The Post-Antibiotic Era"),
    "Species vs Functional": ("Matrix_Species_Functional.png", "Species × Functional Needs Matrix"),
    "Efficacy Matrix": ("Matrix_Efficacy.png", "Ingredient Efficacy vs Market Maturity"),
    "The Regulatory Grey Zone": ("Venn_Nutraceuticals.png", "The Regulatory Grey Zone: Defining Nutraceuticals"),
}

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def replace_figure_placeholders(content):
    """Replace [INSERT FIGURE X:...] blocks with proper markdown images."""
    
    # First, handle existing malformed image embeds (like ![...](figures/...) that appear after [INSERT...])
    # Clean these up first
    content = re.sub(r'!\[[^\]]*\]\(figures/[^)]+\.png\)', '', content)
    
    # Now find all INSERT FIGURE blocks and replace them
    # Pattern matches [INSERT FIGURE X: description...]
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if '[INSERT FIGURE' in line or '[Figure' in line:
            # Try to match which figure this is
            matched = False
            for key, (filename, caption) in FIGURE_MAP.items():
                if key.lower() in line.lower():
                    new_lines.append(f"\n![{caption}](figures/{filename})\n")
                    matched = True
                    break
            if not matched:
                # Keep the line if we couldn't match it
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def clean_embedded_images(content):
    """Fix any already-embedded images that got malformed."""
    # Pattern: ![caption](path) that's split across lines or has extra text
    # First, normalize any existing image tags
    
    # Remove duplicate image tags (same file appearing twice)
    lines = content.split('\n')
    seen_images = set()
    cleaned_lines = []
    
    for line in lines:
        # Check if this line contains an image
        img_match = re.search(r'!\[[^\]]*\]\(figures/([^)]+)\)', line)
        if img_match:
            img_file = img_match.group(1)
            if img_file in seen_images:
                continue  # Skip duplicate
            seen_images.add(img_file)
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def remove_file_headers(content):
    """Remove internal file header markers."""
    # Remove lines like "# 20260118_PartIII.docx"
    content = re.sub(r'^#\s+\d+.*\.docx.*$', '', content, flags=re.MULTILINE)
    # Remove PARAGRAPHE DE TRANSITION markers
    content = re.sub(r'^.*PARAGRAPHE DE TRANSITION.*$', '', content, flags=re.MULTILINE)
    return content

def polish_wording(content):
    """Improve wording for publication quality."""
    
    # Fix common issues
    replacements = [
        # Remove citation markers for cleaner reading
        (r'\[\d+\]', ''),
        # Fix double spaces
        (r'  +', ' '),
        # Fix multiple blank lines
        (r'\n{4,}', '\n\n\n'),
        # Standardize dashes
        (r'–', '—'),
        # Remove trailing whitespace
        (r' +\n', '\n'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    return content

def main():
    print("Reading source file...")
    content = read_file(INPUT_FILE)
    
    print("Removing internal headers...")
    content = remove_file_headers(content)
    
    print("Replacing figure placeholders...")
    content = replace_figure_placeholders(content)
    
    print("Cleaning embedded images...")
    content = clean_embedded_images(content)
    
    print("Polishing wording...")
    content = polish_wording(content)
    
    # Add proper document title
    title_block = """# Animal Nutraceuticals: The Wellness Market at an Inflection Point

*Strategic White Paper | January 2026*

---

"""
    
    # Check if content starts with a title already
    if not content.strip().startswith('# '):
        content = title_block + content
    
    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("DONE.")

if __name__ == "__main__":
    main()
