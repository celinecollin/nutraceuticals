import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_strategic_matrix():
    # Setup the figure layout
    fig = plt.figure(figsize=(12, 14))
    fig.patch.set_facecolor('white')
    
    # === PART 1: THE MATIX ===
    # Add axes for the matrix (top half) with more height
    ax_matrix = fig.add_axes([0.1, 0.55, 0.8, 0.4])
    ax_matrix.set_xlim(0, 10)
    ax_matrix.set_ylim(0, 10)
    ax_matrix.axis('off')
    
    # Title for Matrix
    ax_matrix.text(5, 10.5, 'The "Winner\'s Matrix" (Strategic Positioning)', 
                  ha='center', va='center', fontsize=18, fontweight='bold', color='#003057')
    
    # Draw Quadrant backgrounds
    # Q1: High Evidence / High Brand (Top Right)
    q1 = patches.Rectangle((5, 5), 5, 5, facecolor='#e6f3ff', edgecolor='white') # Light Blue
    ax_matrix.add_patch(q1)
    
    # Q2: Low Evidence / High Channel Power (Bottom Right -> "High Channel" maps to High Brand Axis typically, 
    # but let's interpret X as "Commercial/Brand Power" and Y as "Clinical Evidence")
    # So Q2 (Low Ev, High Channel) is Bottom Right
    q2 = patches.Rectangle((5, 0), 5, 5, facecolor='#fff2cc', edgecolor='white') # Light Yellow/Orange
    ax_matrix.add_patch(q2)
    
    # Q3: Low Evidence / Low Brand (Bottom Left)
    q3 = patches.Rectangle((0, 0), 5, 5, facecolor='#ffe6e6', edgecolor='white') # Light Red
    ax_matrix.add_patch(q3)
    
    # Empty Top Left (High Evidence / Low Brand?) - Not defined in text, leave grey or white
    q4 = patches.Rectangle((0, 5), 5, 5, facecolor='#f5f5f5', edgecolor='white') # Grey
    ax_matrix.add_patch(q4)
    ax_matrix.text(2.5, 7.5, "Niche / Scientific\n(Not Strategic Focus)", ha='center', va='center', color='#888', fontstyle='italic')

    # Axes Labels
    ax_matrix.arrow(0, 0, 10, 0, head_width=0.3, head_length=0.3, fc='black', ec='black') # X Axis
    ax_matrix.arrow(0, 0, 0, 10, head_width=0.3, head_length=0.3, fc='black', ec='black') # Y Axis
    
    ax_matrix.text(10.5, 0, "Brand & Channel Power", ha='center', va='center', fontweight='bold')
    ax_matrix.text(0, 10.5, "Clinical Evidence", ha='center', va='center', fontweight='bold', rotation=0)

    # Quadrant 1 Content
    ax_matrix.text(7.5, 9, 'Quadrant 1: The "Clinical Moat"', ha='center', va='center', fontweight='bold', fontsize=12)
    ax_matrix.text(7.5, 7.5, 'Examples: Nutramax, Swedencare,\nHill\'s Prescription Diet\n\nStrategy: Premium pricing, vet endorsement\n\nAction: Buy/Overweight', 
                  ha='center', va='center', fontsize=10, wrap=True)

    # Quadrant 2 Content
    ax_matrix.text(7.5, 4, 'Quadrant 2: The "Volume Scale"', ha='center', va='center', fontweight='bold', fontsize=12)
    ax_matrix.text(7.5, 2.5, 'Examples: Private Label (Amazon/Chewy),\nCommodity Feed Premixers\n\nStrategy: Cost leadership, efficiency\n\nAction: Hold for cash flow', 
                  ha='center', va='center', fontsize=10, wrap=True)

    # Quadrant 3 Content
    ax_matrix.text(2.5, 4, 'Quadrant 3: The "Speculative Fringe"', ha='center', va='center', fontweight='bold', fontsize=12)
    ax_matrix.text(2.5, 2.5, 'Examples: Generic white-label,\n"me-too" dropshippers\n\nStrategy: Price wars, churn-and-burn\n\nAction: Avoid', 
                  ha='center', va='center', fontsize=10, wrap=True)

    # === PART 2: THE WATCHLIST TABLE ===
    # Add axes for table (bottom half)
    ax_table = fig.add_axes([0.1, 0.1, 0.8, 0.35])
    ax_table.axis('off')
    
    # Title for Table
    ax_table.text(0.5, 1.1, "Watchlist: The Top Picks", ha='center', va='center', fontsize=18, fontweight='bold', color='#003057')

    # Table Data
    col_labels = ['Ticker/Company', 'Segment', 'Moat Source', 'Catalyst']
    table_data = [
        ['Zoetis (ZTS)', 'Pharma/Pet', 'Review-gated\nformulations', 'Expanding "Clarify"\ndiagnostics integration'],
        ['Novonesis', 'Biotech', 'Fermentation IP', 'Biosolutions growth >8%'],
        ['Swedencare', 'Pet Nutra', 'Brand + Oral Health\nPatent', 'US market expansion'],
        ['DSM-Firmenich', 'Feed', 'Bovaer (Methane) IP', 'ESG procurement\nmandates']
    ]
    
    # Colors
    header_color = '#003057'
    row_colors = ['#f4f6f8', 'white']
    
    # Draw Table
    table = ax_table.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='left')
    
    # Style Table
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5) # Increase row height
    
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(header_color)
            cell.set_edgecolor('white')
            cell.set_height(0.15)
        else:
            cell.set_facecolor(row_colors[(row-1)%2])
            cell.set_edgecolor('#dddddd')
            cell.set_height(0.15)
            # Center vertically
            cell.set_text_props(va='center')

    # Save
    output_path = 'report/master_report/figures/Figure_IV_5_Strategic_matrix.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Figure saved to {output_path}")

if __name__ == "__main__":
    create_strategic_matrix()
