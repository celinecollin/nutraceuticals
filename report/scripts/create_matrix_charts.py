
import matplotlib.pyplot as plt
import os
import numpy as np

# Define output directory
output_dir = "report/master_report/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Style Settings matching the user's reference
COLORS = {
    'gold_standard': '#3b5b75',   # Dark Slate Blue
    'rising_star': '#5ea0d6',     # Medium Blue
    'commodity': '#d9824f',       # Orange/Rust
    'neutral': '#59a6cf',         # Light Blue
    'grid': '#e0e0e0',
    'text': '#333333'
}

def create_matrix_chart(title, data, filename):
    """
    data format: list of dicts:
    {'label': 'Name', 'x': Maturity(0-10), 'y': Evidence(0-10), 'size': Revenue($M), 'type': 'category', 
     'label_dx': float, 'label_dy': float}
    Categories: 'gold_standard', 'rising_star', 'commodity', 'neutral'
    """
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Extract data
    x = [d['x'] for d in data]
    y = [d['y'] for d in data]
    sizes = [d['size'] for d in data]
    labels = [d['label'] for d in data]
    colors = [COLORS[d['type']] for d in data]
    
    # Normalize sizes for bubble display (scale factor)
    sizes_area = [np.sqrt(s) * 30 for s in sizes] 

    # Plot
    scatter = ax.scatter(x, y, s=sizes_area, c=colors, alpha=0.9, edgecolors='white', linewidth=1.5)
    
    # Grid and Ranges
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 11)
    
    # Dashed Quadrant Lines
    ax.axhline(5, color=COLORS['grid'], linestyle='--')
    ax.axvline(5, color=COLORS['grid'], linestyle='--')
    
    # Quadrant Labels
    ax.text(1, 10.5, "RISING STARS\n(Innovation)", color=COLORS['rising_star'], fontsize=10, weight='bold', ha='left', va='top')
    ax.text(10.5, 10.5, "GOLD STANDARD\n(High Value)", color=COLORS['gold_standard'], fontsize=10, weight='bold', ha='right', va='top')
    ax.text(10.5, 1.5, "COMMODITY TRAP\n(Low Efficacy)", color=COLORS['commodity'], fontsize=10, weight='bold', ha='right', va='bottom')
    
    # Labels for Points
    for i, d in enumerate(data):
        label = d['label']
        # Default offsets
        dx = d.get('label_dx', 0)
        dy = d.get('label_dy', 0.3) # Default slightly above
        
        # Calculate new position
        pos_x = d['x'] + dx
        pos_y = d['y'] + dy
        
        ax.text(pos_x, pos_y, label, fontsize=8, ha='center', weight='bold', color='#333333')

    # Axis Labels
    ax.set_xlabel("Market Maturity (Emerging → Commodities)", fontsize=10, weight='bold')
    ax.set_ylabel("Clinical Evidence (Anecdotal → Level A RCTs)", fontsize=10, weight='bold')
    
    # Title
    ax.set_title(title, fontsize=14, weight='bold', pad=20)
    
    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['grid'])
    ax.spines['bottom'].set_color(COLORS['grid'])
    
    # Save
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Generated {output_path}")

# --- DATA DEFINITIONS ---

# II.1 Mobility
data_mobility = [
    {'label': 'Omega-3 (EPA/DHA)', 'x': 9, 'y': 9, 'size': 1300, 'type': 'gold_standard'},
    {'label': 'UC-II Collagen', 'x': 5.5, 'y': 8, 'size': 200, 'type': 'rising_star'},
    {'label': 'Green Lipped Mussel', 'x': 5, 'y': 5, 'size': 185, 'type': 'neutral'},
    {'label': 'Egg Shell Membrane', 'x': 2.5, 'y': 5, 'size': 65, 'type': 'neutral'},
    {'label': 'Glucosamine', 'x': 9, 'y': 3, 'size': 1100, 'type': 'commodity', 'label_dy': 0.5},
    {'label': 'Chondroitin', 'x': 8.5, 'y': 2, 'size': 800, 'type': 'commodity'},
    {'label': 'MSM', 'x': 7, 'y': 4, 'size': 240, 'type': 'neutral'},
    {'label': 'Boswellia/Curcumin', 'x': 4, 'y': 6, 'size': 125, 'type': 'rising_star'}
]

# II.2 Gut Health (FIXED OVERLAPS)
data_gut = [
    {'label': 'Probiotics', 'x': 9, 'y': 9, 'size': 6000, 'type': 'gold_standard', 'label_dy': -1.8}, # Huge bubble, move label way down
    {'label': 'Enzymes (Phytase)', 'x': 9.5, 'y': 9.5, 'size': 1800, 'type': 'gold_standard', 'label_dx': 0.8, 'label_dy': -0.3}, # Move right to avoid title collision
    {'label': 'Prebiotics', 'x': 7, 'y': 6, 'size': 650, 'type': 'neutral'},
    {'label': 'Synbiotics', 'x': 6, 'y': 7, 'size': 1250, 'type': 'rising_star'},
    {'label': 'Postbiotics', 'x': 3, 'y': 8, 'size': 500, 'type': 'rising_star'},
    {'label': 'Organic Acids', 'x': 8, 'y': 5, 'size': 4000, 'type': 'neutral', 'label_dy': -1.2}, # Big bubble, move down
    {'label': 'Herbal Soothers', 'x': 2, 'y': 2, 'size': 100, 'type': 'neutral'}
]

# II.3 Immunity
data_immunity = [
    {'label': 'Seaweed/Polysaccharides', 'x': 5, 'y': 5, 'size': 4460, 'type': 'neutral', 'label_dy': -1.2}, # Big bubble
    {'label': 'Spray-Dried Plasma', 'x': 8, 'y': 9, 'size': 2200, 'type': 'gold_standard', 'label_dy': 0.8},
    {'label': 'Nucleotides', 'x': 6, 'y': 7, 'size': 622, 'type': 'rising_star'},
    {'label': 'Beta-Glucans', 'x': 7, 'y': 6, 'size': 38, 'type': 'neutral'},
    {'label': 'Lactoferrin', 'x': 3, 'y': 4, 'size': 297, 'type': 'neutral'},
    {'label': 'Vit C/E/Selenium', 'x': 9, 'y': 6, 'size': 430, 'type': 'commodity'}
]

# II.4 Cognitive
data_cognitive = [
    {'label': 'MCTs', 'x': 8, 'y': 9, 'size': 450, 'type': 'gold_standard', 'label_dy': 0.5},
    {'label': 'DHA', 'x': 9, 'y': 8, 'size': 350, 'type': 'gold_standard', 'label_dy': -0.5},
    {'label': 'Antioxidants', 'x': 8.5, 'y': 7, 'size': 300, 'type': 'commodity'},
    {'label': 'SAMe', 'x': 6, 'y': 5, 'size': 100, 'type': 'neutral'},
    {'label': 'Phosphatidylserine', 'x': 4, 'y': 4, 'size': 15, 'type': 'rising_star'}
]

# II.5 Calming (FIXED OVERLAPS)
data_calming = [
    {'label': 'Multi-Complexes', 'x': 8, 'y': 5, 'size': 500, 'type': 'neutral', 'label_dy': 0.6}, # Move up
    {'label': 'CBD/Hemp', 'x': 5, 'y': 6, 'size': 330, 'type': 'rising_star'},
    {'label': 'Alpha-Casozepine', 'x': 6, 'y': 8, 'size': 30, 'type': 'gold_standard'}, 
    {'label': 'L-Theanine', 'x': 6.5, 'y': 7, 'size': 50, 'type': 'rising_star'},
    {'label': 'Tryptophan', 'x': 7.5, 'y': 5, 'size': 80, 'type': 'commodity', 'label_dy': -0.5}, # Move down and
    {'label': 'Botanicals', 'x': 8, 'y': 3, 'size': 100, 'type': 'commodity'}
]

# II.6 Performance
data_performance = [
    {'label': 'Yeast Culture', 'x': 9, 'y': 7, 'size': 2000, 'type': 'gold_standard', 'label_dy': -0.8},
    {'label': 'Protected Amino Acids', 'x': 8, 'y': 8, 'size': 1200, 'type': 'gold_standard'},
    {'label': 'Xylanase', 'x': 9, 'y': 9, 'size': 1000, 'type': 'gold_standard'}, 
    {'label': 'Phytagenics', 'x': 6, 'y': 6, 'size': 890, 'type': 'neutral'},
    {'label': 'Protease', 'x': 7, 'y': 8, 'size': 200, 'type': 'rising_star'}
]

# II.7 Niches
data_niches = [
    {'label': 'Astaxanthin (Aqua)', 'x': 9, 'y': 8, 'size': 1350, 'type': 'gold_standard', 'label_dy': 0.8},
    {'label': 'Zinc Methionine', 'x': 8, 'y': 7, 'size': 175, 'type': 'neutral'},
    {'label': 'Omega-6', 'x': 8.5, 'y': 6, 'size': 120, 'type': 'commodity'},
    {'label': 'Biotin', 'x': 9, 'y': 4, 'size': 56, 'type': 'commodity', 'label_dy': -0.4}
]

# II.8 Ectoparasite (Natural)
data_ectoparasite = [
    {'label': 'Natural Repellents', 'x': 8, 'y': 4, 'size': 550, 'type': 'commodity'}, 
    {'label': 'Skin Barrier Stacks', 'x': 6, 'y': 5, 'size': 150, 'type': 'neutral'},
    {'label': 'Garlic', 'x': 9, 'y': 2, 'size': 40, 'type': 'commodity'}
]

# II.9 Nutrigenomics
data_nutrigenomics = [
    {'label': 'Gut Integrity Tools', 'x': 8, 'y': 8, 'size': 2170, 'type': 'gold_standard', 'label_dy': 0.8},
    {'label': 'Biomarkers', 'x': 4, 'y': 7, 'size': 613, 'type': 'rising_star'},
    {'label': 'Nrf2 Activators', 'x': 3, 'y': 6, 'size': 200, 'type': 'rising_star'},
    {'label': 'Vaccine Adjuncts', 'x': 5, 'y': 6, 'size': 300, 'type': 'neutral'}
]

# II.10 Delivery
data_delivery = [
    {'label': 'Rumen Protection', 'x': 9, 'y': 9, 'size': 3800, 'type': 'gold_standard', 'label_dy': -1.2},
    {'label': 'Soft Chews', 'x': 9, 'y': 8, 'size': 2450, 'type': 'gold_standard', 'label_dy': 0.8}, 
    {'label': 'Smart Boluses', 'x': 6, 'y': 8, 'size': 2500, 'type': 'rising_star'},
    {'label': 'Aqua Coatings', 'x': 7, 'y': 7, 'size': 1120, 'type': 'neutral'},
    {'label': 'Nanocarriers', 'x': 3, 'y': 7, 'size': 180, 'type': 'rising_star'}
]

# II.11 Sustainability
data_sustainability = [
    {'label': 'Nitrogen Efficiency', 'x': 8, 'y': 8, 'size': 2250, 'type': 'gold_standard', 'label_dy': -0.8},
    {'label': 'Phytase (P)', 'x': 9.5, 'y': 9.5, 'size': 640, 'type': 'gold_standard', 'label_dy': 0.6},
    {'label': 'Algal DHA', 'x': 6, 'y': 7, 'size': 250, 'type': 'rising_star'},
    {'label': '3-NOP (Methane)', 'x': 4, 'y': 9, 'size': 60, 'type': 'rising_star'}, 
    {'label': 'Asparagopsis', 'x': 2, 'y': 6, 'size': 25, 'type': 'rising_star'},
    {'label': 'Natural Reducers', 'x': 5, 'y': 4, 'size': 120, 'type': 'neutral'}
]

if __name__ == "__main__":
    create_matrix_chart("Mobility Ingredients: Evidence vs. Maturity", data_mobility, "Figure_II_1_Matrix.png")
    create_matrix_chart("Gut Health Ingredients: Evidence vs. Maturity", data_gut, "Figure_II_2_Matrix.png")
    create_matrix_chart("Immunity Ingredients: Evidence vs. Maturity", data_immunity, "Figure_II_3_Matrix.png")
    create_matrix_chart("Cognitive Ingredients: Evidence vs. Maturity", data_cognitive, "Figure_II_4_Matrix.png")
    create_matrix_chart("Calming Ingredients: Evidence vs. Maturity", data_calming, "Figure_II_5_Matrix.png")
    create_matrix_chart("Performance Ingredients: Evidence vs. Maturity", data_performance, "Figure_II_6_Matrix.png")
    create_matrix_chart("Niche Ingredients: Evidence vs. Maturity", data_niches, "Figure_II_7_Matrix.png")
    create_matrix_chart("Ectoparasite Ingredients: Evidence vs. Maturity", data_ectoparasite, "Figure_II_8_Matrix.png")
    create_matrix_chart("Nutrigenomics: Evidence vs. Maturity", data_nutrigenomics, "Figure_II_9_Matrix.png")
    create_matrix_chart("Delivery Systems: Tech Maturity vs. Validation", data_delivery, "Figure_II_10_Matrix.png")
    create_matrix_chart("Sustainability Tools: Evidence vs. Maturity", data_sustainability, "Figure_II_11_Matrix.png")
