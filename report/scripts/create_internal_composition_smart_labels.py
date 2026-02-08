
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def generate_internal_composition_smart_labels():
    # 1. DATA INPUT
    sectors = [
        'Gut Health', 'Delivery Systems', 'Immunity', 'Performance & FCR',
        'Mobility', 'Sustainability', 'Nutrigenomics', 'Special Niches',
        'Cognition', 'Calming', 'Ectoparasite'
    ]

    # Values: [Top1, Top2, Top3, Others]
    data_vals = [
        [50, 13, 9, 28], [35, 24, 23, 18], [55, 27, 8, 10], [29, 18, 15, 38],
        [39, 36, 7, 18], [67, 19, 8, 6],   [66, 19, 9, 6],   [77, 10, 7, 6],
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

    # 2. PLOT SETUP
    fig, ax = plt.subplots(figsize=(14, 8))
    y_pos = np.arange(len(sectors))
    colors = ['#1f4e79', '#2e75b6', '#9dc3e6', '#d9d9d9'] # Dark -> Light -> Grey

    # 3. GENERATION LOOP
    left_offset = np.zeros(len(sectors))
    overflow_labels = [[] for _ in range(len(sectors))] # Store text that doesn't fit inside

    for i in range(4):
        vals = [row[i] for row in data_vals]
        bars = ax.barh(y_pos, vals, 0.7, left=left_offset, color=colors[i], edgecolor='white')
        
        # Labeling Logic
        for j, bar in enumerate(bars):
            width = bar.get_width()
            name = data_names[j][i]
            
            if width > 0: # Ignore empty segments
                # CONDITION 1: Fits Inside? (Threshold > 12%)
                if width > 12: 
                    # Choose color based on background darkness
                    text_color = 'white' if i < 2 else '#333333'
                    # Print Name AND % inside
                    label_text = f"{name}\n{int(width)}%"
                    ax.text(bar.get_x() + width/2, bar.get_y() + 0.35, 
                            label_text, ha='center', va='center', 
                            color=text_color, fontsize=8, fontweight='bold')
                
                # CONDITION 2: Too small? Move to Overflow List
                else:
                    # Add to the list for this row
                    # Format: "Name (5%)"
                    overflow_labels[j].append(f"{name} ({int(width)}%)")

        left_offset += vals

    # 4. DRAW OVERFLOW TEXT (The "Side Labels")
    for j, labels in enumerate(overflow_labels):
        if labels:
            # Join all small items with commas
            text_string = ", ".join(labels)
            # Place text at x=101 (just right of the bar)
            ax.text(102, j, text_string, va='center', ha='left', 
                    fontsize=9, color='#444444', fontstyle='italic')

    # 5. FORMATTING
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sectors, fontweight='bold', fontsize=10)
    ax.set_xlabel('Share of Revenue (%)', fontweight='bold')
    ax.set_title('Internal Composition: Key Ingredients Breakdown', fontsize=14, fontweight='bold', pad=20)

    ax.set_xlim(0, 100) # Bars stop at 100
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False) # Open design
    ax.invert_yaxis()

    # 6. SAVE
    plt.tight_layout()
    # Leave space on right for the overflow text
    plt.subplots_adjust(right=0.85) 
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."
             
    output_path = os.path.join(output_dir, 'Internal_Composition_SmartLabels.png')
    plt.savefig(output_path, dpi=300)
    print(f"Success: Generated chart with 'Direct + Overflow' labeling at {output_path}")

if __name__ == "__main__":
    generate_internal_composition_smart_labels()
