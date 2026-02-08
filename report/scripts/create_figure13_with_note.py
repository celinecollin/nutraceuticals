
import matplotlib.pyplot as plt
import pandas as pd
import os

def generate_figure13_with_note():
    # 1. DATA (Hardcoded for accuracy)
    data = { 
        'Segment': ['Spare No Expense', 'Value-Conscious', 'Basic Care'], 
        'Households_Pct': [20, 50, 30], 
        'Revenue_Pct': [48, 42, 10] 
    } 
    df = pd.DataFrame(data)

    # 2. SETUP PLOT
    # Increased height slightly for the footer
    fig, ax1 = plt.subplots(figsize=(7, 5.5)) 

    # 3. PLOT LAYOUT (Combo)
    # Bars (Volume)
    bars = ax1.bar(df['Segment'], df['Households_Pct'], color='#8D99A6', width=0.5, label='% Households') 
    ax1.set_ylabel('% Households', color='#4A4A4A', fontweight='bold') 
    ax1.set_ylim(0, 60)

    # Line (Value)
    ax2 = ax1.twinx() 
    line = ax2.plot(df['Segment'], df['Revenue_Pct'], color='#0B2C4D', linewidth=3, marker='o', label='% Revenue') 
    ax2.set_ylabel('% Revenue', color='#0B2C4D', fontweight='bold') 
    ax2.set_ylim(0, 60)

    # 4. LABELS & LEGEND
    # Add data labels
    for bar in bars: 
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{int(bar.get_height())}%', ha='center', va='bottom', fontsize=9) 
    
    for i, txt in enumerate(df['Revenue_Pct']): 
        ax2.text(i, txt + 2, f'{txt}%', ha='center', va='bottom', color='#0B2C4D', fontweight='bold')

    # Unified Legend
    lines_1, labels_1 = ax1.get_legend_handles_labels() 
    lines_2, labels_2 = ax2.get_legend_handles_labels() 
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)

    # 5. THE PARETO EXPLANATION (The "Footer")
    plt.title('Figure 13: Consumer Segmentation - The "Pareto" Effect', fontsize=12, fontweight='bold', pad=10)

    explanation_text = ( 
        "Note: The 'Pareto Effect' is highlighted by the divergence between volume and value:\n" 
        "The top 20% of households ('Spare No Expense') generate nearly half (48%) of total revenue." 
    ) 
    plt.figtext(0.5, 0.02, explanation_text, ha="center", fontsize=9, style='italic', color='#555555', bbox={"facecolor":"#f0f0f0", "alpha":0.5, "pad":5, "edgecolor":"none"})

    # 6. SAVE
    plt.subplots_adjust(bottom=0.25) # Make room for the footer 
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        # Fallback if specific dir structure doesn't exist (though it should)
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."
             
    output_path = os.path.join(output_dir, 'Figure13_Pareto_With_Note.png')
    plt.savefig(output_path, dpi=300) 
    print(f"Success: Figure 13 regenerated with Pareto explanation footer at {output_path}")

if __name__ == "__main__":
    generate_figure13_with_note()
