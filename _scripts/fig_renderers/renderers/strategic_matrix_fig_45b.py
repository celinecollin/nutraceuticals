from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 45",
    "mode": "risk_reward",
    "output_file": "Figure_IV_5_Strategic_matrix.png",
    "title": "Strategic Matrix: Evidence vs Scale"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
