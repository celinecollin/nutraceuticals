# Animal Nutraceuticals Master White Paper Project

## Overview
This project consolidates extensive research into a comprehensive "Master White Paper" covering the **Animal Nutraceuticals** market. The report integrates analysis on regulatory landscapes, market demographics (Care Economy vs. Efficiency Economy), competitive landscapes, and investment trends.

## Key Goals
1.  **Consolidate Research**: Merge scattered documents into a single, cohesive narrative.
2.  **Standardize Formatting**: Ensure consistent numbering (Parts I–V) and professional styling.
3.  **Data Visualization**: Identify and create missing figures to support the text.

## Directory Structure
*   `report/`: Main project folder.
    *   `master_report/`: Contains the final consolidated DOCX and modular Markdown parts.
    *   `sources/`: Original research files and raw conversions.
    *   `scripts/`: Python tools for automation (`generate_docx.py`, etc.).
    *   `figures/`: Images and diagrams.

## Quick Start
To generate the latest version of the Master White Paper:

1.  Ensure you have **Python 3** and **Pandoc** installed.
2.  Run the generation script:
    ```bash
    python3 report/scripts/generate_docx.py
    ```
3.  Find the output in `report/master_report/20260118_Master_WhitePaper.docx`.

## for Developers & Agents
See [AGENTS.md](AGENTS.md) for detailed instructions on the scripting architecture, file dependencies, and contribution workflows.
