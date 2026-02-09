from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 30",
    "mode": "multi_donut",
    "output_file": "Figure11_Formats.png",
    "title": "Nutraceutical Delivery Format Preferences",
    "options": {
        "figsize": [13.5, 4.6],
        "title_size": 15,
        "colors": ["#0b3a63", "#1788c3", "#d04a02"],
        "group_titles": {
            "Dogs (%)": "Dogs\n(Taste Driven)",
            "Cats (%)": "Cats\n(Texture Driven)",
            "Horses (%)": "Horses\n(Feed Driven)"
        }
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
