from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 31",
    "mode": "donut",
    "output_file": "Figure12_Wallet.png",
    "title": "Preventive Health Wallet Allocation"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
