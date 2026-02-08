from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 16",
    "mode": "dual_axis_bar_scatter",
    "output_file": "Figure_II_10_Matrix.png",
    "title": "Delivery Systems: Maturity vs Value"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
