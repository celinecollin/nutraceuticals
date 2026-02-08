from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 33",
    "mode": "bar_horizontal",
    "output_file": "Figure14_Psychology.png",
    "title": "Psychological Drivers of Purchase"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
