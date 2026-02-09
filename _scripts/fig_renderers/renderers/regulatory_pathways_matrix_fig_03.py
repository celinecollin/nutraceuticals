from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from ..common import EXPORTS_DIR, RenderContext, dispatch_render

# Source-of-truth mapping: figures_data.xlsx tab -> rendered PNG
SPEC = {
    "tab": "Figure 3",
    "mode": "scatter_cost_claim",
    "output_file": "Figure_I_3_Regulatory_Matrix.png",
    "title": "Regulatory Pathways: Cost vs Claim Strength"
}


def render(ctx: RenderContext):
    # User-mandated visual lock: reuse legacy Figure 3 design from the
    # 2026-02-08 21:01 document build for current Figure 4 placement.
    legacy_doc = EXPORTS_DIR.parents[1] / "_output" / "Nutraceuticals_Whitepaper_20260208-21-01.docx"
    legacy_media = "word/media/rId20.png"
    out = EXPORTS_DIR / SPEC["output_file"]
    if legacy_doc.exists():
        with ZipFile(legacy_doc, "r") as zf:
            if legacy_media in zf.namelist():
                out.write_bytes(zf.read(legacy_media))
                return out
    # Fallback keeps pipeline operational if the legacy build is missing.
    return dispatch_render(ctx, SPEC)
