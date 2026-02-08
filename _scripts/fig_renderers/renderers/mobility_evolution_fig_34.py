from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 34",
    "mode": "stacked_area",
    "output_file": "Figure15_Mobility_Evo.png",
    "title": "Evolution of Mobility Ingredients (Share %)"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
