
import re
import matplotlib.pyplot as plt
import os
import matplotlib.colors as mcolors

# --- Parsing Logic (Reused) ---

def parse_revenue(rev_str):
    if not rev_str: return 0.0
    s = rev_str.replace("USD", "").replace("$", "").replace(",", "").strip()
    s = re.sub(r'\(.*?\)', '', s)
    multiplier = 1.0
    if "Billion" in s or "B" in s:
        multiplier = 1.0
        s = s.replace("Billion", "").replace("B", "")
    elif "Million" in s or "M" in s:
        multiplier = 0.001
        s = s.replace("Million", "").replace("M", "")
    elif "Niche" in s:
        return 0.025
    
    try:
        if "-" in s:
            parts = s.split("-")
            low_match = re.search(r"[\d\.]+", parts[0])
            high_match = re.search(r"[\d\.]+", parts[1])
            if low_match and high_match:
                return (float(low_match.group(0)) + float(high_match.group(0))) / 2.0 * multiplier
        else:
            match = re.search(r"[\d\.]+", s)
            if match:
                return float(match.group(0)) * multiplier
    except:
        pass
    return 0.0

def parse_data(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Structure: segments[segment_name] = [ {'name': 'Probiotics', 'revenue': 1.2} ]
    segments = {}
    current_segment = "Unknown"
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("### II."):
            match = re.search(r"II\.\d+\.\s+(.*?)(\(|$)", line)
            if match:
                current_segment = match.group(1).strip()
                # Aliases
                if "Performance" in current_segment: current_segment = "Performance & FCR"
                if "Gut Health" in current_segment: current_segment = "Gut Health"
                if "Immunity" in current_segment: current_segment = "Immunity"
                if "Cognitive" in current_segment: current_segment = "Cognition"
                if "Calming" in current_segment: current_segment = "Calming"
                if "Mobility" in current_segment: current_segment = "Mobility"
                if "Delivery" in current_segment: current_segment = "Delivery Systems"
                if "Ectoparasite" in current_segment: current_segment = "Ectoparasite"
                if "Nutrigenomics" in current_segment: current_segment = "Nutrigenomics"
                if "Sustainability" in current_segment: current_segment = "Sustainability"
                if "Niches" in current_segment: current_segment = "Special Niches"

        if any(x in line for x in ["| **Nutraceutical family**", "| **Additive family**", 
                                   "| **Delivery Technology**", "| **Strategy**", 
                                   "| **Concept**", "| **Niche**", 
                                   "| **Component**", "| **Technology**"]):
            if current_segment not in segments:
                segments[current_segment] = []
            
            i += 2 
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                cols = [c.strip() for c in row.split('|')][1:-1]
                
                if len(cols) >= 4:
                    name = cols[0].strip().replace("**", "")
                    # Clean up name: prevent "Probiotics (strain specific)" from being too long
                    name = re.sub(r'\(.*?\)', '', name).strip()
                    
                    rev = parse_revenue(cols[-1])
                    
                    if rev > 0:
                        segments[current_segment].append({'name': name, 'revenue': rev})
                i += 1
            continue
        i += 1
    return segments

def generate_breakdown_chart():
    input_file = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/20260122_Master_WhitePaper_V2.md"
    output_dir = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/figures"
    
    segments_data = parse_data(input_file)
    
    # Filter segments with data
    segments_data = {k: v for k, v in segments_data.items() if sum(d['revenue'] for d in v) > 0}
    
    # Sort segments by total revenue for consistency with previous chart
    sorted_segs_keys = sorted(segments_data.keys(), key=lambda k: sum(d['revenue'] for d in segments_data[k]), reverse=False)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Generate distinct colors
    cmap = plt.get_cmap("tab20c") # Using tab20c for a bit more "professional" look
    colors = [cmap(i) for i in range(20)] * 3
    
    bar_width = 0.85
    y_pos = range(len(sorted_segs_keys))
    
    for i, seg in enumerate(sorted_segs_keys):
        items = segments_data[seg]
        total = sum(item['revenue'] for item in items)
        
        # Sort items within bar by revenue descending
        items.sort(key=lambda x: x['revenue'], reverse=True)
        
        left = 0
        small_items = []
        
        for j, item in enumerate(items):
            pct = (item['revenue'] / total)
            width = pct
            
            color = colors[j % len(colors)]
            
            rect = ax.barh(i, width, left=left, height=bar_width, color=color, edgecolor='white', linewidth=0.7)
            
            # --- Labeling Logic ---
            mid = left + (width / 2)
            
            # Clean name (basic)
            clean_name = item['name']
            clean_name = re.sub(r'^.*:\s+', '', clean_name) # Strip "Category:" prefix
            clean_name = re.sub(r'\(.*?\)', '', clean_name).strip() # Strip parens content e.g. " (Feed + Pet)"
            
            # Capitalize
            if len(clean_name) > 0:
                clean_name = clean_name[0].upper() + clean_name[1:]

            # Aggressive Shortening Dictionary
            aliases = {
                "Probiotics": "Probiotics",
                "Digestive enzymes": "Enzymes",
                "Synbiotics": "Synbiotics",
                "Organic acids": "Organic Acids",
                "Clay binders and toxin adsorbents": "Clay Binders",
                "Clay binders": "Clay Binders",
                "Postbiotics and butyrate donors": "Postbiotics",
                "Prebiotics": "Prebiotics",
                "Herbal gut soothers": "Herbal Soothers",
                
                "Rumen Protection Matrices": "Rumen Protect",
                "Smart Monitoring Boluses": "Smart Boluses",
                "Soft Chews": "Soft Chews",
                "Aquafeed Coatings": "Aqua Coatings",
                "Powders & Top Dress": "Powders",
                "Nanocarriers & Microencapsulation": "Nanocarriers",
                "Biofilm-Carrier Probiotics": "Biofilm Probiotics",
                "3D-Printed \"Printlets\"": "3D Printlets",
                "Liposomal Transdermal Gels": "Liposomal Gels",
                
                "Seaweed and polysaccharides": "Seaweed/Poly",
                "Plasma / colostrum & Ig-rich fractions": "Plasma & Ig",
                "Nucleotides": "Nucleotides",
                "Lactoferrin and functional peptides": "Lactoferrin",
                "Selenium & vitamin E": "Se & Vit E",
                "Vitamin C": "Vit C",
                "Beta 1,3 1,6 glucans": "Beta Glucans",
                "Vaccine synergy positioning": "Vaccine Synergy",
                
                "Yeast culture": "Yeast Culture",
                "Amino acid blends & rumen protected amino acids": "AA Blends",
                "Xylanase & carbohydrases": "Xylanase",
                "Phytogenics": "Phytogenics",
                "Electrolytes": "Electrolytes",
                "Phytase": "Phytase",
                "Protease": "Protease",
                "Carnitine, CLA, creatine, beta alanine": "Carnitine/CLA",
                
                "Omega 3": "Omega 3",
                "Omega 3 (EPA/DHA)": "Omega 3",
                "Glucosamine & chondroitin": "Gluco/Chondro",
                "MSM": "MSM",
                "Undenatured type II collagen": "UC-II Collagen",
                "Green lipped mussel": "GLM",
                "Boswellia & curcumin": "Boswellia",
                "Eggshell membrane complexes": "Eggshell Memb",
                "Hyaluronic acid": "Hyaluronic Acid",
                
                "Nitrogen efficiency": "Nitrogen Eff.",
                "Phosphorus excretion management": "Phos. Mgmt",
                "Omega 3 supply chain resilience": "Omega 3 Supply",
                "Natural methane reducers": "Nat. Methane",
                "Methane mitigation": "Methane Mit.",
                
                "Gut integrity as antibiotic alternative infrastructure": "Gut Integrity",
                "Biomarker substantiation": "Biomarkers",
                "Nrf2 & polyphenol pathways": "Nrf2/Polyphenols",
                "Vaccine interaction": "Vaccine Inter.",
                
                "Pigmentation: astaxanthin": "Astaxanthin",
                "Astaxanthin": "Astaxanthin",
                "Dermatology: zinc methionine": "Zn Methionine",
                "Zinc methionine": "Zn Methionine",
                "Dermatology: omega 6, linoleic acid": "Omega 6",
                "Omega 6, linoleic acid": "Omega 6",
                "Dermatology: biotin": "Biotin",
                "Biotin": "Biotin",
                "Urinary tract: cranberry": "Cranberry",
                "Cranberry": "Cranberry",
                
                "MCTs": "MCTs",
                "DHA": "DHA",
                "Antioxidant enriched diets & blends": "Antioxidants",
                "SAMe": "SAMe",
                "B complex vitamins": "Vit B Complex",
                "Phosphatidylserine": "Phosphatidyl.",
                "Ginkgo biloba": "Ginkgo",
                
                "Multi ingredient calming complexes": "Calming Cmplx",
                "Calming complexes": "Calming Cmplx",
                "CBD & hemp derivatives": "CBD & Hemp",
                "Botanicals": "Botanicals",
                "Tryptophan": "Tryptophan",
                "L theanine": "L-Theanine",
                "Alpha casozepine": "Alpha Casozep.",
                "Magnesium & B vitamins": "Mg & Vit B",
                
                "Natural repellents": "Nat. Repellents",
                "Skin barrier support stacks": "Skin Barrier",
                "Skin barrier stacks": "Skin Barrier",
                "Garlic based approaches": "Garlic"
            }
            
            # Apply Dictionary Mapping
            # Check full match first
            if clean_name in aliases:
                clean_name = aliases[clean_name]
            else:
                # Partial match checks if not found
                for k, v in aliases.items():
                    if k in clean_name and len(k) > 5: # avoid short matches
                        clean_name = v
                        break
            
            # Thresholds and Styles - UPDATED FOR READABILITY
            # If > 12%: Show Name + % inside (was 8%)
            # If > 6%: Show % only (was 4%)
            
            if pct >= 0.12: 
                import textwrap
                display_text = f"{clean_name}\n{pct*100:.0f}%"
                # Wrap tighter to fit
                wrapped_text = textwrap.fill(display_text, width=12)
                
                # Dynamic font size
                fontsize = 12 if pct > 0.18 else 10
                
                ax.text(mid, i, wrapped_text, ha='center', va='center', 
                        color='white', fontsize=fontsize, fontweight='bold')
            elif pct >= 0.06:
                # Mid-sized item: just %
                ax.text(mid, i, f"{pct*100:.0f}%", ha='center', va='center', 
                   color='white', fontsize=10, fontweight='bold', alpha=0.95)
            else:
                 small_items.append(f"{clean_name} ({pct*100:.0f}%)")

            left += width
            
        # --- Draw Side List ---
        if small_items:
            # Join with commas
            # limit length if too many?
            side_text_str = ", ".join(small_items)
            import textwrap
            # Wrap standard width ~40 chars for side column
            wrapped_side = textwrap.fill(side_text_str, width=40)
            
            ax.text(1.02, i, wrapped_side, ha='left', va='center', 
                    color='#444444', fontsize=11, fontweight='normal')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_segs_keys, fontsize=11, fontweight='bold')
    ax.set_xlabel('Share of Segment Revenue (%)', fontsize=12)
    ax.set_title('Internal Composition: Key Ingredients Breakdown', fontsize=16, pad=20)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout to make room for side text
    # Standard 1.0 is max x, we are drawing at 1.02.
    # We need to extend the plot area.
    plt.subplots_adjust(right=0.7) # Leave 30% space on right
    
    # X axis formatted as percent
    vals = ax.get_xticks()
    # Limit x ticks to 0-1
    ax.set_xlim(0, 1)
    ax.set_xticklabels(['{:,.0%}'.format(x) for x in vals])
    
    # Manually adjust figure size if needed? figsize=(14,10) is already big.
    # subplots_adjust is key.
    
    output_path = os.path.join(output_dir, "Summary_Chart_Breakdown.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight') # bbox_inches tight helps with side text
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    generate_breakdown_chart()
