from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 5",
    "mode": "innovation_matrix",
    "output_file": "Figure_II_0_1_Innovation_Matrix.png",
    "title": "The Innovation-Premium Matrix: R&D Intensity vs EBITDA Margin"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
