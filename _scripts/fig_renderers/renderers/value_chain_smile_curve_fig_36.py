from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 36",
    "mode": "smile_curve",
    "output_file": "Figure33_Smile_Curve.png",
    "title": "Value Chain Economics: Margin Capture"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
