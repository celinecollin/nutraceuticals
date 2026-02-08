
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def generate_internal_composition_chart():
    # 1. DATA RECONSTRUCTION (Top 3 extracted + Calculated 'Others')
    # We keep the Main Sectors but simplify the composition
    sectors = [
        'Gut Health', 'Delivery Systems', 'Immunity', 'Performance & FCR', 'Mobility', 
        'Sustainability', 'Nutrigenomics', 'Special Niches', 'Cognition', 'Calming', 'Ectoparasite'
    ]

    # Data Structure: [Top1_Value, Top2_Value, Top3_Value, Others_Value]
    # Labels Structure: [Top1_Name, Top2_Name, Top3_Name]
    data = [
        ([50, 13, 9, 28], ['Probiotics', 'Enzymes', 'Prebiotics']),              # Gut Health
        ([35, 24, 23, 18], ['Rumen Protection', 'Smart Boluses', 'Soft Chews']), # Delivery
        ([55, 27, 8, 10], ['Seaweed/Poly sacch', 'Plasma/Colostrum', 'Beta-glucans']), # Immunity
        ([29, 18, 15, 38], ['Yeast Culture', 'Amino Acids', 'Xylanase']),        # Performance
        ([39, 36, 7, 18], ['Omega-3', 'Glucosamine', 'Green Lipped Mussel']),    # Mobility
        ([67, 19, 8, 6], ['N-Efficiency', 'P-Management', 'Natural Reducers']),   # Sustainability
        ([66, 19, 9, 6], ['Gut Infrastr.', 'Biomarker Subst.', 'Gene Markers']),  # Nutrigenomics
        ([77, 10, 7, 6], ['Astaxanthin', 'Biotin', 'Cranberry']),                # Special Niches
        ([35, 27, 23, 15], ['MCTs', 'DHA', 'Antioxidants']),                     # Cognition
        ([46, 30, 9, 15], ['Multi-Complexes', 'CBD/Hemp', 'L-Theanine']),        # Calming
        ([74, 20, 6, 0], ['Natural Repellents', 'Skin Barrier', 'Botanicals'])   # Ectoparasite
    ]

    # 2. PLOT SETUP
    fig, ax = plt.subplots(figsize=(12, 7))
    y_pos = np.arange(len(sectors))
    height = 0.75

    # Colors: Top 1 (Dark Blue), Top 2 (Med Blue), Top 3 (Light Blue), Others (Grey)
    colors = ['#1f4e79', '#2e75b6', '#9dc3e6', '#d9d9d9']

    # 3. BUILD THE STACKED BARS
    left_offset = np.zeros(len(sectors))

    for i in range(4): # Loop through the 4 segments (Top 1, 2, 3, Others)
        segment_values = [row[0][i] for row in data]

        # Plot segment
        bars = ax.barh(y_pos, segment_values, height, left=left_offset, color=colors[i], edgecolor='white')
        
        # Add Labels (Only if segment > 5% to avoid clutter)
        for j, bar in enumerate(bars):
            width = bar.get_width()
            if width > 8 and i < 3: # Only label the named segments, not 'Others'
                label_text = data[j][1][i] # Get name
                ax.text(bar.get_x() + width/2, bar.get_y() + height/2, 
                        f"{label_text}\n{int(width)}%", 
                        ha='center', va='center', color='white', fontsize=9, fontweight='bold')
            elif width > 8 and i == 3: # Label 'Others' differently
                ax.text(bar.get_x() + width/2, bar.get_y() + height/2, 
                        f"Others\n{int(width)}%", 
                        ha='center', va='center', color='#555555', fontsize=8)

        left_offset += segment_values

    # 4. FORMATTING
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sectors, fontweight='bold', fontsize=10)
    ax.set_xlabel('Share of Segment Revenue (%)', fontweight='bold')
    ax.set_title('Internal Composition: Key Ingredients Snapshot (Top 3 Drivers)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 100)

    # Clean layout
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.invert_yaxis() # Put first sector at top

    # 5. SAVE
    plt.tight_layout()
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."
             
    output_path = os.path.join(output_dir, 'Internal_Composition_Clean.png')
    plt.savefig(output_path, dpi=300)
    print(f"Success: Chart simplified to 'Top 3 + Others' view at {output_path}")

if __name__ == "__main__":
    generate_internal_composition_chart()
