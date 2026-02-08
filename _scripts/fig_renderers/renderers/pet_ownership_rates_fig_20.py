from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 20",
    "mode": "bar_vertical",
    "output_file": "Figure1_Pet_Ownership.png",
    "title": "Pet Ownership Rates in Developed Markets"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
