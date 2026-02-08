from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 37",
    "mode": "line",
    "output_file": "Figure18_Channel_Economics.png",
    "title": "Vet Channel Margin Erosion (Due to E-Comm)"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
