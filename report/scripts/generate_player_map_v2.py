
import io
import os
import sys
import textwrap
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------
# STEP 1: DATA (Top 5-10 per region)
# ---------------------------------------------------------
ENTITIES = {
    "North America": [
        "Zoetis (Pharma Leader)",
        "Elanco (Pharma Leader)",
        "Mars Petcare (Consolidator)",
        "General Mills (Blue Buffalo)",
        "Native Pet (Startup)",
        "Bond Pet Foods (Startup)",
        "BiomEdit (Biotech)",
        "Digitalis Ventures (VC)",
        "S2G Investments (VC)"
    ],
    "EMEA": [
        "DSM-Firmenich (Ingredients)",
        "Novonesis (Biosolutions)",
        "Virbac (Pharma/Pet)",
        "EQT Group (PE - IVC/Dechra)",
        "Cinven (PE - Arcaplanet)",
        "BC Partners (PE - PetSmart)",
        "Veramaris (Scaleup)",
        "MicroHarvest (Biotech)",
        "Aqua-Spark (VC)"
    ],
    "APAC": [
        "H&H Group (Swisse/Zesty Paws)",
        "CP Foods (Agri-Giant)",
        "Godrej Agrovet (Agri-Giant)",
        "Rumin8 (Methane - Australia)",
        "Sea6 Energy (Seaweed - India)",
        "Gambol Pet Group (Manufacturing)"
    ],
    "LATAM": [
        "Brazil (Agri-Export Hub)",
        "Argentina (Agri-Export Hub)",
        "MAPA (Regulator)",
        "JBS (Global Meat/Feed)",
        "BRF (Global Meat/Feed)"
    ]
}

# ---------------------------------------------------------
# STEP 2: HELPER TO EXTRACT IMAGE FROM PDF
# ---------------------------------------------------------
def extract_map_image(pdf_path, output_image_path):
    print(f"Extracting image from {pdf_path}...")
    try:
        reader = PdfReader(pdf_path)
        page = reader.pages[0]
        
        if not page.images:
            print("No images found in PDF!")
            return False
        
        # Extract the first image found
        image_file_object = page.images[0]
        print(f"Found image: {image_file_object.name}")
        
        with open(output_image_path, "wb") as fp:
            fp.write(image_file_object.data)
            
        print(f"Saved base map to {output_image_path}")
        return True
    except Exception as e:
        print(f"Error extracting image: {e}")
        return False

# ---------------------------------------------------------
# STEP 3: SMART VISUALIZATION LOGIC
# ---------------------------------------------------------
def create_map(background_path, data, output_path):
    print(f"Generating map from {background_path}...")
    
    # Load Image
    try:
        img = Image.open(background_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    width, height = img.size
    print(f"Image Dimensions: {width}x{height}")
    
    draw = ImageDraw.Draw(img)

    # DYNAMIC SCALING: Font size is 1.5% of image width
    # Adjusted to 1.2% as 1.5% might be slightly too large for long lists
    font_size = int(width * 0.012) 
    margin = int(font_size * 0.5)
    
    print(f"Calculated Font Size: {font_size}")
    
    # Load Font (Fallback to default if needed)
    try:
        # Try finding a nice font on Mac
        font_path = "/System/Library/Fonts/Helvetica.ttc"
        if not os.path.exists(font_path):
             font_path = "arial.ttf" # Try generic
             
        font = ImageFont.truetype(font_path, font_size)
        # Using same font for header but maybe bold if we could find it, 
        # otherwise just use the same font
        header_font = font 
        try:
            # Try to get bold version
            header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica-Bold.ttc", font_size)
        except:
            pass
            
    except Exception as e:
        print(f"Font loading warning: {e}. Using default.")
        font = ImageFont.load_default()
        header_font = font

    # Coordinates (Percent of Width/Height) to avoid overlap
    # Tuned slightly based on standard world map projections
    coords = {
        "North America": (0.05, 0.20),
        "EMEA": (0.45, 0.10),
        "APAC": (0.75, 0.25),
        "LATAM": (0.28, 0.60)
    }

    for region, entities in data.items():
        if region not in coords: continue
        
        # Format Text
        header = region.upper()
        body = "\n".join([f"• {e}" for e in entities])
        full_text = f"{header}\n{body}"
        
        # Calculate Position
        x = int(coords[region][0] * width)
        y = int(coords[region][1] * height)
        
        # Draw Background Box (Semi-transparent White)
        try:
            bbox = draw.textbbox((x, y), full_text, font=font)
        except AttributeError:
             # Fallback for older Pillow versions
             bbox = draw.textsize(full_text, font=font)
             bbox = (x, y, x + bbox[0], y + bbox[1])

        # Add padding
        box = (bbox[0]-margin, bbox[1]-margin, bbox[2]+margin, bbox[3]+margin)
        
        overlay = Image.new('RGBA', img.size, (255,255,255,0))
        d_ov = ImageDraw.Draw(overlay)
        d_ov.rectangle(box, fill=(255,255,255,230), outline="black", width=2)
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img) # Refresh draw object
        
        # Draw Text (Blue Header, Black Body)
        # Draw Header
        draw.text((x, y), header, font=header_font, fill=(0,0,139))
        
        # Calculate header height to offset body
        try:
             header_bbox = draw.textbbox((0,0), header, font=header_font)
             header_height = header_bbox[3] - header_bbox[1]
        except AttributeError:
             header_height = draw.textsize(header, font=header_font)[1]
             
        # Draw Body
        draw.text((x, y + header_height + margin), body, font=font, fill="black")

    # Save
    img = img.convert("RGB")
    img.save(output_path)
    print(f"Success! Saved to {output_path}")

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    pdf_input = "report/20260121_new input/MapChart_Map .pdf"
    temp_image = "report/20260121_new input/temp_map_base_v2.png"
    final_output = "Global_Antigravity_Landscape_HighRes.png"
    
    # Check if we need to extract the map again
    if not os.path.exists(temp_image):
        if not extract_map_image(pdf_input, temp_image):
            print("Failed to extract map. Exiting.")
            sys.exit(1)
            
    create_map(temp_image, ENTITIES, final_output)
    
    # Clean up temp
    if os.path.exists(temp_image):
        os.remove(temp_image)
