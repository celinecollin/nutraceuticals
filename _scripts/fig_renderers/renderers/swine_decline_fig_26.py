from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 26",
    "mode": "line",
    "output_file": "Figure7_Swine_Decline.png",
    "title": "EU Swine Herd Structural Decline (Index 2014=100)"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
