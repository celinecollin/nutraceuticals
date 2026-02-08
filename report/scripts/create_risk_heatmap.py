
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

def generate_risk_heatmap():
    # 1. DATA RECONSTRUCTION (From your heatmap)
    data = { 
        'Region': ['North America', 'Europe', 'Asia-Pacific', 'LATAM', 'Middle East'], 
        'Regulatory': [4, 3, 5, 5, 6], 
        'Scientific/Efficacy': [3, 4, 5, 6, 7], 
        'Commercial/Channel': [5, 6, 4, 7, 8], 
        'Currency/Macro': [3, 5, 6, 8, 7] 
    } 
    df = pd.DataFrame(data).set_index('Region')

    # Transpose to match the layout (Risks on Y-axis, Regions on X-axis)
    df_heatmap = df.T

    # 2. SETUP PLOT
    plt.figure(figsize=(10, 6))

    # 3. PLOT HEATMAP WITH FORCED BLACK TEXT
    # We use 'annot=True' to show numbers
    # We use 'fmt="d"' for integers
    # Crucial: 'annot_kws={"color": "black"}' forces the text black everywhere
    # RdYlGn_r: Low (Green) -> High (Red) for Risk
    ax = sns.heatmap(df_heatmap, annot=True, fmt="d", cmap="RdYlGn_r", linewidths=0.5, 
                     cbar_kws={'label': 'Risk Level (1=Low, 10=High)'}, 
                     annot_kws={"color": "black", "weight": "bold", "size": 12})

    # 4. FORMATTING
    plt.title('Risk Assessment Heatmap by Region', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=11)
    plt.yticks(rotation=0, fontsize=11)

    # 5. SAVE
    plt.tight_layout()
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."
             
    output_path = os.path.join(output_dir, 'Risk_Heatmap_BlackText.png')
    plt.savefig(output_path, dpi=300)
    print(f"Success: Heatmap regenerated with all numbers in black at {output_path}")

if __name__ == "__main__":
    generate_risk_heatmap()
