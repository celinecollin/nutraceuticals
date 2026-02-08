from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 21",
    "mode": "donut",
    "output_file": "Figure2_EU_Pet_Pop.png",
    "title": "EU Pet Population Structure"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
