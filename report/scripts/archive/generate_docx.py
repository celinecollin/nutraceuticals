
import re
import os
import subprocess

# Define file paths
BASE_DIR = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals"
SOURCE_DIR = os.path.join(BASE_DIR, "report", "sources")
OUTPUT_DIR = os.path.join(BASE_DIR, "report", "master_report")
DOCX_OUTPUT = os.path.join(OUTPUT_DIR, "20260118_Master_WhitePaper.docx")

# Source files
FILE_LEGACY_WP = os.path.join(SOURCE_DIR, "2026015_WhitePaper.md")
FILE_PART_3 = os.path.join(SOURCE_DIR, "20260118_PartIII.md")
FILE_PART_4_SOURCE = os.path.join(SOURCE_DIR, "20260113_PartV.md")
FILE_PART_5_SOURCE = os.path.join(SOURCE_DIR, "VI. Notable Transactions and Investment Landscape (2015 to 2025) 20260113.md")

# Output Part files
OUT_PART_1_2 = os.path.join(OUTPUT_DIR, "20260118_01_Part_I_II.md")
OUT_PART_3 = os.path.join(OUTPUT_DIR, "20260118_02_Part_III.md")
OUT_PART_4 = os.path.join(OUTPUT_DIR, "20260118_03_Part_IV.md")
OUT_PART_5 = os.path.join(OUTPUT_DIR, "20260118_04_Part_V.md")
OUT_REFERENCES = os.path.join(OUTPUT_DIR, "20260118_05_References.md")
OUT_MISSING = os.path.join(OUTPUT_DIR, "20260118_06_Missing_Figures.md") # Optional inclusion

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {os.path.basename(path)}")

def process_and_split():
    print("--- Processing and Splitting Files ---")
    
    # 1. Part I & II (from Legacy WhitePaper)
    print(f"Processing Part I & II from {os.path.basename(FILE_LEGACY_WP)}...")
    content_wp = read_file(FILE_LEGACY_WP)
    
    # Regex to find start of Section III to cut off
    match_iii = re.search(r'(^#+\s*III\.|^III\.)', content_wp, re.MULTILINE)
    
    # Regex to find References (usually at the end)
    match_ref = re.search(r'(^#+\s*References|^References)', content_wp, re.MULTILINE)
    
    part_1_2_content = ""
    references_content = ""
    
    if match_iii:
        part_1_2_content = content_wp[:match_iii.start()]
    else:
        # Fallback if regex fails, careful split
        print("WARNING: Could not find 'III.' header. Splitting manually at line estimated.")
        part_1_2_content = content_wp # Fallback
        
    if match_ref:
         references_content = content_wp[match_ref.start():]
    
    write_file(OUT_PART_1_2, part_1_2_content)
    write_file(OUT_REFERENCES, references_content)

    # 2. Part III
    print(f"Processing Part III from {os.path.basename(FILE_PART_3)}...")
    content_p3 = read_file(FILE_PART_3)
    write_file(OUT_PART_3, content_p3)

    # 3. Part IV (Was Part V "Competitive Landscape" -> Renumber to IV)
    print(f"Processing Part IV from {os.path.basename(FILE_PART_4_SOURCE)}...")
    content_p4 = read_file(FILE_PART_4_SOURCE)
    # Renumber V. to IV.
    content_p4 = re.sub(r'^(#+\s*)V(\.\s)', r'\1IV\2', content_p4, flags=re.MULTILINE)
    content_p4 = re.sub(r'^(#+\s*)V(\.\d)', r'\1IV\2', content_p4, flags=re.MULTILINE)
    write_file(OUT_PART_4, content_p4)

    # 4. Part V (Was VI "Transactions" -> Renumber to V)
    print(f"Processing Part V from {os.path.basename(FILE_PART_5_SOURCE)}...")
    content_p5 = read_file(FILE_PART_5_SOURCE)
    # Determine if it's numbered V or VI in source.
    # Source appears to be "V. Notable..." or "VI. Notable...". 
    # We want it to be V.
    # Replace VI. with V.
    content_p5 = re.sub(r'^(#+\s*)VI(\.\s)', r'\1V\2', content_p5, flags=re.MULTILINE)
    content_p5 = re.sub(r'^(#+\s*)VI(\.\d)', r'\1V\2', content_p5, flags=re.MULTILINE)
    # If it was already V, ensure it stays V (no change needed if it matches output format)
    write_file(OUT_PART_5, content_p5)

    return [OUT_PART_1_2, OUT_PART_3, OUT_PART_4, OUT_PART_5, OUT_REFERENCES]

def convert_to_docx(file_list):
    print("\n--- Converting to DOCX ---")
    
    # Check for pandoc
    pandoc_cmd = "pandoc"
    if os.path.exists("/opt/homebrew/bin/pandoc"):
        pandoc_cmd = "/opt/homebrew/bin/pandoc"
    elif os.path.exists("/usr/local/bin/pandoc"):
        pandoc_cmd = "/usr/local/bin/pandoc"

    try:
        subprocess.run([pandoc_cmd, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Pandoc found: {pandoc_cmd}")
    except FileNotFoundError:
        print("Error: Pandoc not found. Please install pandoc.")
        return
    except subprocess.CalledProcessError:
         print("Error: Pandoc check failed.")
         return

    # We construct the command
    cmd = [pandoc_cmd, "-o", DOCX_OUTPUT]
    cmd.extend(file_list)
    
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print(f"SUCCESS: Generated {DOCX_OUTPUT}")
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e}")

if __name__ == "__main__":
    files = process_and_split()
    convert_to_docx(files)
