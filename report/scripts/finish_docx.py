
import sys
import os
import shutil

# Add scripts dir to path
sys.path.append(os.path.join(os.getcwd(), 'report/scripts'))

try:
    import generate_docx_robust as gdr
except ImportError:
    # If standard import fails, try direct file load spec but sys.path should work
    print("Could not import generate_docx_robust")
    sys.exit(1)

docx_path = "report/master_report/Master_WhitePaper_Final.docx"
review_dir = "/Users/celinecollin/Documents/review"

print("Running Post-Processing...")

# 1. Style
gdr.apply_style_enhancements(docx_path)

# 2. Cover
gdr.add_cover_and_toc(docx_path)

# 3. Clean bookmarks
gdr.remove_bookmarks_from_xml(docx_path)

# 4. Copy to review
print("Copying to review folder...")
os.makedirs(review_dir, exist_ok=True)
review_path = os.path.join(review_dir, os.path.basename(docx_path))
shutil.copy2(docx_path, review_path)
print(f"  ✓ Copied to {review_path}")

print("Done.")
