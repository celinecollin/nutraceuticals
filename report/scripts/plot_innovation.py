import matplotlib.pyplot as plt
import numpy as np

# Data (15 Data Points)
companies = [
    'Novonesis', 'Zoetis', 'Elanco', 'Vetoquinol', 'DSM-Firmenich', 'Virbac', 'H&H Group', 
    'Symrise (Pet)', 'Phibro', 'ForFarmers', 'Dechra', 'Balchem', 'Givaudan', 'Swedencare', 'Aker BioMarine'
]

# R&D Intensity (%)
rd_intensity = [
    10.8, 8.0, 7.7, 8.1, 5.5, 8.0, 1.8, 
    6.5, 2.9, 0.8, 7.5, 1.5, 8.0, 0.1, 0.5
]

# EBITDA Margin (%)
margins = [
    36.1, 38.0, 20.5, 19.3, 16.5, 16.0, 15.0, 
    22.2, 11.0, 4.0, 22.0, 7.0, 24.0, 22.0, 15.0
]

# Sectors mapped to colors:
# Pharma-Nutra (Green): Novonesis, Zoetis, Elanco, Vetoquinol, Virbac, Dechra
# Ingredient Tech (Blue): DSM-Firmenich, Symrise, Givaudan, Aker
# Brand/Consumer (Purple): H&H Group, Swedencare
# Commodity/Feed (Red): Phibro, ForFarmers, Balchem

colors = [
    '#2ecc71', '#2ecc71', '#2ecc71', '#2ecc71', '#3498db', '#2ecc71', '#9b59b6', 
    '#3498db', '#e74c3c', '#e74c3c', '#2ecc71', '#e74c3c', '#3498db', '#9b59b6', '#3498db'
]

# Set up the plot
plt.figure(figsize=(14, 9)) # Increased size
plt.grid(True, linestyle='--', alpha=0.5)

# Calculate dynamic limits with padding
x_min, x_max = min(rd_intensity), max(rd_intensity)
y_min, y_max = min(margins), max(margins)
x_pad = (x_max - x_min) * 0.15
y_pad = (y_max - y_min) * 0.15

plt.xlim(x_min - x_pad, x_max + x_pad)
plt.ylim(y_min - y_pad, y_max + y_pad)

# Create Scatter Plot
plt.scatter(rd_intensity, margins, c=colors, s=300, alpha=0.8, edgecolors='black', zorder=2)

# Add Labels dealing with overlaps roughly
# Since we can't use adjustText, we use a simple offset logic or manual tweaks for known clusters
for i, txt in enumerate(companies):
    x = rd_intensity[i]
    y = margins[i]
    y_offset = 0.8
    x_offset = 0.1
    
    # Manual Tweaks for known close points from data analysis
    if txt == 'Virbac': y_offset = -1.8
    if txt == 'DSM-Firmenich': y_offset = -1.8
    if txt == 'Swedencare': y_offset = 1.2; x_offset=0
    if txt == 'Aker BioMarine': y_offset = -1.5
    if txt == 'Elanco': y_offset = -1.8
    if txt == 'Dechra': x_offset = -0.6
    if txt == 'Symrise (Pet)': x_offset = -0.8
    if txt == 'Givaudan': y_offset = 1.2
    
    plt.text(x + x_offset, y + y_offset, txt, fontsize=11, weight='semibold', zorder=3)

# Add Threshold Lines
plt.axvline(x=5, color='gray', linestyle='--', alpha=0.5, zorder=1)
plt.axhline(y=15, color='gray', linestyle='--', alpha=0.5, zorder=1)

# Annotations for Quadrants (Dynamic placement)
plt.text(x_min, y_max, 'Innovation Premium\n(High R&D, High Margin)', color='green', alpha=0.6, fontsize=14, ha='left', va='top')
plt.text(x_min, y_min, 'Commodity Trap\n(Low R&D, Low Margin)', color='red', alpha=0.6, fontsize=14, ha='left', va='bottom')

# Titles and Axis
plt.title('The Innovation-Premium Correlation (2024/2025)', fontsize=18, weight='bold', pad=20)
plt.xlabel('R&D Investment (% of Revenue)', fontsize=14)
plt.ylabel('EBITDA Margin (%)', fontsize=14)

# Save
plt.tight_layout()
output_path = '/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/figures/Figure_II_0_1_Innovation_Matrix.png'
plt.savefig(output_path, dpi=300)
print(f"Figure generated successfully at {output_path}")
