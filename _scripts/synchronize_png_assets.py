import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add script directory to path to allow import
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from generate_master_excel_full import FIGURES

# --- CONFIG ---
OUTPUT_DIR = '/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/figures'

# Brand Colors - Financial Standard
COLORS = {
    'primary': '#003057',    # Navy Blue (Evaluation / Strong)
    'secondary': '#0089cf',  # Bright Blue (Growth / Highlight)
    'accent1': '#b4a996',    # Beige/Gold (Neutral / Context)
    'accent2': '#d04a02',    # Burnt Orange (Alert / Secondary Metric)
    'accent3': '#4d6b7b',    # Slate Teal (Stable / Support)
    'grey': '#cccccc',       # Gridlines (Lighter for data-ink)
    'text': '#333333',       # Main Text
    'white': '#ffffff',
    'light_bg': '#ffffff'    # Clean white background
}

# Mapping from Excel Figure ID to MD Filename
FIGURE_MAP = {
    'Figure 1': 'Table_US_vs_EU.png',
    'Figure 2': 'Timeline_Regulations.png',
    'Figure 3': 'Figure_I_3_Regulatory_Matrix.png',
    'Figure 4': 'Figure_TAM_Reconciliation.png',
    'Figure 5': 'Figure_II_0_1_Innovation_Matrix.png',
    'Figure 6': 'Figure_II_0_2_Market_Bifurcation.png',
    'Figure 7': 'Figure_II_1_Matrix.png',
    'Figure 8': 'Figure_II_2_Matrix.png',
    'Figure 9': 'Figure_II_3_Matrix.png',
    'Figure 10': 'Figure_II_4_Matrix.png',
    'Figure 11': 'Figure_II_5_Matrix.png',
    'Figure 12': 'Figure_II_6_Matrix.png',
    'Figure 13': 'Figure_II_7_Matrix.png',
    'Figure 14': 'Figure_II_8_Matrix.png',
    'Figure 15': 'Figure_II_9_Matrix.png',
    'Figure 16': 'Figure_II_10_Matrix.png',
    'Figure 17': 'Figure_II_11_Matrix.png',
    'Figure 20': 'Figure1_Pet_Ownership.png',
    'Figure 21': 'Figure2_EU_Pet_Pop.png',
    'Figure 22': 'Figure3_EU_Growth.png',
    'Figure 23': 'Figure4_Regional_Market.png',
    'Figure 24': 'Figure5_Probiotics_Share.png',
    'Figure 25': 'Figure6_Poultry_HPAI.png',
    'Figure 26': 'Figure7_Swine_Decline.png',
    'Figure 27': 'Figure8_Cattle_Inventory.png',
    'Figure 28': 'Figure9_Livestock_Trends.png',
    'Figure 29': 'Figure11_Aquaculture_Production.png',
    'Figure 30': 'Figure11_Formats.png',
    'Figure 31': 'Figure12_Wallet.png',
    'Figure 32': 'Figure13_Segmentation.png',
    'Figure 33': 'Figure14_Psychology.png',
    'Figure 34': 'Figure15_Mobility_Evo.png', 
    'Figure 35': 'Figure16_Senior_Growth.png',
    'Figure 36': 'Figure17_Value_Chain.png',
    'Figure 37': 'Figure18_Channel_Economics.png',
    'Figure 38': 'Figure19_Value_Waterfall.png',
    'Figure 39': 'Figure20_Risk_Reward.png',
    'Figure 40': 'Figure21_Pharma_Funnel.png',
    'Figure 45': 'Figure_MA_Matrix.png' 
}


def set_financial_style():
    sns.set_theme(style="white")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.color'] = COLORS['grey']
    plt.rcParams['grid.alpha'] = 0.5
    plt.rcParams['grid.linestyle'] = '--'

def standardize_units(label):
    """Standardize currency/quantity abbreviations: $B→bn, $M→m, Millions→m."""
    if not isinstance(label, str):
        return label
    replacements = [
        ('($B)', '(bn)'), ('$B', 'bn'), ('Billions', 'bn'),
        ('($M)', '(m)'), ('$M', 'm'), 
        ('(Millions)', '(m)'), ('Millions', 'm'),
        ('Million Tonnes', 'm tonnes'), ('Million', 'm')
    ]
    result = label
    for old, new in replacements:
        result = result.replace(old, new)
    return result

def create_dual_axis_chart(figure_id, df, title, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Generating Dual-Axis {figure_id} -> {filename}...")
    
    # Setup Plot
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Primary Axis (Left Y) - Evidence Level - Bar Chart
    categories = df.iloc[:, 0]
    metric1_name = df.columns[1]
    metric1_values = df.iloc[:, 1]
    metric2_name = df.columns[2]
    metric2_values = df.iloc[:, 2]
    
    # Plot Bar on Primary - Simple Color for Professional Look
    sns.barplot(x=categories, y=metric1_values, ax=ax1, color=COLORS['primary'], alpha=0.8, label=metric1_name)
    ax1.set_ylabel(standardize_units(metric1_name), color=COLORS['primary'], fontsize=11, weight='bold')
    ax1.tick_params(axis='y', labelcolor=COLORS['primary'])
    ax1.set_xlabel('')
    ax1.set_xticklabels(categories, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Secondary Axis (Right Y) - Value - Scatter Plot (No Line)
    ax2 = ax1.twinx()
    # Use scatterplot to avoid implying continuity in categorical data
    sns.scatterplot(x=categories, y=metric2_values, ax=ax2, color=COLORS['accent2'], s=150, edgecolor='white', linewidth=1.5, label=metric2_name, zorder=10)
    ax2.set_ylabel(standardize_units(metric2_name), color=COLORS['accent2'], fontsize=11, weight='bold')
    ax2.tick_params(axis='y', labelcolor=COLORS['accent2'])
    ax2.spines['top'].set_visible(False) 
    ax2.set_ylim(0, max(metric2_values) * 1.2) # Add headroom for markers

    
    # Title
    plt.title(title, fontsize=14, color=COLORS['primary'], weight='bold', pad=20)
    
    # Clean Legend
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    # Unique labels to avoid duplicates from barplot hue
    by_label = dict(zip(labels_1 + labels_2, lines_1 + lines_2))
    ax1.legend(by_label.values(), by_label.keys(), loc='upper left', frameon=False)

    # Add explanatory footnote for Efficacy vs Value charts
    fig.text(0.5, 0.01, 
             'Evidence Level: Aggregate score from clinical trials (1-10). Est. Value: Segment market size.',
             ha='center', fontsize=8, style='italic', color=COLORS['text'], alpha=0.8)

    plt.tight_layout(rect=[0, 0.03, 1, 1])  # Leave room for footnote
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

def create_concentric_chart(figure_id, df, title, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Generating Concentric {figure_id} -> {filename}...")
    
    # Data
    labels = df.iloc[:, 0].tolist()
    values = df.iloc[:, 1].tolist()
    
    # Explicit Radii as requested: TAM (100%), SAM (33%), SOM (12%)
    # Data is sorted: TAM, SAM, SOM
    defined_radii = [1.0, 0.33, 0.12]
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Colors
    chart_colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent2']]
    
    # Draw Circles (Largest first)
    legend_handles = []
    
    for i, r in enumerate(defined_radii):
        # Circle - Add white border for high contrast separation
        circle = plt.Circle((0, 0), r, color=chart_colors[i % len(chart_colors)], label=labels[i], edgecolor='white', linewidth=3)
        ax.add_artist(circle)
        
        # Legend Handle (for proper labeling)
        import matplotlib.patches as mpatches
        label_text = f"{labels[i]}: ${values[i]}B"
        patch = mpatches.Patch(color=chart_colors[i % len(chart_colors)], label=label_text)
        legend_handles.append(patch)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Title
    plt.title(title, fontsize=12, color=COLORS['primary'], weight='bold') # Reduced pad, size
    
    # Legend to the right
    plt.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, fontsize=10)
    
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

def create_chart(figure_id, df, chart_type, title, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Generating {figure_id} -> {filename}...")
    
    # Setup Plot with Financial Style
    plt.figure(figsize=(10, 6))
    
    try:
        if chart_type == 'table':
            # Create a table plot - Detailed and Clean
            plt.axis('off')
            table = plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.8)
            
            # Style header
            for (row, col), cell in table.get_celld().items():
                if row == 0:
                    cell.set_text_props(weight='bold', color='white')
                    cell.set_facecolor(COLORS['primary'])
                    cell.set_edgecolor(COLORS['white'])
                else:
                    cell.set_edgecolor(COLORS['grey'])
                    if row % 2 == 0:
                        cell.set_facecolor(COLORS['light_bg'])
                    cell.set_linewidth(0.5)

        elif chart_type == 'pie':
            # Convert to DONUT CHART for Financial Standard
            colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent1'], COLORS['accent3'], COLORS['accent2']]
            # Wedgeprops width creates the donut hole
            wedges, texts, autotexts = plt.pie(df.iloc[:, 1], labels=df.iloc[:, 0], autopct='%1.1f%%', 
                                               colors=colors, startangle=90, pctdistance=0.85, 
                                               wedgeprops=dict(width=0.4, edgecolor='w'))
            
            # center_circle = plt.Circle((0,0),0.60,fc='white')
            # fig = plt.gcf()
            # fig.gca().add_artist(center_circle)
            
            # Styling text
            plt.setp(texts, size=10, weight="medium", color=COLORS['text'])
            plt.setp(autotexts, size=9, weight="bold", color="white")
            
        elif chart_type == 'scatter':
            x_col = df.columns[1]
            y_col = df.columns[2]
            label_col = df.columns[0]
            
            sns.scatterplot(x=x_col, y=y_col, data=df, s=150, color=COLORS['secondary'], edgecolor=COLORS['primary'], alpha=0.8)
            
            # Add clean labels
            for i in range(df.shape[0]):
                plt.text(df[x_col][i], df[y_col][i]+0.2, str(df[label_col][i]), 
                         horizontalalignment='center', size='small', color=COLORS['text'], weight='medium')
            
            # Axes labels
            plt.xlabel(x_col, weight='bold', color=COLORS['text'])
            plt.ylabel(y_col, weight='bold', color=COLORS['text'])

        elif chart_type in ['bar', 'column', 'combination']:
            # Reshape for seaborn
            df_melted = df.melt(id_vars=df.columns[0], var_name="Metric", value_name="Value")
            
            # Smart Color Logic: Use hue only if multiple metrics
            use_hue = len(df.columns) > 2
            palette = [COLORS['primary'], COLORS['secondary'], COLORS['accent3']] if use_hue else None
            color = COLORS['primary'] if not use_hue else None

            if chart_type == 'bar': # Horizontal
                ax = sns.barplot(data=df_melted, y=df.columns[0], x="Value", hue="Metric" if use_hue else None, 
                            palette=palette, color=color, alpha=0.9)
                plt.grid(axis='x', linestyle='--', alpha=0.5)
                plt.grid(axis='y', alpha=0) # No horizontal grid for horizontal bars
            else: # Vertical (Column)
                ax = sns.barplot(data=df_melted, x=df.columns[0], y="Value", hue="Metric" if use_hue else None, 
                            palette=palette, color=color, alpha=0.9)
                plt.grid(axis='y', linestyle='--', alpha=0.5)
                plt.grid(axis='x', alpha=0)
            
            plt.xticks(rotation=45, ha='right')
            plt.xlabel('')
            plt.ylabel('')
            
            if use_hue:
                plt.legend(frameon=False)

            # Special Handling for Figure 22 (EU Pet Growth) - Add Axis Labels
            if figure_id == 'Figure 22':
                plt.xlabel('Species', weight='bold', color=COLORS['text'])
                plt.ylabel('Growth Rate (%)', weight='bold', color=COLORS['text'])
                # Add % suffix to values if bar labels exist, or to ticks
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{int(x)}%"))

            # Special Handling for Figure 29 (Aquaculture) - Add Axis Labels
            if figure_id == 'Figure 29':
                plt.xlabel('Production Source', weight='bold', color=COLORS['text'])
                plt.ylabel('Production (m tonnes)', weight='bold', color=COLORS['text'])

            # Special Handling for Figure 35 (Senior Pet Wellness Market) - Add Axis Labels and Data Labels
            if figure_id == 'Figure 35':
                plt.xlabel('Year', weight='bold', color=COLORS['text'])
                plt.ylabel('Market Size (bn)', weight='bold', color=COLORS['text'])
                # Add data labels on top of each bar
                for container in ax.containers:
                    ax.bar_label(container, fmt='$%.0fbn', fontweight='bold', color=COLORS['primary'], padding=3)

            # Explanatory footnotes for ratio/index figures
            footnotes = {
                'Figure 32': 'Pareto Effect: Top 20% of households (Premium) capture 48% of revenue.',
                'Figure 26': 'Index: 2014 = 100 baseline. Decline reflects ASF-driven herd reduction.',
                'Figure 28': 'Index: 2018 = 100 baseline. Poultry growth offsets bovine decline.'
            }
            if figure_id in footnotes:
                plt.figtext(0.5, 0.01, footnotes[figure_id], 
                           ha='center', fontsize=8, style='italic', color=COLORS['text'], alpha=0.8)
                plt.subplots_adjust(bottom=0.12)  # Make room for footnote

        elif chart_type == 'line':
             df_melted = df.melt(id_vars=df.columns[0], var_name="Metric", value_name="Value")
             
             # Line styling
             sns.lineplot(data=df_melted, x=df.columns[0], y="Value", hue="Metric" if len(df.columns) > 2 else None, 
                          linewidth=2.5, palette=[COLORS['primary'], COLORS['secondary']] if len(df.columns) > 2 else [COLORS['primary']],
                          marker='o')
             
             plt.xticks(rotation=45)
             plt.xlabel('')
             plt.ylabel('')
             plt.grid(axis='y', linestyle='--', alpha=0.5)
             plt.legend(frameon=False)
             
             # Footnotes for Index line charts
             line_footnotes = {
                 'Figure 26': 'Index: 2014 = 100 baseline. Decline reflects ASF-driven herd reduction.',
                 'Figure 28': 'Index: 2018 = 100 baseline. Poultry growth offsets bovine decline.'
             }
             if figure_id in line_footnotes:
                 plt.figtext(0.5, 0.01, line_footnotes[figure_id],
                            ha='center', fontsize=8, style='italic', color=COLORS['text'], alpha=0.8)
                 plt.subplots_adjust(bottom=0.15)
        elif chart_type == 'area':
             # Clean area plot
             df.set_index(df.columns[0]).plot(kind='area', stacked=True, 
                                              color=[COLORS['primary'], COLORS['secondary'], COLORS['accent1'], COLORS['accent3']], 
                                              alpha=0.8)
             plt.xticks(rotation=45)
             plt.xlabel('')
             plt.grid(axis='y', linestyle='--', alpha=0.5)
             plt.legend(frameon=False)

        # Title and Clean Layout
        plt.title(title, fontsize=14, color=COLORS['primary'], weight='bold', pad=20)
        sns.despine(trim=True) # Remove top and right spines, trim left/bottom
        plt.tight_layout()
        
        # Save
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        print(f"Error generating {figure_id}: {e}")
        plt.close()

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    set_financial_style()    
    print(f"Synchronizing {len(FIGURES)} figures with Financial Standard Style...")
    
    for fig in FIGURES:
        fig_id = fig['id']
        
        # Batch Handling for Dual Axis (Figure 7 to Figure 17)
        # These are all Mobility/Functional Segments with Evidence (Bar) vs Value (Scatter)
        # Figure 32 (Segmentation) also uses this style: Households (Bar) vs Revenue (Scatter)
        dual_axis_figures = [f'Figure {i}' for i in range(7, 18)] + ['Figure 24', 'Figure 32']
        
        if fig_id in dual_axis_figures:
             if fig_id in FIGURE_MAP:
                filename = FIGURE_MAP[fig_id]
                create_dual_axis_chart(fig_id, fig['data'], fig['title'], filename)
             continue
        
        # Special Handling for Concentric (Figure 4)
        if fig_id == 'Figure 4':
             filename = FIGURE_MAP[fig_id]
             # Check if 'concentric' type in fig, else default logic
             if fig.get('type') == 'concentric':
                 create_concentric_chart(fig_id, fig['data'], fig['title'], filename)
             else:
                 # Fallback if type wasn't updated in generation script
                 create_chart(fig_id, fig['data'], 'pie', fig['title'], filename)
             continue
        
        if fig_id in FIGURE_MAP:
            filename = FIGURE_MAP[fig_id]
            create_chart(fig_id, fig['data'], fig['type'], fig['title'], filename)
        else:
             pass # Skip ones not in MD
    
    print("Synchronization Complete.")
