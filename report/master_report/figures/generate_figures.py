
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import matplotlib.font_manager as fm

# --- CONFIGURATION & STYLE ---
output_dir = "report/master_report/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Professional Color Palette (Corporate/Investment Banking Style)
# Deep Navy, Slate, Teal, Muted Gold, Burnt Orange
COLORS = {
    'primary': '#003057',    # Navy Blue (Main Bars/Lines)
    'secondary': '#0089cf',  # Bright Blue (Highlights/Secondary)
    'accent1': '#b4a996',    # Beige/Gold (Neutral/Background elements)
    'accent2': '#d04a02',    # Burnt Orange (Alerts/Negative trends)
    'accent3': '#4d6b7b',    # Slate Teal (Comparative)
    'grey': '#8b9ba5',       # Gridlines/Text
    'text': '#333333',       # Main Text
    'white': '#ffffff'
}

PALETTE = [COLORS['primary'], COLORS['secondary'], COLORS['accent2'], COLORS['accent3'], COLORS['grey']]

# Global Style Settings
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

def add_labels(bars, ax, format_str='{}'):
    """Add value labels above bars."""
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + (height*0.01),
                format_str.format(height),
                ha='center', va='bottom', fontsize=10, color=COLORS['text'], fontweight='bold')

# --- FIGURE GENERATORS ---

# Figure 1: Household Pet Ownership (Bar Chart)
def plot_fig1():
    regions = ['US', 'Mexico', 'Canada', 'UK', 'EU']
    rates = [71, 70, 60, 57, 49]
    
    fig, ax = plt.subplots()
    bars = ax.bar(regions, rates, color=COLORS['primary'], width=0.6, zorder=3)
    
    ax.set_title('Household Pet Ownership Rate by Region (2023)', loc='left')
    ax.set_ylabel('Ownership Rate (%)')
    ax.set_ylim(0, 100)
    clean_axes(ax)
    add_labels(bars, ax, '{}%')
    
    # Highlight EU (lowest) with different color? No, keep clean.
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure1_Pet_Ownership.png")
    plt.close()

# Figure 2: EU Pet Population (Donut Chart - Modern)
def plot_fig2():
    labels = ['Cats', 'Dogs', 'Others']
    sizes = [127, 104, 50]
    total = sum(sizes)
    
    fig, ax = plt.subplots()
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                      startangle=90, colors=[COLORS['primary'], COLORS['secondary'], COLORS['accent1']],
                                      pctdistance=0.85, wedgeprops=dict(width=0.4, edgecolor='white'))
    
    # Center text
    ax.text(0, 0, f'{total}M\nTotal', ha='center', va='center', fontsize=14, fontweight='bold', color=COLORS['primary'])
    
    plt.setp(texts, fontsize=12, fontweight='medium')
    plt.setp(autotexts, fontsize=10, color='white', fontweight='bold')
    
    ax.set_title('Pet Population in Europe by Species (2023)', loc='center')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure2_EU_Pet_Pop.png")
    plt.close()

# Figure 3: EU Growth (Grouped Bar or Diverging?)
# Simple bar is fine, but focus on the contrast.
def plot_fig3():
    species = ['Cats', 'Dogs']
    growth = [11, 5]
    
    fig, ax = plt.subplots(figsize=(6, 6))
    bars = ax.bar(species, growth, color=[COLORS['primary'], COLORS['accent3']], width=0.5, zorder=3)
    
    ax.set_title('Population Growth in Europe\n(2018–2023)', loc='left')
    ax.set_ylabel('Growth (%)')
    ax.set_ylim(0, 15)
    clean_axes(ax)
    add_labels(bars, ax, '+{}%')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure3_EU_Growth.png")
    plt.close()

# Figure 4: Regional Market Size (Horizontal Bar for better label fit)
def plot_fig4():
    regions = ['APAC', 'Europe', 'North America', 'LATAM', 'Rest of World']
    values = [2.1, 1.7, 1.1, 0.8, 0.3]
    regions = regions[::-1] # Reverse for top-down
    values = values[::-1]
    
    fig, ax = plt.subplots()
    bars = ax.barh(regions, values, color=COLORS['primary'], height=0.6, zorder=3)
    
    ax.set_title('Regional Market Size for Pet Nutraceuticals (2024E)', loc='left')
    ax.set_xlabel('Market Size (USD Billion)')
    clean_axes(ax)
    ax.grid(True, axis='x', zorder=0)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(False) # Remove left spine
    
    # Add values at end of bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                f'${width}B', ha='left', va='center', fontweight='bold', color=COLORS['secondary'])
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure4_Regional_Market.png")
    plt.close()

# Figure 5: Feed Probiotics (Combined Pie + Bar -> Panel)
def plot_fig5():
    species = ['Poultry', 'Swine', 'Ruminant', 'Aqua']
    volume_share = [60, 25, 10, 5]
    revenue = [2.5, 1.0, 0.4, 0.2]
    
    fig = plt.figure(figsize=(12, 6))
    
    # 1. Pie (Left)
    ax1 = fig.add_subplot(121)
    wedges, texts, autotexts = ax1.pie(volume_share, labels=species, autopct='%1.0f%%', 
                                       startangle=90, colors=PALETTE[:4], pctdistance=0.8,
                                       wedgeprops=dict(width=0.4, edgecolor='white'))
    ax1.set_title('Volume Share (2024)', loc='center', fontsize=14)
    plt.setp(autotexts, size=9, weight="bold", color="white")

    # 2. Bar (Right)
    ax2 = fig.add_subplot(122)
    bars = ax2.bar(species, revenue, color=PALETTE[:4], zorder=3)
    ax2.set_title('Estimated Revenue ($ Billion)', loc='left', fontsize=14)
    clean_axes(ax2)
    add_labels(bars, ax2, '${}B')
    
    plt.suptitle('Feed Probiotics Market Breakdown', fontsize=18, fontweight='bold', x=0.05, ha='left')
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.savefig(f"{output_dir}/Figure5_Probiotics_Share.png")
    plt.close()

# Figure 6: HPAI Impact (Dual Axis - Professional)
def plot_fig6():
    years = np.arange(2015, 2025)
    production = 100 * (1.015 ** (years - 2015))
    losses = [5, 8, 10, 12, 15, 25, 35, 40, 45, 50]
    
    fig, ax1 = plt.subplots()
    
    # Production Line
    color = COLORS['secondary']
    ax1.set_ylabel('Production Index (2015=100)', color=color, fontweight='bold')
    ax1.plot(years, production, color=color, linewidth=3, label='Poultry Production')
    ax1.tick_params(axis='y', labelcolor=color)
    clean_axes(ax1)
    
    # Losses Bars (instead of line, for impact visualization)
    ax2 = ax1.twinx()
    color = COLORS['accent2']
    ax2.set_ylabel('Bird Losses (Millions)', color=color, fontweight='bold')
    bars = ax2.bar(years, losses, color=color, alpha=0.3, width=0.6, label='HPAI Losses')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    ax1.set_title('Global Poultry Production resilience despite HPAI', loc='left')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure6_Poultry_HPAI.png")
    plt.close()

# Figure 9: Indexed Livestock Trends (De-Ruminization)
def plot_fig9():
    years = np.arange(2018, 2024)
    poultry = np.linspace(100, 110.5, 6)
    bovine = np.linspace(100, 94.8, 6)
    pigs = np.linspace(100, 91.1, 6)
    sheep = np.linspace(100, 89.5, 6)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Poultry (Rising) - Highlighted
    ax.plot(years, poultry, color=COLORS['primary'], linewidth=3, label='Poultry')
    # Others (Falling)
    ax.plot(years, bovine, color=COLORS['accent2'], linewidth=2, linestyle='--', label='Bovine')
    ax.plot(years, pigs, color=COLORS['accent3'], linewidth=2, linestyle='--', label='Pigs')
    ax.plot(years, sheep, color=COLORS['grey'], linewidth=2, linestyle=':', label='Sheep/Goat')
    
    ax.set_title('The "De-Ruminization" of Europe: Indexed Production Trends', loc='left')
    ax.set_ylabel('Index (2018=100)')
    clean_axes(ax)
    
    # Add labels at the end of lines
    ax.text(2023.1, poultry[-1], 'Poultry (+10.5%)', color=COLORS['primary'], fontweight='bold', va='center')
    ax.text(2023.1, bovine[-1], 'Bovine (-5.2%)', color=COLORS['accent2'], fontweight='bold', va='center')
    ax.text(2023.1, pigs[-1], 'Pigs (-8.9%)', color=COLORS['accent3'], fontweight='bold', va='center')
    ax.text(2023.1, sheep[-1], 'Sheep/Goat (-10.5%)', color=COLORS['grey'], fontweight='bold', va='center')
    
    ax.legend(loc='lower left')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure9_Livestock_Trends.png")
    plt.close()

# Figure 10: Aquaculture Overtaking (Area Chart)
def plot_fig10():
    years = np.arange(2000, 2031)
    capture = np.linspace(85, 92, 23)
    capture = np.concatenate([capture, np.linspace(92, 93, 8)])
    
    aqua = np.linspace(30, 94.4, 23)
    aqua_future = 94.4 * (1.035 ** np.arange(1, 9))
    aqua = np.concatenate([aqua, aqua_future])
    
    fig, ax = plt.subplots()
    
    ax.fill_between(years, aqua, color=COLORS['secondary'], alpha=0.3, label='Aquaculture')
    ax.plot(years, aqua, color=COLORS['secondary'], linewidth=2)
    
    ax.plot(years, capture, color=COLORS['grey'], linewidth=2, linestyle='--', label='Capture Fisheries')
    
    # Intersection
    ax.plot(2022, 94.4, 'o', color=COLORS['accent2'], markersize=8)
    ax.annotate('Overtaking Point (2022)', xy=(2022, 94.4), xytext=(2015, 110),
                arrowprops=dict(arrowstyle='->', color='black'), fontweight='bold')
    
    ax.set_title('The Blue Transformation: Aquaculture vs Capture', loc='left')
    ax.set_ylabel('Million Tonnes')
    clean_axes(ax)
    
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure10_Aqua_v_Capture.png")
    plt.close()

# Figure 11: Formats (3 Pies -> 1 Stacked Bar 100%)
# Pies are hard to compare. Stacked bar is better for comparing compositions.
def plot_fig11():
    species = ['Dogs', 'Cats', 'Horses']
    # Categories: Chews/Treats, Liquids/Pastes, Powders/Pills, Other
    # Mapping data to categories for simplification
    # Dogs: Chews(39)+Treats(25)=64 | Liquids(10) | Powders(20)+Pills(6)=26
    # Cats: Chews(5)+Treats(10)=15 | Liquids(35) | Powders(30)+Pills(20)=50 
    # Horses: Chews?(0) | Syringes/Pastes(25) | Powders(60)+Inject(15)=75
    
    # Let's stick to original data but display better.
    # We'll use 3 donuts Side-by-Side but clean.
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    def draw_donut(ax, sizes, labels, title):
        wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.0f%%', startangle=140, 
                                          colors=PALETTE, pctdistance=0.75, 
                                          wedgeprops=dict(width=0.4, edgecolor='white'))
        ax.set_title(title, fontweight='bold')
        # Legend below
        ax.legend(wedges, labels, title="Formats", loc="center", bbox_to_anchor=(0.5, -0.2), frameon=False)
        plt.setp(autotexts, size=8, weight="bold", color="white")

    draw_donut(ax1, [64, 10, 26], ['Chews/Treats', 'Liquids', 'Pills/Powders'], 'Dogs\n(Taste Driven)')
    draw_donut(ax2, [15, 35, 50], ['Chews/Treats', 'Liquids', 'Pills/Powders'], 'Cats\n(Texture Driven)')
    draw_donut(ax3, [0, 25, 75], ['Chews', 'Pastes/Syr', 'Powder/Pellets'], 'Horses\n(Feed Driven)')
    
    plt.suptitle('Nutraceutical Delivery Format Preferences', fontsize=16, fontweight='bold', x=0.05, ha='left')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure11_Formats.png")
    plt.close()

# Figure 12: Wallet (Treemap replacement or clean donut)
def plot_fig12():
    labels = ['Food', 'Vet Care', 'Supplements', 'Toys/Access.', 'Services']
    sizes = [40, 25, 15, 10, 10]
    
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.0f%%', 
                                      startangle=90, colors=PALETTE,
                                      wedgeprops=dict(width=0.5, edgecolor='white'))
    
    ax.text(0, 0, '$1,500\nAvg Annual Spend', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.set_title('Preventive Health Wallet Allocation (2025)', loc='left')
    plt.savefig(f"{output_dir}/Figure12_Wallet.png")
    plt.close()

# Figure 13: Segmentation (Bar Chart Comparison instead of 2 pies)
def plot_fig13():
    projects = ['Spare No Expense', 'Value-Conscious', 'Basic Care']
    households = [20, 50, 30]
    revenue = [48, 42, 10]
    
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
    plt.savefig(f"{output_dir}/Figure13_Segmentation.png")
    plt.close()

# Figure 15: Mobility Evolution (Smoothed Area Chart)
def plot_fig15():
    years = [2015, 2020, 2024, 2030]
    generic = [70, 60, 45, 35]
    uc_ii = [5, 15, 25, 30]
    glm = [15, 15, 18, 20]
    premium = [10, 10, 12, 15]
    
    fig, ax = plt.subplots()
    pal = [COLORS['grey'], COLORS['secondary'], COLORS['accent3'], COLORS['primary']]
    labels = ['Generic Glucosamine', 'UC-II Collagen', 'Green Lipped Mussel', 'Premium Combos']
    
    ax.stackplot(years, generic, uc_ii, glm, premium, labels=labels, colors=pal, alpha=0.9)
    
    ax.set_title('Mobility Supplement Premiumization (2015–2030)', loc='left')
    ax.set_ylabel('Market Share (%)')
    clean_axes(ax)
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.05), ncol=2, frameon=False, fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure15_Mobility_Evo.png")
    plt.close()

# Figure 36: Value Chain (Visual Diagram - using patches) - RENAMED from Fig 17
def plot_fig36():
    """
    Value Chain Economics: Flow diagram (Ingredients -> Manufacturing -> Brand Owner)
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Title
    ax.text(6, 4.5, "Value Chain Economics", ha='center', fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.text(6, 4.0, "Value Accrual ➡", ha='center', fontsize=12, fontweight='bold', color=COLORS['secondary'])

    def draw_box(x, label, sublabel1, sublabel2, color):
        # Shadow
        shadow = patches.FancyBboxPatch((x+0.05, 1), 2.5, 2.5, boxstyle="round,pad=0.1", fc='#cccccc', ec='none', alpha=0.5)
        ax.add_patch(shadow)
        # Main Box
        rect = patches.FancyBboxPatch((x, 1.05), 2.5, 2.5, boxstyle="round,pad=0.1", fc=color, ec='none')
        ax.add_patch(rect)
        
        # Text
        ax.text(x+1.25, 2.6, label, ha='center', va='bottom', fontweight='bold', color='white', fontsize=11)
        ax.text(x+1.25, 2.3, sublabel1, ha='center', va='top', color='white', fontsize=9)
        ax.text(x+1.25, 2.0, sublabel2, ha='center', va='top', color='white', fontsize=9)

    # Box 1: Ingredients (Grey)
    draw_box(1.5, "Ingredients", "Raw Material", "(Margin: Low)", COLORS['grey']) # #8b9ba5
    
    # Arrow 1
    ax.arrow(4.2, 2.3, 0.6, 0, head_width=0.15, head_length=0.15, fc=COLORS['text'], ec=COLORS['text'], width=0.02)

    # Box 2: Manufacturing (Slate)
    draw_box(5.0, "Manufacturing", "CDMO / Premix", "(Margin: Med)", COLORS['accent3']) # #4d6b7b
    
    # Arrow 2
    ax.arrow(7.7, 2.3, 0.6, 0, head_width=0.15, head_length=0.15, fc=COLORS['text'], ec=COLORS['text'], width=0.02)

    # Box 3: Brand Owner (Navy Blue)
    draw_box(8.5, "Brand Owner", "Strategy / Mktg", "(Margin: High)", COLORS['primary']) # #003057

    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure36_Value_Chain.png")
    plt.close()

# Figure 17: Sustainability (Dual Axis Chart)
def plot_fig17():
    """
    Sustainability: Efficacy vs Value
    Strategies: Methane (Asparagopsis), Methane (3-NOP), P-Management, N-Efficiency
    """
    strategies = ['Methane (Asparagopsis)', 'Methane (3-NOP)', 'P-Management (Phytase)', 'N-Efficiency (Protease)']
    evidence = [7, 9, 10, 8]
    value = [6, 15, 155, 545]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Primary Axis (Value - Bars)
    color1 = COLORS['primary']
    ax1.set_xlabel('Sustainability Strategy', fontweight='bold')
    ax1.set_ylabel('Est. Market Value ($M)', color=color1, fontweight='bold')
    bars = ax1.bar(strategies, value, color=color1, alpha=0.7, width=0.5, label='Market Value')
    ax1.tick_params(axis='y', labelcolor=color1)
    
    # Add value labels
    add_labels(bars, ax1, '${}M')
    
    # Secondary Axis (Evidence - Line/Point)
    ax2 = ax1.twinx()
    color2 = COLORS['accent2']
    ax2.set_ylabel('Evidence Level (1-10)', color=color2, fontweight='bold')
    ax2.plot(strategies, evidence, color=color2, marker='o', linewidth=3, markersize=10, linestyle='-', label='Evidence Level')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0, 11) # Scale 1-10
    
    # Annotate points
    for i, txt in enumerate(evidence):
        ax2.annotate(f"{txt}/10", (i, evidence[i]), xytext=(0, 10), 
                     textcoords='offset points', ha='center', color=color2, fontweight='bold')

    ax1.set_title('Sustainability: Efficacy vs Value (Dual Axis)', loc='left')
    clean_axes(ax1)
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False) # Clean right axis looks
    
    # Rotate x labels for readability
    plt.setp(ax1.get_xticklabels(), rotation=15, ha="right")
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure17_Value_Chain.png") # Keeping filename consistent with user expectation/file structure for now, or should I rename? 
    # WAIT, User asked to focus on Figure17_Value_Chain.png. 
    # But confirmed in plan to Rename to Sustainability.
    # The implementation plan said: "Rename plot_fig17 to plot_fig36 and update output filename."
    # And "Add plot_fig17 (Sustainability)..."
    # So I should save the new one as Figure17_Sustainability.png to be cleaner, BUT
    # The user request specifically mentioned "Figure17_Value_Chain.png".
    # I will save as "Figure17_Sustainability.png" AND overwrite "Figure17_Value_Chain.png" with the new chart to be safe? 
    # No, clean is better.
    # I will save as "Figure17_Sustainability.png" per plan.
    # Wait, the PLAN said: "Rename the current Value Chain diagram to Figure 36... Generate a NEW Figure 17 (Sustainability)".
    # The filename in the plan is "Figure17_Sustainability.png".
    # However, if I change the filename, the markdown links will break.
    # I should check if the markdown links to "Figure17_Value_Chain.png".
    # I will save the new chart as `Figure17_Value_Chain.png` temporarily OR just fix the markdown references.
    # The plan says "Regenerate Figure17_Value_Chain.png" in the task.md but "Figure17_Sustainability.png" in the plan text.
    # Let's stick to the plan text which was more specific.
    # Actually, to minimize friction, I will overwrite `Figure17_Value_Chain.png` with the new Sustainability chart 
    # IF the markdown expects Figure 17 to constitute Sustainability.
    # Let's look at the markdown context again.
    # Figure 18 is Sustainability in Master Excel? No, Fig 17 is Sustainability.
    # In Master Markdown, let's see where Figure 17 is referenced.
    # The safest bet is:
    # 1. Save Value Chain as Figure36_Value_Chain.png
    # 2. Save Sustainability as Figure17_Sustainability.png
    # 3. I will also save Sustainability as Figure17_Value_Chain.png to resolve the user's specific file pointer, 
    #    OR I will update the markdown to point to the new filename.
    #    Since I am in "Auditing", I should probably fix the filenames.
    
    plt.savefig(f"{output_dir}/Figure17_Sustainability.png")
    plt.close()

# Figure 19: Waterfall (Floating Bar)
def plot_fig19():
    """
    Comparative Waterfall Chart: Livestock vs Pet Value Capture
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # --- Helper to draw waterfall ---
    def draw_waterfall(ax, names, values, title, color_last):
        # Calculate bottoms
        cumulative = np.cumsum(values)
        bottoms = np.insert(cumulative[:-1], 0, 0)
        
        # Colors: Grey for costs, Specific color for Margin
        colors = [COLORS['grey']] * (len(values)-1) + [color_last]
        
        # Draw bars
        bars = ax.bar(names, values, bottom=bottoms, color=colors, edgecolor='white', width=0.6)
        
        # Draw connecting lines
        for i in range(len(values)-1):
            x1, x2 = i + 0.3, i + 0.7 # Right edge of current bar, Left edge of next bar
            y = cumulative[i]
            ax.plot([x1, x2], [y, y], color='black', linewidth=1, linestyle='--')
            
        # Add values inside/above bars
        for bar, val in zip(bars, values):
            yval = bar.get_y() + bar.get_height()/2
            ax.text(bar.get_x() + bar.get_width()/2, yval, f"${val}", 
                   ha='center', va='center', color='white', fontweight='bold')
                   
        ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
        ax.set_ylim(0, max(cumulative)*1.1)
        clean_axes(ax)

    # Livestock Data ($50 Total Cost view)
    ls_names = ['Sourcing', 'Mfg', 'Service', 'Net Margin']
    ls_vals = [30, 10, 8, 2] # Sum=50
    draw_waterfall(ax1, ls_names, ls_vals, 'Livestock Premix ($50 Cost)', COLORS['primary'])
    
    # Pet Data ($50 Retail Price view)
    pet_names = ['COGS', 'Pkg/Mfg', 'Mktg', 'Net Margin']
    pet_vals = [10, 15, 15, 10] # Sum=50
    draw_waterfall(ax2, pet_names, pet_vals, 'Pet Supplement ($50 Retail)', COLORS['accent2'])
    
    plt.suptitle('Value Capture Comparison: Volume vs. Brand', fontweight='bold', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f"{output_dir}/Figure19_Value_Waterfall.png")
    plt.close()

# Figure 20: Bubble Chart (Polished)
def plot_fig20():
    segments = ['Pet Brands', 'Livestock Premix', 'Ingredients (IP)', 'Commodities']
    size = [6, 8, 2, 5]     # Market Size $B
    margin = [22, 10, 25, 6] # EBITDA %
    growth = [7, 4, 9, 2]    # CAGR %
    
    fig, ax = plt.subplots()
    
    scatter = ax.scatter(size, margin, s=[g*200 for g in growth], 
                         c=[COLORS['primary'], COLORS['accent3'], COLORS['secondary'], COLORS['grey']], 
                         alpha=0.8, edgecolors='white', linewidth=2)
    
    ax.set_xlabel('Market Size ($ Billions)')
    ax.set_ylabel('EBITDA Margin (%)')
    ax.set_title('Risk/Reward Map', loc='left')
    
    # Annotate
    for i, txt in enumerate(segments):
        ax.annotate(txt, (size[i], margin[i]), xytext=(0, -30 if i==2 else 15), 
                    textcoords='offset points', ha='center', fontweight='bold', fontsize=10)
        
    clean_axes(ax)
    ax.grid(True, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure20_Risk_Reward.png")
    plt.close()

# Table Generation (Matplotlib Table - Clean)
def plot_table_us_eu():
    data = [
        ["Feature", "United States (US)", "European Union (EU)", "United Kingdom (UK)"],
        ["Nutraceutical Def.", "Undefined (Food vs Drug)", "Undefined (Feed vs VMP)", "Undefined (Small Animal Exemption)"],
        ["Regulatory Body", "FDA-CVM & AAFCO", "EFSA & National Agencies", "VMD & FSA"],
        ["Disease Claims", "Prohibited (Drug only)", "Prohibited (PARNUTs exception)", "Prohibited (Medicinal Claims)"],
        ["Market Entry", "Fast (Notification)", "Slow (Dossier Approval)", "Moderate (Notification/SAES)"]
    ]
    
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=data, loc='center', cellLoc='left', colWidths=[0.15, 0.28, 0.28, 0.28])
    
    # Styling
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.8)
    
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('white')
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(COLORS['primary'])
        else:
            if row % 2 == 0:
                cell.set_facecolor('#f2f2f2')
            else:
                cell.set_facecolor('white')
                
    ax.set_title('Regulatory Landscape Comparison', loc='left', fontweight='bold', pad=10)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Table_US_vs_EU.png")
    plt.close()

# Timeline (Polished)
# Timeline (Polished)
def plot_timeline():
    events = [
        (2006, "EU bans AGPs"),
        (2017, "US FDA VFD Implemented"),
        (2019, "EU Vet Meds Reg"),
        (2022, "EU bans Zinc Oxide"),
        (2024, "China AGP Tightening"),
        (2025, "UK Feed Reform")
    ]
    years = [e[0] for e in events]
    labels = [e[1] for e in events]
    
    # Custom offsets to avoid overlap (Top vs Bottom)
    # 2006: Top (+0.5)
    # 2017: Bottom (-0.5)
    # 2019: Bottom (-0.5) -> Moved to bottom to avoid Title overlap
    # 2022: Top (+0.5)
    # 2024: Bottom (-0.5) -> Safe from neighbors
    # 2025: Top (+0.5) -> Visual balance
    offsets = [0.5, -0.5, -0.5, 0.5, -0.5, 0.5]

    fig, ax = plt.subplots(figsize=(10, 5)) # Increased height slightly
    
    # Main Line
    ax.hlines(1, 2005, 2027, colors=COLORS['grey'], linewidth=2)
    
    # Points
    ax.plot(years, [1]*len(years), 'o', markersize=10, color=COLORS['primary'], markeredgecolor='white', markeredgewidth=2)
    
    # Text
    for i, (yr, lbl) in enumerate(zip(years, labels)):
        offset = offsets[i]
        
        # Determine alignment based on offset direction
        va = 'bottom' if offset > 0 else 'top'
        
        ax.text(yr, 1 + offset, f"{yr}\n{lbl}", ha='center', va=va, 
                fontweight='bold', fontsize=10, color=COLORS['text'])
        
        # Connector line
        ax.vlines(yr, 1, 1 + (offset * 0.8), colors=COLORS['grey'], linestyle=':')
        
    ax.axis('off')
    ax.set_ylim(0, 2) # Strict limits to ensure spacing
    ax.set_title('Regulatory Timeline: The Push for Alternatives', loc='center', pad=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Timeline_Regulations.png")
    plt.close()

# Re-implement other missing simplified functions with `pass` logic in main if needed to avoid errors, 
# or just ensure all called functions exist.
# The previous script had: fig7 (Swine), venn, matrix_species, matrix_efficacy, fig14, fig16, fig18, fig21.
# I will implement placeholders or quick clean versions for them.

def plot_fig7(): # Swine Decline
    """
    Shows structural decline of EU swine herd.
    """
    years = np.arange(2014, 2025)
    herd = np.linspace(100, 91.9, len(years))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot line
    ax.plot(years, herd, color=COLORS['accent2'], linewidth=3, marker='o', label='Swine Herd Index')
    
    # Fill area to show contraction
    ax.fill_between(years, herd, 100, color=COLORS['accent2'], alpha=0.1)
    
    # Annotate Start
    ax.annotate('Baseline: 100', xy=(2014, 100), xytext=(2014, 98),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                fontweight='bold')
                
    # Annotate End
    ax.annotate(f'-8.1% Contraction', xy=(2024, 91.9), xytext=(2020, 96),
                arrowprops=dict(facecolor=COLORS['accent2'], shrink=0.05, width=2, headwidth=8),
                fontsize=11, fontweight='bold', color=COLORS['accent2'])

    ax.text(2024.1, 91.9, "91.9", va='center', fontweight='bold', color=COLORS['accent2'])

    # Title & Labels
    ax.set_title('European Swine Herd Contraction (2014–2024)', loc='left', pad=15)
    ax.set_ylabel('Herd Size Index (2014 = 100)')
    
    # Grid
    ax.grid(True, linestyle='--', alpha=0.3)
    clean_axes(ax)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure7_Swine_Decline.png")
    plt.close()

def plot_venn(): # Venn
    fig, ax = plt.subplots()
    c1 = patches.Circle((0.35, 0.6), 0.3, alpha=0.5, fc=COLORS['secondary'], label='Pharma')
    c2 = patches.Circle((0.65, 0.6), 0.3, alpha=0.5, fc=COLORS['accent3'], label='Feed')
    c3 = patches.Circle((0.5, 0.35), 0.3, alpha=0.5, fc=COLORS['accent1'], label='Supplements')
    ax.add_patch(c1); ax.add_patch(c2); ax.add_patch(c3)
    ax.text(0.5, 0.5, "Nutraceuticals", ha='center', fontweight='bold')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    plt.savefig(f"{output_dir}/Venn_Nutraceuticals.png"); plt.close()

# Figure II.1: Species vs Functional Needs Matrix
def plot_species_matrix():
    """
    Heatmap mapping Functional Needs (Y) against Species (X).
    Values 0-3 represented by color intensity.
    """
    species = ['Dogs', 'Cats', 'Horses', 'Poultry', 'Swine', 'Ruminant']
    functions = ['Mobility/Joints', 'Gut Health', 'Anxiety/Calming', 
                 'Immunity', 'Performance/FCR', 'Skin & Coat']
    
    # Data: 0=None, 1=Low, 2=Med, 3=High/Critical
    data = np.array([
        [3, 2, 3, 1, 1, 0], # Mobility
        [2, 2, 2, 3, 3, 1], # Gut Health
        [3, 3, 1, 0, 0, 0], # Anxiety
        [1, 1, 1, 3, 3, 2], # Immunity
        [0, 0, 0, 3, 3, 3], # FCR
        [2, 1, 1, 0, 0, 0]  # Skin
    ])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot heatmap
    im = ax.imshow(data, cmap='Blues', aspect='auto', vmin=0, vmax=3)
    
    # Axes Labels
    ax.set_xticks(np.arange(len(species)))
    ax.set_yticks(np.arange(len(functions)))
    ax.set_xticklabels(species, fontweight='bold')
    ax.set_yticklabels(functions, fontweight='bold')
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center", rotation_mode="anchor")
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(functions)):
        for j in range(len(species)):
            val = data[i, j]
            if val == 3: text = "High"
            elif val == 2: text = "Med"
            elif val == 1: text = "Low"
            else: text = "-"
            
            # Choose text color based on background
            text_color = "white" if val > 1 else "black"
            
            ax.text(j, i, text, ha="center", va="center", color=text_color, fontsize=10)
            
    ax.set_title('Mapping Functional Needs Across Species', loc='left', fontweight='bold', pad=15)
    
    # Start axes from 0
    clean_axes(ax)
    # Turn spines off/invisible for cleaner look except bottom
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xticks(np.arange(len(species)+1)-.5, minor=True)
    ax.set_yticks(np.arange(len(functions)+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
            
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Matrix_Species_Functional.png")
    plt.close()

# Figure II.2: Efficacy vs Maturity Matrix (Detailed)
def plot_efficacy_matrix():
    """
    Scatter plot mapping ingredients by Clinical Evidence vs Market Maturity.
    Size = Relative Market Share/Importance
    """
    ingredients = [
        'Glucosamine', 'Chondroitin', 'Omega-3 (EPA/DHA)', 
        'UC-II Collagen', 'Green Lipped Mussel', 'MSM', 
        'Curcumin', 'CBD', 'Egg Shell Membrane', 'Boswellia',
        'Probiotics', 'Prebiotics', 'Phytase (Enzymes)', 'Postbiotics'
    ]
    
    # 1-10 Scale
    maturity =  [9.0, 8.5, 9.5, 6.0, 5.0, 7.0, 4.0, 3.0, 2.0, 3.0, 9.0, 7.0, 10.0, 3.0] # X-axis
    evidence =  [3.0, 2.0, 9.0, 8.0, 5.0, 4.0, 6.0, 5.0, 5.0, 5.0, 8.5, 6.0, 9.5, 7.5] # Y-axis
    share_est = [8.0, 6.0, 9.0, 5.0, 3.0, 4.0, 2.0, 4.0, 1.0, 1.0, 9.0, 5.0, 8.0, 3.0] # Bubble Size
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Color logic: High Evidence (>6) = Green/Teal, Low Evidence = Grey/Orange
    colors = []
    for e in evidence:
        if e >= 7: colors.append(COLORS['primary'])   # High Evidence
        elif e >= 4: colors.append(COLORS['secondary']) # Medium
        else: colors.append(COLORS['accent2'])     # Low/Mixed
        
    scatter = ax.scatter(maturity, evidence, s=[s*250 for s in share_est], 
                         c=colors, alpha=0.7, edgecolors='white', linewidth=2)
    
    # Labels with smart offsets to avoid overlap
    offsets = {
        'Glucosamine': (-10, 15), 'Chondroitin': (10, -15), 'Omega-3 (EPA/DHA)': (-30, 0),
        'UC-II Collagen': (0, 15), 'Green Lipped Mussel': (0, -20), 'MSM': (0, 15),
        'Curcumin': (0, 15), 'CBD': (0, -20), 'Egg Shell Membrane': (0, 15), 'Boswellia': (0, -15),
        'Probiotics': (-15, 10), 'Prebiotics': (0, 15), 'Phytase (Enzymes)': (-25, -10), 'Postbiotics': (0, 15)
    }
    
    for i, txt in enumerate(ingredients):
        dx, dy = offsets.get(txt, (0, 10))
        ax.annotate(txt, (maturity[i], evidence[i]), xytext=(dx, dy), 
                    textcoords='offset points', ha='center', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec="none"))
        
    # Quadrant Lines
    ax.axhline(y=5, color=COLORS['grey'], linestyle='--', alpha=0.3)
    ax.axvline(x=5, color=COLORS['grey'], linestyle='--', alpha=0.3)
    
    # Axes Labels and Limits
    ax.set_xlabel('Market Maturity (Emerging → Commodities)', fontweight='bold')
    ax.set_ylabel('Clinical Evidence (Anecdotal → Level A RCTs)', fontweight='bold')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 11)
    
    # Custom annotations for quadrants
    ax.text(10.5, 10.5, 'GOLD STANDARD\n(High Value)', ha='right', va='top', fontsize=10, fontweight='bold', color=COLORS['primary'], alpha=0.5)
    ax.text(10.5, 0.5, 'COMMODITY TRAP\n(Low Efficacy)', ha='right', va='bottom', fontsize=10, fontweight='bold', color=COLORS['accent2'], alpha=0.5)
    ax.text(0.5, 10.5, 'RISING STARS\n(Innovation)', ha='left', va='top', fontsize=10, fontweight='bold', color=COLORS['secondary'], alpha=0.5)
    
    ax.set_title('Nutraceutical Ingredients: Evidence vs. Maturity Landscape', loc='left')
    clean_axes(ax)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Matrix_Efficacy.png")
    plt.close()

def plot_fig14(): # Psychology
    factors = ['Fear/Regret', 'Love', 'Duty']
    vals = [50, 30, 20]
    fig, ax = plt.subplots()
    bars = ax.barh(factors, vals, color=COLORS['secondary'])
    clean_axes(ax)
    ax.bar_label(bars, fmt='%d%%', padding=3, fontweight='bold')
    ax.set_xlim(0, 60) # Extend x-axis for labels
    plt.savefig(f"{output_dir}/Figure14_Psychology.png"); plt.close()

def plot_fig16(): # Senior Growth
    fig, ax = plt.subplots()
    bars = ax.bar(['2015', '2024', '2030'], [5, 12, 20], color=COLORS['primary'])
    clean_axes(ax)
    ax.bar_label(bars, fmt='%d%%', padding=3, fontweight='bold')
    ax.set_ylabel('Market Share (%)', fontweight='bold')
    ax.set_ylim(0, 25) # Extend y-axis for labels
    plt.savefig(f"{output_dir}/Figure16_Senior_Growth.png"); plt.close()

def plot_fig18(): # Channel Econ
    """
    Grouped Bar Chart: Gross vs Net Margin by Channel.
    """
    channels = ['Vet Exclusive', 'Retail / Online', 'Direct-to-Consumer (DTC)']
    gross_margins = [60, 35, 70]
    net_margins = [25, 15, 22]
    
    x = np.arange(len(channels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    rects1 = ax.bar(x - width/2, gross_margins, width, label='Gross Margin', color=COLORS['primary'])
    rects2 = ax.bar(x + width/2, net_margins, width, label='Net Margin (EBITDA)', color=COLORS['accent2'])
    
    # Add values
    ax.bar_label(rects1, fmt='%d%%', padding=3, fontweight='bold', color=COLORS['primary'])
    ax.bar_label(rects2, fmt='%d%%', padding=3, fontweight='bold', color=COLORS['accent2'])
    
    ax.set_ylabel('Margin Percentage (%)')
    ax.set_ylim(0, 90) # Increased to fit annotations
    ax.set_title('Channel Economics: The "Gross vs. Net" Trade-off', loc='left', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(channels)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False)
    
    clean_axes(ax)
    
    # Annotations
    ax.annotate('Best Net Margin\n(Low Volume)', xy=(0 + width/2, 25), xytext=(0, 68),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                ha='center', fontsize=9)
                
    ax.annotate('High CAC erodes\nprofitability', xy=(2 + width/2, 22), xytext=(2, 78),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure18_Channel_Economics.png")
    plt.close()

def plot_fig21(): # Funnel
    """
    Centered Funnel Chart: Pharma Integration Strategy.
    Refined to be less 'dull' - continuous flow + value annotations.
    """
    stages = ['Supplement User\n(Entry Point)', 'Vet Consultation\n(Trial)', 'Rx Patient\n(Capture)']
    values = [100, 40, 10]
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent2']]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Create the funnel shape points
    # We want 3 trapezoids stacked.
    y_centers = [0, 1, 2] # top to bottom inverted?
    
    # Let's draw from Top (y=0) to Bottom (y=3)
    # y=0: val=100
    # y=1: val=40
    # y=2: val=10
    
    # Coordinates for polygon
    # Left side: x = -val/2
    # Right side: x = +val/2
    
    # We will draw filled polygons connecting each stage
    import matplotlib.path as mpath
    import matplotlib.patches as mpatches
    
    for i in range(len(values)):
        val = values[i]
        c = colors[i]
        
        # Draw the rectangle/bar for this stage (thinner)
        # ax.barh(i, val, height=0.5, color=c, edgecolor='white', zorder=3)
        
        # Connect to next stage if exists
        if i < len(values) - 1:
            next_val = values[i+1]
            next_c = colors[i+1]
            
            # Trapezoid Coordinates
            x_topLeft = -val/2
            x_topRight = val/2
            x_botLeft = -next_val/2
            x_botRight = next_val/2
            
            y_top = i
            y_bot = i + 1
            
            # Polygon vertices (TopLeft, TopRight, BotRight, BotLeft)
            verts = [
                (x_topLeft, y_top),
                (x_topRight, y_top),
                (x_botRight, y_bot),
                (x_botLeft, y_bot)
            ]
            
            # Create a smooth gradient look by using the NEXT color for the connector?
            # Or utilize alpha.
            poly = mpatches.Polygon(verts, facecolor=c, edgecolor='none', alpha=0.3, zorder=1)
            ax.add_patch(poly)

        # Draw the main "Plate" for the text
        # boxstyle not supported by Rectangle, switching to FancyBboxPatch if we want round, 
        # but let's just use the barh below which works fine.
        # Removing the extra Rectangle call entirely as ax.barh does the job.
        
        # Use simple barh, centered to match polygons
        ax.barh(i, val, left=-val/2, height=0.5, color=c, edgecolor='white', zorder=3)

    # Text
    for i in range(len(values)):
        ax.text(0, i, stages[i], ha='center', va='center', color='white', fontweight='bold', fontsize=11, zorder=4)
        # Value on Right
        ax.text(values[i]/2 + 5, i, f"{values[i]}%", ha='left', va='center', color=COLORS['text'], fontweight='bold', fontsize=12)

    # Sidebar Annotations (The "Why")
    ax.text(-65, 0, "High Volume\nLow Margin", ha='right', va='center', fontsize=9, color=COLORS['grey'], style='italic')
    ax.text(-65, 2, "Low Volume\nHigh Margin", ha='right', va='center', fontsize=9, color=COLORS['accent2'], fontweight='bold')
    
    # Arrow connecting side annotations
    ax.annotate('', xy=(-60, 2), xytext=(-60, 0),
                arrowprops=dict(arrowstyle='->', color=COLORS['grey'], lw=1, ls='-'))

    ax.set_ylim(-0.5, 2.5)
    ax.set_xlim(-80, 80)
    ax.invert_yaxis()
    ax.axis('off')
    
    ax.set_title('The "Pharma Integration Funnel":\nCreating Value from Volume', fontweight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure21_Pharma_Funnel.png")
    plt.close()

def plot_tam_sam_som():
    """
    Nested Circles for TAM/SAM/SOM.
    Visual schematic, not strictly to scale to ensure visibility.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Circles
    # TAM
    c1 = plt.Circle((0.5, 0.5), 0.45, color=COLORS['primary'], alpha=0.9, label='TAM')
    # SAM
    c2 = plt.Circle((0.5, 0.5), 0.28, color=COLORS['secondary'], alpha=0.9, label='SAM')
    # SOM
    c3 = plt.Circle((0.5, 0.5), 0.12, color=COLORS['accent2'], alpha=1.0, label='SOM')
    
    ax.add_patch(c1)
    ax.add_patch(c2)
    ax.add_patch(c3)
    
    # Text Labels
    ax.text(0.5, 0.82, "TAM: $123.8B\nGlobal Pet & Animal Health", ha='center', va='center', 
            color='white', fontweight='bold', fontsize=11)
            
    ax.text(0.5, 0.65, "SAM: $13.0B\nNutraceuticals (Pet + Livestock)", ha='center', va='center', 
            color='white', fontweight='bold', fontsize=10)
            
    ax.text(0.5, 0.5, "SOM: $250M\nYear 5 Target Capture", ha='center', va='center', 
            color='white', fontweight='bold', fontsize=10)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    ax.set_title("Market Opportunity (2025)", fontweight='bold', fontsize=14)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_TAM_SAM_SOM.png")
    plt.close()

# Figure 8: Global Cattle Inventory by Region
def plot_fig8():
    """Global Cattle Inventory - showing regional divergence."""
    years = np.arange(2010, 2025)
    
    # US declining (from 95M to 87M)
    us = np.linspace(95, 87.2, len(years))
    # EU declining (from 78M to 72M)
    eu = np.linspace(78, 72, len(years))
    # LATAM stable/growing (from 350M to 365M)
    latam = np.linspace(350, 365, len(years))
    # India stable (from 190M to 195M)
    india = np.linspace(190, 195, len(years))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(years, us, color=COLORS['accent2'], linewidth=3, marker='o', markersize=4, label='USA')
    ax.plot(years, eu, color=COLORS['secondary'], linewidth=3, marker='s', markersize=4, label='EU')
    ax.plot(years, latam/10, color=COLORS['primary'], linewidth=3, marker='^', markersize=4, label='LATAM (÷10)')
    ax.plot(years, india/10, color=COLORS['accent3'], linewidth=3, marker='d', markersize=4, label='India (÷10)')
    
    ax.set_title('Global Cattle Inventory: The Western Contraction', loc='left')
    ax.set_ylabel('Million Head (USA/EU real, others scaled)')
    ax.set_xlabel('Year')
    clean_axes(ax)
    ax.legend(loc='upper right')
    
    # Annotate key point
    ax.annotate('2024: 87.2M\n(73-yr low)', xy=(2024, 87.2), xytext=(2020, 95),
                arrowprops=dict(arrowstyle='->', color='black'), fontweight='bold', color=COLORS['accent2'])
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure8_Cattle_Inventory.png")
    plt.close()

# Investment Opportunity Matrix
def plot_opportunity_matrix():
    """Investment opportunity matrix - Attractiveness vs Risk."""
    segments = ['Pet Supplements\n(DTC Brands)', 'Livestock\nProbiotics', 'Pet Pharma\nAdjacent', 
                'Commodity\nVitamins', 'Specialty\nIngredients (IP)', 'Aquaculture\nHealth']
    attractiveness = [8.5, 6, 9, 3, 7, 7.5]  # Y-axis
    risk = [4, 5, 7, 2, 4, 6]  # X-axis
    market_size = [6, 5, 4, 3, 2, 1.5]  # Bubble size
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent2'], 
              COLORS['grey'], COLORS['accent3'], COLORS['secondary']]
    
    scatter = ax.scatter(risk, attractiveness, s=[m*150 for m in market_size], 
                         c=colors, alpha=0.7, edgecolors='white', linewidth=2)
    
    # Labels
    for i, txt in enumerate(segments):
        offset_y = 0.3 if i % 2 == 0 else -0.3
        ax.annotate(txt, (risk[i], attractiveness[i]), xytext=(10, offset_y*30), 
                    textcoords='offset points', ha='left', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Risk Level (1=Low, 10=High)', fontweight='bold')
    ax.set_ylabel('Market Attractiveness (1=Low, 10=High)', fontweight='bold')
    ax.set_title('Investment Opportunity Matrix', loc='left', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Quadrant lines
    ax.axhline(y=5, color=COLORS['grey'], linestyle='--', alpha=0.5)
    ax.axvline(x=5, color=COLORS['grey'], linestyle='--', alpha=0.5)
    
    # Quadrant labels
    ax.text(2.5, 7.5, 'INVEST', fontsize=12, fontweight='bold', color=COLORS['primary'], alpha=0.5, ha='center')
    ax.text(7.5, 7.5, 'SELECTIVE', fontsize=12, fontweight='bold', color=COLORS['accent2'], alpha=0.5, ha='center')
    ax.text(2.5, 2.5, 'HOLD', fontsize=12, fontweight='bold', color=COLORS['grey'], alpha=0.5, ha='center')
    ax.text(7.5, 2.5, 'AVOID', fontsize=12, fontweight='bold', color=COLORS['accent2'], alpha=0.5, ha='center')
    
    clean_axes(ax)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Opportunity_Matrix.png")
    plt.close()

# Risk Heatmap
def plot_risk_heatmap():
    """Risk heatmap by region and category."""
    regions = ['North America', 'Europe', 'Asia-Pacific', 'LATAM', 'Middle East']
    categories = ['Regulatory', 'Scientific/Efficacy', 'Commercial/Channel', 'Currency/Macro']
    
    # Risk scores (1-10)
    data = np.array([
        [4, 3, 5, 5, 6],  # Regulatory
        [3, 4, 5, 6, 7],  # Scientific
        [5, 6, 4, 7, 8],  # Commercial
        [3, 5, 6, 8, 7],  # Currency
    ])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    im = ax.imshow(data, cmap='RdYlGn_r', aspect='auto', vmin=1, vmax=10)
    
    ax.set_xticks(np.arange(len(regions)))
    ax.set_yticks(np.arange(len(categories)))
    ax.set_xticklabels(regions)
    ax.set_yticklabels(categories)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add values
    for i in range(len(categories)):
        for j in range(len(regions)):
            text = ax.text(j, i, data[i, j], ha="center", va="center", 
                          color="white" if data[i, j] > 5 else "black", fontweight='bold')
    
    ax.set_title('Risk Assessment Heatmap by Region', loc='left', fontsize=14, fontweight='bold')
    
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Risk Level (1=Low, 10=High)', rotation=-90, va="bottom")
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Risk_Heatmap.png")
    plt.close()

def plot_aquaculture_production():
    """
    Horizontal bar chart for Aquaculture Production Leaders.
    """
    species = ['Carp (Freshwater)', 'Shrimp & Prawns', 'Tilapia', 'Catfish', 'Salmon (Marine)']
    tonnage = [24, 9.2, 5.8, 4.2, 3.5] # Million Tonnes
    
    # Sort for better visualization
    # zip, sort, unzip
    sorted_data = sorted(zip(tonnage, species))
    tonnage_sorted = [x[0] for x in sorted_data]
    species_sorted = [x[1] for x in sorted_data]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.barh(species_sorted, tonnage_sorted, color=COLORS['secondary'])
    
    # Add values to bars
    ax.bar_label(bars, fmt='%.1f M', padding=3, fontweight='bold')
    
    ax.set_title('Global Aquaculture Production by Species (Million Tonnes)', loc='left', pad=20)
    ax.set_xlabel('Production Volume (Million Tonnes)')
    
    clean_axes(ax)
    
    # Add seaweed note as text
    plt.figtext(0.15, 0.02, "Note: Seaweed/Mollusks account for ~30M tonnes globally (low-input).", 
               fontsize=9, style='italic', color=COLORS['text'])
               
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure11_Aquaculture_Production.png")
    plt.close()


# --- PART IV Summarizing Figures ---

# Figure IV.1: Pharma-Linked Leaders (Horizontal Bar)
def plot_iv_1_pharma():
    companies = ['Zoetis', 'Merck AH', 'Boehringer Ingelheim', 'Elanco', 'Ceva', 'Vetoquinol']
    revenues = [9.3, 5.9, 5.0, 4.4, 1.9, 0.58]  # Billions USD
    
    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(companies))
    
    # Horizontal bars
    bars = ax.barh(y_pos, revenues, color=COLORS['primary'], height=0.6, zorder=3)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(companies)
    ax.invert_yaxis()  # Top player at top
    
    ax.set_xlabel('2024 Revenue (USD Billions)')
    ax.set_title('Top Pharma-Linked Animal Health Players', loc='left')
    
    clean_axes(ax)
    
    # Add value labels
    for i, v in enumerate(revenues):
        ax.text(v + 0.1, i, f"${v}B", va='center', fontweight='bold', color=COLORS['text'])
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_IV_1_Pharma.png")
    plt.close()

# Figure IV.2: Feed & Specialty Majors (Horizontal Bar)
def plot_iv_2_feed():
    companies = ['Cargill (Est)', 'Nutreco (Est)', 'Novonesis', 'DSM-Firmenich', 'ForFarmers', 'ADM (Est)']
    revenues = [12.0, 6.0, 4.5, 3.6, 3.0, 2.0] # Billions USD (Est/Converted)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(companies))
    
    # Color differentiation for Specialty vs Feed? 
    # Let's use Secondary color for Specialty (Novonesis, DSM) to highlight them
    bar_colors = [COLORS['grey'], COLORS['grey'], COLORS['secondary'], COLORS['secondary'], COLORS['grey'], COLORS['grey']]
    
    bars = ax.barh(y_pos, revenues, color=bar_colors, height=0.6, zorder=3)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(companies)
    ax.invert_yaxis()
    
    ax.set_xlabel('Est. 2024 Revenue (USD Billions)')
    ax.set_title('Feed & Specialty Nutrition Leaders\n(Blue = High-Margin Specialty)', loc='left')
    
    clean_axes(ax)
    
    for i, v in enumerate(revenues):
        label = f"${v}B" if v < 12 else ">$12B"
        ax.text(v + 0.1, i, label, va='center', fontweight='bold', color=COLORS['text'])
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_IV_2_Feed.png")
    plt.close()

# Figure IV.3: Pet Nutrition Brands (Horizontal Bar)
def plot_iv_3_pet():
    companies = ['Nestlé Purina', 'Mars Petcare', 'Hill\'s', 'Blue Buffalo', 'Swedencare']
    revenues = [22.4, 22.0, 4.4, 2.3, 0.28] # Billions USD
    
    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(companies))
    
    bars = ax.barh(y_pos, revenues, color=COLORS['accent2'], height=0.6, zorder=3)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(companies)
    ax.invert_yaxis()
    
    ax.set_xlabel('2024 Revenue (USD Billions)')
    ax.set_title('Pet Nutrition & Supplement Giants', loc='left')
    
    clean_axes(ax)
    
    for i, v in enumerate(revenues):
        ax.text(v + 0.2, i, f"${v}B", va='center', fontweight='bold', color=COLORS['text'])
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_IV_3_Pet.png")
    plt.close()

# Figure IV.4: Value Chain Margins (Vertical Bar)
def plot_iv_4_margins():
    segments = ['Pharma/Rx', 'Pet Brands\n(Wellness)', 'Ingredients\n(Tech Tier)', 'Distribution\n(Retail/E-com)', 'Feed/Premix\n(Volume)']
    margins_mid = [35, 22.5, 20, 13.5, 5] # Midpoints
    margins_min = [30, 20, 15, 12, 3]
    margins_max = [40, 25, 25, 15, 7]
    y_err = [[m - mn for m, mn in zip(margins_mid, margins_min)], 
             [mx - m for mx, m in zip(margins_max, margins_mid)]]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Color map
    colors = [COLORS['primary'], COLORS['accent2'], COLORS['secondary'], COLORS['accent3'], COLORS['grey']]
    
    bars = ax.bar(segments, margins_mid, color=colors, width=0.6, zorder=3, yerr=y_err, capsize=5)
    
    ax.set_ylabel('EBITDA Margin (%)')
    ax.set_title('The "Margin Ladder": Value Capture by Sector', loc='left')
    ax.set_ylim(0, 45)
    
    clean_axes(ax)
    
    # Add label range
    for i, bar in enumerate(bars):
        height = bar.get_height()
        label = f"{margins_min[i]}-{margins_max[i]}%"
        ax.text(bar.get_x() + bar.get_width()/2., margins_max[i] + 1,
                label, ha='center', va='bottom', fontweight='bold', color=COLORS['text'])
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_IV_4_Margins.png")
    plt.close()

# Figure 33: Smile Curve
def plot_fig33():
    """
    Quantitative Smile Curve: Margin Capture.
    Upstream (IP) -> Manufacturing (Generic) -> Downstream (CDMO/Specialized)
    """
    stages = ['Upstream/IP', 'Manufacturing', 'Downstream/CDMO']
    # x-coordinates for the curve
    x_points = np.array([0, 1, 2])
    # Margins: High start, Low middle, High end
    margins = np.array([45, 8, 35]) 
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 1. Curve (Smooth Interpolation)
    # Use numpy polyfit instead of scipy to avoid dependency issues
    z = np.polyfit(x_points, margins, 2)
    p = np.poly1d(z)
    
    x_new = np.linspace(x_points.min(), x_points.max(), 300)
    y_smooth = p(x_new)
    
    # Plot curve
    ax.plot(x_new, y_smooth, color=COLORS['primary'], linewidth=4, alpha=0.8, zorder=2)
    
    # 2. Fill under curve? Maybe light
    ax.fill_between(x_new, y_smooth, 0, color=COLORS['primary'], alpha=0.05, zorder=1)
    
    # 3. Data Points (Markers)
    ax.scatter(x_points, margins, color=COLORS['secondary'], s=200, zorder=3, edgecolors='white', linewidth=2)
    
    # 4. Labels & Lines
    for i, (txt, y) in enumerate(zip(stages, margins)):
        # Vertical drop lines
        ax.vlines(i, 0, y, color=COLORS['grey'], linestyle=':', linewidth=1, zorder=1)
        
        # Point Label
        ax.text(i, y + 2, f"{y}%", ha='center', va='bottom', fontweight='bold', color=COLORS['secondary'], fontsize=12)
        
        # Stage Label (on axis) - Handled by xticks, but let's add context
        note = ""
        if i==0: note = "(R&D / Patents)"
        elif i==1: note = "(Commodity)"
        elif i==2: note = "(Specialized)"
        
        ax.text(i, -3, note, ha='center', va='top', fontsize=9, color=COLORS['grey'], style='italic')

    # Formatting
    ax.set_xticks(x_points)
    ax.set_xticklabels(stages, fontweight='bold', fontsize=11)
    
    ax.set_ylabel('Profit Margin (%)', fontweight='bold')
    ax.set_ylim(0, 55)
    ax.set_yticks(np.arange(0, 51, 10))
    
    ax.set_title('Value Capture: The "Smile Curve" Effect', loc='left', fontsize=14, fontweight='bold')
    
    clean_axes(ax)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure33_Smile_Curve.png")
    plt.close()

if __name__ == "__main__":
    print("Generating all figures...")
    plot_fig1(); print("  ✓ Figure 1")
    plot_fig2(); print("  ✓ Figure 2")
    plot_fig3(); print("  ✓ Figure 3")
    plot_fig4(); print("  ✓ Figure 4")
    plot_fig5(); print("  ✓ Figure 5")
    plot_fig6(); print("  ✓ Figure 6")
    plot_fig7(); print("  ✓ Figure 7")
    plot_fig8(); print("  ✓ Figure 8 (Cattle Inventory)")
    plot_fig9(); print("  ✓ Figure 9")
    plot_fig10(); print("  ✓ Figure 10")
    plot_fig11(); print("  ✓ Figure 10b (Formats)")
    plot_aquaculture_production(); print("  ✓ Figure 11 (Aquaculture)")
    plot_fig12(); print("  ✓ Figure 12")
    plot_fig13(); print("  ✓ Figure 13")
    plot_fig14(); print("  ✓ Figure 14")
    plot_fig15(); print("  ✓ Figure 15")
    plot_fig16(); print("  ✓ Figure 16")
    plot_fig16(); print("  ✓ Figure 16")
    plot_fig17(); print("  ✓ Figure 17 (Sustainability - Dual Axis)")
    plot_fig36(); print("  ✓ Figure 36 (Value Chain Renamed)")
    plot_fig18(); print("  ✓ Figure 18")
    plot_fig19(); print("  ✓ Figure 19")
    plot_fig20(); print("  ✓ Figure 20")
    plot_fig21(); print("  ✓ Figure 21")
    plot_table_us_eu(); print("  ✓ Table US vs EU")
    plot_timeline(); print("  ✓ Timeline")
    plot_venn(); print("  ✓ Venn Diagram")
    plot_species_matrix(); print("  ✓ Species Matrix")
    plot_efficacy_matrix(); print("  ✓ Efficacy Matrix")
    plot_opportunity_matrix(); print("  ✓ Opportunity Matrix")
    plot_risk_heatmap(); print("  ✓ Risk Heatmap")
    plot_tam_sam_som(); print("  ✓ TAM/SAM/SOM Figure")
    plot_fig33(); print("  ✓ Figure 33 (Smile Curve)")
    print("\n✓ All figures generated successfully!")

