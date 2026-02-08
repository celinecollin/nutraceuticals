
import io
import os
import sys
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------
# STEP 1: VERIFIED DATA (Strictly from Whitepaper)
# ---------------------------------------------------------
DATA = {
    "North America": {
        "CORPORATES": [
            "Zoetis", 
            "Elanco", 
            "Mars Petcare", 
            "General Mills (Blue Buffalo)", 
            "Purina (Nestlé)", 
            "Phibro Animal Health", 
            "Nutramax Laboratories",
            "Simmons Pet Food",
            "Merck Animal Health"
        ],
        "STARTUPS": [
            "Native Pet (Clean Label)", 
            "Bond Pet Foods (Fermentation)", 
            "BiomEdit (Microbiome)", 
            "Loyal (Longevity)", 
            "AnimalBiome (FMT)", 
            "Gallant (Stem Cells)", 
            "Hoofprint Biome",
            "Wild Earth"
        ],
        "INVESTORS": [
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
        "CORPORATES": [
            "DSM-Firmenich", 
            "Novonesis", 
            "Virbac", 
            "Vetoquinol", 
            "Dechra", 
            "IVC Evidensia", 
            "Symrise (Pet)", 
            "Nutreco",
            "Boehringer Ingelheim",
            "Ceva Santé Animale"
        ],
        "STARTUPS": [
            "Veramaris (Algal Oil)", 
            "Innovafeed (Insect)", 
            "MicroHarvest (Biotech)", 
            "Protix (Insect)", 
            "Gnubiotics (Glycans)", 
            "Mootral (Methane)", 
            "Mammaly (Supplements)",
            "Proteon Pharmaceuticals"
        ],
        "INVESTORS": [
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
        "CORPORATES": [
            "H&H Group (Swisse/Zesty Paws)", 
            "CP Foods (Thailand)", 
            "Godrej Agrovet (India)", 
            "Gambol Pet Group (China)", 
            "New Hope Group"
        ],
        "STARTUPS": [
            "Rumin8 (Australia - Methane)", 
            "Sea6 Energy (India - Seaweed)", 
            "SyAqua (Genetics)", 
            "Biofeyn (Aqua-Tech)"
        ],
        "INVESTORS": [
            "Temasek (Agri-Food)",
            "Openspace Ventures"
        ]
    },
    "LATAM": {
        "CORPORATES": [
            "Brazil (Agri-Export Hub)",
            "Argentina (Agri-Export Hub)"
        ],
        "STARTUPS": [
            "The Not Company (Alt-Protein)"
        ],
        "INVESTORS": [
            "SP Ventures"
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
# STEP 3: "PERFECT FIT" VISUALIZATION SCRIPT
# ---------------------------------------------------------
def create_perfect_fit_map(background_path, data, output_path):
    print(f"Generating perfect-fit map from {background_path}...")
    
    # 1. Load Image
    img = Image.open(background_path).convert("RGBA")
    width, height = img.size
    print(f"Image Dimensions: {width}x{height}")
    draw = ImageDraw.Draw(img)

    # 2. Optimized Scaling (1.8% - slightly smaller than HighVis to prevent overlap)
    base_scale = width / 100
    header_size = int(base_scale * 2.2)  # Reduced from 3.0
    sub_size = int(base_scale * 1.8)     # Reduced from 2.2
    body_size = int(base_scale * 1.5)    # Reduced from 2.0
    margin = int(header_size * 0.6)
    
    print(f"Font Sizes - Header: {header_size}, Sub: {sub_size}, Body: {body_size}")

    # 3. Load Fonts
    try:
        # Verified Mac System Font
        font_path = "/System/Library/Fonts/Helvetica.ttc"
        try:
            # Index 1 = Bold, Index 0 = Regular
            font_header = ImageFont.truetype(font_path, header_size, index=1)
            font_sub = ImageFont.truetype(font_path, sub_size, index=1)
        except:
            font_header = ImageFont.truetype(font_path, header_size, index=0)
            font_sub = ImageFont.truetype(font_path, sub_size, index=0)
            
        font_body = ImageFont.truetype(font_path, body_size, index=0)

    except Exception as e:
        print(f"Font loading error: {e}")
        font_header = ImageFont.load_default()
        font_sub = font_header
        font_body = font_header

    # 4. Adjusted Coordinates (Spaced out to prevent collisions)
    coords = {
        "North America": (0.01, 0.15),  # Shifted Left
        "EMEA": (0.48, 0.05),           # Shifted Right (away from NA)
        "APAC": (0.78, 0.20),           # Shifted Right
        "LATAM": (0.28, 0.65)           # Shifted Down/Right
    }

    # 5. Draw Loop
    for region, categories in data.items():
        if region not in coords: continue
        
        # A. Prepare Text Lines
        lines_to_draw = []
        lines_to_draw.append((region.upper(), font_header, (0,0,139), int(base_scale * 0.5)))
        
        for cat_name, items in categories.items():
            if not items: continue
            lines_to_draw.append((f"\n{cat_name}", font_sub, (139,0,0), int(base_scale * 0.2)))
            for item in items:
                lines_to_draw.append((f"• {item}", font_body, (0,0,0), int(base_scale * 0.1)))

        # B. Measure Box
        max_w = 0
        total_h = 0
        dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1,1)))
        
        for text, fnt, col, space in lines_to_draw:
            # Use textbbox if available (newer Pillow)
            try:
                bbox = dummy_draw.textbbox((0, 0), text, font=fnt)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
            except AttributeError:
                 w, h = dummy_draw.textsize(text, font=fnt)
                 
            if w > max_w: max_w = w
            total_h += h + space

        # C. Draw Background Box
        start_x = int(coords[region][0] * width)
        start_y = int(coords[region][1] * height)
        
        # Clamp to width
        if start_x + max_w > width:
             start_x = width - max_w - margin
        
        box = (start_x - margin, start_y - margin, 
               start_x + max_w + margin, start_y + total_h + margin)
        
        overlay = Image.new('RGBA', img.size, (255,255,255,0))
        d_ov = ImageDraw.Draw(overlay)
        d_ov.rectangle(box, fill=(255, 255, 255, 230), outline="black", width=2)
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img) 

        # D. Draw Text
        cur_y = start_y
        for text, fnt, col, space in lines_to_draw:
            draw.text((start_x, cur_y), text, font=fnt, fill=col)
            try:
                  h = draw.textbbox((0,0), text, font=fnt)[3] - draw.textbbox((0,0), text, font=fnt)[1]
            except AttributeError:
                  h = draw.textsize(text, font=fnt)[1]
            cur_y += h + space

    # 6. Save
    img = img.convert("RGB")
    img.save(output_path)
    print(f"Map generated: {output_path}")

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    pdf_input = "report/20260121_new input/MapChart_Map .pdf"
    temp_image = "report/20260121_new input/temp_map_base_perfect.png"
    final_output = "Global_Antigravity_Landscape_PerfectFit.png"
    
     # Check if we need to extract the map again
    if not os.path.exists(temp_image):
        if not extract_map_image(pdf_input, temp_image):
            print("Failed to extract map. Exiting.")
            sys.exit(1)
            
    create_perfect_fit_map(temp_image, DATA, final_output)
    
    # Clean up temp
    if os.path.exists(temp_image):
        os.remove(temp_image)
