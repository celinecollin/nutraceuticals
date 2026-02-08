from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 44",
    "mode": "bar_vertical",
    "output_file": "Figure_IV_4_Margins.png",
    "title": "The Margin Ladder: Value Capture by Step"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
