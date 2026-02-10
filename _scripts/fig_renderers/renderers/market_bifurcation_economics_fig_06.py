from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 6",
    "mode": "grouped_bar",
    "output_file": "Figure_II_0_2_Market_Bifurcation.png",
    "title": "The Innovation Divergence: Pet vs. Livestock Structural Economics",
    "options": {
        "xlabel": "Structural Dimension",
        "ylabel": "Relative Intensity (1-10 scale)",
        "xtick_rotation": 10,
        "legend_loc": "upper right",
        "ymin": 0,
    },
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
