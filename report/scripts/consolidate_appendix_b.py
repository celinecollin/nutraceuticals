import re

INPUT_FILE = "report/source_material/20260125_New_Input_Consolidated.md"
OUTPUT_FILE = "report/source_material/Appendix_B_Exhaustive.md"

def parse_markdown_table(table_str):
    """Parses a markdown table string into a list of dictionaries."""
    try:
        # Remove outer pipes and split
        lines = table_str.strip().split('\n')
        if len(lines) < 3: return []
        
        # Header
        header_line = lines[0].strip()
        headers = [h.strip() for h in header_line.split('|') if h.strip()]
        
        data = []
        for line in lines[2:]: # Skip separator
            if not line.strip(): continue
            # Split by pipe, but be careful of escaped pipes if any (simple split for now)
            cols = [c.strip() for c in line.split('|')]
            # Remove empty first/last if they exist due to leading/trailing pipes
            if len(cols) > len(headers):
                 # simplistic trimming of empty start/end
                 if cols[0] == '': cols.pop(0)
                 if cols[-1] == '': cols.pop(-1)
            
            row = {}
            for i, h in enumerate(headers):
                if i < len(cols):
                    row[h] = cols[i]
                else:
                    row[h] = ""
            data.append(row)
        return data
    except Exception as e:
        print(f"Error parsing table: {e}")
        return []

def extract_tables_from_file(content, filename_pattern):
    """Extracts table blocks belonging to a specific file section."""
    # Find the file section
    file_match = re.search(f"## FILE:.*?{filename_pattern}.*?=+.*?\n(.*?)(?=\n## FILE:|$)", content, re.DOTALL)
    if not file_match:
        print(f"File section not found for: {filename_pattern}")
        return []
    
    section_content = file_match.group(1)
    
    # Find all tables (blocks starting with | ... |)
    lines = section_content.split('\n')
    current_table = []
    current_sheet = "Unknown"
    
    extracted_data = []

    in_table = False
    for line in lines:
        if line.strip().startswith("#### Sheet:"):
            current_sheet = line.strip().replace("#### Sheet:", "").strip()
            continue

        if line.strip().startswith("|") and "---" not in line:
            if not in_table:
                # Potential start of table header
                in_table = True
                current_table = [line]
            else:
                current_table.append(line)
        elif "---" in line and in_table:
            current_table.append(line)
        else:
            if in_table:
                # End of table
                table_data = parse_markdown_table("\n".join(current_table))
                # Add sheet context
                for row in table_data:
                    row['_Sheet'] = current_sheet
                extracted_data.extend(table_data)
                current_table = []
                in_table = False
    
    if in_table: # EOF case
        table_data = parse_markdown_table("\n".join(current_table))
        for row in table_data:
            row['_Sheet'] = current_sheet
        extracted_data.extend(table_data)
        
    return extracted_data

def normalize_companies(data_list, source_name):
    """Normalizes list of dicts to the master schema."""
    normalized = []
    for entry in data_list:
        norm = {
            "Company": "",
            "Category": "",
            "Product": "",
            "Species": "",
            "Summary": "",
            "Investor": "",
            "_Source": source_name
        }
        
        # MAPPING LOGIC
        if source_name == "SelectedList": # 20251217_SelectedList_Nutraceuticals
            norm["Company"] = entry.get("Company", "")
            norm["Product"] = entry.get("Product", "")
            norm["Species"] = entry.get("Target Species", "")
            norm["Summary"] = entry.get("Concern", "") + ". " + entry.get("Nutraceutical Ingredients", "")
            norm["Category"] = "Nutraceuticals"

        elif source_name == "VC_Portfolio": # VC_PE_Portfolio
            norm["Company"] = entry.get("Company Name", "")
            norm["Category"] = entry.get("Classification", "")
            norm["Investor"] = entry.get("Fund", "")
            norm["Summary"] = entry.get("Detailed Summary of Operations", "")
            if not norm["Summary"] and "Link" in entry:
                 norm["Summary"] = f"Portfolio entry. Link: {entry.get('Link', '')}"

        elif source_name == "CompaniesContact": # Companies to contact
            norm["Company"] = entry.get("Company", "")
            norm["Category"] = entry.get("Sector", "")
            norm["Product"] = entry.get("Key Products / Focus", "")
            norm["Summary"] = entry.get("Strategic Positioning", "")
            norm["Investor"] = entry.get("Financing", "")
        
        elif source_name == "ValueChain": # Value_Chain_Companies
            norm["Company"] = entry.get("Company (Commercial)", "") or entry.get("Company", "") or entry.get("Technology Owner", "")
            norm["Product"] = entry.get("Product", "") or entry.get("Commercial Product", "")
            norm["Species"] = entry.get("Target Species", "")
            norm["Summary"] = entry.get("The Strategic Claim", "") or entry.get("Strategic Claim", "")
            norm["Category"] = entry.get("_Sheet", "") # Use sheet name as category
            
        if norm["Company"]:
            normalized.append(norm)
    return normalized

def main():
    with open(INPUT_FILE, "r") as f:
        content = f.read()

    # 1. Extract data
    data_selected = extract_tables_from_file(content, "20251217_SelectedList_Nutraceuticals.xlsx")
    data_vc = extract_tables_from_file(content, "20260115_VC_PE_Portfolio.xlsx")
    data_contact = extract_tables_from_file(content, "Companies to contact.xlsx")
    data_valuechain = extract_tables_from_file(content, "Value_Chain_Companies.xlsx")

    # 2. Normalize
    all_rows = []
    all_rows.extend(normalize_companies(data_selected, "SelectedList"))
    all_rows.extend(normalize_companies(data_vc, "VC_Portfolio"))
    all_rows.extend(normalize_companies(data_contact, "CompaniesContact"))
    all_rows.extend(normalize_companies(data_valuechain, "ValueChain"))

    # 3. Merge/Deduplicate
    merged = {}
    
    for row in all_rows:
        name = row["Company"].strip()
        # Basic cleanup: remove (Vertical), (Licensor) annotations sometimes present
        name_clean = name.split(' (')[0].strip()
        
        if not name_clean: continue
        
        key = name_clean.lower()
        
        if key not in merged:
            merged[key] = {
                "Company": name_clean,
                "Category": set(),
                "Product": set(),
                "Species": set(),
                "Summary": set(),
                "Investor": set()
            }
        
        # Aggregate
        if row["Category"]: merged[key]["Category"].add(row["Category"])
        if row["Product"]: merged[key]["Product"].add(row["Product"])
        if row["Species"]: merged[key]["Species"].add(row["Species"])
        if row["Investor"]: merged[key]["Investor"].add(row["Investor"])
        
        # Summary: Keep the longest ones to avoid noise, or accumulate if distinct
        brief = row["Summary"].strip()
        if brief and len(brief) > 5:
            merged[key]["Summary"].add(brief)

    # 4. Format Output
    final_list = []
    for k, v in merged.items():
        # Pick best category (prefer "Pharma", "Startups" over "Other")
        cats = sorted(list(v["Category"]))
        cat_str = ", ".join(cats)
        
        # Products
        prods = sorted(list(v["Product"]))
        prod_str = ", ".join(prods[:5]) # Limit to 5
        if len(prods) > 5: prod_str += "..."
        
        # Species
        species = sorted(list(v["Species"]))
        spec_str = ", ".join(species)
        
        # Summary - join unique, but limit length
        sums = sorted(list(v["Summary"]), key=len, reverse=True)
        # Prefer the longest detailed summary
        sum_str = sums[0] if sums else ""
        if len(sums) > 1:
             # Look for a different one to add context?
             pass
             
        # Investor
        invs = sorted(list(v["Investor"]))
        inv_str = ", ".join(invs)
        
        # Sanitize for Markdown Table
        def sanitize(s): return str(s).replace("|", "/").replace("\n", " ").strip()
        
        final_list.append([
            sanitize(v["Company"]),
            sanitize(cat_str),
            sanitize(prod_str),
            sanitize(spec_str),
            sanitize(sum_str),
            sanitize(inv_str)
        ])
    
    # Sort by Company
    final_list.sort(key=lambda x: x[0])
    
    # Write Markdown
    header = ["Company", "Category", "Key Product/Focus", "Target Species", "Strategic Summary", "Investor/Source"]
    
    with open(OUTPUT_FILE, "w") as f:
        f.write("# Appendix B: Comprehensive Industry Players List\n\n")
        f.write("This exhaustive list consolidates key market players, startups, and investors identified throughout the research.\n\n")
        
        # Write Table Header
        f.write("| " + " | ".join(header) + " |\n")
        f.write("| " + " | ".join(["---"] * len(header)) + " |\n")
        
        for row in final_list:
            f.write("| " + " | ".join(row) + " |\n")

    print(f"Successfully wrote {len(final_list)} companies to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
