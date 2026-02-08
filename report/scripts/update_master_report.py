import os

MASTER_FILE = "report/master_report/20260122_Master_WhitePaper_V2.md"
APPENDIX_FILE = "report/source_material/Appendix_B_Exhaustive.md"

def main():
    with open(MASTER_FILE, "r") as f:
        master_content = f.read()

    with open(APPENDIX_FILE, "r") as f:
        appendix_content = f.read()

    # Find where Appendix B starts
    # Note: Using the exact header found earlier
    # 2058:## Appendix B: Strategic Business Case Targets
    
    marker = "## Appendix B:"
    split_index = master_content.find(marker)
    
    if split_index == -1:
        # Try finding just "## Appendix B"
        marker = "## Appendix B"
        split_index = master_content.find(marker)

    if split_index == -1:
        print("Error: Could not find '## Appendix B' in master report.")
        return

    # Keep content strictly BEFORE the marker.
    # We want to replace the marker and everything after it.
    new_content = master_content[:split_index] + "\n\n" + appendix_content
    
    with open(MASTER_FILE, "w") as f:
        f.write(new_content)
        
    print(f"Successfully updated {MASTER_FILE} with new Appendix B content.")

if __name__ == "__main__":
    main()
