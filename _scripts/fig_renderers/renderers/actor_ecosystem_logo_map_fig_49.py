from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from ..common import RenderContext, read_df_from_tab, save_figure

SPEC = {
    "tab": "Figure 49",
    "mode": "custom",
    "output_file": "Figure_49_Actor_Ecosystem_Map.png",
    "title": "Strategic Actor Ecosystem: Pharma, Nutraceuticals, Feed, Retail, and Investors",
}


def render(ctx: RenderContext):
    df = read_df_from_tab(ctx.wb, SPEC["tab"])
    logo_dir = Path(__file__).resolve().parents[3] / "_figures" / "exports" / "logos"

    groups = []
    for g in df.iloc[:, 0].astype(str).tolist():
        if g not in groups:
            groups.append(g)

    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor("#f5f7fb")
    ax.set_facecolor("#f5f7fb")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    x_positions = [10, 30, 50, 70, 90]
    for i, g in enumerate(groups[:5]):
        x = x_positions[i]
        ax.text(x, 95, g, ha="center", va="center", fontsize=12, fontweight="bold", color="#0b3a63")
        part = df[df.iloc[:, 0].astype(str) == g]
        for j, row in enumerate(part.itertuples(index=False)):
            y = 82 - j * 14
            company = str(row[1])
            slug = str(row[2])
            lp = logo_dir / f"{slug}.png"
            if lp.exists():
                img = mpimg.imread(lp)
                ax.imshow(img, extent=(x - 3, x + 3, y - 3, y + 3), zorder=3)
            ax.text(x, y - 4.6, company, ha="center", va="top", fontsize=8, color="#333")

    ax.text(
        50,
        4,
        "Portfolio actor map derived from in-repo platform coverage tables (B.1/C.1). Logos are standardized in-repo badges for layout-consistent screening.",
        ha="center",
        va="center",
        fontsize=9,
        color="#555",
    )
    ax.set_title(SPEC["title"], fontsize=18, fontweight="bold", pad=14)
    return save_figure(fig, SPEC["output_file"], dpi=240)
