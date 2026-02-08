
import re
import matplotlib.pyplot as plt
import os

# --- Parsing Logic ---

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

def detect_sector(species_text):
    s = species_text.lower()
    pets = ['dog', 'cat', 'horse', 'companion']
    livestock = ['swine', 'poultry', 'ruminant', 'livestock', 'broiler', 'piglet', 'cattle', 'sheep', 'aquaculture', 'fish', 'shrimp']
    is_pet = any(p in s for p in pets)
    is_liv = any(l in s for l in livestock)
    if is_pet and is_liv: return "Multi-Species"
    elif is_pet: return "Pet / Companion"
    elif is_liv: return "Livestock / Aqua"
    else: return "Multi-Species"

def parse_data(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Structure: segments[segment_name] = { 'Pet / Companion': 0.0, 'Livestock / Aqua': 0.0, 'Multi-Species': 0.0 }
    segments = {}
    current_segment = "Unknown"
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect Segment Title
        if line.startswith("### II."):
            match = re.search(r"II\.\d+\.\s+(.*?)(\(|$)", line)
            if match:
                current_segment = match.group(1).strip()
                # Aliases for chart readability
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

        # Detect Table Header
        if any(x in line for x in ["| **Nutraceutical family**", "| **Additive family**", 
                                   "| **Delivery Technology**", "| **Strategy**", 
                                   "| **Concept**", "| **Niche**", 
                                   "| **Component**", "| **Technology**"]):
            if current_segment not in segments:
                segments[current_segment] = {'Pet / Companion': 0.0, 'Livestock / Aqua': 0.0, 'Multi-Species': 0.0}
            
            i += 2 # Skip header and separator
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                cols = [c.strip() for c in row.split('|')][1:-1]
                
                if len(cols) >= 4: # Min cols needed
                    # Last col is revenue
                    rev = parse_revenue(cols[-1])
                    
                    # Sector is mostly passed in column 2 (index 2) by previous tool
                    # But verifying logic: 
                    # Col 0: Name, Col 1: Species, Col 2: Sector
                    
                    sector = "Multi-Species"
                    # Try to match known sector strings in any column (safeguard)
                    found_sector = False
                    for c in cols:
                        if c in ['Pet / Companion', 'Livestock / Aqua', 'Multi-Species']:
                            sector = c
                            found_sector = True
                            break
                    
                    if not found_sector:
                        sector = detect_sector(cols[1]) # Fallback to species column
                    
                    # Aggregate
                    if sector in segments[current_segment]:
                        segments[current_segment][sector] += rev
                    else:
                        segments[current_segment]['Multi-Species'] += rev # Default bin
                i += 1
            continue
        i += 1
    return segments

def generate_chart():
    input_file = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/20260122_Master_WhitePaper_V2.md"
    output_dir = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/figures"
    
    segments_data = parse_data(input_file)
    
    # Sort segments by total revenue
    sorted_segs = sorted(segments_data.items(), key=lambda x: sum(x[1].values()))
    
    labels = [k for k,v in sorted_segs]
    pet_vals = [v.get('Pet / Companion', 0.0) for k,v in sorted_segs]
    liv_vals = [v.get('Livestock / Aqua', 0.0) for k,v in sorted_segs]
    mul_vals = [v.get('Multi-Species', 0.0) for k,v in sorted_segs]
    
    # Plotting standard stacked bar
    fig, ax = plt.subplots(figsize=(14, 9)) # Larger figure size
    
    # Colors
    c_pet = "#4E79A7" # Blue
    c_liv = "#F28E2B" # Orange
    c_mul = "#59A14F" # Green
    
    bar_height = 0.7
    
    # First layer: Livestock
    bars1 = ax.barh(labels, liv_vals, height=bar_height, label='Livestock / Aqua', color=c_liv)
    
    # Second layer: Multi (bottom = Livestock)
    bars2 = ax.barh(labels, mul_vals, height=bar_height, left=liv_vals, label='Multi-Species', color=c_mul)
    
    # Third layer: Pet (bottom = Livestock + Multi)
    left_pet = [l + m for l, m in zip(liv_vals, mul_vals)]
    bars3 = ax.barh(labels, pet_vals, height=bar_height, left=left_pet, label='Pet / Companion', color=c_pet)
    
    # Increase general text size
    plt.rcParams.update({'font.size': 14})
    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=12)
    
    ax.set_xlabel('Revenue (USD Billion)', fontsize=14, fontweight='bold')
    ax.set_title('Global Revenue by Functional Segment & Sector', fontsize=18, fontweight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=12)
    
    # Add numerical labels INSIDE the bars (the "box") if they fit
    totals = []
    for i, (l_v, m_v, p_v) in enumerate(zip(liv_vals, mul_vals, pet_vals)):
        total = l_v + m_v + p_v
        totals.append(total)
        
        # Determine center points for labels
        # Livestock label
        if l_v >= 0.2:
            fsize = 11 if l_v > 0.4 else 9
            ax.text(l_v/2, i, f"${l_v:.1f}B", ha='center', va='center', color='white', fontweight='bold', fontsize=fsize)
            
        # Multi label
        if m_v >= 0.2:
            fsize = 11 if m_v > 0.4 else 9
            ax.text(l_v + m_v/2, i, f"${m_v:.1f}B", ha='center', va='center', color='white', fontweight='bold', fontsize=fsize)
            
        # Pet label
        if p_v >= 0.2:
            fsize = 11 if p_v > 0.4 else 9
            ax.text(l_v + m_v + p_v/2, i, f"${p_v:.1f}B", ha='center', va='center', color='white', fontweight='bold', fontsize=fsize)

        # TOTAL label at the end (outside) for Clarity
        ax.text(total + 0.05, i, f"${total:.1f}B", va='center', fontweight='bold', fontsize=14, color='black')
        
    plt.tight_layout()
    output_path = os.path.join(output_dir, "Summary_Chart_Revenue.png")
    plt.savefig(output_path, dpi=300)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    generate_chart()
