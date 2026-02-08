# Unverified Claims Tracker

**STATUS: ONLY TRULY UNSOURCED CLAIMS REMAIN (2026-02-08)**

Most legacy reinstated content is now source-bound (including `S128` for legacy v18 material). The remaining items below are the only claims that still have no direct, auditable source mapping in-repo.

## Current Unverified Scope

- **Total active `[UNVERIFIED]` claims in registry:** 3
- **Claim IDs:** `C054, C056, C058`
- **Primary impacted sections:** `I.2, I.3`

## What Is Unverified (By Theme)

- **Threshold heuristic validation gap:** prior internal threshold convention (`>5% R&D` and `>20% EBITDA`) is still not mapped to a direct source artifact (`C054`).
- **Segment overlay split gap:** specific monetization splits for selected overlays remain unbound (`C056`).
- **Concentration assumption gap:** comparative concentration assumptions for validated vs commodity categories remain unbound (`C058`).

## Resolution Workflow

1. Open `_registry/source_registry.xlsx` → `Claims` tab.
2. Filter `source_ids = UNVERIFIED`.
3. Validate each claim against an in-repo primary source.
4. Replace `[UNVERIFIED]` in section text with `[Sxxx]` tags.
5. Update each claim row (`source_ids`, `source_location`, `verified`, `date_verified`, `notes`).
6. Update this tracker summary after each verification pass.

**Resolved in this pass (2026-02-08):**

- C061 (Urban/Suburban trends) -> [S123]
- C063 (ROI 3:1) -> [S122]
- C072, C073, C084, C086 (Deal Multiples & Consolidation) -> [S125]
- C074 (Green Claims) -> [S126]
- C075 (Nutrigenomics) -> [S127]
- C076 (APAC AGP Dividend) -> [S124]
- C053, C070, C081, C088, C089, C090 -> [S128] (legacy v18 source added to `sources/internal/`)
