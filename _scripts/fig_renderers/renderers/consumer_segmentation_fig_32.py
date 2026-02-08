from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 32",
    "mode": "dual_axis_bar_scatter",
    "output_file": "Figure13_Segmentation.png",
    "title": "Consumer Segmentation: The Pareto Effect"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
