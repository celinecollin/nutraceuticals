from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 43",
    "mode": "donut",
    "output_file": "Figure_IV_3_Pet.png",
    "title": "Global Pet Nutrition Market Share (Est. 2024)",
    "options": {
        "figsize": [10.8, 6.8],
        "colors": ["#d95d02", "#e67f22", "#f59e0b", "#facc15", "#92a1a6"],
        "ring_width": 0.34,
        "pctdistance": 0.84,
        "label_fontsize": 11,
        "pct_fontsize": 10,
        "center_total_text": "Top 2 players\ncontrol >45%",
        "center_fontsize": 17,
        "center_color": "#2f2f2f"
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
