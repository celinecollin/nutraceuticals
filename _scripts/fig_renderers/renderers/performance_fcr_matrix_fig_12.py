from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 12",
    "mode": "dual_axis_bar_scatter",
    "output_file": "Figure_II_6_Matrix.png",
    "title": "Performance/FCR: Efficacy vs Value"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
