# Unverified Claims Tracker

**STATUS: ACTIVE UNVERIFIED CLAIMS PRESENT AFTER v19 REINTEGRATION (2026-02-08)**

The report now intentionally contains unresolved items tagged `[UNVERIFIED]` where legacy `Master_WhitePaper_Final_v19.docx` content was restored but direct source traceability is not yet complete.

## Current Unverified Scope

- **Total active `[UNVERIFIED]` claims in registry:** 18
- **Claim IDs:** `C053, C054, C056, C058, C061, C063, C066, C070, C072, C073, C074, C075, C076, C077, C078, C079, C080, C081`
- **Primary impacted sections:** `I.2, I.3, II.1, II.2, II.3, III.1, III.2, III.3`

## What Is Unverified (By Theme)

- **Evidence-premium thresholds:** legacy Level A/B/C premium ranges and threshold conventions pending direct source linkage (`C053, C054`).
- **Segment overlays and concentration assumptions:** ectoparasite/pre-senior monetization splits and comparative concentration statements (`C056, C058, C066`).
- **Demography and ROI heuristics from legacy analysis:** format/channel-demography coupling and livestock 3:1 ROI hurdle assumption (`C061, C063`).
- **Strategic opportunity sizing assumptions:** legacy SOM target and scenario overlays from prior internal models (`C070, C076, C077`).
- **Competitive/valuation overlays:** legacy deal baskets, investor clustering, margin-ladder assumptions (`C072, C073, C078, C079, C080`).
- **Frontier framework assumptions:** green-label taxonomy details and gene-editing/longevity pathway assumptions (`C074, C075`).
- **Figure-source gaps:** Figures 38, 42, 43, and 44 currently point to unresolved source provenance (`C077, C079, C080, C081`).

## Resolution Workflow

1. Open `_registry/source_registry.xlsx` → `Claims` tab.
2. Filter `source_ids = UNVERIFIED`.
3. Validate each claim against an in-repo primary source.
4. Replace `[UNVERIFIED]` in section text with `[Sxxx]` tags.
5. Update each claim row (`source_ids`, `source_location`, `verified`, `date_verified`, `notes`).
6. Update this tracker summary after each verification pass.
