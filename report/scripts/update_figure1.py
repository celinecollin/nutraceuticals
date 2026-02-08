
import pandas as pd
import matplotlib.pyplot as plt
import os

def update_figure1():
    # Paths
    csv_path = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/Figure1_Pet_Ownership.csv"
    output_dir = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/figures"
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Plot
    plt.figure(figsize=(10, 6))
    
    # Define colors (Blue for US, classic for others)
    colors = ['#1f77b4' if x == 'US' else '#aec7e8' for x in df['Region']]
    
    # Bar chart
    bars = plt.bar(df['Region'], df['Ownership Rate (%)'], color=colors)
    
    # Formatting
    plt.title('Pet Ownership Rates by Region', fontsize=16, fontweight='bold')
    plt.ylabel('Ownership Rate (%)', fontsize=12)
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add values on top
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{int(height)}%',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.tight_layout()
    
    # Save
    output_path = os.path.join(output_dir, "Figure1_Pet_Ownership.png")
    plt.savefig(output_path, dpi=300)
    print(f"Figure 1 updated: {output_path}")

if __name__ == "__main__":
    update_figure1()
