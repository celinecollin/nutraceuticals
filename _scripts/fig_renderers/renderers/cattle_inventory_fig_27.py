from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 27",
    "mode": "line",
    "output_file": "Figure8_Cattle_Inventory.png",
    "title": "US Cattle Inventory: The 70-Year Low"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
