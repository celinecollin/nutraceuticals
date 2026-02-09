from __future__ import annotations

from ..common import RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 27",
    "mode": "bar_horizontal",
    "output_file": "Figure11_Aquaculture_Production.png",
    "title": "Global Aquaculture Production by Species (Million Tonnes)",
    "options": {
        "bar_color": "#1788c3",
        "figsize": [10.8, 6.1],
        "show_values": True,
        "value_suffix": " M",
        "xlabel": "Production Volume (Million Tonnes)"
    }
}


def render(ctx: RenderContext):
    return dispatch_render(ctx, SPEC)
