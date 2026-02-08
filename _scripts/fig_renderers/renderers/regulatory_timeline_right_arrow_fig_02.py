from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 2",
    "mode": "timeline",
    "output_file": "Regulatory_Timeline_RightArrow.png",
    "title": "Regulatory Timeline: The Push for Alternatives"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
