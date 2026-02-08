
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def generate_regulatory_tradeoff_fixed():
    # 1. SETUP PLOT
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off') # We draw custom axes

    # 2. DRAW CUSTOM AXES (The "Fixed" Axis Arrows)
    # Y-Axis (Claims)
    ax.arrow(0.5, 0.5, 0, 7, head_width=0.2, head_length=0.3, fc='black', ec='black', width=0.02)
    ax.text(-0.2, 4, "Claim Strength (Effect) -->", rotation=90, va='center', fontsize=11, fontweight='bold')

    # X-Axis (Cost)
    ax.arrow(0.5, 0.5, 11, 0, head_width=0.2, head_length=0.3, fc='black', ec='black', width=0.02)
    ax.text(6, -0.3, "Development Cost & Time -->", ha='center', fontsize=11, fontweight='bold')

    # 3. DEFINE BOXES (Coordinates: x, y, width, height)
    # Box 1: Feed Material (Blue)
    box1 = patches.Rectangle((1, 1), 3, 2.5, linewidth=2, edgecolor='#3b86c4', facecolor='#e6f2ff')

    # Box 2: Feed Additive (Orange)
    box2 = patches.Rectangle((5, 3), 3, 2.5, linewidth=2, edgecolor='#ed7d31', facecolor='#fff2cc')

    # Box 3: Vet Drug (Red)
    box3 = patches.Rectangle((9, 5), 2.5, 2.5, linewidth=2, edgecolor='#c00000', facecolor='#fce4d6')

    ax.add_patch(box1)
    ax.add_patch(box2)
    ax.add_patch(box3)

    # 4. DRAW CONNECTING ARROWS (The "Fix")
    # Arrow from Box 1 to Box 2
    ax.annotate("", xy=(5, 4.25), xytext=(4, 2.25), arrowprops=dict(arrowstyle="->", color="grey", lw=2, connectionstyle="arc3,rad=-0.2"))

    # Arrow from Box 2 to Box 3
    ax.annotate("", xy=(9, 6.25), xytext=(8, 4.25), arrowprops=dict(arrowstyle="->", color="grey", lw=2, connectionstyle="arc3,rad=-0.2"))

    # 5. ADD TEXT CONTENT
    # Box 1 Text
    ax.text(2.5, 2.5, "FEED MATERIAL\n(Compliance)", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1f4e79')
    ax.text(2.5, 1.5, "No Claims\nGeneric Safety", ha='center', va='center', fontsize=9, style='italic')

    # Box 2 Text
    ax.text(6.5, 4.5, "FEED ADDITIVE\n(Function)", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#bf5a15')
    ax.text(6.5, 3.5, "Zootechnical Claims\nPerformance/Efficiency\n(EFSA/FDA Reviewed)", ha='center', va='center', fontsize=9, style='italic')

    # Box 3 Text
    ax.text(10.25, 6.5, "VET DRUG\n(Therapy)", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#990000')
    ax.text(10.25, 5.7, "Disease Claims\nCure/Mitigate\n(EMA/FDA Approved)", ha='center', va='center', fontsize=8, style='italic')

    # 6. FORMATTING
    ax.set_title("The Regulatory Trade-Off: Claims vs. Cost", fontsize=16, fontweight='bold', pad=20)

    # 7. SAVE
    plt.tight_layout()
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."
             
    output_path = os.path.join(output_dir, 'Regulatory_Tradeoff_FixedArrows.png')
    plt.savefig(output_path, dpi=300)
    print(f"Success: Arrows fixed to connect the strategic steps at {output_path}")

if __name__ == "__main__":
    generate_regulatory_tradeoff_fixed()
