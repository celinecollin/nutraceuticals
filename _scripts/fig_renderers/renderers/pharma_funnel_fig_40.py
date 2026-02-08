from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 40",
    "mode": "funnel",
    "output_file": "Figure21_Pharma_Funnel.png",
    "title": "Pharma Integration Funnel"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
