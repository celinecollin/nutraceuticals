from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 24",
    "mode": "dual_axis_bar_scatter",
    "output_file": "Figure5_Probiotics_Share.png",
    "title": "Probiotics Market: Volume Share vs Revenue"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
