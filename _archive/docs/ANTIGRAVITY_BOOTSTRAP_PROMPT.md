# PASTE THIS INTO ANTI-GRAVITY'S CODING AGENT

---

I'm restructuring this white paper project. I have three reference documents that describe the target state. I'll paste their contents below. **Do NOT delete any existing work.** This is a live project with real content.

Execute the following steps IN ORDER. After each major step, tell me what you did and wait for my OK before continuing. Do not batch everything silently.

---

## STEP 1: Assess current state

Before changing anything:
- List the current folder structure (all files and folders, recursive)
- Identify the main report file(s) — the Markdown file(s) containing the white paper content
- Identify any existing AGENTS.md or agent instruction files
- Identify any Excel files (figures data, source tracking, etc.)
- Identify loose source files (PDFs, datasets, articles scattered around)
- Show me a summary of what you found. Do not modify anything yet.

## STEP 2: Create the folder skeleton

Create the new folder structure WITHOUT moving any existing files yet:

```
_registry/
sections/
sources/reports/
sources/datasets/
sources/articles/
sources/academic/
sources/regulatory/
sources/internal/
_figures/exports/
_output/latest/
_output/archive/
_scripts/
_workspace/notes/
_workspace/scratch/
```

Also create these empty starter files if they don't already exist:
- `CHANGELOG.md` (with a header and first entry: "Project restructured")
- `report_master.md` (empty template, we'll populate after splitting)

## STEP 3: Merge AGENTS.md

If an AGENTS.md already exists:
- Read the existing one carefully
- Merge it with the new AGENTS.md content below — keep any existing project-specific instructions, custom rules, or context that are still relevant
- The new version's structure and rules take priority, but don't lose useful existing content
- Put any displaced existing content in a "## Legacy Instructions" section at the bottom if you're unsure whether to keep it

If no AGENTS.md exists, create it from the content below.

Show me the merged result before writing it.

## STEP 4: Split the monolithic Markdown (if applicable)

If the report is currently in a single Markdown file:
- Split it into individual section files in `sections/`
- Each major section (H1 or H2 heading) becomes its own file
- Naming: `XX_short_name.md` (e.g., `01_executive_summary.md`, `03_market_overview.md`)
- **PRESERVE ALL CONTENT EXACTLY** — do not rewrite, reformat, edit, or "improve" anything
- Do not change any existing source references or citations
- After splitting, populate `report_master.md` with the file list in order
- **Keep the original monolithic file as a backup** — rename it to `_workspace/original_report_backup.md`

If the report is already split into multiple files, skip this step but still create `report_master.md` listing the existing files in order.

Show me the list of section files created and their approximate line counts before proceeding.

## STEP 5: Sort source files

Identify all files that appear to be source/reference materials (PDFs, CSVs, data Excel files that aren't the main figures workbook, articles, etc.) — anything that's NOT the report content, NOT scripts, NOT config.

For each file, propose:
- Which `sources/` subfolder it belongs in (reports, datasets, articles, academic, regulatory, internal)
- A suggested source_id (S001, S002...)

**Show me the proposed mapping as a table. Do not move files until I approve.**

## STEP 6: Move figures and scripts

- Move any figures/charts Excel workbook to `_figures/figures_data.xlsx` (or rename in place if already well-located)
- Move any exported chart images to `_figures/exports/`
- Move any build/conversion scripts to `_scripts/`
- Move any existing Word output files to `_output/archive/` with their current dates

## STEP 7: Create the Source Registry Excel

Create `_registry/source_registry.xlsx` with four tabs:

**Tab: Sources** — columns: source_id, short_name, type, filename, original_url, date_published, date_added, added_by, notes

**Tab: Claims** — columns: claim_id, section, claim_text, source_ids, source_location, verified (checkbox), agent_generated (checkbox), date_added, date_verified, notes

**Tab: Figures** — columns: figure_id, title, type, data_source_ids, excel_tab, report_section, status, last_updated, notes

**Tab: Sections** — columns: section_id, title, md_file, status, figure_ids, key_sources, owner, notes

Pre-populate:
- The Sources tab with whatever source files we mapped in Step 5
- The Sections tab with the section files from Step 4
- Leave Claims and Figures tabs with headers only (we'll populate incrementally)

## STEP 8: Initialize Git

```bash
git init
```

Create `.gitignore`:
```
_output/
_workspace/
.DS_Store
*.tmp
~$*
```

Stage everything and make the initial commit:
```bash
git add -A
git commit -m "Project restructured: modular sections, source registry, agent onboarding"
```

Create `_scripts/auto_commit.sh`:
```bash
#!/bin/bash
cd "$(dirname "$0")/.."
if [[ $(git status --porcelain) ]]; then
    git add -A
    git commit -m "Auto-save $(date '+%Y-%m-%d %H:%M')"
fi
```

Make it executable: `chmod +x _scripts/auto_commit.sh`

## STEP 9: Clean up root

After everything is moved, the project root should only contain:
- `AGENTS.md`
- `CHANGELOG.md`
- `report_master.md`
- The folders from the structure above
- `.git/` and `.gitignore`
- Any config files needed by the IDE/build system

If there are files left at the root that don't fit anywhere, move them to `_workspace/scratch/` — do NOT delete them.

Show me the final folder structure when done.

---

## IMPORTANT BEHAVIORAL RULES FOR THIS SESSION

- **Do not rewrite or edit any report content.** You are reorganizing files, not editing the paper.
- **Do not delete any files.** Move them or rename them. If truly unnecessary, move to `_workspace/scratch/`.
- **Show me what you plan to do before doing it** for steps 3, 4, 5, and any ambiguous decisions.
- **If you're unsure where something goes, ask.** Don't guess.
- **The conversion script paths will break after restructuring.** Flag this — we'll fix it in a follow-up session.

---

## REFERENCE DOCUMENT 1: AGENTS.md (new version to merge)

[PASTE THE CONTENTS OF AGENTS.md HERE]

---

## REFERENCE DOCUMENT 2: PRD — Source Registry System

[PASTE THE CONTENTS OF PRD_SOURCE_REGISTRY.md HERE — OR JUST TELL THE AGENT: "See AGENTS.md for the registry spec, it covers the same information"]

---

## REFERENCE DOCUMENT 3: Folder Structure Reference

[PASTE THE CONTENTS OF FOLDER_RESTRUCTURING_GUIDE.md HERE — OR JUST TELL THE AGENT: "The folder structure is defined in Steps 2-6 above, follow that"]

---

**Start with Step 1 now. Show me the current state of the project before changing anything.**
