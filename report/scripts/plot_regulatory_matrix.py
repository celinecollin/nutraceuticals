import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Setup
fig, ax = plt.subplots(figsize=(12, 8)) # Increased size for better spacing
ax.set_xlim(0, 11) # Expanded limits to prevent cutoff
ax.set_ylim(0, 11)
ax.axis('off')

# Helper for collision detection (manual spacing)
def check_overlap(y_text, y_box_bottom, buffer=0.3):
    return max(y_text, y_box_bottom + buffer)

# Define Zones
# Zone 1: Compliance (Feed Material)
rect1 = patches.Rectangle((1, 1), 3, 3, linewidth=2, edgecolor='#3498db', facecolor='#ebf5fb', zorder=1)
ax.add_patch(rect1)
ax.text(2.5, 3.2, "FEED MATERIAL\n(Compliance)", ha='center', va='center', fontsize=11, weight='bold', color='#2980b9', zorder=2)
# Adjusted text position (Key Attributes)
ax.text(2.5, 1.8, "No Claims\nGeneric Safety", ha='center', va='center', fontsize=9, style='italic', color='#555555', zorder=2)

# Zone 2: Function (Feed Additive)
rect2 = patches.Rectangle((4.5, 4), 3, 4, linewidth=2, edgecolor='#f39c12', facecolor='#fef5e7', zorder=1)
ax.add_patch(rect2)
ax.text(6, 7.2, "FEED ADDITIVE\n(Function)", ha='center', va='center', fontsize=11, weight='bold', color='#d35400', zorder=2)
# Adjusted text position
ax.text(6, 5, "Zootechnical Claims\nPerformance/Efficiency\n(EFSA/FDA Reviewed)", ha='center', va='center', fontsize=9, style='italic', color='#555555', zorder=2)

# Zone 3: Therapy (Vet Drug)
rect3 = patches.Rectangle((8, 7), 2.5, 3, linewidth=2, edgecolor='#e74c3c', facecolor='#fdedec', zorder=1)
ax.add_patch(rect3)
ax.text(9.25, 9.2, "VET DRUG\n(Therapy)", ha='center', va='center', fontsize=11, weight='bold', color='#c0392b', zorder=2)
# Adjusted text position
ax.text(9.25, 8, "Disease Claims\nCure/Mitigate\n(EMA/FDA Approved)", ha='center', va='center', fontsize=9, style='italic', color='#555555', zorder=2)

# Connectors (Arrows)
ax.annotate("", xy=(4.5, 5.5), xytext=(4.0, 2.5), arrowprops=dict(arrowstyle="->", color="gray", lw=1.5, connectionstyle="arc3,rad=-0.2"))
ax.annotate("", xy=(8.0, 8.5), xytext=(7.5, 6.0), arrowprops=dict(arrowstyle="->", color="gray", lw=1.5, connectionstyle="arc3,rad=-0.2"))

# Axis Labels (Manual) - visual arrow
ax.arrow(1, 0.5, 9, 0, head_width=0.2, head_length=0.2, fc='k', ec='k', length_includes_head=True)
ax.text(5.5, 0.2, "Development Cost & Time -->", ha='center', va='top', fontsize=12, weight='bold')

ax.arrow(0.5, 1, 0, 9, head_width=0.2, head_length=0.2, fc='k', ec='k', length_includes_head=True)
ax.text(0.2, 5.5, "Claim Strength (Effect) -->", va='center', ha='right', rotation=90, fontsize=12, weight='bold')

plt.title("The Regulatory Trade-Off: Claims vs. Cost", fontsize=16, weight='bold', pad=20)
plt.tight_layout()

output_path = '/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/figures/Figure_I_3_Regulatory_Matrix.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Regulatory Matrix generated at {output_path}")
