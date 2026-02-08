
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def generate_internal_composition_labels():
    # 1. DATA RECONSTRUCTION (Top 3 + Others)
    sectors = [ 
        'Gut Health', 'Delivery Systems', 'Immunity', 'Performance & FCR', 'Mobility', 
        'Sustainability', 'Nutrigenomics', 'Special Niches', 'Cognition', 'Calming', 'Ectoparasite' 
    ]

    # Data: [Top1_Val, Top2_Val, Top3_Val, Others_Val], [Name1, Name2, Name3]
    data = [ 
        ([50, 13, 9, 28], ['Probiotics', 'Enzymes', 'Prebiotics']), 
        ([35, 24, 23, 18], ['Rumen Prot.', 'Smart Boluses', 'Soft Chews']), 
        ([55, 27, 8, 10], ['Seaweed', 'Plasma/Colos', 'Beta-glucans']), 
        ([29, 18, 15, 38], ['Yeast Culture', 'Amino Acids', 'Xylanase']), 
        ([39, 36, 7, 18], ['Omega-3', 'Glucosamine', 'Green Lipped']), 
        ([67, 19, 8, 6], ['N-Efficiency', 'P-Mgmt', 'Nat. Reducers']), 
        ([66, 19, 9, 6], ['Gut Infrastr.', 'Biomarkers', 'Gene Markers']), 
        ([77, 10, 7, 6], ['Astaxanthin', 'Biotin', 'Cranberry']), 
        ([35, 27, 23, 15], ['MCTs', 'DHA', 'Antioxidants']), 
        ([46, 30, 9, 15], ['Multi-Complex', 'CBD/Hemp', 'L-Theanine']), 
        ([74, 20, 6, 0], ['Nat. Repellents', 'Skin Barrier', 'Botanicals']) 
    ]

    # 2. PLOT SETUP
    fig, ax = plt.subplots(figsize=(12, 8)) 
    y_pos = np.arange(len(sectors)) 
    height = 0.75 
    colors = ['#1f4e79', '#2e75b6', '#9dc3e6', '#d9d9d9'] # Dark -> Light -> Grey

    # 3. PLOT LOOPS
    left_offset = np.zeros(len(sectors))

    for i in range(4): # Iterate through segment layers (Top1, Top2, Top3, Others)
        segment_values = [row[0][i] for row in data] 
        bars = ax.barh(y_pos, segment_values, height, left=left_offset, color=colors[i], edgecolor='white')

        # LABELING LOGIC
        for j, bar in enumerate(bars):
            width = bar.get_width()
            if width > 6: # Threshold: Only label if >6% width
                # Determine Text
                if i < 3:
                    label = f"{data[j][1][i]}\n{int(width)}%" # Name + %
                else:
                    label = f"Others\n{int(width)}%" # Just "Others" + %
                
                # Determine Color (White for dark bars, Black for light bars)
                text_color = 'white' if i < 2 else '#333333'
                
                ax.text(bar.get_x() + width/2, bar.get_y() + height/2, 
                        label, ha='center', va='center', 
                        color=text_color, fontsize=8, fontweight='bold')
        left_offset += segment_values

    # 4. FORMATTING
    ax.set_yticks(y_pos) 
    ax.set_yticklabels(sectors, fontweight='bold', fontsize=10) 
    ax.set_xlabel('Share of Segment Revenue (%)', fontweight='bold') 
    ax.set_title('Internal Composition: Key Ingredients Snapshot', fontsize=14, fontweight='bold', pad=20) 
    ax.set_xlim(0, 100) 
    ax.spines['top'].set_visible(False) 
    ax.spines['right'].set_visible(False) 
    ax.invert_yaxis()

    # 5. SAVE
    plt.tight_layout() 
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."

    output_path = os.path.join(output_dir, 'Internal_Composition_DirectLabels.png')
    plt.savefig(output_path, dpi=300) 
    print(f"Success: All segments explicitly labeled within the graph at {output_path}")

if __name__ == "__main__":
    generate_internal_composition_labels()
