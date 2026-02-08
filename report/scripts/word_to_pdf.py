import os
import subprocess
import sys

def docx_to_pdf(docx_path, pdf_path):
    docx_path = os.path.abspath(docx_path)
    pdf_path = os.path.abspath(pdf_path)
    
    # AppleScript to convert DOCX to PDF using Word
    script = f'''
    tell application "Microsoft Word"
        set docPath to "{docx_path}"
        set pdfPath to "{pdf_path}"
        
        -- Open the document
        open docPath
        set aggressive to active document
        
        -- Save as PDF
        save as aggressive file name pdfPath file format format PDF
        
        -- Close without saving changes
        close aggressive saving no
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True)
        print(f"Successfully converted to {pdf_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting document: {e}")
        sys.exit(1)

if __name__ == "__main__":
    base_dir = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report"
    docx = os.path.join(base_dir, "Master_WhitePaper_Final.docx")
    pdf = os.path.join(base_dir, "Master_WhitePaper_Final_Verify.pdf")
    
    if not os.path.exists(docx):
        print(f"File not found: {docx}")
        sys.exit(1)
        
    docx_to_pdf(docx, pdf)
