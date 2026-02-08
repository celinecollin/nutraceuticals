
import markdown
import os

INPUT_FILE = "report/master_report/20260118_Master_WhitePaper_Refined.md"
OUTPUT_FILE = "report/master_report/20260118_Master_WhitePaper_Presentation.html"

# CSS Styles matching "Data Centres 2026" quality
# Fonts: Inter (Sans) for modern feel.
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&display=swap');

:root {
    --primary: #003057;
    --secondary: #0089cf;
    --accent: #d04a02;
    --text: #333;
    --bg: #fff;
    --grey: #f4f6f8;
}

body {
    font-family: 'Inter', sans-serif;
    color: var(--text);
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background: var(--bg);
}

/* Page Layout */
.container {
    max-width: 1000px; /* A4 width approx */
    margin: 0 auto;
    padding: 40px;
}

/* Cover Page */
.cover {
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: linear-gradient(135deg, var(--primary) 0%, #001529 100%);
    color: white;
    padding: 60px;
    margin-bottom: 60px;
}

.cover h1 {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 20px;
    border-bottom: 4px solid var(--accent);
    padding-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: -0.02em;
}

.cover p {
    font-size: 1.5rem;
    font-weight: 300;
    opacity: 0.9;
}

.cover .meta {
    margin-top: auto;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    opacity: 0.7;
}

/* Typography */
h1, h2, h3, h4 {
    color: var(--primary);
    margin-top: 2em;
    margin-bottom: 0.5em;
    font-weight: 700;
}

h1 { font-size: 2.2rem; border-bottom: 2px solid var(--grey); padding-bottom: 10px; color: var(--accent); }
h2 { font-size: 1.8rem; margin-top: 2.5em; }
h3 { font-size: 1.4rem; color: var(--secondary); }
h4 { font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; color: #666; }

p {
    margin-bottom: 1.2em;
    font-size: 1rem;
    text-align: justify;
}

/* Multi-column layout for body */
.content-body {
    column-count: 2;
    column-gap: 40px;
}

.content-body h1, 
.content-body h2, 
.content-body .full-width,
.content-body figure {
    column-span: all;
}

/* Components */
blockquote {
    border-left: 4px solid var(--accent);
    margin: 20px 0;
    padding: 20px;
    background: var(--grey);
    font-family: 'Merriweather', serif;
    font-style: italic;
    font-size: 1.1rem;
    color: #444;
}

ul, ol {
    margin-bottom: 1.2em;
    padding-left: 20px;
}

li {
    margin-bottom: 0.5em;
}

/* Images/Figures */
figure {
    margin: 30px 0;
    break-inside: avoid;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

figcaption {
    margin-top: 10px;
    font-size: 0.85rem;
    color: #666;
    font-weight: 600;
    text-align: center;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 0.9rem;
}

th, td {
    padding: 12px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}

th {
    background-color: var(--primary);
    color: white;
    font-weight: 600;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

/* Print Optimizations */
@media print {
    body { background: white; }
    .cover { height: 100vh; margin: 0; -webkit-print-color-adjust: exact; }
    .container { width: 100%; max-width: none; padding: 0; }
    .content-body { column-fill: auto; }
    h2 { break-before: always; page-break-before: always; }
    figure { break-inside: avoid; }
}
</style>
"""

def main():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Pre-process Markdown
    # 1. Separate Title Block for Hero
    lines = md_text.splitlines()
    title = "Animal Nutraceutical Landscape"
    subtitle = "Strategic White Paper (2024-2030)"
    
    # Try to extract title from first line
    if lines[0].startswith("# "):
        title = lines[0].replace("# ", "")
        lines = lines[1:] # Remove title from body
    
    body_md = "\n".join(lines)
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(body_md, extensions=['extra', 'toc', 'tables'])
    
    # Fix image paths (Markdown has "figures/", HTML needs relative or absolute?)
    # Since HTML is in same folder as markdown? No, let's put it in master_report
    # Markdown has "figures/Figure..."
    # If HTML is in master_report, "figures/Figure..." is correct.
    
    # Assembly
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {CSS}
</head>
<body>

    <!-- Cover Page -->
    <div class="cover">
        <div class="meta">January 2026 | Market Intelligence</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
        <div class="meta" style="margin-top: 40px;">CONFIDENTIAL | INTERNAL REVIEW</div>
    </div>

    <!-- Main Content -->
    <div class="container">
        <div class="content-body">
            {html_content}
        </div>
    </div>

</body>
</html>
"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    print(f"HTML Report generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
