#!/usr/bin/env python3
"""
Insert figures strategically throughout the document to break up prose.
"""

import re
import os

BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
INPUT_MD = os.path.join(BASE_DIR, "report/master_report/20260118_Master_WhitePaper_Final.md")
OUTPUT_MD = os.path.join(BASE_DIR, "report/master_report/20260118_Master_WhitePaper_Final.md")

# Figure insertions: section keyword -> (figure_file, caption)
FIGURE_INSERTIONS = [
    # Part I - Definition & Regulatory
    (r'(## I\. Definition, Scope and Structural Dynamics\n)', 
     r'\1\n![The Nutraceutical Landscape](figures/Venn_Nutraceuticals.png)\n*Figure: The nutraceutical market spans the intersection of nutrition, pharmaceuticals, and functional foods.*\n\n'),
    
    # After I.1 Terminology
    (r'(### I\.1\. Terminology\n\n.{500,800}?)(### I\.2\.)', 
     r'\1\n![US vs EU Regulatory Comparison](figures/Table_US_vs_EU.png)\n*Table: Key regulatory differences between US and EU frameworks.*\n\n\2'),
    
    # After regulatory landscape intro
    (r'(### I\.2\. Regulatory Landscape by Region\n)', 
     r'\1\n![Regulatory Timeline](figures/Timeline_Regulations.png)\n*Figure: Evolution of animal nutraceutical regulation (2020-2026).*\n\n'),
    
    # Part II - Functional Segmentation
    (r'(## II\. Functional Segmentation)', 
     r'![Species vs Functional Needs](figures/Matrix_Species_Functional.png)\n*Figure: Mapping functional needs across companion and production animal species.*\n\n\1'),
    
    # After II.1 (Gut Health section)
    (r'(### II\.1\. Gut Health and Digestive Function\n)', 
     r'\1\n![Probiotics Market Share](figures/Figure5_Probiotics_Share.png)\n*Figure: Feed probiotics market share by species.*\n\n'),
    
    # After II.2 (Mobility section)
    (r'(### II\.2\. Mobility and Joint Health\n.{300,600}?)(The clinical)', 
     r'\1![Mobility Supplement Evolution](figures/Figure15_Mobility_Evo.png)\n*Figure: Premiumization trend in mobility supplements.*\n\n\2'),
    
    # After II.3 (Immunity section)
    (r'(### II\.3\. Immunity and Resilience\n)', 
     r'\1\n![Efficacy Landscape](figures/Matrix_Efficacy.png)\n*Figure: Ingredient efficacy landscape by functional category.*\n\n'),
    
    # After II.4 (Cognitive section)
    (r'(### II\.4\. Cognitive Support and Aging\n.{200,400}?)(Propelled|The clinical)', 
     r'\1![Senior Pet Market Growth](figures/Figure16_Senior_Growth.png)\n*Figure: Growth trajectory of senior pet wellness market.*\n\n\2'),
    
    # Part III - Market Structure
    (r'(## III\. Market Structure and Value Capture\n)', 
     r'\1\n![Value Chain Economics](figures/Figure17_Value_Chain.png)\n*Figure: Value chain breakdown across the animal nutrition ecosystem.*\n\n'),
    
    # After pet demographics
    (r'(### III\.1\.1\. Companion Animals.{100,200}?)\n\n(The Global Pet)', 
     r'\1\n\n![Pet Ownership Rates](figures/Figure1_Pet_Ownership.png)\n*Figure: Household pet ownership rates by region.*\n\n\2'),
    
    # After European section
    (r'(### III\.1\.1\.2\. European Union.{50,150}?)\n\n(Europe represents)', 
     r'\1\n\n![EU Pet Population](figures/Figure2_EU_Pet_Pop.png)\n*Figure: Pet population distribution across European markets.*\n\n\2'),
    
    # Livestock section
    (r'(### III\.1\.2\. Livestock.{50,150}?)\n\n', 
     r'\1\n\n![Livestock Trends](figures/Figure9_Livestock_Trends.png)\n*Figure: Global livestock production trends and "de-ruminization" shift.*\n\n'),
    
    # Aquaculture section
    (r'(### III\.1\.2\.3\. Aquaculture.{50,150}?)\n\n',
     r'\1\n\n![Aquaculture vs Capture](figures/Figure10_Aqua_v_Capture.png)\n*Figure: Aquaculture overtakes wild capture fisheries in global protein supply.*\n\n'),
    
    # Part IV - Competitive
    (r'(## IV\. Competitive Landscape\n)',
     r'\1\n![Risk-Reward Segment Map](figures/Figure20_Risk_Reward.png)\n*Figure: Risk/reward positioning across animal health segments.*\n\n'),
    
    # Channel economics
    (r'(### IV\.3\. Valuation Patterns.{50,150}?)\n\n',
     r'\1\n\n![Channel Economics](figures/Figure18_Channel_Economics.png)\n*Figure: Channel economics evolution (vet, retail, DTC).*\n\n'),
]

def insert_figures(content):
    """Insert figures at strategic points."""
    inserted_count = 0
    
    for pattern, replacement in FIGURE_INSERTIONS:
        try:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
                inserted_count += 1
        except Exception as e:
            print(f"  Warning: Pattern failed - {str(e)[:50]}")
    
    return content, inserted_count

def main():
    print("=" * 60)
    print("FIGURE DISTRIBUTION")
    print("=" * 60)
    
    with open(INPUT_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Read {len(content)} characters")
    
    content, count = insert_figures(content)
    print(f"Inserted {count} figures")
    
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {len(content)} characters")
    
    print("=" * 60)
    print("✓ COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
