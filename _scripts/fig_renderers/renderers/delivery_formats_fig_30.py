from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 30",
    "mode": "stacked_column",
    "output_file": "Figure11_Formats.png",
    "title": "Preferred Delivery Formats by Species"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
