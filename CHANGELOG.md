# CHANGELOG

All notable changes to this project will be documented in this file.

---

## 2026-02-08

### Project Restructured
- **What:** Reorganized project folder structure for modular sections, source registry, and agent onboarding
- **Files created:**
  - Folder skeleton: `_registry/`, `sections/`, `sources/` (with subfolders), `_figures/`, `_output/`, `_scripts/`, `_workspace/`
  - `CHANGELOG.md` (this file)
  - `report_master.md` (section assembly order)
- **Agent:** Antigravity (Claude)
- **Notes:** This is the initial restructuring. Content migration will follow.

### Report Split into Modular Sections
- **What:** Split monolithic `Master_WhitePaper_Final.md` into 6 section files
- **Files created:**
  - `sections/00_front_matter.md` (~3KB)
  - `sections/01_executive_summary.md` (~3KB)
  - `sections/02_part_i_structural_bifurcation.md` (~16KB)
  - `sections/03_part_ii_strategic_bifurcation.md` (~12KB)
  - `sections/04_part_iii_value_chain.md` (~9KB)
  - `sections/05_appendices.md` (~7KB)
- **Backup created:** `_workspace/backup_20260208/` and `_workspace/original_report_backup.md`
- **report_master.md:** Updated with section assembly order
- **Agent:** Antigravity (Claude)
- **Notes:** All content preserved exactly. Original files untouched.

### Source Files Sorted (Step 5)
- **What:** Organized loose files from root into proper folders
- **Moves executed:**
  - `sources/academic/` ← 48 PDF research papers
  - `sources/datasets/` ← 37 CSV/Excel data files
  - `sources/internal/` ← 9 company lists/shortlists
  - `_figures/` ← 3 master Excel workbooks
  - `_workspace/scratch/` ← 96 DOCX drafts (archived)
- **Root cleaned:** No loose PDF/CSV/XLSX/DOCX files remain
- **Agent:** Antigravity (Claude)
- **Notes:** User ran mv commands manually due to OneDrive sync.

### Steps 6-9: Figures, Scripts, Git, and Root Cleanup
- **What:** Completed final restructuring per ANTIGRAVITY_BOOTSTRAP_PROMPT.md
- **Step 6 — Figure exports moved:**
  - `report/master_report/figures/*.png` → `_figures/exports/` (148 files)
  - Root-level `Figure*.png`, `Matrix_*.png`, `Table_*.png` → `_figures/exports/`
  - Total: 155 figure exports in `_figures/exports/`
  - Essential scripts copied to `_scripts/` (8 files: generate_docx_robust.py, fix_figures.py, etc.)
  - DOCX/PDF outputs → `_output/archive/`
- **Step 8 — Git initialized:**
  - Created `.gitignore` (excludes _output/, _workspace/, .DS_Store, *.tmp, ~$*, .venv/)
  - Created `_scripts/auto_commit.sh`
- **Step 9 — Root cleaned:**
  - 27 PPTX presentations → `_workspace/presentations/`
  - 9 Excel data files → `sources/datasets/`
  - 14 temp MD files → `_workspace/scratch/`
  - 4 reference docs (PRD, Bootstrap, etc.) → `_workspace/docs/`
  - 3 legacy folders (Articles, Adverse effects, archive) → `_workspace/archive/`
- **Final root contents:** AGENTS.md, CHANGELOG.md, GUIDE_POUR_DOUDOU.md, README.md, report_master.md, .gitignore
- **Agent:** Antigravity (Claude)
- **Notes:** Step 7 (source_registry.xlsx) pending. All file moves executed successfully via agent.
