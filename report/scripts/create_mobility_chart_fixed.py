
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def generate_mobility_chart():
    # 1. DATA RECONSTRUCTION (Approximated from image)
    years = [2015, 2018, 2020, 2022, 2024, 2026, 2028, 2030]

    # Creating the stacked data layers
    # Generic Glucosamine (Grey): Declining from ~70% to ~35%
    generic = [70, 64, 60, 52, 45, 42, 38, 35]

    # UC-II Collagen (Blue): Growing from ~5% to ~30%
    ucii = [5, 11, 15, 19, 25, 27, 28, 30]

    # Green Lipped Mussel (Dark Grey): Roughly stable ~15-20%
    mussel = [15, 15, 15, 16, 17, 18, 19, 20]

    # Premium Combos (Navy): Growing from ~10% to ~15%
    premium = [10, 10, 10, 13, 13, 13, 15, 15]

    df = pd.DataFrame({
        'Year': years,
        'Generic Glucosamine': generic,
        'UC-II Collagen': ucii,
        'Green Lipped Mussel': mussel,
        'Premium Combos': premium
    })

    # 2. SETUP PLOT
    fig, ax = plt.subplots(figsize=(8, 5))

    # 3. PLOT STACKED AREA
    labels = ["Generic Glucosamine", "UC-II Collagen", "Green Lipped Mussel", "Premium Combos"]
    # Matching your image palette
    colors = ['#95a1a9', '#3b86c4', '#5f707f', '#223b5c']

    # Note: stackplot expects x, y1, y2, y3... so we unpack the columns
    ax.stackplot(df['Year'], 
                 df['Generic Glucosamine'], 
                 df['UC-II Collagen'], 
                 df['Green Lipped Mussel'], 
                 df['Premium Combos'], 
                 labels=labels, colors=colors, alpha=0.95)

    # 4. FIXING THE LEGEND (The Key Update)
    # Move legend below the chart (bbox_to_anchor) and spread horizontally (ncol=2 or 4)
    # User requested ncol=2 in code snippet but logic says spread horizontally (ncol=4 is usually better for horizontal spread)
    # The snippet says "ncol=2" inside the code block. I will stick to the provided code snippet: ncol=2
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), 
              fancybox=False, shadow=False, ncol=2, frameon=False, fontsize=9)

    # 5. FORMATTING
    ax.set_title('Mobility Supplement Premiumization (2015–2030)', fontsize=12, fontweight='bold', loc='left', pad=20)
    ax.set_ylabel('Market Share (%)', fontsize=10)
    ax.set_xlim(2015, 2030)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle=':', alpha=0.4)

    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 6. SAVE
    # Important: Increase bottom margin so the new legend isn't cut off
    plt.subplots_adjust(bottom=0.2)
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."
             
    output_path = os.path.join(output_dir, 'Mobility_Premiumization_Fixed.png')
    plt.savefig(output_path, dpi=300)
    print(f"Success: Legend moved to bottom footer to prevent overlap at {output_path}")

if __name__ == "__main__":
    generate_mobility_chart()
