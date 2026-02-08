
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_regulatory_timeline_arrow():
    # 1. DATA
    events = [ 
        (2006, "EU bans\nAGPs", 3),
        (2017, "US FDA VFD\nImplemented", -3),
        (2019, "EU Vet\nMeds Reg", 2),
        (2022, "EU bans\nZinc Oxide", -2),
        (2024, "China AGP\nTightening", 3),
        (2025, "UK Feed\nReform", -3)
    ]

    years = [e[0] for e in events]
    levels = [e[2] for e in events]

    # 2. PLOT SETUP
    fig, ax = plt.subplots(figsize=(12, 5))

    # 3. DRAW BASELINE (Directional)
    # Main line
    ax.plot([2005, 2026], [0, 0], color="#1f4e79", linewidth=2, zorder=1)

    # Arrowhead: ONLY on the right side ('>')
    # We remove the left arrow ('<') code entirely
    ax.plot(2026, 0, '>', color="#1f4e79", markersize=12, zorder=2, clip_on=False)

    # 4. DRAW STEMS & DOTS
    ax.vlines(years, 0, levels, color="#1f4e79", linestyle=":", linewidth=1.5)
    ax.plot(years, np.zeros_like(years), "o", color="#1f4e79", markeredgecolor="white", markersize=9, zorder=3)

    # 5. ADD TEXT LABELS
    for year, label, level in events: 
        va = 'bottom' if level > 0 else 'top'
        offset = 0.2 if level > 0 else -0.2

        full_text = f"{year}\n{label}"
        ax.text(year, level + offset, full_text, horizontalalignment='center', verticalalignment=va, 
                fontsize=10, fontweight='bold', color='#333333', 
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.8))

    # 6. FORMATTING
    ax.set_title("Regulatory Timeline: The Push for Alternatives", fontsize=14, fontweight='bold', pad=30)
    ax.yaxis.set_visible(False)
    ax.spines[['left', 'top', 'right', 'bottom']].set_visible(False)
    ax.xaxis.set_visible(False)

    ax.set_ylim(-5, 5)
    ax.set_xlim(2004, 2027)

    # 7. SAVE
    plt.tight_layout()
    
    output_dir = "report/master_report/figures"
    if not os.path.exists(output_dir):
        if os.path.exists("report/figures"):
             output_dir = "report/figures"
        else:
             output_dir = "."
             
    output_path = os.path.join(output_dir, 'Regulatory_Timeline_RightArrow.png')
    plt.savefig(output_path, dpi=300)
    print(f"Success: Timeline generated with a single right-pointing arrow at {output_path}")

if __name__ == "__main__":
    generate_regulatory_timeline_arrow()
