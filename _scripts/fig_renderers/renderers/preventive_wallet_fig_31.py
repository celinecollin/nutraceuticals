from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 31",
    "mode": "donut",
    "output_file": "Figure12_Wallet.png",
    "title": "Preventive Health Wallet Allocation (2025)",
    "options": {
        "figsize": [10.8, 6.3],
        "colors": ["#0b3a63", "#1788c3", "#d04a02", "#4c6f86", "#8a9ca8"],
        "ring_width": 0.43,
        "pctdistance": 0.72,
        "label_fontsize": 12,
        "pct_fontsize": 11,
        "center_total_text": "$1,500\\nAvg Annual",
        "center_fontsize": 15,
        "center_color": "#0b3a63"
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
