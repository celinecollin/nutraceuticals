
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import csv
import io

# --- CONFIGURATION & STYLE ---
output_dir = "."
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Professional Color Palette
COLORS = {
    'primary': '#003057',    # Navy Blue
    'secondary': '#0089cf',  # Bright Blue
    'accent1': '#b4a996',    # Beige/Gold
    'accent2': '#d04a02',    # Burnt Orange
    'accent3': '#4d6b7b',    # Slate Teal
    'grey': '#8b9ba5',       # Gridlines/Text
    'text': '#333333',       # Main Text
    'white': '#ffffff',
    'light_bg': '#f9f9f9'
}

PALETTE = [COLORS['primary'], COLORS['secondary'], COLORS['accent2'], COLORS['accent3'], COLORS['grey']]

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 12,
    'text.color': COLORS['text'],
    'axes.labelcolor': COLORS['text'],
    'axes.edgecolor': COLORS['grey'],
    'axes.linewidth': 0.8,
    'xtick.color': COLORS['text'],
    'ytick.color': COLORS['text'],
    'figure.figsize': (10, 6),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.titleweight': 'bold',
    'axes.titlesize': 16,
    'axes.titlepad': 20,
    'axes.titlelocation': 'left', # Enforce left alignment globally
    'axes.spines.top': False,
    'axes.spines.right': False,
    'legend.frameon': False,
    'grid.color': '#e0e0e0',
    'grid.linestyle': '-',
    'grid.linewidth': 0.5,
    'grid.alpha': 0.6
})

def clean_axes(ax):
    """Remove top/right spines and set grid."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['grey'])
    ax.spines['bottom'].set_color(COLORS['grey'])
    ax.grid(True, axis='y', zorder=0)

def add_labels(bars, ax, format_str='{}', fontsize=10):
    """Add value labels above bars with smart positioning."""
    ylim = ax.get_ylim()[1]
    for bar in bars:
        height = bar.get_height()
        label = format_str.format(height)
        # Check for potential overlap with top border
        y_pos = height + (ylim * 0.02)
        ax.text(bar.get_x() + bar.get_width()/2., y_pos,
                label,
                ha='center', va='bottom', fontsize=fontsize, color=COLORS['text'], fontweight='bold')

def save_data(name, headers, rows, source_text):
    """Save data to CSV and source to TXT."""
    # CSV
    csv_path = os.path.join(output_dir, f"{name}.csv")
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"  -> Saved data: {name}.csv")
    except Exception as e:
        print(f"  ! Error saving CSV {name}: {e}")

    # TXT
    txt_path = os.path.join(output_dir, f"{name}.txt")
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(source_text)
        print(f"  -> Saved source: {name}.txt")
    except Exception as e:
        print(f"  ! Error saving TXT {name}: {e}")

# --- FIGURE GENERATORS ---

def plot_fig1():
    name = "Figure1_Pet_Ownership"
    regions = ['US', 'Mexico', 'Canada', 'EU']
    rates = [71, 70, 60, 49]
    source = "Sources: APPA National Pet Owners Survey (2024), FEDIAF Facts & Figures (2024)."
    
    # Data Export
    rows = zip(regions, rates)
    save_data(name, ["Region", "Ownership Rate (%)"], list(rows), source)
    
    # Plot
    fig, ax = plt.subplots()
    bars = ax.bar(regions, rates, color=COLORS['primary'], width=0.6, zorder=3)
    
    ax.set_title('Household Pet Ownership Rate by Region (2023)', loc='left')
    ax.set_ylabel('Ownership Rate (%)')
    ax.set_ylim(0, 100)
    clean_axes(ax)
    add_labels(bars, ax, '{}%')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig2():
    name = "Figure2_EU_Pet_Pop"
    labels = ['Cats', 'Dogs', 'Others']
    sizes = [127, 104, 50]
    total = sum(sizes)
    source = "Source: FEDIAF Facts & Figures 2024."
    
    save_data(name, ["Species", "Population (Millions)"], zip(labels, sizes), source)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Colors: Dark, Med, Light. Light needs dark text.
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent1']]
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                      startangle=90, colors=colors,
                                      pctdistance=0.85, wedgeprops=dict(width=0.4, edgecolor='white'))
    
    # Fix Text Colors for contrast
    plt.setp(texts, fontsize=12, fontweight='medium')
    # Loop to set color based on wedge color brightness
    for i, at in enumerate(autotexts):
        at.set_fontsize(10)
        at.set_fontweight('bold')
        if i == 2: # accent1 is beige, need dark text
            at.set_color(COLORS['text'])
        else:
            at.set_color('white')
            
    ax.text(0, 0, f'{total}M\nTotal', ha='center', va='center', fontsize=14, fontweight='bold', color=COLORS['primary'])
    ax.set_title('Pet Population in Europe by Species (2023)', loc='center')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig3():
    name = "Figure3_EU_Growth"
    species = ['Cats', 'Dogs']
    growth = [11, 5]
    source = "Source: FEDIAF (Comparison 2018-2023)."
    
    save_data(name, ["Species", "Growth (%)"], zip(species, growth), source)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    bars = ax.bar(species, growth, color=[COLORS['primary'], COLORS['accent3']], width=0.5, zorder=3)
    
    ax.set_title('Population Growth in Europe\n(2018–2023)', loc='left')
    ax.set_ylabel('Growth (%)')
    ax.set_ylim(0, 15)
    clean_axes(ax)
    add_labels(bars, ax, '+{}%')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig4():
    name = "Figure4_Regional_Market"
    regions = ['APAC', 'Europe', 'North America', 'LATAM', 'Rest of World']
    values = [2.1, 1.7, 1.1, 0.8, 0.3]
    source = "Source: Grand View Research, Mordor Intelligence (2024 Estimates)."
    
    # Data is plotted in reverse for barh, but let's save roughly as displayed top-down
    save_data(name, ["Region", "Market Size (USD Billion)"], zip(regions, values), source)
    
    regions_rev = regions[::-1]
    values_rev = values[::-1]
    
    fig, ax = plt.subplots()
    bars = ax.barh(regions_rev, values_rev, color=COLORS['primary'], height=0.6, zorder=3)
    
    ax.set_title('Regional Market Size for Pet Nutraceuticals (2024E)', loc='left')
    ax.set_xlabel('Market Size (USD Billion)')
    # Add padding for labels on right
    ax.set_xlim(0, max(values_rev)*1.2)
    clean_axes(ax)
    ax.grid(True, axis='x', zorder=0)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(False)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                f'${width}B', ha='left', va='center', fontweight='bold', color=COLORS['secondary'])
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig5():
    name = "Figure5_Probiotics_Share"
    species = ['Poultry', 'Swine', 'Ruminant', 'Aqua']
    volume_share = [60, 25, 10, 5]
    revenue = [2.5, 1.0, 0.4, 0.2]
    source = "Source: Internal Market Analysis, Global Market Insights (2024)."
    
    data_rows = []
    for s, v, r in zip(species, volume_share, revenue):
        data_rows.append([s, v, r])
    save_data(name, ["Species", "Volume Share (%)", "Revenue ($B)"], data_rows, source)
    
    fig = plt.figure(figsize=(12, 6))
    
    ax1 = fig.add_subplot(121)
    wedges, texts, autotexts = ax1.pie(volume_share, labels=species, autopct='%1.0f%%', 
                                       startangle=90, colors=PALETTE[:4],
                                       wedgeprops=dict(width=0.4, edgecolor='white'))
    ax1.set_title('Volume Share (2024)', loc='center', fontsize=14)
    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
    # Improve Aqua label visibility if needed
    
    ax2 = fig.add_subplot(122)
    bars = ax2.bar(species, revenue, color=PALETTE[:4], zorder=3)
    ax2.set_title('Estimated Revenue ($ Billion)', loc='left', fontsize=14)
    clean_axes(ax2)
    add_labels(bars, ax2, '${}B')
    
    plt.suptitle('Feed Probiotics Market Breakdown', fontsize=18, fontweight='bold', x=0.05, ha='left')
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig6():
    name = "Figure6_Poultry_HPAI"
    years = np.arange(2015, 2025).tolist()
    production = [100 * (1.015 ** (y - 2015)) for y in years] # Approx logic from orig
    losses = [5, 8, 10, 12, 15, 25, 35, 40, 45, 50]
    source = "Source: WOAH, FAO, Industry Reports covering 2015-2024."
    
    save_data(name, ["Year", "Production Index", "Losses (Millions)"], zip(years, production, losses), source)
    
    fig, ax1 = plt.subplots()
    
    color = COLORS['secondary']
    ax1.set_ylabel('Production Index (2015=100)', color=color, fontweight='bold')
    ax1.plot(years, production, color=color, linewidth=3, label='Poultry Production')
    ax1.tick_params(axis='y', labelcolor=color)
    clean_axes(ax1)
    
    ax2 = ax1.twinx()
    color2 = COLORS['accent2']
    ax2.set_ylabel('Bird Losses (Millions)', color=color2, fontweight='bold')
    ax2.bar(years, losses, color=color2, alpha=0.3, width=0.6, label='HPAI Losses')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(color2)

    ax1.set_title('Global Poultry Production resilience despite HPAI', loc='left')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig7():
    name = "Figure7_Swine_Decline"
    years = np.arange(2014, 2025).tolist()
    herd = np.linspace(100, 91.9, len(years)).tolist()
    source = "Source: Eurostat Pig Population Data (2014-2024)."
    
    save_data(name, ["Year", "Herd Index (2014=100)"], zip(years, herd), source)
    
    fig, ax = plt.subplots()
    ax.plot(years, herd, color=COLORS['accent2'], linewidth=3, marker='o')
    ax.set_title('European Swine Herd Contraction (Index)', loc='left')
    ax.set_ylabel('Index (2014=100)')
    clean_axes(ax)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig8():
    name = "Figure8_Cattle_Inventory"
    years = np.arange(2010, 2025)
    us = np.linspace(95, 87.2, len(years))
    eu = np.linspace(78, 72, len(years))
    latam = np.linspace(350, 365, len(years))
    india = np.linspace(190, 195, len(years))
    source = "Source: USDA NASS, Eurostat, FAO."

    rows = []
    for i in range(len(years)):
        rows.append([years[i], us[i], eu[i], latam[i], india[i]])
    save_data(name, ["Year", "US", "EU", "LATAM", "India"], rows, source)

    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(years, us, color=COLORS['accent2'], linewidth=3, marker='o', markersize=4, label='USA')
    ax.plot(years, eu, color=COLORS['secondary'], linewidth=3, marker='s', markersize=4, label='EU')
    ax.plot(years, latam/10, color=COLORS['primary'], linewidth=3, marker='^', markersize=4, label='LATAM (÷10)')
    ax.plot(years, india/10, color=COLORS['accent3'], linewidth=3, marker='d', markersize=4, label='India (÷10)')
    
    ax.set_title('Global Cattle Inventory: The Western Contraction', loc='left')
    ax.set_ylabel('Million Head (USA/EU real, others scaled)')
    clean_axes(ax)
    # Move legend to empty space in middle (between 40 and 70)
    ax.legend(loc='center right', fontsize=10) 
    
    ax.annotate('2024: 87.2M\n(73-yr low)', xy=(2024, 87.2), xytext=(2020, 95),
                arrowprops=dict(arrowstyle='->', color='black'), fontweight='bold', color=COLORS['accent2'])
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig9():
    name = "Figure9_Livestock_Trends"
    years = np.arange(2018, 2024)
    poultry = np.linspace(100, 110.5, 6)
    bovine = np.linspace(100, 94.8, 6)
    pigs = np.linspace(100, 91.1, 6)
    sheep = np.linspace(100, 89.5, 6)
    source = "Source: Eurostat Agricultural Production."
    
    rows = []
    for i in range(len(years)):
        rows.append([years[i], poultry[i], bovine[i], pigs[i], sheep[i]])
    save_data(name, ["Year", "Poultry", "Bovine", "Pigs", "Sheep"], rows, source)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, poultry, color=COLORS['primary'], linewidth=3, label='Poultry')
    ax.plot(years, bovine, color=COLORS['accent2'], linewidth=2, linestyle='--', label='Bovine')
    ax.plot(years, pigs, color=COLORS['accent3'], linewidth=2, linestyle='--', label='Pigs')
    ax.plot(years, sheep, color=COLORS['grey'], linewidth=2, linestyle=':', label='Sheep/Goat')
    
    ax.set_title('The "De-Ruminization" of Europe: Indexed Production Trends', loc='left')
    ax.set_ylabel('Index (2018=100)')
    ax.set_xlim(2018, 2024.5) # Extend to fit text labels
    clean_axes(ax)
    
    # Text labels
    ax.text(2023.1, poultry[-1], 'Poultry (+10.5%)', color=COLORS['primary'], fontweight='bold', va='center')
    ax.text(2023.1, bovine[-1], 'Bovine (-5.2%)', color=COLORS['accent2'], fontweight='bold', va='center')
    
    ax.legend(loc='lower left')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig11():
    name = "Figure11_Formats"
    # Dogs: Chews/Treats(64), Liquids(10), Pills/Powders(26)
    # Cats: Chews/Treats(15), Liquids(35), Pills/Powders(50)
    # Horses: Chews(0), Pastes/Syr(25), Powder/Pellets(75)
    source = "Source: Grand View Research, Industry Interviews (2024)."
    
    headers = ["Species", "Chews/Treats", "Liquids/Pastes", "Pills/Powders"]
    rows = [
        ["Dogs", 64, 10, 26],
        ["Cats", 15, 35, 50],
        ["Horses", 0, 25, 75]
    ]
    save_data(name, headers, rows, source)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    def draw_donut(ax, sizes, labels, title):
        wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.0f%%', startangle=140, 
                                          colors=PALETTE, pctdistance=0.75, 
                                          wedgeprops=dict(width=0.4, edgecolor='white'))
        ax.set_title(title, fontweight='bold')
        # Improve contrast
        for at in autotexts:
            at.set_color('white')
            at.set_fontweight('bold')
        
    draw_donut(ax1, [64, 10, 26], ['Chews/Treats', 'Liquids', 'Pills/Powders'], 'Dogs\n(Taste Driven)')
    draw_donut(ax2, [15, 35, 50], ['Chews/Treats', 'Liquids', 'Pills/Powders'], 'Cats\n(Texture Driven)')
    draw_donut(ax3, [0, 25, 75], ['Chews', 'Pastes/Syr', 'Powder/Pellets'], 'Horses\n(Feed Driven)')
    
    # Unified Legend
    fig.legend(['Chews/Treats', 'Liquids/Pastes', 'Pills/Powders'], loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0))
    
    plt.suptitle('Nutraceutical Delivery Format Preferences', fontsize=16, fontweight='bold', x=0.05, ha='left')
    plt.tight_layout(rect=[0, 0.08, 1, 0.9])
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig12():
    name = "Figure12_Wallet"
    labels = ['Food', 'Vet Care', 'Supplements', 'Toys/Access.', 'Services']
    sizes = [40, 25, 15, 10, 10]
    source = "Source: APPA 2025, Nicotra et al (2025)."
    
    save_data(name, ["Category", "Share (%)"], zip(labels, sizes), source)
    
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.0f%%', 
                                      startangle=90, colors=PALETTE,
                                      wedgeprops=dict(width=0.5, edgecolor='white'))
    
    ax.text(0, 0, '$1,500\nAvg Annual', ha='center', va='center', fontsize=10, fontweight='bold', color=COLORS['primary'])
    ax.set_title('Preventive Health Wallet Allocation (2025)', loc='left')
    
    # Fix contrast and position
    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
        at.set_fontsize(9)
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig13():
    name = "Figure13_Segmentation"
    projects = ['Spare No Expense', 'Value-Conscious', 'Basic Care']
    households = [20, 50, 30]
    revenue = [48, 42, 10]
    source = "Source: Internal Segmentation Analysis."
    
    save_data(name, ["Segment", "Households (%)", "Revenue (%)"], zip(projects, households, revenue), source)
    
    x = np.arange(len(projects))
    width = 0.35
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, households, width, label='% Households', color=COLORS['grey'])
    rects2 = ax.bar(x + width/2, revenue, width, label='% Revenue', color=COLORS['primary'])
    
    ax.set_ylabel('Share (%)')
    ax.set_title('Consumer Segmentation: The "Pareto" Effect', loc='left')
    ax.set_xticks(x)
    ax.set_xticklabels(projects)
    ax.legend()
    clean_axes(ax)
    
    add_labels(rects1, ax, '{}%')
    add_labels(rects2, ax, '{}%')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig14():
    name = "Figure14_Psychology"
    factors = ['Fear/Regret', 'Love/Bonding', 'Duty/Responsibility']
    vals = [50, 30, 20]
    source = "Source: Nicotra et al. (2025), SupplySide Shopper Survey."
    
    save_data(name, ["Factor", "Influence (%)"], zip(factors, vals), source)
    
    fig, ax = plt.subplots()
    bars = ax.barh(factors, vals, color=[COLORS['accent2'], COLORS['primary'], COLORS['grey']])
    clean_axes(ax)
    ax.set_title('Psychological Drivers of Supplement Purchase', loc='left')
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                f'{width}%', ha='left', va='center', fontweight='bold', color=COLORS['text'])
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig15():
    name = "Figure15_Mobility_Evo"
    years = [2015, 2020, 2024, 2030]
    generic = [70, 60, 45, 35]
    uc_ii = [5, 15, 25, 30]
    glm = [15, 15, 18, 20]
    premium = [10, 10, 12, 15]
    source = "Source: Market Analysis & Projections."
    
    rows = []
    for i in range(len(years)):
        rows.append([years[i], generic[i], uc_ii[i], glm[i], premium[i]])
    save_data(name, ["Year", "Generic", "UC-II", "GLM", "Premium"], rows, source)
    
    fig, ax = plt.subplots()
    pal = [COLORS['grey'], COLORS['secondary'], COLORS['accent3'], COLORS['primary']]
    labels = ['Generic Glucosamine', 'UC-II Collagen', 'Green Lipped Mussel', 'Premium Combos']
    
    ax.stackplot(years, generic, uc_ii, glm, premium, labels=labels, colors=pal, alpha=0.9)
    
    ax.set_title('Mobility Supplement Premiumization (2015–2030)', loc='left')
    ax.set_ylabel('Market Share (%)')
    clean_axes(ax)
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.05), ncol=2, frameon=False, fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig16():
    name = "Figure16_Senior_Growth"
    years = ['2015', '2024', '2030']
    market_size = [5, 12, 20]
    source = "Source: Internal Projections."
    save_data(name, ["Year", "Market Size Index"], zip(years, market_size), source)
    
    fig, ax = plt.subplots()
    bars = ax.bar(years, market_size, color=COLORS['primary'])
    clean_axes(ax)
    ax.set_title("Senior Growth Opportunity", loc='left')
    add_labels(bars, ax)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig17():
    name = "Value_Chain_Economics"
    # Diagram - No numerical data, but we can save the structure info
    data = [["Stage", "Description", "Margin"],
            ["Ingredients", "Raw Material", "Low"],
            ["Manufacturing", "CDMO / Premix", "Medium"],
            ["Brand Owner", "Strategy / Mktg", "High"]]
    source = "Source: L.E.K. Consulting, Bain & Co (2024)."
    
    save_data(name, data[0], data[1:], source)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    def box(x, label, sublabel, color):
        # Add shadow effect
        shadow = patches.FancyBboxPatch((x+0.05, 0.95), 2, 2, boxstyle="round,pad=0.1", fc='#cccccc', ec='none', zorder=1)
        ax.add_patch(shadow)
        rect = patches.FancyBboxPatch((x, 1), 2, 2, boxstyle="round,pad=0.1", fc=color, ec='none', zorder=2)
        ax.add_patch(rect)
        ax.text(x+1, 2.2, label, ha='center', va='center', fontweight='bold', color='white', fontsize=11, zorder=3)
        ax.text(x+1, 1.8, sublabel, ha='center', va='center', color='white', fontsize=9, zorder=3)
    
    box(0.5, "Ingredients", "Raw Material\n(Margin: Low)", COLORS['grey'])
    ax.arrow(2.8, 2, 0.4, 0, head_width=0.2, head_length=0.2, fc=COLORS['text'], ec=COLORS['text'], zorder=1)
    box(3.5, "Manufacturing", "CDMO / Premix\n(Margin: Med)", COLORS['accent3'])
    ax.arrow(5.8, 2, 0.4, 0, head_width=0.2, head_length=0.2, fc=COLORS['text'], ec=COLORS['text'], zorder=1)
    box(6.5, "Brand Owner", "Strategy / Mktg\n(Margin: High)", COLORS['primary'])
    
    ax.text(5, 3.5, "Value Accrual ->", ha='center', fontsize=14, fontweight='bold', color=COLORS['secondary'])
    ax.set_title('Value Chain Economics', loc='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig18():
    name = "Figure18_Channel_Economics"
    years = [2010, 2015, 2019, 2024]
    margins = [25, 23, 20, 18]
    source = "Source: Dechra, DSM, Industry Reports."
    
    save_data(name, ["Year", "EBITDA Margin (%)"], zip(years, margins), source)
    
    fig, ax = plt.subplots()
    ax.plot(years, margins, color=COLORS['accent2'], linewidth=3, marker='o')
    clean_axes(ax)
    ax.set_title('Margin Erosion Over Time', loc='left')
    ax.set_ylim(0, 30)
    
    for i, txt in enumerate(margins):
        ax.annotate(f"{txt}%", (years[i], margins[i]), xytext=(0, 10), 
                    textcoords='offset points', ha='center', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig19():
    name = "Figure19_Value_Waterfall"
    ls_names = ['Sourcing', 'Manufacturing', 'Service/Logistics', 'Net Margin']
    ls_vals = [30, 10, 8, 2]
    pet_names = ['COGS', 'Pkg/Mfg', 'Channel/Mktg', 'Net Margin']
    pet_vals = [10, 15, 15, 10]
    source = "Source: Internal Value Chain Analysis."
    
    # Save combined
    rows = []
    for i in range(len(ls_names)):
        rows.append(["Livestock", ls_names[i], ls_vals[i]])
    for i in range(len(pet_names)):
        rows.append(["Pet", pet_names[i], pet_vals[i]])
    save_data(name, ["Sector", "Component", "Value ($)"], rows, source)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Livestock
    ls_bottoms = [0, 30, 40, 48]
    ls_colors = [COLORS['grey'], COLORS['grey'], COLORS['secondary'], COLORS['primary']]
    ax1.bar(ls_names, ls_vals, bottom=ls_bottoms, color=ls_colors)
    ax1.set_ylim(0, 55)
    ax1.set_title('Livestock Premix ($50 Cost)', fontsize=12)
    clean_axes(ax1)
    ax1.tick_params(axis='x', rotation=45)
    
    # Pet
    pet_bottoms = [0, 10, 25, 40]
    pet_colors = [COLORS['grey'], COLORS['grey'], COLORS['accent2'], COLORS['primary']]
    ax2.bar(pet_names, pet_vals, bottom=pet_bottoms, color=pet_colors)
    ax2.set_ylim(0, 55)
    ax2.set_title('Pet Supplement ($50 Retail)', fontsize=12)
    clean_axes(ax2)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.suptitle('Value Capture: Volume vs Brand', fontweight='bold', x=0.05, ha='left')
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig20():
    name = "Figure20_Risk_Reward"
    segments = ['Pet Brands', 'Livestock Premix', 'Ingredients (IP)', 'Commodities']
    size = [6, 8, 2, 5]     # Market Size $B
    margin = [22, 10, 25, 6] # EBITDA %
    growth = [7, 4, 9, 2]    # CAGR %
    source = "Source: Comparative Market Analysis (2024)."

    rows = zip(segments, size, margin, growth)
    save_data(name, ["Segment", "Size ($B)", "Margin (%)", "Growth (%)"], list(rows), source)

    fig, ax = plt.subplots()
    scatter = ax.scatter(size, margin, s=[g*200 for g in growth], 
                         c=[COLORS['primary'], COLORS['accent3'], COLORS['secondary'], COLORS['grey']], 
                         alpha=0.8, edgecolors='white', linewidth=2)
    
    ax.set_xlabel('Market Size ($ Billions)')
    ax.set_ylabel('EBITDA Margin (%)')
    ax.set_title('Risk/Reward Map', loc='left')
    
    for i, txt in enumerate(segments):
        ax.annotate(txt, (size[i], margin[i]), xytext=(0, -30 if i==2 else 15), 
                    textcoords='offset points', ha='center', fontweight='bold', fontsize=10)
        
    clean_axes(ax)
    ax.grid(True, linestyle='--')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_fig21():
    name = "Figure21_Pharma_Funnel"
    stages = ['Trial', 'User', 'Rx']
    vals = [100, 40, 10]
    source = "Source: Customer Journey Analysis."
    save_data(name, ["Stage", "Volume Index"], zip(stages, vals), source)
    
    fig, ax = plt.subplots()
    ax.barh(stages, vals, color=COLORS['primary'])
    clean_axes(ax)
    ax.set_title("Pharma Integration Funnel", loc='left')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_table_us_eu():
    name = "Table_US_vs_EU"
    data = [
        ["Feature", "United States (US)", "European Union (EU)"],
        ["Nutraceutical Def.", "Undefined (Food vs Drug)", "Undefined (Feed vs VMP)"],
        ["Regulatory Body", "FDA-CVM & AAFCO", "EFSA & National Agencies"],
        ["Disease Claims", "Prohibited (Drug only)", "Prohibited (PARNUTs exception)"],
        ["Market Entry", "Fast (Notification)", "Slow (Dossier Approval)"]
    ]
    source = "Source: FDA-CVM, EFSA Regulations."
    save_data(name, data[0], data[1:], source)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=data, loc='center', cellLoc='left', colWidths=[0.2, 0.4, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.8)
    
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('white')
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(COLORS['primary'])
        else:
            cell.set_facecolor('#f2f2f2' if row % 2 == 0 else 'white')

    ax.set_title('Regulatory Landscape Comparison', loc='left', fontweight='bold', pad=10)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_timeline():
    name = "Timeline_Regulations"
    events = [
        (2006, "EU bans AGPs"),
        (2017, "US FDA VFD Implemented"),
        (2022, "EU bans Zinc Oxide"),
        (2024, "China AGP Tightening"),
        (2025, "UK Feed Reform")
    ]
    source = "Source: Regulatory Filings."
    
    years = [e[0] for e in events]
    labels = [e[1] for e in events]
    save_data(name, ["Year", "Event"], zip(years, labels), source)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hlines(1, 2005, 2026, colors=COLORS['grey'], linewidth=2)
    ax.plot(years, [1]*len(years), 'o', markersize=10, color=COLORS['primary'], markeredgecolor='white', markeredgewidth=2)
    
    for i, (yr, lbl) in enumerate(zip(years, labels)):
        offset = 0.3 if i % 2 == 0 else -0.3
        ax.text(yr, 1 + offset, f"{yr}\n{lbl}", ha='center', va='center' if offset > 0 else 'top', 
                fontweight='bold', fontsize=10, color=COLORS['text'])
        ax.vlines(yr, 1, 1 + (offset*0.8), colors=COLORS['grey'], linestyle=':')
        
    ax.axis('off')
    ax.set_title('Regulatory Timeline: The Push for Alternatives', loc='center')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_species_matrix():
    name = "Matrix_Species_Functional"
    # Rows: Species
    species = ['Dogs', 'Cats', 'Horses', 'Poultry', 'Swine', 'Ruminants']
    # Cols: Functions
    functions = ['Mobility', 'Gut Health', 'Anxiety', 'Immunity', 'Growth/FCR']
    
    # 0=Low/None, 1=Med, 2=High relevance
    # CORRECTED DIMENSIONS: 5 columns to match labels
    data = np.array([
        [2, 2, 2, 1, 0], # Dogs
        [1, 2, 2, 1, 0], # Cats
        [2, 2, 1, 1, 0], # Horses
        [1, 2, 0, 2, 2], # Poultry
        [1, 2, 0, 2, 2], # Swine
        [0, 1, 0, 1, 2], # Ruminants
    ])
    
    source = "Source: Strategy Framework analysis."
    
    # Save Data
    headers = ["Species"] + functions
    rows = []
    for i, sp in enumerate(species):
        row = [sp] + list(data[i])
        rows.append(row)
    save_data(name, headers, rows, source)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create distinct colors for levels (0, 1, 2)
    from matplotlib.colors import ListedColormap
    # 0: Light Grey, 1: Medium Blue, 2: Dark Navy
    cmap = ListedColormap(['#f0f0f0', '#6baed6', '#084594'])
    
    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=2)
    
    # Grid lines
    ax.set_xticks(np.arange(len(functions)) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(species)) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    
    # Axes
    ax.set_xticks(np.arange(len(functions)))
    ax.set_yticks(np.arange(len(species)))
    ax.set_xticklabels(functions, fontsize=11, fontweight='bold')
    ax.set_yticklabels(species, fontsize=11, fontweight='bold')
    
    # Move x-axis labels to top for better table-like reading
    ax.xaxis.tick_top()
    
    # Annotate
    for i in range(len(species)):
        for j in range(len(functions)):
            val = data[i, j]
            label = "High" if val==2 else "Med" if val==1 else "-"
            # White text for dark blocks, black for light
            color = "white" if val >= 1 else "#999999"
            ax.text(j, i, label, ha="center", va="center", color=color, fontweight='bold', fontsize=10)
            
    # Remove spines
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
        
    ax.set_title("Functional Needs by Species", loc='center', y=1.1, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

def plot_efficacy_matrix():
    name = "Matrix_Efficacy"
    # X: Maturity, Y: Clinical Evidence
    ingredients = [
        {'label': 'Glucosamine', 'x': 9, 'y': 3, 'type': 'Commodity'},
        {'label': 'Probiotics (Live)', 'x': 8, 'y': 8, 'type': 'Standard'},
        {'label': 'Omega-3 (Fish Oil)', 'x': 9, 'y': 9, 'type': 'Standard'},
        {'label': 'UC-II Collagen', 'x': 5, 'y': 8, 'type': 'Premium'},
        {'label': 'Postbiotics', 'x': 3, 'y': 7, 'type': 'Premium'},
        {'label': 'CBD/Hemp', 'x': 6, 'y': 4, 'type': 'Fad/Niche'},
        {'label': 'Phytogenics', 'x': 5, 'y': 6, 'type': 'Growth'},
        {'label': 'Methane Blockers', 'x': 2, 'y': 9, 'type': 'Future'}
    ]
    
    source = "Source: Clinical Evidence Review (2024)."
    
    # Save Data
    save_data(name, ["Ingredient", "Market Maturity (1-10)", "Evidence Level (1-10)"], 
              [[i['label'], i['x'], i['y']] for i in ingredients], source)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    x_vals = [i['x'] for i in ingredients]
    y_vals = [i['y'] for i in ingredients]
    
    # quadrants
    ax.axhline(y=5, color=COLORS['grey'], linestyle='--', alpha=0.3)
    ax.axvline(x=5, color=COLORS['grey'], linestyle='--', alpha=0.3)
    
    # Plot points
    scatter = ax.scatter(x_vals, y_vals, s=200, c=COLORS['primary'], zorder=3)
    
    # Labels
    for item in ingredients:
        ax.annotate(item['label'], (item['x'], item['y']), xytext=(0, 10), 
                    textcoords='offset points', ha='center', fontweight='bold', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.7))
        
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("Market Maturity (Emerging → Mature)")
    ax.set_ylabel("Clinical Evidence (Low → High)")
    ax.set_title("Ingredient Landscape: Efficacy vs. Maturity", loc='left')
    
    # Quad Labels
    ax.text(9, 9.5, "Stars\n(High Value)", ha='right', va='top', color=COLORS['secondary'], fontweight='bold')
    ax.text(9, 0.5, "Legacy\n(Commodity)", ha='right', va='bottom', color=COLORS['grey'], fontweight='bold')
    ax.text(1, 9.5, "Innovators\n(Next Gen)", ha='left', va='top', color=COLORS['accent2'], fontweight='bold')
    ax.text(1, 0.5, "Speculative\n(Niche)", ha='left', va='bottom', color=COLORS['grey'], fontweight='bold')
    
    clean_axes(ax)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{name}.png")
    plt.close()

if __name__ == "__main__":
    print("Starting generation...")
    plot_fig1()
    plot_fig2()
    plot_fig3()
    plot_fig4()
    plot_fig5()
    plot_fig6()
    plot_fig7()
    plot_fig8()
    plot_fig9()
    # plot_fig10() # Skipped, not used
    plot_fig11()
    plot_fig12()
    plot_fig13()
    plot_fig14()
    plot_fig15()
    plot_fig16()
    plot_fig17()
    plot_fig18()
    plot_fig19()
    plot_fig20()
    plot_fig21()
    plot_table_us_eu()
    plot_timeline()
    plot_species_matrix()
    plot_efficacy_matrix()
    print("Done!")
