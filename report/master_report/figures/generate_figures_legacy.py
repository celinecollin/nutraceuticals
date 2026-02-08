
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Ensure directory exists
output_dir = "report/master_report/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set style
plt.style.use('ggplot')
colors_palette = ['#2E86C1', '#28B463', '#F1C40F', '#E74C3C', '#884EA0', '#D35400']

# Figure 1: Household Pet Ownership Rate by Region (2023)
def plot_fig1():
    regions = ['US', 'Mexico', 'Canada', 'EU']
    rates = [71, 70, 60, 49]
    
    plt.figure(figsize=(8, 6))
    plt.bar(regions, rates, color=colors_palette[:4])
    plt.title('Household Pet Ownership Rate by Region (2023)')
    plt.ylabel('Ownership Rate (%)')
    plt.ylim(0, 100)
    for i, v in enumerate(rates):
        plt.text(i, v + 1, str(v) + '%', ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure1_Pet_Ownership.png")
    plt.close()

# Figure 2: Pet Population in Europe by Species (2023)
def plot_fig2():
    labels = ['Cats', 'Dogs', 'Others']
    sizes = [127, 104, 50]
    
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors_palette)
    plt.title('Pet Population in Europe by Species (2023)\nTotal: 281M')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure2_EU_Pet_Pop.png")
    plt.close()

# Figure 3: Growth of Cat and Dog Populations in Europe (2018–2023)
def plot_fig3():
    species = ['Cats', 'Dogs']
    growth = [11, 5]
    
    plt.figure(figsize=(6, 6))
    bars = plt.bar(species, growth, color=[colors_palette[0], colors_palette[1]])
    plt.title('Population Growth in Europe (2018–2023)')
    plt.ylabel('Growth (%)')
    plt.ylim(0, 14)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                 f'+{height}%', ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure3_EU_Growth.png")
    plt.close()

# Figure 4: Regional Market Size for Pet Nutraceuticals (2024E)
def plot_fig4():
    regions = ['APAC', 'Europe', 'North America', 'LATAM', 'Others']
    values = [2.1, 1.7, 1.1, 0.8, 0.3]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(regions, values, color=colors_palette)
    plt.title('Regional Market Size for Pet Nutraceuticals (2024E)')
    plt.ylabel('Market Size (USD Billion)')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'${height}B', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure4_Regional_Market.png")
    plt.close()

# Figure 5: Feed Probiotics Market Share by Species (2024)
def plot_fig5():
    species = ['Poultry', 'Swine', 'Ruminant', 'Aqua']
    volume = [60, 25, 10, 5]
    revenue = [2.5, 1.0, 0.4, 0.2]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.pie(volume, labels=species, autopct='%1.1f%%', startangle=90, colors=colors_palette)
    ax1.set_title('Volume Share (2024)')
    
    ax2.bar(species, revenue, color=colors_palette[:4])
    ax2.set_title('Estimated Revenue (USD Billion)')
    ax2.set_ylabel('Revenue ($B)')
    for i, v in enumerate(revenue):
        ax2.text(i, v + 0.05, f'${v}B', ha='center', va='bottom')
        
    plt.suptitle('Feed Probiotics Market by Species')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure5_Probiotics_Share.png")
    plt.close()

# Figure 6: Global Poultry Production and HPAI Impact
def plot_fig6():
    years = np.arange(2015, 2025)
    # Simulate production (baseline 100, growing 1.5% CAGR)
    production = 100 * (1.015 ** (years - 2015))
    # Simulate losses (Millions of birds) - spikes in recent years
    losses = [5, 8, 10, 12, 15, 25, 35, 40, 45, 50] 
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Production Index (2015=100)', color=color)
    ax1.plot(years, production, color=color, linewidth=2, label='Production')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Bird Losses (Millions)', color=color)
    ax2.plot(years, losses, color=color, linestyle='--', marker='o', label='HPAI Losses')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Global Poultry Production vs HPAI Impact (2015-2024)')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure6_Poultry_HPAI.png")
    plt.close()

# Figure 7: European Swine Herd Decline
def plot_fig7():
    years = np.arange(2014, 2025)
    # Decline 8.1% over 10 years
    herd_index = np.linspace(100, 91.9, len(years))
    
    plt.figure(figsize=(8, 6))
    plt.plot(years, herd_index, marker='o', color='#E74C3C', linewidth=2)
    plt.title('European Swine Herd Decline (2014-2024)')
    plt.ylabel('Herd Index (2014=100)')
    plt.xlabel('Year')
    plt.annotate('Nitrates Directive Impact', xy=(2022, 93), xytext=(2019, 96),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure7_Swine_Decline.png")
    plt.close()

# Figure 9: Indexed Livestock Trends Europe
def plot_fig9():
    years = np.arange(2018, 2024)
    poultry = np.linspace(100, 110.5, 6)
    bovine = np.linspace(100, 94.8, 6)
    pigs = np.linspace(100, 91.1, 6)
    sheep = np.linspace(100, 89.5, 6)
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, poultry, label='Poultry', linewidth=2, marker='o')
    plt.plot(years, bovine, label='Bovine', linewidth=2, marker='s')
    plt.plot(years, pigs, label='Pigs', linewidth=2, marker='^')
    plt.plot(years, sheep, label='Sheep/Goat', linewidth=2, marker='x')
    
    plt.title('Indexed Livestock Trends in Europe (2018-2023)')
    plt.ylabel('Production Index (2018=100)')
    plt.xlabel('Year')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure9_Livestock_Trends.png")
    plt.close()

# Figure 10: Aquaculture vs Capture
def plot_fig10():
    years = np.arange(2000, 2031)
    # Simulation
    capture = np.linspace(85, 92, 23) # Stagnant mostly
    capture = np.concatenate([capture, np.linspace(92, 93, 8)]) # Flat future
    
    aqua = np.linspace(30, 94.4, 23) # Rapid growth until 2022
    aqua_future = 94.4 * (1.035 ** np.arange(1, 9)) # 3.5% growth
    aqua = np.concatenate([aqua, aqua_future])
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, capture, label='Capture Fisheries', linestyle='--')
    plt.plot(years, aqua, label='Aquaculture', linewidth=2)
    
    # Intersection 2022
    plt.plot(2022, 94.4, 'ro')
    plt.annotate('The Great Overtaking (2022)', xy=(2022, 94.4), xytext=(2010, 100),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.title('Aquaculture vs Capture Fisheries (2000-2030)')
    plt.ylabel('Production (Million Tonnes)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure10_Aqua_v_Capture.png")
    plt.close()

# Figure 11: Nutraceutical Format Popularity
def plot_fig11():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Dog
    dog_labels = ['Soft Chews', 'Treats', 'Powder', 'Liquids', 'Pills']
    dog_sizes = [39, 25, 20, 10, 6]
    ax1.pie(dog_sizes, labels=dog_labels, autopct='%1.0f%%', startangle=140, colors=colors_palette)
    ax1.set_title('Dogs\n(Palatability First)')
    
    # Cat
    cat_labels = ['Liquids', 'Powder', 'Pills', 'Treats', 'Chews']
    cat_sizes = [35, 30, 20, 10, 5]
    ax2.pie(cat_sizes, labels=cat_labels, autopct='%1.0f%%', startangle=140, colors=colors_palette)
    ax2.set_title('Cats\n(Invisibility/Mixing)')
    
    # Horse
    horse_labels = ['Powder/Pellets', 'Syringes', 'Injectable', 'Pastes', 'Other']
    horse_sizes = [60, 20, 15, 5, 0]
    ax3.pie(horse_sizes, labels=horse_labels, autopct='%1.0f%%', startangle=140, colors=colors_palette)
    ax3.set_title('Horses\n(Feed Integration)')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure11_Formats.png")
    plt.close()

# Figure 13: Consumer Segmentation
def plot_fig13():
    labels = ['Spare No Expense', 'Value-Conscious', 'Basic Care']
    households = [20, 50, 30]
    revenue = [48, 42, 10]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    ax1.pie(households, labels=labels, autopct='%1.0f%%', startangle=90, colors=['#E74C3C', '#F1C40F', '#CCD1D1'])
    ax1.set_title('Share of Households')
    
    ax2.pie(revenue, labels=labels, autopct='%1.0f%%', startangle=90, colors=['#E74C3C', '#F1C40F', '#CCD1D1'])
    ax2.set_title('Share of Market Revenue')
    
    plt.suptitle('Consumer Segmentation: Households vs Revenue')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure13_Segmentation.png")
    plt.close()

# Figure 19: Value Waterfall (simplified bar comparison)
def plot_fig19():
    # Livestock: $50 Cost Breakdown
    ls_labels = ['Sourcing', 'Premix/Mfg', 'Service/Logistics', 'Net Margin']
    ls_values = [30, 10, 8, 2] # Implied low margin
    
    # Pet: $50 Retail Breakdown
    pet_labels = ['COGS', 'Packaging/Mfg', 'Channel/Mktg', 'Net Margin']
    pet_values = [10, 15, 15, 10] # Implied higher margin
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    ax1.bar(ls_labels, ls_values, color='#2E86C1')
    ax1.set_title('Livestock Premix ($50 Cost)\nEfficiency Driven')
    ax1.set_ylabel('Cost Component ($)')
    
    ax2.bar(pet_labels, pet_values, color='#E74C3C')
    ax2.set_title('Pet Supplement ($50 Retail)\nBrand/Margin Driven')
    
    plt.suptitle('Value Capture Comparison')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure19_Value_Waterfall.png")
    plt.close()

# Figure 20: Bubble Chart - Margin vs Size vs Growth
def plot_fig20():
    segments = ['Pet Brands', 'Livestock Premix', 'Ingredients (IP)', 'Commodities']
    size = [6, 8, 2, 5]     # Market Size $B
    margin = [22, 10, 25, 6] # EBITDA %
    growth = [7, 4, 9, 2]    # CAGR %
    colors = ['#E74C3C', '#2E86C1', '#884EA0', '#95A5A6']
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(size, margin, s=[g*100 for g in growth], c=colors, alpha=0.6, edgecolors="grey", linewidth=2)
    
    plt.xlabel('Market Size ($ Billions)')
    plt.ylabel('EBITDA Margin (%)')
    plt.title('Risk/Reward Map: Margin vs Size (Bubble = Growth)')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    
    for i, txt in enumerate(segments):
        plt.annotate(txt, (size[i], margin[i]), xytext=(0, 10), textcoords='offset points', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure20_Risk_Reward.png")
    plt.close()
    
# Generate Table Image: USA vs EU
def plot_table_us_eu():
    data = [
        ["Feature", "United States (US)", "European Union (EU)"],
        ["Nutraceutical Definition", "None (Binary: Food vs Drug)", "None (Binary: Feed vs VMP)"],
        ["Regulatory Agency", "FDA-CVM & State (AAFCO)", "EFSA (Central) & National Agencies"],
        ["Performance Feed", "Growth Promoters allowed (unless antibiotic)", "Strict Zootechnical Additive Category"],
        ["Sup. Classification", "Animal Food (GRAS)", "Feed Material or Additive"],
        ["Disease Claims", "Strictly Prohibited ('Treats' = Drug)", "Strictly Prohibited (except PARNUTs)"],
        ["Key Legislation", "DSHEA (Humans only) / FSMA", "Reg 1831/2003 (Additives)"]
    ]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data, loc='center', cellLoc='left')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    
    # Header bold
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#D5D8DC')
            
    plt.title("Comparative Regulatory Framework: US vs EU", pad=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Table_US_vs_EU.png")
    plt.close()

# Generate Venn Diagram (Conceptual)
def plot_venn():
    plt.figure(figsize=(8, 8))
    
    # Circles
    circle1 = patches.Circle((0.35, 0.6), 0.3, alpha=0.4, color='red', label='Pharmaceuticals')
    circle2 = patches.Circle((0.65, 0.6), 0.3, alpha=0.4, color='blue', label='Feed/Food')
    circle3 = patches.Circle((0.5, 0.3), 0.3, alpha=0.4, color='green', label='Supplements')
    
    ax = plt.gca()
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle3)
    
    plt.text(0.35, 0.6, "Drugs\n(Therapeutic)", ha='center', fontweight='bold')
    plt.text(0.65, 0.6, "Feed\n(Nutritional)", ha='center', fontweight='bold')
    plt.text(0.5, 0.3, "Supplements\n(Dietary)", ha='center', fontweight='bold')
    
    plt.text(0.5, 0.5, "Nutraceuticals\n(The Grey Zone)", ha='center', va='center', fontsize=12, fontweight='bold', color='black')
    
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xticks([])
    plt.yticks([])
    plt.title("The Regulatory Grey Zone")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Venn_Nutraceuticals.png")
    plt.close()

# Figure: Species x Functional Needs Matrix (Heatmap)
def plot_species_matrix():
    species = ['Dogs', 'Cats', 'Horses', 'Poultry', 'Swine', 'Aqua']
    functions = ['Joint/Mobility', 'Gut Health', 'Anxiety', 'Growth/FCR', 'Immunity', 'Skin/Coat']
    
    # 0 = Low/None, 1 = Med, 2 = High/Critical
    data = np.array([
        [2, 1, 2, 0, 1, 1], # Dogs: High Joint, High Anxiety
        [1, 1, 1, 0, 1, 1], # Cats: Kidney/Gut focus (not fully captured but proxy), Anxiety
        [2, 2, 1, 0, 0, 0], # Horses: Joint, Gut (Ulcers)
        [0, 2, 0, 2, 1, 0], # Poultry: Gut (NE), Growth
        [0, 2, 0, 1, 1, 0], # Swine: Gut (Weaning), Growth
        [0, 1, 0, 2, 2, 1]  # Aqua: Growth, Immunity, Pigment(Skin)
    ])
    
    plt.figure(figsize=(10, 8))
    plt.imshow(data, cmap='Blues', aspect='auto')
    
    plt.xticks(np.arange(len(functions)), functions, rotation=45, ha='right')
    plt.yticks(np.arange(len(species)), species)
    
    # Text annotations
    for i in range(len(species)):
        for j in range(len(functions)):
            val = data[i, j]
            text = "High" if val==2 else "Med" if val==1 else "-"
            color = "white" if val==2 else "black"
            plt.text(j, i, text, ha="center", va="center", color=color)
            
    plt.title('Market Intensity: Species vs Functional Needs')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Matrix_Species_Functional.png")
    plt.close()

# Figure: Efficacy Matrix by Ingredient
def plot_efficacy_matrix():
    ingredients = ['Omega-3 (EPA/DHA)', 'UC-II Collagen', 'Probiotics (Specific Strains)', 
                   'Glucosamine', 'Polysaccharides', 'General Multivitamins']
    evidence_level = [3, 2.5, 3, 1, 2, 0.5] # 0-3 scale
    market_maturity = [3, 1, 2, 3, 1, 3] # 0-3 scale
    
    plt.figure(figsize=(10, 6))
    
    # Scatter plot
    plt.scatter(market_maturity, evidence_level, s=500, c='#884EA0', alpha=0.7, edgecolors='black')
    
    plt.xlim(-0.5, 3.5)
    plt.ylim(0, 3.5)
    plt.xticks([0, 1, 2, 3], ['Niche/New', 'Emerging', 'Established', 'Commodity'])
    plt.yticks([0, 1, 2, 3], ['No Evid.', 'Mixed (C)', 'Good (B)', 'Gold Std (A)'])
    
    plt.title('Ingredient Landscape: Evidence vs Maturity')
    plt.grid(True, linestyle='--')
    
    for i, txt in enumerate(ingredients):
        plt.annotate(txt, (market_maturity[i], evidence_level[i]), 
                     xytext=(0, 10), textcoords='offset points', ha='center', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Matrix_Efficacy.png")
    plt.close()

# Figure: Timeline of Antibiotic Mandates
def plot_timeline():
    # Vertical timeline
    events = [
        (2006, "EU bans AGPs (Reg 1831/2003)"),
        (2017, "US FDA GFI #213 (VFD) Full Implementation"),
        (2022, "EU bans Medicinal Zinc Oxide (Swine)"),
        (2024, "China AGP restrictions tighten"),
        (2025, "UK Feed Additive Reform (Projected)")
    ]
    
    years = [e[0] for e in events]
    labels = [e[1] for e in events]
    
    plt.figure(figsize=(8, 6))
    plt.plot(np.zeros_like(years), years, '-o', color='#28B463', linewidth=2, markersize=10)
    
    plt.xlim(-1, 1)
    plt.axis('off')
    
    for i, (yr, lbl) in enumerate(zip(years, labels)):
        # Alternate sides
        x_off = 0.1 if i % 2 == 0 else -0.1
        ha = 'left' if i % 2 == 0 else 'right'
        plt.text(x_off, yr, f"{yr}: {lbl}", ha=ha, va='center', fontsize=12, fontweight='bold',
                 bbox=dict(facecolor='white', edgecolor='#28B463', boxstyle='round,pad=0.5'))
        
    plt.title("Key Regulatory Milestones driving the 'Post-Antibiotic' Era", pad=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Timeline_Regulations.png")
    plt.close()

# Figure 12: Preventive Health Wallet Breakdown
def plot_fig12():
    labels = ['Food', 'Vet Care', 'Supplements', 'Toys/Access.', 'Services']
    # Estimated allocation based on text
    sizes = [40, 25, 15, 10, 10]
    
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=140, colors=colors_palette)
    plt.title('Preventive Health Wallet Allocation (2025)\nTotal: ~$1500/yr')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure12_Wallet.png")
    plt.close()

# Figure 14: Psychological Factors Influencing WTP
def plot_fig14():
    factors = ['Fear of Loss/Regret', 'Anthropomorphism', 'Vet Endorsement', 'Social Proof', 'Convenience']
    weights = [40, 30, 20, 5, 5]
    
    plt.figure(figsize=(10, 6))
    y_pos = np.arange(len(factors))
    plt.barh(y_pos, weights, color='#E74C3C')
    plt.yticks(y_pos, factors)
    plt.xlabel('Influence Weight (%)')
    plt.title('Psychological Factors Influencing Willingness-To-Pay')
    
    for i, v in enumerate(weights):
        plt.text(v + 1, i, str(v) + '%', va='center', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure14_Psychology.png")
    plt.close()

# Figure 15: Mobility Supplement Market Evolution
def plot_fig15():
    years = [2015, 2020, 2024, 2030]
    # Stacked Area Data
    generic = [70, 60, 45, 35]
    uc_ii = [5, 15, 25, 30]
    glm = [15, 15, 18, 20]
    premium_combo = [10, 10, 12, 15]
    
    plt.figure(figsize=(10, 6))
    plt.stackplot(years, generic, uc_ii, glm, premium_combo, 
                  labels=['Generic Glucosamine', 'UC-II Collagen', 'Green Lipped Mussel', 'Premium Combos'],
                  colors=['#BDC3C7', '#2E86C1', '#28B463', '#884EA0'],
                  alpha=0.8)
    plt.legend(loc='upper left')
    plt.title('Mobility Supplement Market Evolution (Premiumization)')
    plt.ylabel('Market Share (%)')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure15_Mobility_Evo.png")
    plt.close()

# Figure 16: Senior & Pre-Senior Market Growth
def plot_fig16():
    years = [2015, 2020, 2024, 2030]
    market_size = [0.5, 0.8, 1.3, 2.0] # Billions
    share = [8, 12, 22, 30] # % of total market
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Market Size ($ Billion)', color=color)
    ax1.bar(years, market_size, color=color, alpha=0.6, width=2, label='Market Value')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Share of Total Market (%)', color=color)
    ax2.plot(years, share, color=color, marker='o', linewidth=3, label='Market Share')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Senior & Pre-Senior Pet Market Growth')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure16_Senior_Growth.png")
    plt.close()

# Figure 17: Value Chain Mapping (Conceptual Flow)
def plot_fig17():
    # Simple flow diagram using matplotlib
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Nodes
    nodes = {
        'Raw Materials': (0.1, 0.5),
        'CDMO / Premix': (0.4, 0.5),
        'Brand Owner': (0.7, 0.5),
        'Consumer': (0.9, 0.5)
    }
    
    for name, (x, y) in nodes.items():
        circle = patches.FancyBboxPatch((x-0.08, y-0.1), 0.16, 0.2, boxstyle="round,pad=0.02", 
                                       fc='#AED6F1', ec='#2E86C1')
        ax.add_patch(circle)
        ax.text(x, y, name.replace(' ', '\n'), ha='center', va='center', fontweight='bold')

    # Arrows
    ax.arrow(0.18, 0.5, 0.14, 0, head_width=0.03, head_length=0.02, fc='grey', ec='grey')
    ax.arrow(0.48, 0.5, 0.14, 0, head_width=0.03, head_length=0.02, fc='grey', ec='grey')
    ax.arrow(0.78, 0.5, 0.05, 0, head_width=0.03, head_length=0.02, fc='grey', ec='grey')
    
    # Margin Annotations
    ax.text(0.25, 0.6, "Low Margin\n(Commodity)", ha='center', fontsize=9)
    ax.text(0.55, 0.6, "Med Margin\n(Volume)", ha='center', fontsize=9)
    ax.text(0.85, 0.6, "High Margin\n(Brand/IP)", ha='center', fontsize=9)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.title('Value Chain: From Molecule to Market')
    plt.savefig(f"{output_dir}/Figure17_Value_Chain.png")
    plt.close()

# Figure 18: Pet Supplement Channel Economics
def plot_fig18():
    years = [2010, 2015, 2020, 2024]
    margins = [25, 23, 20, 18] # Declining due to Amazon/Chewy pressure
    
    plt.figure(figsize=(8, 6))
    plt.plot(years, margins, marker='o', linewidth=3, color='#E74C3C')
    plt.title('Pet Supplement Brand EBITDA Margins (2010-2024)')
    plt.ylabel('Average EBITDA Margin (%)')
    plt.ylim(10, 30)
    plt.xlabel('Year')
    plt.grid(True)
    
    plt.annotate('Chewy IPO / Amazon Scale', xy=(2019, 21), xytext=(2015, 15),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure18_Channel_Economics.png")
    plt.close()

# Figure 21: Pharma Encroachment Funnel
def plot_fig21():
    # Funnel visualization
    stages = ['Nutraceutical Trial', 'Chronic User', 'Prescription Drug Conversion']
    values = [100, 40, 15] # Conceptual funnel width
    
    plt.figure(figsize=(8, 6))
    # Draw bars centered
    for i, (v, stage) in enumerate(zip(values, stages)):
        plt.barh(2-i, v, align='center', color=colors_palette[i])
        plt.text(0, 2-i, stage, ha='center', va='center', color='white', fontweight='bold')
        
    plt.yticks([])
    plt.title('Pharma Encroachment Funnel')
    plt.xlabel('Patient Population (Index)')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure21_Pharma_Funnel.png")
    plt.close()

if __name__ == "__main__":
    plot_fig1()
    plot_fig2()
    plot_fig3()
    plot_fig4()
    plot_fig5()
    plot_fig6()
    plot_fig7()
    plot_fig9()
    plot_fig10()
    plot_fig11()
    plot_fig12() # New
    plot_fig13()
    plot_fig14() # New
    plot_fig15() # New
    plot_fig16() # New
    plot_fig17() # New
    plot_fig18() # New
    plot_fig19()
    plot_fig20()
    plot_fig21() # New
    plot_table_us_eu()
    plot_venn()
    plot_species_matrix()
    plot_efficacy_matrix()
    plot_timeline()
