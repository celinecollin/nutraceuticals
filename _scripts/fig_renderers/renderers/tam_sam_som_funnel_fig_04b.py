from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 4",
    "mode": "concentric",
    "output_file": "Figure_TAM_SAM_SOM.png",
    "title": "Strategic Opportunity Funnel: TAM to SAM to SOM"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
