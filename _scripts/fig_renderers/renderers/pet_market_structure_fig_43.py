from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 43",
    "mode": "donut",
    "output_file": "Figure_IV_3_Pet.png",
    "title": "Global Pet Nutrition Market Share"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
