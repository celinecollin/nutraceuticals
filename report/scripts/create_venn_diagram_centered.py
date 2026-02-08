
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def generate_venn_diagram_centered():
    # 1. SETUP PLOT
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')
    ax.axis('off')

    # 2. DEFINE CIRCLES (Centers are Key here)
    # Center 1: (-1.2, 1)
    circle_pharma = patches.Circle((-1.2, 1), 2.2, alpha=0.6, color='#3b86c4')
    # Center 2: (1.2, 1)
    circle_nutrition = patches.Circle((1.2, 1), 2.2, alpha=0.6, color='#95a1a9')
    # Center 3: (0, -1.2)
    circle_prevent = patches.Circle((0, -1.2), 2.2, alpha=0.5, color='#d0cfc9')

    ax.add_patch(circle_pharma)
    ax.add_patch(circle_nutrition)
    ax.add_patch(circle_prevent)

    # 3. ADD LABELS (Now aligned to the geometric centers above)
    font_main = {'fontweight': 'bold', 'fontsize': 14, 'color': '#333333'}
    font_center = {'fontweight': 'bold', 'fontsize': 16, 'color': '#0B2C4D'}

    # Text 1: Centered in Blue Circle
    ax.text(-1.2, 1, "Pharmaceuticals\n(Curative)", ha='center', va='center', **font_main)
    # Text 2: Centered in Grey Circle
    ax.text(1.2, 1, "Nutrition\n(Feed)", ha='center', va='center', **font_main)
    # Text 3: Centered in Light Circle
    ax.text(0, -1.2, "Preventative Care\n(Wellness)", ha='center', va='center', **font_main)
    # Text 4: The Intersection
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
             
    output_path = os.path.join(output_dir, 'Nutraceuticals_Venn_Centered.png')
    plt.savefig(output_path, dpi=300)
    print(f"Success: Venn diagram regenerated with perfectly centered text at {output_path}")

if __name__ == "__main__":
    generate_venn_diagram_centered()
