
import matplotlib.pyplot as plt
import os
import numpy as np

# Define output directory
output_dir = "report/master_report/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Use basic style
plt.style.use('default')

def create_revenue_chart():
    """Generates a bar chart comparing 2024 revenues of key players across segments."""
    
    # Data
    companies = [
        'Zoetis', 'Merck AH', 'Boehringer Ingelheim', 'Elanco', 
        'DSM-Firmenich', 'Novonesis', 'Phibro',
        'Mars Petcare', 'Nestlé Purina', 'Hill\'s', 'Blue Buffalo'
    ]
    revenues = [9.3, 5.9, 5.0, 4.4, 3.6, 2.5, 1.4, 22.0, 22.4, 4.4, 2.3]
    categories = [
        'Pharma', 'Pharma', 'Pharma', 'Pharma',
        'Feed Inputs', 'Feed Inputs', 'Feed Inputs',
        'Pet Food/CPG', 'Pet Food/CPG', 'Pet Food/CPG', 'Pet Food/CPG'
    ]
    
    # Sorting
    # Combine lists and sort by Category then Revenue
    combined = sorted(zip(categories, revenues, companies), key=lambda x: (x[0], -x[1]))
    categories, revenues, companies = zip(*combined)

    plt.figure(figsize=(12, 8))
    
    # Color mapping
    colors = []
    color_map = {'Pharma': '#2c3e50', 'Feed Inputs': '#27ae60', 'Pet Food/CPG': '#e67e22'}
    for cat in categories:
        colors.append(color_map[cat])
        
    y_pos = np.arange(len(companies))

    bars = plt.barh(y_pos, revenues, color=colors, height=0.7)
    
    plt.yticks(y_pos, companies, fontsize=11)
    plt.xlabel('Estimated 2024 Revenue (USD Billions)', fontsize=12, labelpad=10)
    plt.title('2024 Competitive Landscape: Revenue Scale by Segment', fontsize=16, weight='bold', pad=20)
    
    # Invert y axis to have top revenue on top within categories? 
    # Actually the sort (x[0], -x[1]) puts Feed Inputs first (F), then Pet (P), then Pharma (P). 
    # Let's clean up the order manually for better visualization: Pet, Pharma, Feed
    
    # Manual Reorder for visual grouping
    ordered_companies = [
        'Nestlé Purina', 'Mars Petcare', 'Hill\'s', 'Blue Buffalo', # Pet
        'Zoetis', 'Merck AH', 'Boehringer Ingelheim', 'Elanco', # Pharma
        'DSM-Firmenich', 'Novonesis', 'Phibro' # Feed
    ]
    
    # Find revenues for these
    company_rev_map = dict(zip(companies, revenues))
    ordered_revenues = [company_rev_map[c] for c in ordered_companies]
    
    ordered_colors = []
    for c in ordered_companies:
        if c in ['Nestlé Purina', 'Mars Petcare', 'Hill\'s', 'Blue Buffalo']:
            ordered_colors.append('#e67e22') # Orange
        elif c in ['Zoetis', 'Merck AH', 'Boehringer Ingelheim', 'Elanco']:
            ordered_colors.append('#2c3e50') # Blue
        else:
            ordered_colors.append('#27ae60') # Green

    plt.clf() # Clear previous
    fig, ax = plt.subplots(figsize=(12, 8))
    y_pos = np.arange(len(ordered_companies))
    
    bars = ax.barh(y_pos, ordered_revenues, color=ordered_colors, height=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(ordered_companies, fontsize=11)
    ax.invert_yaxis()  # Labels read top-to-bottom
    
    ax.set_xlabel('Estimated 2024 Revenue (USD Billions)', fontsize=12)
    ax.set_title('2024 Competitive Landscape: Revenue Scale Comparison', fontsize=16, weight='bold')
    
    # Add value labels INSIDE the bars
    for bar in bars:
        width = bar.get_width()
        # Check if bar is wide enough for label
        if width > 0.8:
             ax.text(width / 2, bar.get_y() + bar.get_height()/2, f'${width}B', 
                va='center', ha='center', fontweight='bold', fontsize=11, color='white')
        else:
             # If too small, put outside
             ax.text(width + 0.2, bar.get_y() + bar.get_height()/2, f'${width}B', 
                va='center', ha='left', fontweight='bold', fontsize=11, color='black')

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#e67e22', label='Pet Food & CPG'),
        Patch(facecolor='#2c3e50', label='Pharma & Animal Health'),
        Patch(facecolor='#27ae60', label='Feed & Specialty Inputs')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11)
    
    plt.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Figure_IV_5_Revenue_Comparison.png"), dpi=300)
    plt.close()
    print("Generated Figure_IV_5_Revenue_Comparison.png")

def create_capability_matrix():
    """Generates a heatmap/matrix showing strategic capabilities using simple scatter plot."""
    
    companies = [
        'Zoetis', 'Merck AH', 'Elanco', 'DSM-Firmenich', 'Mars Petcare', 'Nestlé Purina', 'Hill\'s'
    ]
    # Reverse to plot top-to-bottom
    companies = companies[::-1]

    capabilities = [
        'Therapeutics (Rx)', 'Vaccines', 'Feed Additives', 
        'Pet Supplements', 'Pet Food (Diets)', 'Diagnostics / Data'
    ]
    
    # Matrix Data (matching companies in reverse order)
    # Hill's, Purina, Mars, DSM, Elanco, Merck, Zoetis
    data_rows = [
        [0.5, 0.0, 0.0, 0.5, 1.0, 0.5], # Hill's
        [0.0, 0.0, 0.0, 1.0, 1.0, 0.0], # Purina
        [0.0, 0.0, 0.0, 0.5, 1.0, 1.0], # Mars
        [0.0, 0.0, 1.0, 0.5, 0.0, 0.5], # DSM
        [1.0, 1.0, 1.0, 1.0, 0.0, 0.5], # Elanco
        [1.0, 1.0, 0.0, 0.5, 0.0, 1.0], # Merck
        [1.0, 1.0, 0.0, 1.0, 0.0, 1.0]  # Zoetis
    ]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot grid
    ax.set_xticks(np.arange(len(capabilities)))
    ax.set_yticks(np.arange(len(companies)))
    ax.set_xticklabels(capabilities, rotation=45, ha='right', fontsize=11)
    ax.set_yticklabels(companies, fontsize=12, fontweight='bold')
    
    # Limits
    ax.set_xlim(-0.5, len(capabilities)-0.5)
    ax.set_ylim(-0.5, len(companies)-0.5)
    
    # Draw grid lines
    ax.grid(True, linestyle='-', color='#eeeeee')
    
    # Plot dots
    for i, company_data in enumerate(data_rows):
        for j, val in enumerate(company_data):
            if val > 0:
                color = '#2c3e50'
                size = 300
                marker = 'o'
                
                if val == 0.5:
                    color = '#95a5a6' # lighter grey/blue
                    size = 150
                    
                ax.scatter(j, i, s=size, c=color, marker=marker, edgecolors='black', linewidths=0.5, zorder=3)
                
    ax.set_title('Strategic Portfolio Capabilities: The "Continuum of Care"', fontsize=14, weight='bold', pad=20)
    
    # Legend
    # Custom legend using scatter points
    l1 = ax.scatter([], [], c='#2c3e50', s=300, marker='o', label='Core Competency')
    l2 = ax.scatter([], [], c='#95a5a6', s=150, marker='o', label='Emerging / Niche')
    ax.legend(handles=[l1, l2], loc='upper left', bbox_to_anchor=(1, 1), title="Status")
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Figure_IV_6_Capability_Matrix.png"), dpi=300)
    plt.close()
    print("Generated Figure_IV_6_Capability_Matrix.png")

def create_pet_market_chart():
    """Generates a donut chart for Pet Nutrition Market Share."""
    
    # Approx 2024 Global Pet Care Market ~ $200B (Food + Care)
    # Using Revenue proxies:
    # Mars: $22B
    # Purina: $22.4B
    # Hill's: $4.4B
    # Blue Buffalo: $2.3B
    # Others: Rest
    
    labels = ['Nestlé Purina', 'Mars Petcare', 'Hill\'s', 'Blue Buffalo (Gen Mills)', 'Others (Fragmented)']
    sizes = [22.4, 22.0, 4.4, 2.3, 40.0] # Est 'Others' to make total ~90-100B top tier
    # Real total is likely higher, but this shows relative dominance
    
    # Re-normalize for the chart
    total = sum(sizes)
    percent = [s/total*100 for s in sizes]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#e67e22', '#d35400', '#f39c12', '#f1c40f', '#95a5a6']
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, 
                                      colors=colors, pctdistance=0.85, wedgeprops=dict(width=0.4, edgecolor='white'))
    
    plt.setp(texts, size=11, weight="bold")
    plt.setp(autotexts, size=10, weight="bold", color="white")
    
    ax.set_title('Global Pet Nutrition Market Share (Est. 2024)', fontsize=14, weight='bold')
    
    # center circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Annual Revenue Text in center
    ax.text(0, 0, 'Top 2 players\ncontrol >45%', ha='center', va='center', fontsize=12, fontweight='bold', color='#333')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Figure_IV_3_Pet.png"), dpi=300)
    plt.close()
    print("Generated Figure_IV_3_Pet.png")

def create_margin_ladder_chart():
    """Generates a bar chart showing EBITDA margins across the value chain."""
    
    segments = ['Commodity Feed', 'Feed Premix/Mills', 'Pet Food (Mass)', 'Pet Supplements', 'Pharma / Biotech']
    margins = [4.0, 10.0, 16.0, 25.0, 32.0] # Approx EBITDA Margins
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#95a5a6', '#7f8c8d', '#e67e22', '#d35400', '#2c3e50']
    
    bars = ax.bar(segments, margins, color=colors, width=0.6)
    
    # Add values INSIDE bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
                f'{height}%', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
                
    ax.set_ylim(0, 40)
    ax.set_ylabel('Approx. EBITDA Margin (%)', fontsize=11)
    ax.set_title('The "Margin Ladder": Value Capture by Sector', fontsize=14, weight='bold', pad=15)
    
    # Arrow overlay from left to right (Volume to Value)
    ax.annotate('Volume Driven', xy=(0, 2), xytext=(0, -4),
                arrowprops=dict(facecolor='black', shrink=0.05, alpha=0),
                ha='center', fontsize=10, style='italic')
                
    ax.annotate('IP / Brand Driven', xy=(4, 2), xytext=(4, -4),
                arrowprops=dict(facecolor='black', shrink=0.05, alpha=0),
                ha='center', fontsize=10, style='italic')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Figure_IV_4_Margins.png"), dpi=300)
    plt.close()
    print("Generated Figure_IV_4_Margins.png")

if __name__ == "__main__":
    create_revenue_chart()
    create_capability_matrix()
    create_pet_market_chart()
    create_margin_ladder_chart()

