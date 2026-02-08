from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 46",
    "mode": "global_landscape",
    "output_file": "Global_Antigravity_Landscape_Final.png",
    "title": "Global corporate, startup, and investor landscape by region."
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
