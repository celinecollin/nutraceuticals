
import os
import re

# Paths
BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
INPUT_FILE = os.path.join(BASE_DIR, "report/master_report/20260118_Master_WhitePaper.md")
OUTPUT_FILE = os.path.join(BASE_DIR, "report/master_report/20260118_Master_WhitePaper_Refined.md")
FIGURES_DIR = os.path.join(BASE_DIR, "report/master_report/figures")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def clean_lines(lines):
    # Remove file headers like "# 2026015_WhitePaper.docx"
    cleaned = []
    for line in lines:
        if re.match(r'^#\s+.*\.docx', line):
            continue
        # Remove the PARAGRAPHE DE TRANSITION marker
        if "PARAGRAPHE DE TRANSITION" in line:
            continue
        cleaned.append(line)
    return "".join(cleaned)

def main():
    print("Reading input file...")
    lines = read_file(INPUT_FILE)
    
    # 1. Extract Part I & II
    # From start to line 554 roughly. 
    # Termination marker: "# 20260118_PartIII.docx"
    part1_2 = []
    for line in lines:
        if "# 20260118_PartIII.docx" in line:
            break
        part1_2.append(line)
    
    print(f"Extracted Part I & II: {len(part1_2)} lines")

    # 2. Extract Part III (Market Structure)
    # This was labeled "IV. Market Structure and Value Capture" at line 1860
    # Search for this header
    part3_start = -1
    part3_end = -1
    part4_start = -1  # "V. Mapping the Competitive Landscape – Comprehensive Edition" (3088)
    part5_start = -1  # "V. Notable Transactions" (1360)
    
    for i, line in enumerate(lines):
        if "IV. Market Structure and Value Capture" in line and part3_start == -1:
            part3_start = i
        if "V. Mapping the Competitive Landscape – Comprehensive Edition" in line:
            part4_start = i
        if "V. Notable Transactions and Investment Landscape" in line and "Comprehensive" not in line and part5_start == -1:
            part5_start = i
            
    # Logic:
    # Part 3 Block: from part3_start to (end of file or next section?)
    # part3 starts at 1860. It ends at 3088 (part4_start).
    # Part 4 Block: from part4_start to End.
    # Part 5 Block: from part5_start to roughly 1718 (before part3_start?)
    
    # Refine end points
    # Part 5 is "Transactions" (1360). It ends before "IV. Market Structure" (1860).
    # Actually, let's verify if there is reference section between 1360 and 1860. 
    # Lines 1718-1859 are references. Include them in Part V or move to end?
    # Better to move all references to end.
    
    raw_part_3 = lines[part3_start:part4_start]
    raw_part_4 = lines[part4_start:] # To End
    raw_part_5 = lines[part5_start:part3_start] # 1360 to 1860. Contains references.
    
    print(f"Extraction indices: P3={part3_start}, P4={part4_start}, P5={part5_start}")
    
    # Process text and renumber
    
    # --- PART III PROCESSING ---
    # Rename "IV. Market Structure" to "III. Market Structure"
    # Rename subsections IV.1 -> III.1 etc
    text_part_3 = "".join(raw_part_3)
    text_part_3 = re.sub(r'IV\.(\s*Market Structure)', r'III.\1', text_part_3)
    text_part_3 = re.sub(r'IV\.(\d+)', r'III.\1', text_part_3)
    
    # --- PART IV PROCESSING ---
    # "V. Mapping..." -> "IV. Mapping..."
    # "V.1" -> "IV.1"
    text_part_4 = "".join(raw_part_4)
    text_part_4 = re.sub(r'V\.(\s*Mapping)', r'IV.\1', text_part_4)
    # Be careful not to replace V. Transactions (if mentioned)
    # Use strict regex for headers
    text_part_4 = re.sub(r'^##\s*V\.(\d+)', r'## IV.\1', text_part_4, flags=re.MULTILINE)
    text_part_4 = re.sub(r'^V\.(\d+)', r'IV.\1', text_part_4, flags=re.MULTILINE) # Handle non-markdown headers if any
    
    # --- PART V PROCESSING ---
    # "V. Notable Transactions" -> "V. Notable Transactions" (Keep as V)
    # But clean up references
    text_part_5 = "".join(raw_part_5)
    # Remove references from Part V block to move to end?
    # Or keep them there? User said "remove redundant info". 
    # Usually references go to the end. I'll strip them and append to a global ref list if possible.
    # But for now, let's keep them content-wise, maybe simpler.
    
    # --- INSERT FIGURES ---
    def insert_figure(text, content_anchor, image_file, caption):
        img_markdown = f"\n\n![{caption}](figures/{image_file})\n\n"
        # Find best place: after the header or relevant paragraph
        if content_anchor in text:
            return text.replace(content_anchor, content_anchor + img_markdown, 1)
        else:
            print(f"WARNING: Anchor '{content_anchor}' not found for {image_file}")
            return text

    # Part I & II
    text_part_1_2 = "".join(part1_2)
    text_part_1_2 = insert_figure(text_part_1_2, "Definition, Scope and Structural Dynamics", "Venn_Nutraceuticals.png", "Figure I.1: The Regulatory Grey Zone")
    text_part_1_2 = insert_figure(text_part_1_2, "I.2. Regulatory Landscape by Region", "Table_US_vs_EU.png", "Table I.1: Comparative Regulatory Framework")
    text_part_1_2 = insert_figure(text_part_1_2, "II. Functional Segmentation, Use Cases", "Matrix_Species_Functional.png", "Figure II.1: Species vs Functional Needs Intensity")
    text_part_1_2 = insert_figure(text_part_1_2, "II.1. Mobility and Joint Health", "Matrix_Efficacy.png", "Figure II.2: Ingredient Efficacy vs Maturity")

    # Part III (Market Structure)
    # Figures: Growth, Pop, Maps
    text_part_3 = insert_figure(text_part_3, "Household Pet Ownership Rate by Region", "Figure1_Pet_Ownership.png", "Figure III.1: Household Pet Ownership Rate (2023)")
    text_part_3 = insert_figure(text_part_3, "Pet Population in Europe by Species", "Figure2_EU_Pet_Pop.png", "Figure III.2: EU Pet Population Split")
    text_part_3 = insert_figure(text_part_3, "Growth of Cat and Dog Populations in Europe", "Figure3_EU_Growth.png", "Figure III.3: EU Population Growth (2018-2023)") 
    text_part_3 = insert_figure(text_part_3, "Regional Market Size for Pet Nutraceuticals", "Figure4_Regional_Market.png", "Figure III.4: Regional Market Size (2024E)")
    text_part_3 = insert_figure(text_part_3, "Feed Probiotics Market Share by Species", "Figure5_Probiotics_Share.png", "Figure III.5: Feed Probiotics Market Share")
    text_part_3 = insert_figure(text_part_3, "Global Poultry Production and HPAI Impact", "Figure6_Poultry_HPAI.png", "Figure III.6: Poultry Production & HPAI Impact")
    text_part_3 = insert_figure(text_part_3, "European Swine Herd Decline", "Figure7_Swine_Decline.png", "Figure III.7: EU Swine Herd Decline")
    text_part_3 = insert_figure(text_part_3, "The \"De-Ruminization\" of Europe", "Figure9_Livestock_Trends.png", "Figure III.8: Livestock Trends in Europe")
    text_part_3 = insert_figure(text_part_3, "Aquaculture vs Capture Fisheries", "Figure10_Aqua_v_Capture.png", "Figure III.9: The Great Overtaking (Fish)")
    text_part_3 = insert_figure(text_part_3, "Format Popularity by Species", "Figure11_Formats.png", "Figure III.10: Format Popularity by Species")
    text_part_3 = insert_figure(text_part_3, "Preventive Health Wallet", "Figure12_Wallet.png", "Figure III.10.B: Preventive Health Wallet Breakdown")
    text_part_3 = insert_figure(text_part_3, "Consumer Segmentation by WTP", "Figure13_Segmentation.png", "Figure III.11: Consumer Segmentation")
    text_part_3 = insert_figure(text_part_3, "Psychological Factors Influencing WTP", "Figure14_Psychology.png", "Figure III.11.B: Psychological Drivers")
    text_part_3 = insert_figure(text_part_3, "Mobility Supplement Market Evolution", "Figure15_Mobility_Evo.png", "Figure III.12: Mobility Market Evolution")
    text_part_3 = insert_figure(text_part_3, "Senior & Pre-Senior Pet Market Growth", "Figure16_Senior_Growth.png", "Figure III.13: Senior Market Growth")
    text_part_3 = insert_figure(text_part_3, "Value Chain Mapping – Molecule to Market", "Figure17_Value_Chain.png", "Figure III.14: Value Chain Mapping")
    text_part_3 = insert_figure(text_part_3, "Pet Supplement Channel Economics", "Figure18_Channel_Economics.png", "Figure III.15: Channel Economics")
    text_part_3 = insert_figure(text_part_3, "Value Waterfall – Premixer vs Pet Brand", "Figure19_Value_Waterfall.png", "Figure III.16: Value Capture Waterfall")
    text_part_3 = insert_figure(text_part_3, "Risk/Reward Map", "Figure20_Risk_Reward.png", "Figure III.17: Risk/Reward Map")
    text_part_3 = insert_figure(text_part_3, "Pharma Encroachment Funnel", "Figure21_Pharma_Funnel.png", "Figure III.18: Pharma Encroachment Funnel")
    
    # Part V (Timeline)
    text_part_5 = insert_figure(text_part_5, "V. Notable Transactions and Investment Landscape", "Timeline_Regulations.png", "Figure V.1: Regulatory Timeline")

    # Combine
    full_text = f"""# Master White Paper: The Animal Nutraceutical Landscape (2024-2030)

{clean_lines([text_part_1_2])}

---

{clean_lines([text_part_3])}

---

{clean_lines([text_part_4])}

---

{clean_lines([text_part_5])}
"""
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"DONE. Written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
