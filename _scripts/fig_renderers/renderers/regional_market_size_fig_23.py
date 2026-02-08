from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 23",
    "mode": "bar_horizontal",
    "output_file": "Figure4_Regional_Market.png",
    "title": "Regional Market Size: Pet Nutraceuticals"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
