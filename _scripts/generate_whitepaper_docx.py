#!/usr/bin/env python3
"""
Generate complete white paper DOCX from modular sections using Pandoc + python-docx.
Works with restructured project (sections/*.md → final DOCX).
"""

import os
import subprocess
from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# === CONFIGURATION ===
BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
SECTIONS_DIR = os.path.join(BASE_DIR, "sections")
OUTPUT_DIR = os.path.join(BASE_DIR, "_output")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")  # Symlink to _figures/exports
TIMESTAMP = datetime.now().strftime("%Y%m%d-%H-%M")
OUTPUT_DOCX = os.path.join(OUTPUT_DIR, f"Nutraceuticals_Whitepaper_{TIMESTAMP}.docx")
TEMP_MD = os.path.join(OUTPUT_DIR, "temp_combined.md")

# Section order (from report_master.md)
SECTION_FILES = [
    "00_front_matter.md",
    "01_executive_summary.md",
    "02_part_i_structural_bifurcation.md",
    "03_part_ii_strategic_bifurcation.md",
    "04_part_iii_value_chain.md",
    "05_appendices.md"
]

# Color scheme for styling
COLORS = {
    'primary': RGBColor(0, 48, 87),      # Navy
    'secondary': RGBColor(0, 137, 207),   # Blue
    'accent': RGBColor(208, 74, 2),       # Orange
    'text': RGBColor(51, 51, 51),         # Dark grey
    'grey': RGBColor(139, 155, 165),      # Grey
}

def combine_sections():
    """Combine all section files into single markdown."""
    print(f"Combining {len(SECTION_FILES)} sections...")
    
    combined_content = []
    
    for section_file in SECTION_FILES:
        section_path = os.path.join(SECTIONS_DIR, section_file)
        if not os.path.exists(section_path):
            print(f"  ⚠ Skipping missing section: {section_file}")
            continue
        
        with open(section_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add page break between main sections (not front matter)
        if section_file != "00_front_matter.md":
            combined_content.append("\n\\newpage\n\n")
        
        combined_content.append(content)
        combined_content.append("\n\n")
        print(f"  ✓ {section_file}")
    
    # Write combined markdown
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(TEMP_MD, 'w', encoding='utf-8') as f:
        f.write(''.join(combined_content))
    
    print(f"  ✓ Combined markdown: {TEMP_MD}")
    return TEMP_MD

def convert_with_pandoc(input_md, output_docx):
    """Convert markdown to DOCX using Pandoc."""
    print("Running Pandoc conversion...")
    
    cmd = [
        'pandoc',
        input_md,
        '-o', output_docx,
        '--from', 'markdown+smart+pipe_tables+strikeout',
        '--to', 'docx',
        '--toc',
        '--toc-depth=3',
        '--standalone',
        '--resource-path', f"{SECTIONS_DIR}:{BASE_DIR}",
        '-V', 'mainfont=Georgia',
        '-V', 'sansfont=Arial',
        '--reference-doc=' + os.path.join(BASE_DIR, '_scripts/reference.docx') if os.path.exists(os.path.join(BASE_DIR, '_scripts/reference.docx')) else ''
    ]
    
    # Remove empty reference-doc arg if file doesn't exist
    cmd = [arg for arg in cmd if arg]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"  ✗ Pandoc error: {result.stderr}")
        return False
    
    print(f"  ✓ Pandoc conversion complete")
    return True

def set_cell_shading(cell, color_hex):
    """Set cell background color."""
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color_hex)
    cell._tc.get_or_add_tcPr().append(shading)

def apply_styling(docx_path):
    """Apply professional styling to the document."""
    print("Applying professional styling...")
    
    doc = Document(docx_path)
    
    h1_count = 0
    
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ''
        
        # Heading 1 (Part titles)
        if style_name == 'Heading 1':
            h1_count += 1
            for run in para.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(24)
                run.font.bold = True
                run.font.color.rgb = COLORS['accent']
            para.paragraph_format.space_before = Pt(24)
            para.paragraph_format.space_after = Pt(12)
            if h1_count > 1:
                para.paragraph_format.page_break_before = True
        
        # Heading 2 (Major sections)
        elif style_name == 'Heading 2':
            for run in para.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(18)
                run.font.bold = True
                run.font.color.rgb = COLORS['primary']
            para.paragraph_format.space_before = Pt(18)
            para.paragraph_format.space_after = Pt(6)
        
        # Heading 3
        elif style_name == 'Heading 3':
            for run in para.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(14)
                run.font.bold = True
                run.font.color.rgb = COLORS['secondary']
            para.paragraph_format.space_before = Pt(12)
            para.paragraph_format.space_after = Pt(6)
        
        # Body text
        elif style_name in ['Normal', 'Body Text', 'First Paragraph']:
            for run in para.runs:
                run.font.name = 'Georgia'
                run.font.size = Pt(11)
                run.font.color.rgb = COLORS['text']
            para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            para.paragraph_format.space_after = Pt(8)
        
        # Figure captions
        if para.text.strip().startswith('Figure') and len(para.text) < 200:
            for run in para.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(9)
                run.font.italic = True
                run.font.color.rgb = COLORS['grey']
            para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.space_before = Pt(6)
            para.paragraph_format.space_after = Pt(12)
    
    # Style tables
    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header row
        if len(table.rows) > 0:
            for cell in table.rows[0].cells:
                set_cell_shading(cell, '003057')
                for para in cell.paragraphs:
                    for run in para.runs:
                        run.font.name = 'Arial'
                        run.font.size = Pt(10)
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
        
        # Data rows (alternating)
        for row_idx, row in enumerate(table.rows[1:], start=1):
            for cell in row.cells:
                if row_idx % 2 == 1:
                    set_cell_shading(cell, 'f4f6f8')
                for para in cell.paragraphs:
                    for run in para.runs:
                        run.font.name = 'Arial'
                        run.font.size = Pt(9)
    
    print(f"  ✓ Styled {h1_count} main sections, {len(doc.tables)} tables")
    doc.save(docx_path)
    return True

def add_cover_page(docx_path):
    """Add professional cover page."""
    print("Adding cover page...")
    
    doc = Document(docx_path)
    
    if doc.paragraphs:
        first_para = doc.paragraphs[0]
        
        # Date/Classification
        new_para = first_para.insert_paragraph_before()
        run = new_para.add_run("FEBRUARY 2026 | STRATEGIC INTELLIGENCE")
        run.font.name = 'Arial'
        run.font.size = Pt(10)
        run.font.color.rgb = COLORS['grey']
        run.font.bold = True
        new_para.paragraph_format.space_after = Pt(36)
        
        # Title
        title_para = first_para.insert_paragraph_before()
        run = title_para.add_run("ANIMAL NUTRACEUTICALS")
        run.font.name = 'Arial'
        run.font.size = Pt(42)
        run.font.bold = True
        run.font.color.rgb = COLORS['primary']
        
        # Subtitle
        sub_para = first_para.insert_paragraph_before()
        run = sub_para.add_run("Market Bifurcation and Value Creation")
        run.font.name = 'Arial'
        run.font.size = Pt(24)
        run.font.color.rgb = COLORS['secondary']
        sub_para.paragraph_format.space_after = Pt(24)
        
        # Tagline
        tag_para = first_para.insert_paragraph_before()
        run = tag_para.add_run("A $13B global market split between\\nPet humanization and livestock efficiency")
        run.font.name = 'Georgia'
        run.font.size = Pt(14)
        run.font.italic = True
        tag_para.paragraph_format.space_after = Pt(60)
    
    doc.save(docx_path)
    print("  ✓ Cover page added")

def main():
    print("=" * 60)
    print("NUTRACEUTICALS WHITE PAPER - DOCX GENERATOR")
    print("=" * 60)
    
    # Step 1: Combine sections
    combined_md = combine_sections()
    
    # Step 2: Convert with Pandoc
    if not convert_with_pandoc(combined_md, OUTPUT_DOCX):
        print("ERROR: Pandoc conversion failed")
        return
    
    # Step 3: Apply styling
    apply_styling(OUTPUT_DOCX)
    
    # Step 4: Add cover page
    add_cover_page(OUTPUT_DOCX)
    
    print("=" * 60)
    print(f"✓ COMPLETE: {OUTPUT_DOCX}")
    print("=" * 60)

if __name__ == "__main__":
    main()
