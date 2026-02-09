from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 34",
    "mode": "stacked_area",
    "output_file": "Figure15_Mobility_Evo.png",
    "title": "Mobility Supplement Premiumization (2015-2030)",
    "options": {
        "figsize": [11.0, 6.3],
        "colors": ["#9aa8b4", "#2692c9", "#637d8f", "#244f75"],
        "ylabel": "Market Share (%)",
        "legend_loc": "upper left",
        "legend_size": 10
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
