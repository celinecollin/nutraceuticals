
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def generate_venn_diagram():
    # 1. SETUP PLOT
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.axis('off') # Hide axes for a clean look

    # 2. DEFINE CIRCLES (The "Banker" Palette)
    # Circle 1: Pharmaceuticals (Top Left) - Blue
    circle_pharma = patches.Circle((-1.2, 1), 2.2, alpha=0.6, color='#3b86c4', label='Pharma')

    # Circle 2: Nutrition (Top Right) - Grey
    circle_nutrition = patches.Circle((1.2, 1), 2.2, alpha=0.6, color='#95a1a9', label='Nutrition')

    # Circle 3: Preventative (Bottom) - Light Grey/Beige
    circle_prevent = patches.Circle((0, -1.2), 2.2, alpha=0.5, color='#d0cfc9', label='Preventative')

    # Add patches to plot
    ax.add_patch(circle_pharma)
    ax.add_patch(circle_nutrition)
    ax.add_patch(circle_prevent)

    # 3. ADD LABELS
    # Font settings
    font_main = {'fontweight': 'bold', 'fontsize': 14, 'color': '#333333'}
    font_center = {'fontweight': 'bold', 'fontsize': 16, 'color': '#0B2C4D'}

    # External Labels (The Categories)
    ax.text(-2.5, 2.5, "Pharmaceuticals\n(Curative)", ha='center', va='center', **font_main)
    ax.text(2.5, 2.5, "Nutrition\n(Feed)", ha='center', va='center', **font_main)
    ax.text(0, -2.8, "Preventative Care\n(Wellness)", ha='center', va='center', **font_main)

    # Center Label (The Intersection)
    ax.text(0, 0, "NUTRACEUTICALS", ha='center', va='center', **font_center)

    # 4. FORMATTING
    ax.set_title("The Strategic Convergence: What Defines a Nutraceutical?", fontsize=16, fontweight='bold', pad=20)

    # 5. SAVE
    plt.tight_layout()
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."
             
    output_path = os.path.join(output_dir, 'Nutraceuticals_Venn_Complete.png')
    plt.savefig(output_path, dpi=300)
    print(f"Success: Venn diagram generated with completed industry labels at {output_path}")

if __name__ == "__main__":
    generate_venn_diagram()
