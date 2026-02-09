from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 28",
    "mode": "line",
    "output_file": "Figure9_Livestock_Trends.png",
    "title": "Global protein production by species (2018-2023)",
    "options": {
        "xlabel": "Year",
        "ylabel": "Index (2018=100)",
        "colors": ["#0b3a63", "#d04a02", "#4c6f86", "#7f95a5"],
        "linestyles": ["-", "--", "--", ":"],
        "markers": False,
        "linewidth": 2.6,
        "legend_loc": "lower left",
        "end_labels": True,
        "end_label_fmt": "{name} ({change:+.1f}%)",
        "ymin": 88.5,
        "ymax": 111.5,
        "legend_labels": {
            "Poultry Index": "Poultry",
            "Bovine Index": "Bovine",
            "Pigs Index": "Pigs",
            "Sheep/Goat Index": "Sheep/Goat"
        }
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
