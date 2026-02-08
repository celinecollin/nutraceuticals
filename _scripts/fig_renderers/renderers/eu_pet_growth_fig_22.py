from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 22",
    "mode": "bar_vertical",
    "output_file": "Figure3_EU_Growth.png",
    "title": "EU Pet Population Growth (2018-2023)"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
