
import io
import os
import sys
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------
# STEP 1: STRICTLY VERIFIED DATA (Do Not Alter)
# ---------------------------------------------------------
DATA = {
    "North America": {
        "CORPORATES": [
            "Zoetis (Animal Health)",
            "Elanco (Therapeutics/Feed)",
            "Mars Petcare (Nutrition/Health)",
            "General Mills (Blue Buffalo)",
            "Purina (Pet Nutrition)",
            "Phibro (Mineral Nutrition)",
            "Nutramax (Supplements)",
            "Simmons Pet Food (Manufacturing)",
            "Merck Animal Health (Tech/Pharma)"
        ],
        "STARTUPS": [
            "Native Pet (Functional Toppers)",
            "Bond Pet Foods (Fermentation Protein)",
            "BiomEdit (Microbiome/Probiotics)",
            "Loyal (Longevity Therapeutics)",
            "AnimalBiome (Gut Health/FMT)",
            "Gallant (Stem Cells/Therapeutics)",
            "Hoofprint Biome (Methane Reduction)",
            "Wild Earth (Koji Protein)"
        ],
        "INVESTORS": [
            "Ani.vc (Pet Care VC)",
            "Digitalis Ventures (Health/Tech)",
            "S2G Investments (Agri-Food)",
            "Borealis Ventures (Health)",
            "MSCP (Morgan Stanley)",
            "Vestar Capital (Pet Care)",
            "Cavallo Ventures (General Mills)",
            "Stray Dog Capital (Alt-Protein)",
            "Gryphon Investors (Pet Care)"
        ]
    },
    "UK": {
        "CORPORATES": [
            "Dechra (Pharma/Nutrition)",
            "IVC Evidensia (Vet Services)",
            "Anpario (Feed Additives)",
            "Eco Animal Health (Pharma/Feed)"
        ],
        "STARTUPS": [
            "Biome9 (Gut Health/AI)",
            "YuMOVE (Joint Supplements)"
        ],
        "INVESTORS": [
            "Ocean 14 Capital (Blue Economy)",
            "Cinven (PE - Pet/Health)",
            "Grosvenor Food & AgTech (Agri-Invest)"
        ]
    },
    "EMEA": {
        "CORPORATES": [
            "DSM-Firmenich (Additives/Gut Health)",
            "Novonesis (Biosolutions/Enzymes)",
            "Virbac (Pharma/Nutrition)",
            "Vetoquinol (Therapeutics)",
            "Symrise (Pet Food Palatability)",
            "Nutreco (Feed/Aquaculture)",
            "Boehringer Ingelheim (Health)",
            "Ceva Santé Animale (Health)"
        ],
        "STARTUPS": [
            "Veramaris (Algal EPA/DHA)",
            "Innovafeed (Insect Protein)",
            "MicroHarvest (Single Cell Protein)",
            "Protix (Insect Ingredients)",
            "Gnubiotics (Glycans/Microbiome)",
            "Mootral (Methane Reduction)",
            "Mammaly (Supplements)",
            "Proteon (Bacteriophages)"
        ],
        "INVESTORS": [
            "EQT Group (PE - IVC/Dechra)",
            "Aqua-Spark (Aquaculture)",
            "Anterra Capital (AgTech)",
            "Five Seasons Ventures (Food Tech)",
            "Blue Horizon (Sustainable Food)",
            "Seventure Partners (Microbiome)"
        ]
    },
    "APAC": {
        "CORPORATES": [
            "H&H Group (Zesty Paws/Swisse)",
            "CP Foods (Feed/Agri)",
            "Godrej Agrovet (Feed/Agri)",
            "Gambol Pet Group (Manufacturing)",
            "New Hope Group (Feed/Agri)",
            "SyAqua (Advanced Shrimp Feed)"
        ],
        "STARTUPS": [
            "Rumin8 (Methane Reducers)",
            "Sea6 Energy (Seaweed Additives)",
            "Biofeyn (Aqua-Feed Tech)",
            "Varkalah Farms (Sustainable Feed)"
        ],
        "INVESTORS": [
            "Temasek (Agri-Food)",
            "ADM Capital (Cibus Fund)",
            "Openspace Ventures (Tech)"
        ]
    },
    "LATAM": {
        "CORPORATES": [
            "JBS (Global Feed/Meat)",
            "BRF S.A. (Feed/Pet Food)",
            "PremieRpet (Pet Nutrition)"
        ],
        "STARTUPS": [], 
        "INVESTORS": [
            "SP Ventures (AgTech)"
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
# STEP 3: HIGH-DENSITY VISUALIZATION SCRIPT
# ---------------------------------------------------------
def create_final_map(background_path, data, output_path):
    print(f"Generating final densely populated map from {background_path}...")
    
    # 1. Load Image
    img = Image.open(background_path).convert("RGBA")
    width, height = img.size
    print(f"Image Dimensions: {width}x{height}")
    draw = ImageDraw.Draw(img)

    # 2. Density Settings (1.1% scale for max information density)
    base_scale = width / 100
    header_size = int(base_scale * 1.4)  
    sub_size = int(base_scale * 1.2)     
    body_size = int(base_scale * 1.1)    
    margin = int(header_size * 0.4)
    
    print(f"Font Sizes - Header: {header_size}, Sub: {sub_size}, Body: {body_size}")

    # 3. Load Fonts (Fixed for MacOS)
    try:
        font_path = "/System/Library/Fonts/Helvetica.ttc"
        try:
             # Index 1 = Bold
             font_header = ImageFont.truetype(font_path, header_size, index=1)
             font_sub = ImageFont.truetype(font_path, sub_size, index=1)
        except:
             font_header = ImageFont.truetype(font_path, header_size, index=0)
             font_sub = ImageFont.truetype(font_path, sub_size, index=0)
             
        font_body = ImageFont.truetype(font_path, body_size, index=0)
    except Exception as e:
        print(f"Font error ({e}), utilizing default.")
        font_header = ImageFont.load_default()
        font_sub = font_header
        font_body = font_header

    # 4. Precise Coordinates
    coords = {
        "North America": (0.005, 0.10), # Left
        "UK": (0.31, 0.02),             # North Atlantic (Center-Left)
        "EMEA": (0.50, 0.02),           # Europe (Center-Right)
        "APAC": (0.80, 0.15),           # Far Right
        "LATAM": (0.28, 0.65)           # Bottom Left
    }

    # 5. Draw Loop
    for region, categories in data.items():
        if region not in coords: continue
        
        # Build Text Block
        lines = []
        lines.append((region.upper(), font_header, (0,0,139), int(base_scale * 0.4)))
        
        for cat_name, items in categories.items():
            if not items: continue
            lines.append((f"\n{cat_name}", font_sub, (139,0,0), int(base_scale * 0.1)))
            for item in items:
                lines.append((f"• {item}", font_body, (0,0,0), int(base_scale * 0.05)))

        # Measure Box
        max_w = 0
        total_h = 0
        dummy = ImageDraw.Draw(Image.new("RGBA", (1,1)))
        for text, fnt, col, space in lines:
            try:
                bbox = dummy.textbbox((0, 0), text, font=fnt)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
            except AttributeError:
                w, h = dummy.textsize(text, font=fnt)
                
            if w > max_w: max_w = w
            total_h += h + space

        # Draw Background
        sx = int(coords[region][0] * width)
        sy = int(coords[region][1] * height)
        
        # Prevent bottom overflow
        if sy + total_h > height: sy = height - total_h - margin
        # Prevent right overflow
        if sx + max_w > width: sx = width - max_w - margin

        box = (sx - margin, sy - margin, sx + max_w + margin, sy + total_h + margin)
        
        overlay = Image.new('RGBA', img.size, (255,255,255,0))
        d_ov = ImageDraw.Draw(overlay)
        d_ov.rectangle(box, fill=(255, 255, 255, 240), outline="black", width=1)
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img) 

        # Draw Text
        cy = sy
        for text, fnt, col, space in lines:
            draw.text((sx, cy), text, font=fnt, fill=col)
            try:
                 h = draw.textbbox((0,0), text, font=fnt)[3] - draw.textbbox((0,0), text, font=fnt)[1]
            except AttributeError:
                 h = draw.textsize(text, font=fnt)[1]
            cy += h + space

    # 6. Save
    img = img.convert("RGB")
    img.save(output_path)
    print(f"Map generated: {output_path}")

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    pdf_input = "report/20260121_new input/MapChart_Map .pdf"
    temp_image = "report/20260121_new input/temp_map_base_final.png"
    final_output = "Global_Antigravity_Landscape_Final.png"
    
    # Check if we need to extract the map again
    if not os.path.exists(temp_image):
        if not extract_map_image(pdf_input, temp_image):
            print("Failed to extract map. Exiting.")
            sys.exit(1)
            
    create_final_map(temp_image, DATA, final_output)
    
    # Clean up temp
    if os.path.exists(temp_image):
        os.remove(temp_image)
