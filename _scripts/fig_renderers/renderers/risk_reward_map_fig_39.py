from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 39",
    "mode": "risk_reward",
    "output_file": "Figure20_Risk_Reward.png",
    "title": "Risk/Reward Map: Size vs Margin"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
