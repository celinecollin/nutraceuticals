from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 21",
    "mode": "donut",
    "output_file": "Figure2_EU_Pet_Pop.png",
    "title": "Pet Population in Europe by Species (2023)",
    "options": {
        "figsize": [8.8, 5.4],
        "colors": ["#0b3a63", "#1788c3", "#b3aa99"],
        "ring_width": 0.40,
        "pctdistance": 0.78,
        "startangle": 90,
        "label_fontsize": 12,
        "pct_fontsize": 10,
        "center_total_text": "281M\nTotal",
        "center_fontsize": 15,
        "center_color": "#0b3a63"
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
