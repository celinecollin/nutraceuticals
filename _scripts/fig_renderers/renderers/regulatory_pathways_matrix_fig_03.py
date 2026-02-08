from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 3",
    "mode": "scatter_cost_claim",
    "output_file": "Figure_I_3_Regulatory_Matrix.png",
    "title": "Regulatory Pathways: Cost vs Claim Strength"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
