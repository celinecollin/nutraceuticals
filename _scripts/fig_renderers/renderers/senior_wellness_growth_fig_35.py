from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 35",
    "mode": "bar_vertical",
    "output_file": "Figure16_Senior_Growth.png",
    "title": "Growth of the Senior Pet Wellness Market"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
