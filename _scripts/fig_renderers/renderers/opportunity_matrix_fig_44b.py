from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 44",
    "mode": "bar_horizontal",
    "output_file": "Opportunity_Matrix.png",
    "title": "Opportunity Matrix: Post-Commodity Technology Bets"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
