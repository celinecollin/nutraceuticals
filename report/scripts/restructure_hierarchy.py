
import re

input_file = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/Master_WhitePaper_Final.md"
output_file = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/Master_WhitePaper_Final_Restructured.md"

def flatten_content(text):
    """
    Converts H2, H3, H4, H5 to Bold Paragraphs.
    e.g. "## Header" -> "**Header.**"
    """
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        # Check for headers #, ##, ### etc.
        # Note: We assume H1s have been handled/stripped before calling this, or we handle them here?
        # Actually, the chunks we pass here will be the *content* of the old sections.
        # The old H1s are already removed or handled by the main loop.
        
        # We need to flatten ##, ###, ####
        match = re.match(r'^(#{2,6})\s+(.+)$', line)
        if match:
            # It's a header
            title = match.group(2).strip()
            # Convert to "**Title.**"
            # Add an empty line before if needed
            new_lines.append(f"\n**{title}.**") 
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

with open(input_file, 'r') as f:
    content = f.read()

# 1. Split by H1 headers
# We use a regex that looks for ^# Title
# We capture the Title and the Content
parts = re.split(r'(^# .+)', content, flags=re.MULTILINE)

# parts[0] is intro/preamble (Executive Summary usually)
# parts[1] is Header 1, parts[2] is Content 1, parts[3] is Header 2...

# Let's map existing headers to our new structure
# Existing Headers found in previous step:
# 1. Executive Summary (Keep as Preamble?) Or Part 1.1? User said "3 main parts". Exec Summary is usually outside.
# Let's keep Exec Summary separate at the top.

# The sections are:
# 1. Market Fundamentals... ("# 1.")
# 2. Economic Physics... ("# 2.")
# 3. Market Structure... ("# 3.")
# 4. Companion Animals... ("# 4.")
# 5. Strategic Value... ("# 5.")
# 6. Competitive Landscape... ("# 6.") -> Note: This might be empty or short?
# 7. Mapping the Competitive... ("# 7.")
# 8. Market Structure Summary... ("# 8.")
# 9. Strategic Frontiers... ("# 9.")
# 10. Investment Roadmap... ("# 10.")

sections = {}
current_header = "Preamble"
sections[current_header] = ""

for part in parts:
    if part.strip().startswith('# '):
        current_header = part.strip()
        sections[current_header] = ""
    else:
        sections[current_header] += part

# Helper to get content of a section by partial name
def get_content(key_sub):
    found_key = None
    for k in sections.keys():
        if key_sub in k:
            found_key = k
            break
    if found_key:
        return flatten_content(sections[found_key])
    return ""

def get_header(key_sub):
    for k in sections.keys():
        if key_sub in k:
            return k.replace('# ', '').strip()
    return "Section"

# Now Assemble the New Structure

new_doc = []

# Title & Preamble
# Assuming Preamble contains "Master White Paper..." title and "Executive Summary"
# We process Preamble to flatten any subheaders in Exec Summary
new_doc.append(flatten_content(sections.get("Preamble", "") + sections.get("# Executive Summary", ""))) 
# Wait, "Preamble" usually has the # Title.
# Let's verify what keys we have. 
# "Preamble" (metadata, etc), "# ANIMAL NUTRACEUTICALS", "# Executive Summary"
# I will grab everything before "# 1."

intro_text = ""
for k, v in sections.items():
    if "1." in k: break
    # Don't flatten the Main Title if it's there
    if "ANIMAL NUTRACEUTICALS" in k:
        intro_text += k + "\n" + v
    elif "Executive Summary" in k:
        # Keep Exec Summary as H1 or just Bold? User said "3 main parts".
        # Typically Exec Summary is distinct. I'll keep it as H1 "Executive Summary" above the 3 parts.
        intro_text += "# Executive Summary\n" + flatten_content(v)
    else:
        # Other intro stuff
        intro_text += v

new_doc.append(intro_text)

# PART 1
new_doc.append("\n# PART I: THE STRUCTURAL & ECONOMIC FOUNDATION\n")

# 1.1
new_doc.append("\n## I.1. Market Fundamentals & Regulatory Definitions\n")
new_doc.append(get_content("# 1."))

# 1.2
new_doc.append("\n## I.2. The Economic Physics of Evidence\n")
new_doc.append(get_content("# 2."))

# 1.3
new_doc.append("\n## I.3. Global Demographics & Segment Dynamics\n")
# Combine 3 and 4
new_doc.append(get_content("# 3.") + "\n" + get_content("# 4."))


# PART 2
new_doc.append("\n# PART II: COMPETITIVE ARCHITECTURE & VALUE CREATION\n")

# 2.1
new_doc.append("\n## II.1. Strategic Value & Business Models\n")
new_doc.append(get_content("# 5."))

# 2.2
new_doc.append("\n## II.2. The Competitive Landscape\n")
# Combine 6 and 7
new_doc.append(get_content("# 6.") + "\n" + get_content("# 7."))

# 2.3
new_doc.append("\n## II.3. Valuation Benchmarks & Deal Mechanics\n")
new_doc.append(get_content("# 8."))


# PART 3
new_doc.append("\n# PART III: STRATEGIC FRONTIERS & OUTLOOK (2026-2030)\n")

# Split # 9 into two subparts? 
# Content of 9: "Strategic Frontiers" -> "Regulatory & Green", "Nutrigenomics", "Livestock Strategic Pivot"
# Let's split at "The Livestock Strategic Pivot"
content_9 = get_content("# 9.")
split_marker = "**The Livestock Strategic Pivot: The \"Great Divergence\" (2026-2030).**" # It will be bold now
if split_marker not in content_9:
    # Try finding the original string if regex failed or formatting diff
    # The flatten_content adds "**Title.**". 
    # Original H2 was "## The Livestock Strategic Pivot: The "Great Divergence" (2026-2030)"
    split_marker = "**The Livestock Strategic Pivot: The \"Great Divergence\" (2026-2030).**"

parts_9 = content_9.split(split_marker)
if len(parts_9) > 1:
    part_3_1_content = parts_9[0]
    part_3_2_content = split_marker + parts_9[1]
else:
    # Fallback if split fails
    part_3_1_content = content_9
    part_3_2_content = ""

# 3.1
new_doc.append("\n## III.1. The New Frontiers: Green, Tech & Longevity\n")
new_doc.append(part_3_1_content)

# 3.2
new_doc.append("\n## III.2. The Global Pivot: Asia & The Post-AGP Era\n")
new_doc.append(part_3_2_content)

# 3.3
new_doc.append("\n## III.3. The Investment Roadmap\n")
new_doc.append(get_content("# 10."))

# Appendices
new_doc.append("\n# Appendices\n")
new_doc.append(get_content("Appendix: Author"))
new_doc.append(get_content("Appendix B"))
new_doc.append(get_content("References"))

final_text = "".join(new_doc)

# Save
with open(output_file, 'w') as f:
    f.write(final_text)

print("Document restructured successfully.")
