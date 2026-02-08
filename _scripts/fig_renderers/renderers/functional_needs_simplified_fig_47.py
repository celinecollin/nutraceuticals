from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 47",
    "mode": "simplified_heatmap",
    "output_file": "Figure_II_1_Simplified.png",
    "title": "Figure II.1 (Simplified): Functional Needs by Species"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
