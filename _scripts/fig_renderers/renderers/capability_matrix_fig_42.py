from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 42",
    "mode": "capability_matrix",
    "output_file": "Figure_IV_6_Capability_Matrix.png",
    "title": "Strategic Portfolio Capabilities: The \"Continuum of Care\"",
    "options": {
        "figsize": [12.2, 6.9],
        "core_color": "#2f455c",
        "emerging_color": "#9aaeb2",
        "none_color": "#ffffff",
        "core_threshold": 0.75,
        "emerging_threshold": 0.25,
        "marker_size": 260,
        "x_rotation": 40,
        "xlabel": "",
        "ylabel": "",
        "legend": True,
        "legend_loc": "upper left",
        "legend_anchor": [1.01, 1.0]
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
