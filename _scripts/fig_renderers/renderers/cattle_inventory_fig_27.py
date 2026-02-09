from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure Cattle Inventory",
    "mode": "line",
    "output_file": "Figure8_Cattle_Inventory.png",
    "title": "Global Cattle Inventory: The Western Contraction",
    "options": {
        "xlabel": "Year",
        "ylabel": "Million Head (USA/EU real, others scaled)",
        "colors": ["#d04a02", "#1788c3", "#0b3a63", "#526d7e"],
        "linestyles": ["-", "-", "-", "-"],
        "marker": "s",
        "markersize": 4.0,
        "linewidth": 2.2,
        "legend_loc": "center left",
        "legend_labels": {
            "US": "USA",
            "EU": "EU",
            "LATAM_scaled": "LATAM (÷10)",
            "India_scaled": "India (÷10)"
        },
        "annotation": {
            "text": "2024: 87.2M\\n(73-yr low)",
            "x": 2024,
            "y": 87.2,
            "text_x": 2020.0,
            "text_y": 93.0,
            "color": "#d04a02"
        }
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
