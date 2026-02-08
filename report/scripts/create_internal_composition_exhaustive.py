
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def generate_internal_composition_exhaustive():
    # 1. DATA (Exhaustive)
    sectors = [ 
        'Gut Health', 'Delivery Systems', 'Immunity', 'Performance & FCR', 'Mobility', 
        'Sustainability', 'Nutrigenomics', 'Special Niches', 'Cognition', 'Calming', 'Ectoparasite' 
    ]

    # Values: [Top1, Top2, Top3, Others]
    data_vals = [ 
        [50, 13, 9, 28], [35, 24, 23, 18], [55, 27, 8, 10], [29, 18, 15, 38], 
        [39, 36, 7, 18], [67, 19, 8, 6], [66, 19, 9, 6], [77, 10, 7, 6], 
        [35, 27, 23, 15], [46, 30, 9, 15], [74, 20, 6, 0] 
    ]

    # Names correspond to the values above
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

    # 2. SETUP PLOT
    # We need a wide figure to hold the table on the right
    fig, ax = plt.subplots(figsize=(16, 8)) 
    y_pos = np.arange(len(sectors)) 
    colors = ['#1f4e79', '#2e75b6', '#9dc3e6', '#d9d9d9'] # Dark Blue -> Light Blue -> Grey

    # 3. PLOT VISUAL BARS (Left Side)
    left_offset = np.zeros(len(sectors)) 
    for i in range(4): 
        vals = [row[i] for row in data_vals] 
        bars = ax.barh(y_pos, vals, 0.6, left=left_offset, color=colors[i], edgecolor='white')

        # Add "Visual %" inside the bar only if it fits nicely
        for j, bar in enumerate(bars):
            width = bar.get_width()
            if width > 5: # Only if segment is > 5% width
                text_color = 'white' if i < 2 else 'black'
                ax.text(bar.get_x() + width/2, bar.get_y() + 0.3, 
                        f"{int(width)}%", ha='center', va='center', 
                        color=text_color, fontsize=8, fontweight='bold')
        left_offset += vals

    # 4. PLOT TEXT TABLE (Right Side)
    # We manually place text columns at fixed X coordinates to create a "Table" effect
    table_start_x = 102 # Start just after the 100% mark 
    col_widths = [28, 28, 28, 15] # Spacing for the columns

    for row_idx in range(len(sectors)): # For each sector, print the 4 ingredients in a row 
        current_x = table_start_x

        for col_idx in range(4):
            val = data_vals[row_idx][col_idx]
            name = data_names[row_idx][col_idx]
            
            if val > 0: # Don't print empty segments (like in Ectoparasite)
                # Format: "● Name (XX%)"
                # Bullet color matches the bar color
                ax.text(current_x, row_idx, "●", color=colors[col_idx], fontsize=12, va='center')
                
                # Text Label
                label_str = f"{name} ({val}%)"
                ax.text(current_x + 2, row_idx, label_str, color='#333333', fontsize=9, va='center')
            
            # Move to next column
            current_x += col_widths[col_idx]

    # 5. FORMATTING
    ax.set_yticks(y_pos) 
    ax.set_yticklabels(sectors, fontweight='bold', fontsize=10) 
    ax.set_xlabel('Share of Revenue (%)', fontweight='bold') 
    ax.set_title('Internal Composition: Exhaustive Breakdown', fontsize=14, fontweight='bold', pad=20)

    ax.set_xlim(0, 100) # The axes stop at 100, the text floats in the whitespace beyond 
    ax.spines['top'].set_visible(False) 
    ax.spines['right'].set_visible(False) 
    ax.invert_yaxis()

    # 6. SAVE
    plt.tight_layout()

    # Crucial: Expand right margin significantly to fit the table
    plt.subplots_adjust(right=0.95) 
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."
             
    output_path = os.path.join(output_dir, 'Internal_Composition_Exhaustive.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight') 
    print(f"Success: Generated Visual Table with 100% exhaustive labelling at {output_path}")

if __name__ == "__main__":
    generate_internal_composition_exhaustive()
