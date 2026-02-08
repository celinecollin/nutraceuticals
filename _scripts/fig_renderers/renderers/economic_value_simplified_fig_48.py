from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 48",
    "mode": "simplified_stacked",
    "output_file": "Figure_II_12_Simplified.png",
    "title": "Figure II.12 (Simplified): Comparative Economic Value by Segment"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
