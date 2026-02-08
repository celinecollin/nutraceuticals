from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 17",
    "mode": "dual_axis_bar_scatter",
    "output_file": "Figure_II_11_Matrix.png",
    "title": "Sustainability: Efficacy vs Value"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
