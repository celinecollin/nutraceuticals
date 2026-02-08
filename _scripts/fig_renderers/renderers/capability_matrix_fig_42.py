from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 42",
    "mode": "capability_matrix",
    "output_file": "Figure_IV_6_Capability_Matrix.png",
    "title": "Capability Matrix: Continuum of Care Coverage"
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
