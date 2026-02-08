
import re

def parse_revenue(rev_str):
    """
    Parses revenue string like "$1.2 - $1.4 Billion" or "$170 - $250 Million"
    Returns revenues in Billions (float).
    """
    if not rev_str or rev_str.strip() == "-" or rev_str.strip() == "":
        return 0.0
    
    # Normalize
    s = rev_str.replace("USD", "").replace("$", "").replace(",", "").strip()
    
    # Remove anything in parentheses
    s = re.sub(r'\(.*?\)', '', s)
    
    # Detect unit
    multiplier = 1.0
    if "Billion" in s or "B" in s:
        multiplier = 1.0
        s = s.replace("Billion", "").replace("B", "")
    elif "Million" in s or "M" in s:
        multiplier = 0.001
        s = s.replace("Million", "").replace("M", "")
    elif "Niche" in s:
        # Treat "Niche (<$50M)" as approx 0.025
        return 0.025
    
    # Clean up any remaining non-numeric chars except . and -
    # We want to keep range like "5.6 - 7.5"
    # Wait, we need to be careful not to merge numbers if space exists
    
    try:
        if "-" in s:
            parts = s.split("-")
            low_match = re.search(r"[\d\.]+", parts[0])
            high_match = re.search(r"[\d\.]+", parts[1])
            if low_match and high_match:
                low = float(low_match.group(0))
                high = float(high_match.group(0))
                val = (low + high) / 2.0
            else:
                return 0.0
        else:
            match = re.search(r"[\d\.]+", s)
            if match:
                val = float(match.group(0))
            else:
                return 0.0
    except:
        return 0.0
        
    return val * multiplier

def extract_all_tables(content):
    headers_regex = re.compile(r"\|.*Est.*% Use.*\|")
    row_pattern = re.compile(r"^\|.*\|$")
    
    lines = content.split('\n')
    tables = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if headers_regex.search(line):
            # Capture table
            table_lines = [line]
            i += 1
            if i < len(lines):
                 table_lines.append(lines[i]) # Separator
            i += 1
            while i < len(lines) and row_pattern.match(lines[i]):
                table_lines.append(lines[i])
                i += 1
            tables.append(table_lines)
            continue
        i += 1
    return tables

def calculate_grand_total(tables):
    grand_total = 0.0
    for table in tables:
        rows = table[2:]
        for row in rows:
            cols = [c.strip() for c in row.strip().split('|')]
            if len(cols) < 5: continue
            rev = parse_revenue(cols[-2]) # Revenue is second to last real column (cols has empty start/end)
            # Actually cols structure: ['', 'Name', ..., 'Seg%', 'Gen%', 'Rev', '']
            # So Rev is index -2 (empty string is -1)
            # wait, let's verify index.
            # | Name | ... | Seg% | Gen% | Rev |
            # ['', 'Name', '...', 'Seg%', 'Gen%', 'Rev', '']
            # So Rev is cols[-2]. Correct.
            grand_total += rev
    return grand_total

def detect_sector(species_text):
    s = species_text.lower()
    pets = ['dog', 'cat', 'horse', 'companion']
    livestock = ['swine', 'poultry', 'ruminant', 'livestock', 'broiler', 'piglet', 'cattle', 'sheep', 'aquaculture', 'fish', 'shrimp']
    
    is_pet = any(p in s for p in pets)
    is_liv = any(l in s for l in livestock)
    
    if is_pet and is_liv:
        return "Multi-Species"
    elif is_pet:
        return "Pet / Companion"
    elif is_liv:
        return "Livestock / Aqua"
    else:
        return "Tyical Multi"

def process_content(content):
    # Pass 1: Extract all tables to calculate Raw Grand Total
    # We need to parse every single revenue line item to get the denominator for scaling.
    tables = extract_all_tables(content)
    raw_grand_total = calculate_grand_total(tables)
    print(f"Raw Data Sum: ${raw_grand_total:.2f} Billion")
    
    GLOBAL_TARGET = 13.0
    scaling_factor = 0.0
    if raw_grand_total > 0:
        scaling_factor = GLOBAL_TARGET / raw_grand_total
    
    print(f"Scaling Factor: {scaling_factor:.4f} (Target $13B / Raw ${raw_grand_total:.2f}B)")
    
    # Pass 2: Iterate and Replace
    # We will apply the scaling factor to the Revenue Value itself.
    
    headers_regex = re.compile(r"\|.*Est.*% Use.*\|")
    row_pattern = re.compile(r"^\|.*\|$")
    
    lines = content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if headers_regex.search(line):
            # Capture table block
            table_lines = [line]
            i += 1
            if i < len(lines): table_lines.append(lines[i])
            i += 1
            while i < len(lines) and row_pattern.match(lines[i]):
                table_lines.append(lines[i])
                i += 1
            
            # Recalculate This Table with SCALING
            # We pass the scaling factor to adjust the Absolute Revenue numbers
            new_table_lines = recalculate_table(table_lines, grand_total=GLOBAL_TARGET, scaling_factor=scaling_factor)
            new_lines.extend(new_table_lines)
            continue
            
        new_lines.append(line)
        i += 1
        
    return "\n".join(new_lines)

def recalculate_table(table_lines, grand_total, scaling_factor=1.0):
    header = table_lines[0]
    separator = table_lines[1]
    rows = table_lines[2:]

    # Check if Sector column already exists
    has_sector_col = "Primary Sector" in header

    # Adjust Header to reflect scaling
    # We look for the Revenue column
    if "(Scaled)" not in header:
        header = header.replace("Est. Global Revenue (Veterinary)", "Est. Global Revenue (Scaled)")

    parsed_rows = []
    total_segment_revenue = 0.0
    
    for row in rows:
        cols = [c.strip() for c in row.strip().split('|')]
        real_cols = cols[1:-1]
        
        # Revenue is last real column
        rev_str = real_cols[-1]
        revenue = parse_revenue(rev_str)
        
        # APPLY SCALING
        scaled_revenue = revenue * scaling_factor
        
        # Detect Sector
        species_text = real_cols[1]
        sector = detect_sector(species_text)
        
        total_segment_revenue += scaled_revenue
        parsed_rows.append({
            'raw': row,
            'cols': real_cols,
            'rev': scaled_revenue, # Use scaled revenue for subsequent calcs
            'sector': sector
        })
        
    new_rows = [header, separator]
    
    for r in parsed_rows:
        cols = r['cols']
        revenue = r['rev']
        sector = r['sector']
        
        # Update Revenue String in the column
        # Formatting: if < 0.1B use Millions
        if revenue < 1.0:
             rev_display = f"${revenue*1000:.0f} Million"
        else:
             rev_display = f"${revenue:.2f} Billion"
        
        # Segment %
        if total_segment_revenue > 0:
            seg_pct = (revenue / total_segment_revenue) * 100
            seg_str = f"{seg_pct:.1f}%"
        else:
            seg_str = "-"
            
        # General % -> Uses GRAND TOTAL 13.0
        if grand_total > 0:
            gen_pct = (revenue / grand_total) * 100
            gen_str = f"{gen_pct:.2f}%"
        else:
            gen_str = "-"
        
        # Replace columns
        # Structure: Name | ... | Seg% | Gen% | Rev
        cols[-3] = seg_str
        cols[-2] = gen_str
        
        # Replace Revenue Column with Scaled Value
        cols[-1] = rev_display
        
        # Insert or Update Sector
        if has_sector_col:
            # We assume it's there. 
            pass 
        else:
            cols.insert(2, sector)
        
        new_line = "| " + " | ".join(cols) + " |"
        new_rows.append(new_line)
        
    return new_rows

if __name__ == "__main__":
    with open("/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/20260122_Master_WhitePaper_V2.md", "r") as f:
        content = f.read()
        
    new_content = process_content(content)
    
    with open("/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/20260122_Master_WhitePaper_V2_recalc.md", "w") as f:
        f.write(new_content)
    print("Recalculation complete.")
