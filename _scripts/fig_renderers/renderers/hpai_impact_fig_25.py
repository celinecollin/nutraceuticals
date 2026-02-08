from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 25",
    "mode": "area",
    "output_file": "Figure6_Poultry_HPAI.png",
    "title": "Impact of HPAI: Cumulative Bird Losses"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
