from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 45",
    "mode": "risk_reward",
    "output_file": "Figure_IV_5_Strategic_matrix.png",
    "title": "The \"Winner's Matrix\" (Strategic Positioning)",
    "options": {
        "figsize": [10.8, 6.4],
        "marker_color": "#2e6ea3",
        "marker_size": 160,
        "quadrants": True,
        "qx": 7.0,
        "qy": 7.0,
        "quadrant_labels": {
            "Q1": "Clinical Moat",
            "Q2": "Volume Scale",
            "Q3": "Speculative Fringe",
            "Q4": "Niche / Scientific"
        }
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
