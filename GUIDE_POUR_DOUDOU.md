# Guide pour Doudou 🐻

## What just happened to your project

Renaud reorganized your white paper project folder. Nothing was deleted. All your content is exactly where it was — it's just been sorted into a proper structure so that both you and the AI agent can find things without going crazy.

Here's the short version: **you now have a control center** (an Excel file) where you can track every source, every key number, and every figure in your report. The agent has been given strict rules about how to behave. And the report itself has been split into manageable pieces instead of one giant file.

---

## The 3 things you actually need to know

### 1. Your control center is the Excel file

**`_registry/source_registry.xlsx`** — this is YOUR file. It has four tabs:

- **Sources** — every PDF, report, dataset you're using. Each one has an ID (S001, S002...). Think of it as your bibliography database.
- **Claims** — every key number and fact in your report. Each one links back to a source. If you see a number and wonder "where did this come from?", look it up here.
- **Figures** — every chart and table, which Excel tab has its data, which sources feed it.
- **Sections** — overview of each section's status (draft, reviewed, final, etc.)

**You don't need to fill this all in yourself.** The agent populates it as it works. But you're the one who marks things as "verified" — the agent can never do that. That's your quality stamp.

### 2. The report is now in pieces (this is a good thing)

Instead of one huge Markdown file, each section of the report is now its own file inside the `sections/` folder:

```
sections/01_executive_summary.md
sections/02_part_i_structural_bifurcation.md
sections/03_part_ii_strategic_bifurcation.md
sections/04_part_iii_value_chain.md
sections/05_appendices.md
```

**Why this helps you:** When you ask the agent to update Section 3, it only opens and edits that one file. It can't accidentally mess up Section 7 while it's in there. And when you review changes, you only see what changed in that section.

The conversion script still produces one Word document at the end — that part doesn't change.

### 3. Every number now has a tag

In the Markdown files, you'll see things like:

> PE fundraising declined 23% YoY [S023, p.8]

That `[S023, p.8]` means: this number comes from Source S023, page 8. You can look up S023 in your Excel's Sources tab to find the actual file.

If you ever see `[AUTHOR-CHECK]` — that means the claim needs your explicit validation before finalization.  
If you ever see `[UNVERIFIED]` — that means no source was identified and it must be resolved before sending.

---

## Your daily workflow

### When you want to work on the report yourself

1. Open the section file you want to edit (e.g., `sections/04_sector_analysis.md`)
2. Edit directly in the Markdown
3. When you add a new fact or number, add a source tag: `[S047, p.12]`
4. If it's a new source, add a row to the Sources tab in your Excel
5. That's it — the auto-save (Git) will capture your changes silently

### When you want the agent to do something

Just tell it what you want in natural language. Examples:

> "Update Section 3 with the latest ECB data. The source is in sources/reports/ecb_jan2026.pdf"

> "Add a new subsection in Section 5 about ESG regulation. Use sources S045 and S067."

> "Check all the numbers in Section 2 and flag anything that doesn't have a source tag."

> "The McKinsey Q4 report has been updated. Replace the old fundraising figures in Sections 3 and 6."

The agent knows the rules. It will:
- Only edit the files you asked about (not the whole report)
- Add source tags to everything
- Update the Claims Tracker in your Excel
- Write a changelog entry so you can see what it did

### When you want to review what the agent changed

1. Open `CHANGELOG.md` — it's at the root of the project. Each entry says: what was changed, which files, which claims, and any flags for you.
2. Open `source_registry.xlsx` → Claims tab → filter by "agent_generated = Y" and "verified = N" — these are the things the agent wrote that you haven't checked yet.
3. Go through them, check each claim against the source, and tick "verified" when you're satisfied.

### When you want to preview the Word document

Ask the agent: "Convert to Word" or run the conversion script. The output lands in `_output/latest/whitepaper.docx`. Old versions are automatically saved in `_output/archive/`.

### When you get a new source document

1. Drop it in the right `sources/` subfolder (reports, datasets, articles, etc.)
2. Add a row to the Sources tab — give it the next S-number, a short name, and the filename
3. Tell the agent: "I added a new source S[number]. Incorporate it into Section X."

Or just tell the agent to do steps 1-2 for you — it knows how.

---

## The folder structure at a glance

```
Your project/
│
├── AGENTS.md                    ← Rules for the AI agent (you don't need to touch this)
├── CHANGELOG.md                 ← Log of everything that changed ← READ THIS REGULARLY
├── report_master.md             ← Which sections go in what order
│
├── _registry/
│   └── source_registry.xlsx     ← YOUR CONTROL CENTER 📊
│
├── sections/                    ← The report, one file per section ← YOU WORK HERE
│   ├── 01_executive_summary.md
│   ├── 02_introduction.md
│   └── ...
│
├── sources/                     ← All your reference materials, sorted by type
│   ├── reports/
│   ├── datasets/
│   ├── articles/
│   └── ...
│
├── _figures/
│   ├── figures_data.xlsx        ← All figure data (one tab per figure)
│   └── exports/                 ← Chart images
│
├── _output/                     ← Word documents live here. Don't edit them.
│   ├── latest/
│   └── archive/
│
├── _workspace/                  ← Your personal notes. Agent NEVER sees this.
│   ├── notes/
│   └── scratch/
│
└── _scripts/                    ← Conversion and utility scripts
```

**Folders starting with `_` are "infrastructure."** You'll mostly live in `sections/`, `sources/`, and `_registry/`.

---

## Things that might worry you (and why they shouldn't)

**"What if the agent messes something up?"**
Git is saving a snapshot of everything every 10 minutes. Nothing is ever truly lost. If something goes wrong, Renaud can roll back to any point in time. You'll never need to touch Git yourself.

**"What if I don't understand the source tags?"**
They're just labels. `[S023, p.8]` = "this fact comes from source number 23, page 8." Look up S023 in your Excel to see which file that is. That's all there is to it.

**"What if I forget to update the Excel?"**
The agent updates it when it works. You only need to update it when YOU add a new source or verify a claim. If you forget sometimes, it's fine — better to have an incomplete registry than no registry.

**"What if I accidentally edit the wrong file?"**
Git has your back. And the conversion script only uses what's listed in `report_master.md`, so a stray edit to a random file won't break the final document.

**"The agent reformatted my whole section again!"**
This shouldn't happen anymore because sections are now separate files. But if it does: the AGENTS.md file explicitly tells the agent not to do this. You can literally say "You violated Rule 2 in AGENTS.md — revert your changes to only the specific edit I asked for."

**"I see [AUTHOR-CHECK] or [UNVERIFIED] in the report and I'm not sure what to do"**
It means the claim is not final-source-verified. Three possibilities:
1. The fact is correct and a strong source exists → replace with a proper `[SXXX]` citation
2. The fact is directionally right but the number/source needs adjustment → revise text and cite correctly
3. The claim can't be validated → delete it

---

## The one habit that makes everything work

**When you finish a work session, spend 2 minutes on the Excel.**

Open `source_registry.xlsx` → Claims tab → sort by "verified = N" → check off the ones you've confirmed. That's it. Over time, you'll have a fully verified, fully traceable report, and you'll sleep better knowing every number has a source.

---

## Quick reference card

| I want to... | Do this |
|---|---|
| Edit the report | Open the section file in `sections/` |
| See what the agent changed | Read `CHANGELOG.md` |
| Check if a number is real | Look it up in Excel → Claims tab |
| Find where a figure's data lives | Excel → Figures tab → "excel_tab" column |
| Find a source PDF | Excel → Sources tab → "filename" column |
| Preview in Word | Ask agent to convert, or run script. Check `_output/latest/` |
| Take personal notes | Use `_workspace/` — agent can't see it |
| Tell the agent what to do | Just describe it in plain language in the chat |
| Scold the agent | "You broke Rule [X] in AGENTS.md" (it will listen) |

---

*This guide lives in the project folder. You can always come back to it. And if something isn't clear, just ask the agent — it's read AGENTS.md and knows the whole system. Or ask Renaud.* 💛
