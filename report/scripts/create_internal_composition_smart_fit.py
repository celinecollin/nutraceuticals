
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def generate_internal_composition_smart_fit():
    # 1. DATA INPUT
    sectors = [ 
        'Gut Health', 'Delivery Systems', 'Immunity', 'Performance & FCR', 'Mobility', 
        'Sustainability', 'Nutrigenomics', 'Special Niches', 'Cognition', 'Calming', 'Ectoparasite' 
    ]

    # Values [Top1, Top2, Top3, Others]
    data_vals = [ 
        [50, 13, 9, 28], [35, 24, 23, 18], [55, 27, 8, 10], [29, 18, 15, 38], 
        [39, 36, 7, 18], [67, 19, 8, 6], [66, 19, 9, 6], [77, 10, 7, 6], 
        [35, 27, 23, 15], [46, 30, 9, 15], [74, 20, 6, 0] 
    ]

    # Names
    data_names = [ 
        ['Probiotics', 'Enzymes', 'Prebiotics', 'Others'], 
        ['Rumen Prot.', 'Smart Boluses', 'Soft Chews', 'Others'], 
        ['Seaweed', 'Plasma/Colos', 'Beta-glucans', 'Others'], 
        ['Yeast Culture', 'Amino Acids', 'Xylanase', 'Others'], 
        ['Omega-3', 'Glucosamine', 'Green Lipped', 'Others'], 
        ['N-Efficiency', 'P-Mgmt', 'Nat. Reducers', 'Others'], 
        ['Gut Infrastr.', 'Biomarkers', 'Gene Markers', 'Others'], 
        ['Astaxanthin', 'Biotin', 'Cranberry', 'Others'], 
        ['MCTs', 'DHA', 'Antioxidants', 'Others'], 
        ['Multi-Complex', 'CBD/Hemp', 'L-Theanine', 'Others'], 
        ['Nat. Repellents', 'Skin Barrier', 'Botanicals', 'Others'] 
    ]

    # 2. PLOT SETUP (Wide Canvas)
    fig, ax = plt.subplots(figsize=(18, 9)) 
    y_pos = np.arange(len(sectors)) 
    colors = ['#1f4e79', '#2e75b6', '#9dc3e6', '#d9d9d9'] # Dark Blue -> Light Blue -> Grey

    # 3. GENERATION LOOP
    left_offset = np.zeros(len(sectors))

    for i in range(4): # Loop columns
        vals = [row[i] for row in data_vals] 
        bars = ax.barh(y_pos, vals, 0.85, left=left_offset, color=colors[i], edgecolor='white', linewidth=1)

        # SMART LABELING LOGIC
        for j, bar in enumerate(bars):
            width = bar.get_width()
            name = data_names[j][i]
            
            if width > 0: # Ignore empty
                # Strategy: Determine Text Content & Size based on width
                
                # Wrap text: Replace spaces with newlines to fit vertically
                wrapped_name = name.replace(" ", "\n").replace("/", "/\n").replace("-", "-\n")
                
                # Default Colors
                text_color = 'white' if i < 2 else 'black'
                font_weight = 'bold'
                
                # Case 1: Big Segment (>12%) - Full Text, Normal Size
                if width > 12:
                    label = f"{wrapped_name}\n{int(width)}%"
                    font_size = 9
                
                # Case 2: Medium Segment (5-12%) - Full Text, Tiny Font
                elif width > 5:
                    label = f"{wrapped_name}\n{int(width)}%"
                    font_size = 7
                    
                # Case 3: Small Segment (<5%) - Only % (Name physically won't fit)
                else:
                    label = f"{int(width)}%"
                    font_size = 7
                    font_weight = 'normal'
                
                # Place Text
                ax.text(bar.get_x() + width/2, bar.get_y() + 0.425, 
                        label, ha='center', va='center', 
                        color=text_color, fontsize=font_size, fontweight=font_weight, linespacing=0.9)
        left_offset += vals

    # 4. FORMATTING
    ax.set_yticks(y_pos) 
    ax.set_yticklabels(sectors, fontweight='bold', fontsize=11) 
    ax.set_xlabel('Share of Revenue (%)', fontweight='bold') 
    ax.set_title('Internal Composition: Ingredients Breakdown', fontsize=16, fontweight='bold', pad=20)

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
             
    output_path = os.path.join(output_dir, 'Internal_Composition_SmartFit.png')
    plt.savefig(output_path, dpi=300) 
    print(f"Success: Chart generated with text wrapped inside columns at {output_path}")

if __name__ == "__main__":
    generate_internal_composition_smart_fit()
