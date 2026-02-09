from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 41",
    "mode": "segmented_barh",
    "output_file": "Figure_IV_5_Revenue_Comparison.png",
    "title": "2024 Competitive Landscape: Revenue Scale Comparison",
    "options": {
        "xlabel": "Estimated 2024 Revenue (USD Billions)",
        "legend_loc": "lower right",
        "figsize": [11.2, 7.0]
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
