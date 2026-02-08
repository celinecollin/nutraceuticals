from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 28",
    "mode": "line",
    "output_file": "Figure9_Livestock_Trends.png",
    "title": "Divergent Production Trends: Poultry vs Bovine"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
