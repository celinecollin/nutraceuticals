
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def generate_figure13():
    # 1. HARDCODED DATA
    data = {
        'Segment': ['Spare No Expense', 'Value-Conscious', 'Basic Care'],
        'Households_Pct': [20, 50, 30],  # The Grey Bars (Population)
        'Revenue_Pct': [48, 42, 10]      # The Blue Line (Yield)
    }
    df = pd.DataFrame(data)

    # 2. SETUP PLOT
    fig, ax1 = plt.subplots(figsize=(7, 5))

    # 3. PLOT BARS (Households - Volume)
    # Using a neutral grey to represent "Volume"
    bars = ax1.bar(df['Segment'], df['Households_Pct'], color='#8D99A6', width=0.5, label='% Households')
    ax1.set_ylabel('% Households', color='#4A4A4A', fontweight='bold')
    ax1.set_ylim(0, 60)  # Headroom for labels
    
    # 4. PLOT LINE (Revenue - Value)
    # Using the deep Navy Blue from the original image for the "Value" line
    ax2 = ax1.twinx()
    line = ax2.plot(df['Segment'], df['Revenue_Pct'], color='#0B2C4D', linewidth=3, marker='o', markersize=8, label='% Revenue')
    ax2.set_ylabel('% Revenue', color='#0B2C4D', fontweight='bold')
    ax2.set_ylim(0, 60)

    # 5. DATA LABELS (The "Banker" Polish)
    # Label the Bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 1, f'{int(height)}%',
                 ha='center', va='bottom', color='black', fontsize=9)

    # Label the Line Points
    for i, txt in enumerate(df['Revenue_Pct']):
        ax2.text(i, txt + 2, f'{txt}%', ha='center', va='bottom', color='#0B2C4D', fontweight='bold', fontsize=10)

    # 6. FORMATTING
    plt.title('Figure 13: Consumer Segmentation - The "Pareto" Effect', fontsize=12, fontweight='bold', pad=20)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    # Legend Handling (Merging two axes into one legend)
    # Get handles and labels from both axes
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    # Combine
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False)

    # 7. SAVE
    plt.tight_layout()
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        # Fallback or create? Assuming directory exists as per previous context
        output_dir = "." 
    
    output_path = os.path.join(output_dir, 'Figure13_Pareto_Combo.png')
    plt.savefig(output_path, dpi=300)
    print(f"Success: Figure 13 regenerated as a Combo Chart at {output_path}")

if __name__ == "__main__":
    generate_figure13()
