
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def generate_internal_composition_tidy():
    # 1. DATA (Same as before)
    sectors = [ 
        'Gut Health', 'Delivery Systems', 'Immunity', 'Performance & FCR', 'Mobility', 
        'Sustainability', 'Nutrigenomics', 'Special Niches', 'Cognition', 'Calming', 'Ectoparasite' 
    ]

    # [Top1, Top2, Top3, Others]
    data_values = [ 
        [50, 13, 9, 28], [35, 24, 23, 18], [55, 27, 8, 10], [29, 18, 15, 38], 
        [39, 36, 7, 18], [67, 19, 8, 6], [66, 19, 9, 6], [77, 10, 7, 6], 
        [35, 27, 23, 15], [46, 30, 9, 15], [74, 20, 6, 0] 
    ]

    data_names = [ 
        ['Probiotics', 'Enzymes', 'Prebiotics'], 
        ['Rumen Prot.', 'Smart Boluses', 'Soft Chews'], 
        ['Seaweed', 'Plasma/Colos', 'Beta-glucans'], 
        ['Yeast Culture', 'Amino Acids', 'Xylanase'], 
        ['Omega-3', 'Glucosamine', 'Green Lipped'], 
        ['N-Efficiency', 'P-Mgmt', 'Nat. Reducers'], 
        ['Gut Infrastr.', 'Biomarkers', 'Gene Markers'], 
        ['Astaxanthin', 'Biotin', 'Cranberry'], 
        ['MCTs', 'DHA', 'Antioxidants'], 
        ['Multi-Complex', 'CBD/Hemp', 'L-Theanine'], 
        ['Nat. Repellents', 'Skin Barrier', 'Botanicals'] 
    ]

    # 2. PLOT SETUP
    # Wider to accommodate side text
    fig, ax = plt.subplots(figsize=(14, 8)) 
    y_pos = np.arange(len(sectors)) 
    colors = ['#1f4e79', '#2e75b6', '#9dc3e6', '#d9d9d9'] # Dark -> Light -> Grey

    # 3. PLOT BARS & INTERNAL NUMBERS
    left_offset = np.zeros(len(sectors))

    for i in range(4): # Loop segments
        segment_values = [row[i] for row in data_values] 
        bars = ax.barh(y_pos, segment_values, 0.7, left=left_offset, color=colors[i], edgecolor='white')

        # Add % numbers inside bars
        for j, bar in enumerate(bars):
            width = bar.get_width()
            if width > 4: # Only show % if width > 4%
                text_color = 'white' if i < 2 else 'black'
                ax.text(bar.get_x() + width/2, bar.get_y() + 0.35, 
                        f"{int(width)}%", ha='center', va='center', 
                        color=text_color, fontsize=9, fontweight='bold')
        left_offset += segment_values

    # 4. RIGHT-SIDE LEGEND (The "Tidy" Fix)
    for j in range(len(sectors)): 
        # Retrieve names for this row
        names = data_names[j]

        # Construct the label with bullets
        # We use mathematical symbols or simple text to simulate a legend
        # Note: Rich colored text is hard in pure matplotlib text(), so we position them manually

        # Bullet 1 (Dark Blue)
        ax.text(102, j, "●", color=colors[0], fontsize=12, va='center') 
        ax.text(104, j, names[0], color='black', fontsize=9, va='center')

        # Bullet 2 (Med Blue) - Offset based on length of first word?
        # To keep it tidy, we use fixed spacing columns
        ax.text(124, j, "●", color=colors[1], fontsize=12, va='center') 
        ax.text(126, j, names[1], color='black', fontsize=9, va='center')

        # Bullet 3 (Light Blue)
        ax.text(146, j, "●", color=colors[2], fontsize=12, va='center') 
        ax.text(148, j, names[2], color='black', fontsize=9, va='center')

    # 5. FORMATTING
    ax.set_yticks(y_pos) 
    ax.set_yticklabels(sectors, fontweight='bold', fontsize=10) 
    ax.set_xlabel('Share of Segment Revenue (%)', fontweight='bold') 
    ax.set_title('Internal Composition: Key Ingredients (Snapshot)', fontsize=14, fontweight='bold', pad=20)

    ax.set_xlim(0, 100) # Keep bars within 100

    # Hide the right spine so the text flows naturally
    ax.spines['top'].set_visible(False) 
    ax.spines['right'].set_visible(False) 
    ax.invert_yaxis()

    # 6. SAVE
    plt.tight_layout()

    # Expand right margin to fit the legends
    plt.subplots_adjust(right=0.75) 
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."

    output_path = os.path.join(output_dir, 'Internal_Composition_Tidy.png')
    plt.savefig(output_path, dpi=300) 
    print(f"Success: Figure regenerated with side-aligned legends for perfect readability at {output_path}")

if __name__ == "__main__":
    generate_internal_composition_tidy()
