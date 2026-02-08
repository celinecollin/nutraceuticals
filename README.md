# Animal Nutraceuticals White Paper

## Overview
Comprehensive equity research report analyzing the global animal nutraceuticals market ($13B+), covering regulatory frameworks, market bifurcation (Pet vs. Livestock), competitive landscape, and value chain economics.

**Target:** Institutional investors, equity research analysts, and strategic acquirers.

---

## Project Structure

```
├── AGENTS.md                      # Agent operating manual (READ FIRST)
├── CHANGELOG.md                   # Project audit trail
├── report_master.md               # Section assembly order
├── sections/                      # Modular report sections
│   ├── 00_front_matter.md
│   ├── 01_executive_summary.md
│   ├── 02_part_i_structural_bifurcation.md
│   ├── 03_part_ii_strategic_bifurcation.md
│   ├── 04_part_iii_value_chain.md
│   └── 05_appendices.md
├── sources/                       # Source materials
│   ├── academic/                  # Academic papers, regulatory docs
│   ├── datasets/                  # Excel/CSV data files
│   ├── reports/                   # Corporate filings and market reports
│   └── internal/                  # Internal analysis files
├── _registry/
│   └── source_registry.xlsx       # 128 sources, 91 tracked claims, 45 figures
├── _figures/exports/              # 155 chart exports (PNG)
├── _output/                       # Generated DOCX outputs
├── _scripts/                      # Automation scripts
└── _workspace/                    # Working files, drafts, backups
```

---

## Source Registry System

All claims, figures, and sources tracked in **`_registry/source_registry.xlsx`**:
- **Sources tab:** 128 registered sources
- **Claims tab:** 91 claims tracked (including active `[UNVERIFIED]` rows for unresolved legacy reintegration items)
- **Figures tab:** 45 figures mapped to Master Excel data
- **Sections tab:** 6 sections tracked

**Verification Status:** ⚠ In progress (`[UNVERIFIED]` claims remain active and require source completion before external distribution).

---

## Quick Start

### For Reviewers
1. Open `_registry/source_registry.xlsx` to browse sources and claims
2. Read sections in `sections/` folder (ordered by `report_master.md`)
3. Check inline source tags (e.g., `[S089, Tab: Figure 4]`) for provenance

### For Authors
1. **Read `AGENTS.md` first** — defines all rules and conventions
2. Edit section files in `sections/`
3. Add new sources to `sources/` and register in `source_registry.xlsx`
4. Update `CHANGELOG.md` after changes

### For AI Agents
1. **Read `AGENTS.md` before ANY edits**
2. Follow source tagging conventions (`[SXXX]`, `[CALCULATION]`, `[AUTHOR-CHECK]`, `[UNVERIFIED]`)
3. Update `source_registry.xlsx` Claims tab for new claims
4. Log changes in `CHANGELOG.md`

---

## Documentation

- **`AGENTS.md`** — Agent onboarding manual (THE key file)
- **`PRD_SOURCE_REGISTRY.md`** — Source registry system design
- **`_archive/docs/FOLDER_RESTRUCTURING_GUIDE.md`** — Project structure rationale (archived reference)
- **`GUIDE_POUR_DOUDOU.md`** — Non-technical project overview
- **`UNVERIFIED_CLAIMS.md`** — Active tracker for unresolved verification items

---

## GitHub Repository
[github.com/celinecollin/nutraceuticals](https://github.com/celinecollin/nutraceuticals)

---

## Status

| Component | Status |
|-----------|--------|
| Source Registry | ✅ Linked (128 sources with in-repo file paths) |
| Sections | ✅ Complete (6 files with inline tags) |
| Figures | ✅ Ready (45 mapped, 155 exports available) |
| DOCX Generation | ✅ Complete (`_output/latest/whitepaper.docx`) |

**Last Updated:** 2026-02-08
