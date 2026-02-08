from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 1",
    "mode": "table",
    "output_file": "Table_US_vs_EU.png",
    "title": "Regulatory Landscape Comparison: US vs EU vs UK vs China"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
