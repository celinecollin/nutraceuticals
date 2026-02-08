
import re
import os

# Define file paths
BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
REPORT_DIR = os.path.join(BASE_DIR, "report", "sources")
OUTPUT_FILE = os.path.join(BASE_DIR, "report", "master_report", "20260118_Master_WhitePaper_Full.md")

# Source files
FILE_PART_1_2 = os.path.join(REPORT_DIR, "2026015_WhitePaper.md")
FILE_PART_3 = os.path.join(REPORT_DIR, "20260118_PartIII.md")
FILE_PART_4 = os.path.join(REPORT_DIR, "20260113_PartV.md")
FILE_PART_5 = os.path.join(REPORT_DIR, "VI. Notable Transactions and Investment Landscape (2015 to 2025) 20260113.md")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def consolidate():
    print("Starting consolidation...")
    
    # 1. Process Part I and II from WhitePaper.md
    print(f"Reading Parts I & II from {FILE_PART_1_2}...")
    content_root = read_file(FILE_PART_1_2)
    
    # Find the split point (Start of Section III)
    # Using regex to find the header "III. Species Priorities" or similar
    # Based on view_file, line 564 is "III. Species Priorities..."
    match = re.search(r'(^#+\s*III\.|^III\.)', content_root, re.MULTILINE)
    
    references_text = ""
    
    if match:
        part_1_2_text = content_root[:match.start()]
        print(f"Part I & II extracted. (Length: {len(part_1_2_text)} chars)")
        
        # Extract References if they exist at the end
        ref_match = re.search(r'(^#+\s*References|^References)', content_root, re.MULTILINE)
        if ref_match:
             references_text = content_root[ref_match.start():]
             print(f"References extracted from original file. (Length: {len(references_text)} chars)")
    else:
        print("WARNING: Could not find Section III start in WhitePaper.md. Using full file?")
        # Fallback: manually look for the transition paragraph or line number 
        # But this is risky. Let's try to be safer. 
        # Ideally we should fail if we can't split.
        lines = content_root.splitlines()
        # Look for "III."
        cut_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("III.") or line.strip().startswith("# III."):
                cut_index = i
                break
        if cut_index != -1:
             part_1_2_text = "\n".join(lines[:cut_index])
        else:
             part_1_2_text = content_root # Fallback
             
    # 2. Process New Part III
    print(f"Reading Part III from {FILE_PART_3}...")
    part_3_text = read_file(FILE_PART_3)
    # Ensure it starts with the right header or adds one?
    # It likely has headers. We assume they are correct ("III. ...")
    
    # 3. Process New Part IV (from Part V file)
    print(f"Reading Part IV from {FILE_PART_4}...")
    part_4_raw = read_file(FILE_PART_4)
    # Renumbering: Replace "V." with "IV." in headers
    # We want to replace headers like "# V." or "V." or "## V.1"
    # Strict regex: Start of line, optional #'s, whitespace, V., whitespace
    def replace_v_with_iv(match):
        prefix = match.group(1)
        suffix = match.group(2)
        return f"{prefix}IV{suffix}"
        
    part_4_text = re.sub(r'^(#*\s*)V(\.| )', replace_v_with_iv, part_4_raw, flags=re.MULTILINE)
    print(f"Part IV processed. (Length: {len(part_4_text)} chars)")

    # 4. Process New Part V (from VI file)
    print(f"Reading Part V from {FILE_PART_5}...")
    part_5_raw = read_file(FILE_PART_5)
    # Renumbering: Replace "VI." with "V." in headers
    def replace_vi_with_v(match):
        prefix = match.group(1)
        suffix = match.group(2)
        return f"{prefix}V{suffix}"

    part_5_text = re.sub(r'^(#*\s*)VI(\.| )', replace_vi_with_v, part_5_raw, flags=re.MULTILINE)
    print(f"Part V processed. (Length: {len(part_5_text)} chars)")

    # 5. Assemble
    full_content = (
        part_1_2_text.strip() + "\n\n" +
        "---\n\n" +
        part_3_text.strip() + "\n\n" +
        "---\n\n" +
        part_4_text.strip() + "\n\n" +
        "---\n\n" +
        part_5_text.strip() + "\n\n" +
        "---\n\n" +
        references_text.strip()
    )
    
    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_content)
        
    print(f"SUCCESS: Master White Paper written to {OUTPUT_FILE}")
    print(f"Total lines: {len(full_content.splitlines())}")

if __name__ == "__main__":
    consolidate()
