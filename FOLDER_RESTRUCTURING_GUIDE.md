# Project Folder Restructuring Guide

## Overview

This guide walks through reorganizing the white paper project from its current state (loose files, no conventions, single monolithic Markdown file) into a clean, maintainable structure that both the human author and AI agents can navigate reliably.

**Time estimate:** 2-4 hours total, done in phases. Can be spread over a weekend.

---

## Target Folder Structure

```
whitepaper/
│
├── AGENTS.md                          ← Agent onboarding instructions (THE key file)
├── CHANGELOG.md                       ← Running edit log
├── report_master.md                   ← Assembly order — defines which sections get stitched
│
├── _registry/
│   └── source_registry.xlsx           ← The control center (Sources, Claims, Figures, Sections tabs)
│
├── sections/                          ← One Markdown file per report section
│   ├── 00_front_matter.md             ← Title, disclaimers, TOC placeholder
│   ├── 01_executive_summary.md
│   ├── 02_introduction.md
│   ├── 03_market_overview.md
│   ├── 04_sector_deep_dive.md
│   ├── 05_competitive_landscape.md
│   ├── 06_financial_analysis.md
│   ├── 07_valuation.md
│   ├── 08_risks_and_outlook.md
│   ├── 09_conclusion.md
│   ├── 10_appendices.md
│   └── 99_bibliography.md             ← Generated from Sources tab
│
├── sources/                           ← All reference materials, organized by type
│   ├── reports/                       ← Industry reports, company filings, analyst notes
│   ├── datasets/                      ← CSV, Excel data files, raw data
│   ├── articles/                      ← Press, news, blog posts
│   ├── academic/                      ← Academic papers, working papers
│   ├── regulatory/                    ← Filings, regulations, policy docs
│   └── internal/                      ← Author's own prior work, firm research
│
├── _figures/
│   ├── figures_data.xlsx              ← All figure data. One tab per figure.
│   └── exports/                       ← Rendered images (PNG) for report embedding
│       ├── fig_01_market_size.png
│       └── ...
│
├── _output/                           ← Generated files. Never edit directly.
│   ├── latest/
│   │   └── whitepaper.docx            ← Most recent Word conversion
│   └── archive/                       ← Timestamped prior versions
│       ├── whitepaper_2026-02-03_1430.docx
│       └── ...
│
├── _scripts/
│   ├── convert.sh                     ← Main MD→Word conversion script
│   ├── validate_sources.py            ← Check all [SXXX] tags resolve to registry
│   └── auto_commit.sh                 ← Cron-based invisible git (optional)
│
├── _workspace/                        ← Author's personal space. Agent NEVER touches.
│   ├── notes/
│   ├── scratch/
│   └── review_comments.md
│
└── .git/                              ← Invisible version control
```

---

## Naming Conventions

### Section Files
- Pattern: `XX_short_name.md`
- `XX` = zero-padded number defining assembly order
- Use lowercase, underscores, no spaces, no special characters
- If you need to insert between 03 and 04: use `03a_new_section.md`
- The number is for ordering only — the actual section heading is inside the file

### Source Files
- Use descriptive names: `mckinsey_pe_dry_powder_q4_2025.pdf` NOT `report_v3_final.pdf`
- Lowercase, underscores, include year/quarter where relevant
- The filename in the folder must EXACTLY match the `filename` column in the Sources tab

### Figure Excel Tabs
- Pattern: `FIG_XX_short_name` (e.g., `FIG_12_pe_dry_powder`)
- Must match the `excel_tab` column in the Figures tracker
- Each tab contains: raw data, any transformations, and an Excel chart

### Output Files
- `_output/latest/whitepaper.docx` is always overwritten by the conversion script
- `_output/archive/` gets a timestamped copy every conversion
- Never edit output files. They're disposable.

---

## The `report_master.md` File

This is the assembly manifest. The conversion script reads it to stitch sections together.

```markdown
# Report Master — Assembly Order
# Lines starting with # are comments/ignored
# One section file per line, in order

sections/00_front_matter.md
sections/01_executive_summary.md
sections/02_introduction.md
sections/03_market_overview.md
sections/04_sector_deep_dive.md
sections/05_competitive_landscape.md
sections/06_financial_analysis.md
sections/07_valuation.md
sections/08_risks_and_outlook.md
sections/09_conclusion.md
sections/10_appendices.md
sections/99_bibliography.md
```

- To temporarily exclude a section (e.g., WIP appendix): delete or comment out the line.
- To reorder: move lines.
- The agent should NOT modify this file without explicit instruction.

---

## Migration Steps

### Step 0: Backup everything (5 minutes)

Before touching anything, make a full copy of the current project folder. Name it `whitepaper_backup_pre_restructure/` and put it somewhere safe (Desktop, external drive, wherever). This is your rollback.

### Step 1: Create the folder skeleton (10 minutes)

From the project root, create all the new folders:

```bash
mkdir -p sections
mkdir -p sources/{reports,datasets,articles,academic,regulatory,internal}
mkdir -p _registry
mkdir -p _figures/exports
mkdir -p _output/{latest,archive}
mkdir -p _scripts
mkdir -p _workspace/{notes,scratch}
```

Create the empty starter files:
```bash
touch AGENTS.md
touch CHANGELOG.md
touch report_master.md
```

### Step 2: Split the monolithic Markdown (30-60 minutes)

**This is the key structural change.** The current single report.md becomes multiple section files.

**Option A — Agent-assisted split (recommended):**

Give the agent this exact instruction:

> Read the current report file [filename]. Split it into individual section files in the `sections/` folder. Each major section (H1 or H2 level heading in the current document) becomes its own file. Follow the naming pattern `XX_short_name.md` where XX is a zero-padded number. Preserve ALL content exactly as-is — do not rewrite, reformat, or edit any text. Do not change any existing source references. After splitting, create `report_master.md` listing the files in order.

**Review the result carefully.** Open each section file and spot-check that content wasn't lost or duplicated.

**Option B — Manual split:**

Open the current report, identify section boundaries, copy-paste into new files. Slower but you maintain full control.

### Step 3: Sort source files (1-2 hours)

This is the tedious part but it's a one-time cost.

**Gather loose files:**

First, identify everything that's a source document. Look for:
- PDFs scattered at the root or in random subfolders
- Excel files that contain reference data (not the figures Excel)
- Downloaded reports, articles, papers

**Agent-assisted sorting:**

> List every file in the project that appears to be a source document (PDFs, CSVs, Excel files that aren't the main figures file, text documents that are reference materials rather than the report itself). For each, suggest: (1) which sources/ subfolder it belongs in, (2) a proposed source_id, (3) a proposed short_name for the registry. Present this as a table for my review before moving anything.

**Review the table.** Correct any misclassifications. Then let the agent execute the file moves.

After files are sorted, create `_registry/source_registry.xlsx` with the Sources tab populated. (The agent can create a starter version; you verify it.)

### Step 4: Build the Claims Tracker (2-3 hours, can be incremental)

This doesn't need to happen all at once. You can build it section by section over multiple work sessions.

**Per-section agent instruction:**

> Read `sections/03_market_overview.md`. Identify every key factual claim — any specific number, percentage, comparison, ranking, or named finding. For each, create a Claims Tracker entry: claim_id, section, claim_text, and your best guess at source_ids based on the sources registered in the Sources tab. If you can identify a source, mark agent_generated=Y, verified=N. If you cannot identify a source, mark it [UNVERIFIED]. Do NOT modify the section file during this step — only build the tracker.

Then the author reviews, verifies, and gradually checks off claims. This is ongoing work, not a one-shot task.

### Step 5: Add inline source tags (1-2 hours, incremental)

Once claims have source IDs assigned, add the `[SXXX]` tags to the Markdown.

**Per-section agent instruction:**

> For each claim in the Claims Tracker for section 03, add the corresponding [SXXX] inline source tag in the Markdown text. Add the tag immediately after the claim it supports. Do not modify the claim text itself. Work surgically — only add tags, change nothing else. Add a CHANGELOG entry for this session.

### Step 6: Populate Figures Tracker (30 min, author task)

Go through `figures_data.xlsx`, note each tab name, match it to a figure in the report. Fill in the Figures tab. The author knows the figure numbering better than anyone.

### Step 7: Move existing figures and scripts (15 min)

- Move the figures Excel to `_figures/figures_data.xlsx`
- Move any chart exports to `_figures/exports/`
- Move the conversion script to `_scripts/convert.sh` (update paths in the script)
- Move the current Word output to `_output/archive/` with a timestamp

### Step 8: Clean up the root (15 min)

After migration, the project root should only contain:
- `AGENTS.md`
- `CHANGELOG.md`
- `report_master.md`
- The folders listed in the target structure

Everything else should be in its proper subfolder, or in the backup if it's truly no longer needed. Don't delete anything you're unsure about — put it in `_workspace/scratch/` for now.

### Step 9: Initialize invisible Git (15 min)

```bash
cd whitepaper/
git init
echo "_output/" >> .gitignore
echo "_workspace/" >> .gitignore
echo ".DS_Store" >> .gitignore
git add -A
git commit -m "Initial commit: project restructured"
```

Optionally, set up auto-commit (save this as `_scripts/auto_commit.sh`):

```bash
#!/bin/bash
cd /path/to/whitepaper
if [[ $(git status --porcelain) ]]; then
    git add -A
    git commit -m "Auto-save $(date '+%Y-%m-%d %H:%M')"
fi
```

Add to cron (every 10 minutes):
```
*/10 * * * * /path/to/whitepaper/_scripts/auto_commit.sh
```

The author never sees or interacts with git. It just silently saves everything.

---

## What Goes Where — Quick Reference

| "I need to..." | Go to... |
|---|---|
| Edit the report | `sections/XX_name.md` |
| See what changed recently | `CHANGELOG.md` |
| Check if a claim is sourced | `_registry/source_registry.xlsx` → Claims tab |
| Find where a figure's data lives | `_registry/source_registry.xlsx` → Figures tab → excel_tab column |
| Find a source PDF | `_registry/source_registry.xlsx` → Sources tab → filename column |
| Preview the Word output | `_output/latest/whitepaper.docx` |
| Take personal notes | `_workspace/` (agent never touches this) |
| See an old draft | `_output/archive/` |

---

## OneDrive Considerations

The project folder can live in OneDrive. A few things to watch:

- The conversion script writes to `_output/latest/` (overwrite) and `_output/archive/` (new file). If Word has the latest file open, the overwrite may fail. The archive copy will still succeed, so you always have it.
- `.git/` inside OneDrive generally works fine for a single-user project. If you see sync conflicts on `.git/` files, add `.git` to OneDrive's exclusion list and keep version control local-only.
- `_workspace/` is personal scratch space — no sync conflicts possible since only the author touches it.
