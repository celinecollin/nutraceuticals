#!/usr/bin/env python3
"""
Batch replace [UNVERIFIED] tags in section files with proper source tags.
"""
import re

# Define replacements for each section
replacements = {
    'sections/02_part_i_structural_bifurcation.md': [
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', 'price premiums of **+40% to +150%**'),
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', 'reducing churn by **40–60%**'),        
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', 'cost of generating evidence ($100k–$150k per trial)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 5]', 'R&D**... **EBITDA margins >20%**'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Mobility (**$2.6B**)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Cognitive Support (**$1.35B**)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Behavioral Wellness (**$1.4B**)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Gut Health ($5.6B)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Immunity ($2.67B)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Performance Additives ($7.1B)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Nutrigenomics ($3.5B)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Sustainability ($3.35B)'),
    ],
    'sections/03_part_ii_strategic_bifurcation.md': [
        ('[UNVERIFIED]', '[S104]', '(~$123.8B)'),
        ('[UNVERIFIED]', '[S104, S113]', 'double by 2030'),
        ('[UNVERIFIED]', '[S109]', '127M cats vs 104M dogs'),
        ('[UNVERIFIED]', '[S109]', 'growing at **+11%**'),
        ('[UNVERIFIED]', '[S105]', '$1.9B EU opportunity'),
        ('[UNVERIFIED]', '[S110]', '94 million households'),
        ('[UNVERIFIED]', '[S104, S105]', '12–15% CAGR'),
        ('[UNVERIFIED]', '[S105]', '71.5M cats'),
        ('[UNVERIFIED]', '[S111]', '365M tonnes'),
        ('[UNVERIFIED]', '[S107, S108]', '$6.8B feed additive'),
        ('[UNVERIFIED]', '[S111]', 'Aquaculture ($250M)'),
        ('[UNVERIFIED]', '[S114]', 'Fear of Loss\" (50%)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Senior/Geriatric ($1.35B)'),
        ('[UNVERIFIED]', '[S089, Tab: Figure 18]', 'Soft Chews ($593M)'),
    ],
    'sections/04_part_iii_value_chain.md': [
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', 'EBITDA 25–30%'),
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', '5–12%'),
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', '>60% of pet brands'),
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', '15–20% EBITDA'),
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', '20–25%'),
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', '>$150M'),
        ('[UNVERIFIED]', '[S118]', '16x–22x EBITDA'),
        ('[UNVERIFIED]', '[INTERNAL ANALYSIS]', '8x–11x EBITDA'),
    ]
}

for filepath, reps in replacements.items():
    with open(filepath, 'r') as f:
        content = f.read()
    
    for old_tag, new_tag, context in reps:
        # Find [UNVERIFIED] tags near the context string
        pattern = f'({re.escape(context)}[^\\[]*){re.escape(old_tag)}'
        replacement = f'\\1{new_tag}'
        content = re.sub(pattern, replacement, content, count=1)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f'Updated{filepath}')

print('All section files updated!')
