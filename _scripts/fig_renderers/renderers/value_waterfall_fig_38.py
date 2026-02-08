from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 38",
    "mode": "value_waterfall",
    "output_file": "Figure19_Value_Waterfall.png",
    "title": "Value Waterfall: Livestock vs Pet Cost Structure"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
