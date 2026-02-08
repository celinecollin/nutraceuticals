# PRD: Source Registry & Traceability System

## Executive Summary

This document defines the traceability infrastructure for an equity research white paper project. The core problem: a 50+ page research report draws on hundreds of sources, and every factual claim, data point, and figure must be traceable to its origin. Without a system, neither the human author nor the AI agent can confidently distinguish verified research from potential hallucination.

The solution is a **Source Registry** — a single Excel workbook that serves as the project's source of truth for all provenance tracking — combined with **inline source tagging** in the report itself and a **changelog** for edit visibility.

---

## Problem Statement

The author is an equity research analyst producing a major white paper. The project involves:

- Hundreds of source documents (PDFs, reports, datasets, analyst notes)
- A 50+ page report written in Markdown, converted to Word for review
- ~30 figures, with underlying data in Excel
- An AI coding agent (Claude Opus via Anti-Gravity/IDX) assisting with edits

Current pain points:

1. **Provenance anxiety**: When the author sees a number in the report, she cannot quickly verify where it came from or whether the agent fabricated it.
2. **Folder chaos**: Source files are scattered with no naming convention or index.
3. **No edit visibility**: The agent makes changes, but there's no systematic record of what changed and why.
4. **Figure-data disconnect**: It's unclear which Excel tabs feed which figures, and whether the data is current.

---

## System Components

### 1. Source Registry (`source_registry.xlsx`)

A single Excel workbook with four tabs. This is the author's **control center**.

#### Tab 1: `Sources`

Every source used in the project gets exactly one row.

| Column | Type | Description |
|---|---|---|
| `source_id` | Text (S001, S002...) | Unique, immutable identifier. Never reuse IDs. |
| `short_name` | Text | Human-readable label (e.g., "McKinsey PE Q4 2025") |
| `type` | Dropdown | Report / Dataset / Interview / Press / Regulatory / Model Output / Internal Analysis |
| `filename` | Text | Relative path from project root (e.g., `sources/reports/mckinsey_pe_q4_2025.pdf`) |
| `original_url` | Text | URL if the source is publicly available (optional) |
| `date_published` | Date | Publication date of the source |
| `date_added` | Date | When it was added to the project |
| `added_by` | Dropdown | Author / Agent |
| `notes` | Text | Any context (e.g., "Key for Section 4, has EU fundraising data") |

**Rules:**
- Every file in `/sources/` MUST have a row here. No exceptions.
- If a file has no row, it is unregistered and must not be cited.
- Source IDs are sequential and never recycled. If S047 is deleted, S047 stays retired.

#### Tab 2: `Claims`

Every key factual claim, statistic, or data point in the report.

| Column | Type | Description |
|---|---|---|
| `claim_id` | Text (C001, C002...) | Unique identifier |
| `section` | Text | Report section reference (e.g., "3.2" or "exec_summary") |
| `claim_text` | Text | The exact claim as it appears (e.g., "PE dry powder reached €320B in 2025") |
| `source_ids` | Text | Comma-separated source IDs (e.g., "S023, S041") |
| `source_location` | Text | Where in the source (e.g., "Page 12, Exhibit 3" or "Tab: GDP, Cell D14") |
| `verified` | Checkbox | Author has personally confirmed this claim against the source |
| `agent_generated` | Checkbox | This claim was written or modified by the AI agent |
| `date_added` | Date | When the claim was added |
| `date_verified` | Date | When verification was completed (blank if not yet verified) |
| `notes` | Text | Any flags, concerns, or context |

**Rules:**
- Not every sentence needs a row — only **key claims**: statistics, percentages, rankings, projections, named findings.
- Agent-generated claims that are unverified should be visually flagged (conditional formatting: red background if `agent_generated = Y` AND `verified = N`).
- The author's review workflow: filter for `verified = N`, work through them one by one.

#### Tab 3: `Figures`

Every figure/chart/table in the report.

| Column | Type | Description |
|---|---|---|
| `figure_id` | Text (FIG-01, FIG-02...) | Matches the figure number in the report |
| `title` | Text | Figure title as it appears in the report |
| `type` | Dropdown | Bar Chart / Line Chart / Scatter / Table / Map / Diagram / Other |
| `data_source_ids` | Text | Which sources the data comes from (e.g., "S012, S034") |
| `excel_tab` | Text | Tab name in `_figures/figures_data.xlsx` where the underlying data lives |
| `excel_range` | Text | Cell range (e.g., "A1:F25") — optional but helpful |
| `report_section` | Text | Which section of the report this figure appears in |
| `status` | Dropdown | Placeholder / Data Entered / Chart Draft / Reviewed / Final |
| `last_updated` | Date | Last time the data or chart was modified |
| `notes` | Text | Any context |

**Rules:**
- Every figure referenced in the report MUST have a row here.
- The `excel_tab` must exactly match a tab name in `_figures/figures_data.xlsx`.
- A figure's status should only be "Final" after the author has personally reviewed both the data and the visual output.

#### Tab 4: `Sections`

High-level tracking of report sections.

| Column | Type | Description |
|---|---|---|
| `section_id` | Text | Section number (1, 2, 3.1, 3.2...) |
| `title` | Text | Section title |
| `md_file` | Text | Which markdown file contains this section (e.g., `sections/03_part_ii_strategic_bifurcation.md`) |
| `status` | Dropdown | Outline / First Draft / Agent Revised / Author Review / Final |
| `word_count_approx` | Number | Approximate word count |
| `figure_ids` | Text | Comma-separated figure IDs in this section |
| `key_sources` | Text | Primary source IDs for this section |
| `owner` | Dropdown | Author / Agent / Joint |
| `notes` | Text | What still needs to be done |

---

### 2. Inline Source Tagging (in Markdown)

Every factual claim in the report Markdown files must include a source tag.

**Format:** `[S023, p.8]` or `[S023, Tab: Regional_Data]` or `[S041, S042]` for multiple sources.

Example:
```
PE fundraising declined 23% YoY [S023, p.8], marking the third consecutive quarter 
of contraction [S023, p.12]. However, Asian markets showed resilience with a 7% 
increase [S041, Tab: Regional_Data].
```

**Special tags:**
- `[UNVERIFIED]` — Agent added this claim but could not trace it to a specific source. Must be resolved before final draft.
- `[AUTHOR-CHECK]` — Agent is reasonably confident but wants the author to verify.
- `[CALCULATION]` — Derived number, not directly from a source. Should reference the Excel tab where the calculation lives: `[CALCULATION, _figures/figures_data.xlsx, Tab: Derived_Metrics]`

The Word conversion script should transform `[S023, p.8]` tags into proper footnotes or endnotes in the final Word output.

---

### 3. Changelog (`CHANGELOG.md`)

A running log of every meaningful edit session.

**Format:**
```
## 2026-02-06 14:32 — Agent Session

### Changes Made
- **Section 3.2**: Updated GDP growth projections using S067 (ECB January Outlook)
- **Section 3.2**: Added new paragraph on inflation trajectory, sources S067, S071
- **Figure 12**: Updated data range in `_figures/figures_data.xlsx` (Tab: GDP_Forecast, extended through Q4 2026)
- **Claims Tracker**: Added C134-C137 for new claims in Section 3.2

### Files Modified
- `sections/03_part_ii_strategic_bifurcation.md`
- `_figures/figures_data.xlsx`
- `_registry/source_registry.xlsx`

### Flags for Author
- C135 marked [AUTHOR-CHECK]: ECB projects 1.8% growth, but IMF source (S034) says 2.1%. Used ECB figure. Please confirm preferred source.

---

## 2026-02-05 10:15 — Author Session

### Changes Made
- **Section 2.1**: Rewrote opening paragraph for clarity
- **Verified**: C098-C105 (all confirmed against original sources)

---
```

---

### 4. Figure Source-of-Truth Build Architecture

Figure production is a deterministic pipeline:

`_figures/figures_data.xlsx` -> `_scripts/build_figures_from_excel.py` -> `_scripts/fig_renderers/renderers/*.py` -> `_figures/exports/*.png` -> `_scripts/generate_whitepaper_docx.py` -> `_output/*.docx`

#### Design Rules

1. `/_figures/figures_data.xlsx` is the single source of truth for figure data.
2. Each figure has one renderer module in `/_scripts/fig_renderers/renderers/`.
3. The orchestrator (`build_figures_from_excel.py`) imports and runs renderers in fixed registry order.
4. Build is fail-fast and must output actionable error context (renderer module, tab, output file).
5. Figure PNGs in `/_figures/exports/` are generated artifacts and should not be manually edited.

#### Figure Registry Coupling

Any figure add/change requires synchronized updates to:
- `/_figures/figures_data.xlsx`
- `/_scripts/fig_renderers/renderers/<figure_renderer>.py`
- `/_scripts/fig_renderers/registry.py`
- `/_registry/source_registry.xlsx` (Figures tab)

`Figures.excel_tab` must exactly match a workbook tab name used by the renderer `SPEC`.

#### Special Case: Global Ecosystem Map (ES-1 / Figure 46)

- Background map source: `sources/internal/MapChart_Map .pdf` (in-repo).
- Overlay entity data source: `Figure 46` tab (`Region`, `Category`, `Entity`) in `figures_data.xlsx`.
- Render mode: `global_landscape` in `_scripts/fig_renderers/common.py`.

---

### 5. Build & QA Artifacts

#### Active Build Scripts

- `python3 _scripts/build_figures_from_excel.py`
- `python3 _scripts/generate_whitepaper_docx.py`

`generate_whitepaper_docx.py` must run figure rebuild as a required pre-step.

#### QA Evidence Outputs

- `_output/qa/figure_render_last_run.json` -> renderer-by-renderer run status.
- `_output/qa/figures_before_refactor.json` / `_output/qa/figures_after_refactor_comparison.*` -> figure regression evidence.
- `_output/qa/pdf_pages_<timestamp>/` -> page PNGs/contact sheets for manual visual final checks.

---

## Verification Workflow

The author's review process for any section:

1. Open the section Markdown file.
2. Open `_registry/source_registry.xlsx`, filter Claims tab to that section.
3. For each claim tagged `agent_generated = Y` and `verified = N`:
   a. Find the source file using the `source_ids` and `filename` columns.
   b. Navigate to the `source_location`.
   c. Confirm the claim matches the source.
   d. Check `verified = Y` and set `date_verified`.
4. Search the section for any `[UNVERIFIED]` or `[AUTHOR-CHECK]` tags and resolve them.
5. Update the section status in the Sections tab.

---

## Success Criteria

The system is working if:

1. The author can pick ANY number in the report and trace it to a source within 30 seconds.
2. The author can see at a glance which claims are verified vs. unverified.
3. The agent never introduces a factual claim without a source tag.
4. Figure data lineage is clear: Figure → Excel Tab → Source IDs.
5. Edit history is always visible via the Changelog.
6. The author feels in control of the project, not the agent.
7. Every figure in the final document is reproducible from `figures_data.xlsx` using the active script stack.
