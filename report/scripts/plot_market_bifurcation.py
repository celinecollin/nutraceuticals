import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['R&D Intensity', 'Gross Margin', 'Price Elasticity', 'Customer Retention']
pet_values = [9, 75, 20, 85] # 9/10, 75%, Low Elasticity (inv), High Retention
livestock_values = [2, 15, 90, 40] # 2/10, 15%, High Elasticity, Low Retention

# Normalize for Radar Chart (0-100 scale conceptually)
# R&D: 10% = 100
# Margin: 80% = 100
# Elasticity: Low is "Good" for business -> Inverted scale. 
# Let's use simple bar comparison instead of radar for clarity.

labels = ['R&D Intensity (%)', 'Gross Margin (%)', 'Price Sensitivity', 'Brand Loyalty']
pet_scores = [9, 72, 2, 8] # 1-10 Scale
livestock_scores = [2, 12, 9, 4] # 1-10 Scale

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, pet_scores, width, label='Pet (Emotional Economy)', color='#2ecc71')
rects2 = ax.bar(x + width/2, livestock_scores, width, label='Livestock (ROI Economy)', color='#3498db')

ax.set_ylabel('Relative Intensity (1-10 Scale)')
ax.set_title('The Innovation Divergence: Pet vs. Livestock Structural Economics', weight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Add value labels
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.savefig('/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/figures/Figure_II_0_2_Market_Bifurcation.png', dpi=300)
print("Market Bifurcation generated.")
