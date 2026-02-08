from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 29",
    "mode": "bar_vertical",
    "output_file": "Figure11_Aquaculture_Production.png",
    "title": "The Blue Transformation: Aquaculture vs Capture"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
