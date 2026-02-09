from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 36",
    "mode": "smile_curve",
    "output_file": "Figure33_Smile_Curve.png",
    "title": "Value Capture: The \"Smile Curve\" Effect",
    "options": {
        "figsize": [11.2, 6.4],
        "show_bars": False,
        "curve_color": "#355a7a",
        "curve_width": 3.4,
        "point_color": "#1788c3",
        "point_size": 180,
        "point_labels": True,
        "point_dy": 1.8,
        "show_guides": True,
        "legend": False,
        "category_subtitles": ["(R&D / Patents)", "(Commodity)", "(Specialized)"]
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
