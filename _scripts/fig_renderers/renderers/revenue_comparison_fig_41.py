from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 41",
    "mode": "bar_vertical",
    "output_file": "Figure_IV_5_Revenue_Comparison.png",
    "title": "Revenue Comparison: Pharma vs Nutrition"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
