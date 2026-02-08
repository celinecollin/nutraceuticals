
import re

file_path = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/Master_WhitePaper_Final.md"

def renumber_figures():
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    seen_paths = set()
    
    current_part = "I" # Default to I
    fig_counter = 0
    
    skip_next = False
    
    # Regex to match image lines: ![Alt](path)
    img_pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
            
        stripped = line.strip()
        
        # Detect PART headers
        if stripped.startswith("# PART I:"):
            current_part = "I"
            fig_counter = 0
            new_lines.append(line)
            continue
        elif stripped.startswith("# PART II:"):
            current_part = "II"
            fig_counter = 0
            new_lines.append(line)
            continue
        elif stripped.startswith("# PART III:"):
            current_part = "III"
            fig_counter = 0
            new_lines.append(line)
            continue
            
        # Detect Image
        img_match = img_pattern.search(line)
        if img_match:
            path = img_match.group(1)
            if path in seen_paths:
                print(f"Removing duplicate figure: {path}")
                # Skip this line AND the next line (caption)
                # Check if next line is a caption
                if i + 1 < len(lines) and lines[i+1].strip().startswith("*Figure"):
                    skip_next = True
                continue
            
            seen_paths.add(path)
            # Increment counter for valid unique figure
            fig_counter += 1
            new_lines.append(line)
            
            # Now handle the caption in the NEXT line
            # We assume caption immediately follows image
            if i + 1 < len(lines) and lines[i+1].strip().startswith("*Figure"):
                caption_line = lines[i+1]
                # Replace *Figure X.Y: with *Figure {Part}.{Counter}:
                # Regex for Caption start
                new_caption = re.sub(r'^\*Figure\s+[\w\d\.]+\s*:', f'*Figure {current_part}.{fig_counter}:', caption_line)
                
                # If regex fails (different format), force it
                if new_caption == caption_line:
                     # Maybe it's missing the colon or weird spacing
                     # Just find the first colon and replace everything before it?
                     parts = caption_line.split(':', 1)
                     if len(parts) > 1:
                         new_caption = f'*Figure {current_part}.{fig_counter}:{parts[1]}'
                
                # Update the next line in our processing loop? 
                # We can't easily modify the 'lines' list we are iterating.
                # We should structure this so we append the modified caption now and skip it next loop.
                new_lines.append(new_caption)
                skip_next = True
            else:
                # Image without caption? Or caption is separated?
                # Just append image line and move on.
                pass
            continue
            
        # If line starts with *Figure but wasn't handled by the image logic (orphaned caption?)
        # We should logically shouldn't hit this if logic above is correct, unless caption is separated by newline.
        # But our standard format is Image \n Caption.
        if stripped.startswith("*Figure"):
            # If we are here, it means this caption was NOT immediately following an image we just processed.
            # Could be orphaned or separated by blank line.
            # If separated by blank line, we might have missed it.
            # Let's just renumber it to match current counter? 
            # No, if we didn't see an image, we shouldn't increment.
            # But maybe the image was processed in previous steps (e.g. blank line in between).
            # Best safe bet: Assume orphan or error, but let's try to fix it.
            # If we didn't increment counter, this caption belongs to NO image?
            # Or maybe the file has Image \n \n Caption.
            pass

        new_lines.append(line)

    with open(file_path, 'w') as f:
        f.writelines(new_lines)
    
    print("Figures renumbered and duplicates removed.")

if __name__ == "__main__":
    renumber_figures()
