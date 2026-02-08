from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 4",
    "mode": "concentric",
    "output_file": "Figure_TAM_Reconciliation.png",
    "title": "Total Addressable Market (TAM) Reconciliation (2024)"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
