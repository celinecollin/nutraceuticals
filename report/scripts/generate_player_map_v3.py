
import io
import os
import sys
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------
# STEP 1: COMPREHENSIVE DATA (Categorized)
# ---------------------------------------------------------
DATA = {
    "North America": {
        "Corporates": [
            "Zoetis", 
            "Elanco", 
            "Mars Petcare", 
            "General Mills (Blue Buffalo)", 
            "Purina (Nestlé)", 
            "Phibro Animal Health", 
            "Nutramax Laboratories",
            "Church & Dwight"
        ],
        "Startups/Scaleups": [
            "Native Pet (Clean Label)", 
            "Bond Pet Foods (Fermentation)", 
            "BiomEdit (Microbiome)", 
            "Loyal (Longevity)", 
            "AnimalBiome (FMT)", 
            "Gallant (Stem Cells)", 
            "Hoofprint Biome"
        ],
        "Investors": [
            "Digitalis Ventures", 
            "S2G Investments", 
            "Borealis Ventures", 
            "MSCP (Morgan Stanley)", 
            "Vestar Capital", 
            "Cavallo Ventures", 
            "Stray Dog Capital", 
            "Gryphon Investors"
        ]
    },
    "EMEA": {
        "Corporates": [
            "DSM-Firmenich", 
            "Novonesis", 
            "Virbac", 
            "Vetoquinol", 
            "Dechra (EQT)", 
            "IVC Evidensia", 
            "Symrise (Pet)", 
            "Nutreco"
        ],
        "Startups/Scaleups": [
            "Veramaris (Algal Oil)", 
            "Innovafeed (Insect)", 
            "MicroHarvest (Biotech)", 
            "Protix (Insect)", 
            "Gnubiotics (Glycans)", 
            "Mootral (Methane)", 
            "Mammaly (Supplements)"
        ],
        "Investors": [
            "EQT Group", 
            "Cinven", 
            "Aqua-Spark", 
            "Anterra Capital", 
            "Five Seasons Ventures", 
            "Blue Horizon", 
            "Ocean 14 Capital", 
            "Seventure Partners"
        ]
    },
    "APAC": {
        "Corporates": [
            "H&H Group (Swisse/Zesty Paws)", 
            "CP Foods (Thailand)", 
            "Godrej Agrovet (India)", 
            "Gambol Pet Group (China)", 
            "New Hope Group", 
            "Shandong Lushang"
        ],
        "Startups/Scaleups": [
            "Rumin8 (Australia - Methane)", 
            "Sea6 Energy (India - Seaweed)", 
            "SyAqua (Genetics)", 
            "Biofeyn (Aqua-Tech)"
        ],
        "Investors": [
            "Temasek (Agri-Food)", 
            "ADM Capital (Cibus)", 
            "Openspace Ventures" 
        ]
    },
    "LATAM": {
        "Corporates": [
            "JBS (Global Meat/Feed)", 
            "BRF S.A.", 
            "Minerva Foods", 
            "Vittia"
        ],
        "Startups/Scaleups": [
            "The Not Company (Alt-Protein)", 
            "Bioheuris"
        ],
        "Investors": [
            "SP Ventures", 
            "Yield Lab LATAM"
        ]
    }
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
        
        image_file_object = page.images[0]
        with open(output_image_path, "wb") as fp:
            fp.write(image_file_object.data)
            
        print(f"Saved base map to {output_image_path}")
        return True
    except Exception as e:
        print(f"Error extracting image: {e}")
        return False

# ---------------------------------------------------------
# STEP 3: ADVANCED VISUALIZATION SCRIPT (User Provided Logic)
# ---------------------------------------------------------
def create_categorized_map(background_path, data, output_path):
    print(f"Generating map from {background_path}...")
    
    # 1. Load Image
    try:
        img = Image.open(background_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    width, height = img.size
    print(f"Image Dimensions: {width}x{height}")
    draw = ImageDraw.Draw(img)

    # 2. Dynamic Sizing
    font_size = int(width * 0.011) 
    margin = int(font_size * 0.6)
    
    print(f"Font Size: {font_size}")

    # 3. Fonts
    try:
        # Mac standard fonts
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica-Bold.ttc", int(font_size * 1.2))
        sub_font = ImageFont.truetype("/System/Library/Fonts/Helvetica-Bold.ttc", font_size)
    except:
        try:
            # Linux/Generic fallback
            font = ImageFont.truetype("arial.ttf", font_size)
            header_font = ImageFont.truetype("arialbd.ttf", int(font_size * 1.2))
            sub_font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            print("Using default font")
            font = ImageFont.load_default()
            header_font = font
            sub_font = font

    # 4. Coordinates 
    coords = {
        "North America": (0.02, 0.15),
        "EMEA": (0.42, 0.05),
        "APAC": (0.76, 0.15),
        "LATAM": (0.28, 0.60)
    }

    # 5. Rendering Loop
    for region, categories in data.items():
        if region not in coords: continue
        
        # A. Construct the text block to calculate size
        lines = []
        lines.append((region.upper(), header_font, (0, 0, 139, 255))) # Main Header (DarkBlue)
        
        for cat_name, items in categories.items():
            if not items: continue
            lines.append((f"\n{cat_name.upper()}", sub_font, (139, 0, 0, 255))) # Category Subheader (DarkRed)
            for item in items:
                lines.append((f"• {item}", font, (0, 0, 0, 255))) # Items (Black)

        # B. Calculate Box Size
        max_w = 0
        total_h = 0
        
        # Temporary draw to measure
        temp_draw = ImageDraw.Draw(Image.new("RGBA", (1,1)))
        
        for text, fnt, color in lines:
            try:
                bbox = temp_draw.textbbox((0, 0), text, font=fnt)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
            except AttributeError:
                w, h = temp_draw.textsize(text, font=fnt)
                
            if w > max_w: max_w = w
            total_h += h + 4 # +4 for line spacing

        # C. Draw Background Box
        start_x = int(coords[region][0] * width)
        start_y = int(coords[region][1] * height)
        
        # Ensure we stay within image bounds (simple clamp)
        if start_x + max_w > width:
            start_x = width - max_w - margin
            
        box_coords = (start_x - margin, start_y - margin, 
                      start_x + max_w + margin, start_y + total_h + margin)
        
        overlay = Image.new('RGBA', img.size, (255,255,255,0))
        d_ov = ImageDraw.Draw(overlay)
        d_ov.rectangle(box_coords, fill=(255, 255, 255, 230), outline="black", width=2)
        img = Image.alpha_composite(img, overlay)
        
        # D. Draw Text
        draw = ImageDraw.Draw(img) # Refresh draw object
        cur_y = start_y
        for text, fnt, color in lines:
            draw.text((start_x, cur_y), text, font=fnt, fill=color)
            try:
                line_h = draw.textbbox((0,0), text, font=fnt)[3] - draw.textbbox((0,0), text, font=fnt)[1]
            except AttributeError:
                line_h = draw.textsize(text, font=fnt)[1]
            cur_y += line_h + 4

    # 6. Save
    img = img.convert("RGB")
    img.save(output_path)
    print(f"Map generated successfully: {output_path}")

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    pdf_input = "report/20260121_new input/MapChart_Map .pdf"
    temp_image = "report/20260121_new input/temp_map_base_v3.png"
    final_output = "Global_Antigravity_Landscape_Detailed.png"
    
    # Check if we need to extract the map again
    if not os.path.exists(temp_image):
        if not extract_map_image(pdf_input, temp_image):
            print("Failed to extract map. Exiting.")
            sys.exit(1)
            
    create_categorized_map(temp_image, DATA, final_output)
    
    # Clean up temp
    if os.path.exists(temp_image):
        os.remove(temp_image)
