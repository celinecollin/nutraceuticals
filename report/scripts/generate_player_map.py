
import io
import os
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont

# Define the entities extracted from the whitepaper
ENTITIES = {
    "North America": [
        "• Zoetis (Pharma Leader)",
        "• Elanco (Pharma Leader)",
        "• Mars Petcare (Consolidator)",
        "• General Mills (Blue Buffalo)",
        "• Native Pet (Startup)",
        "• Bond Pet Foods (Startup)",
        "• BiomEdit (Biotech)",
        "• Digitalis Ventures (VC)",
        "• S2G Investments (VC)",
        "• Clearlake Capital (PE)"
    ],
    "EMEA (Europe)": [
        "• DSM-Firmenich (Ingredients)",
        "• Novonesis (Biosolutions)",
        "• Virbac (Pharma/Pet)",
        "• EQT Group (PE - IVC/Dechra)",
        "• Cinven (PE - Arcaplanet)",
        "• BC Partners (PE - PetSmart)",
        "• Veramaris (Scaleup)",
        "• MicroHarvest (Biotech)",
        "• Aqua-Spark (Sustainability VC)",
        "• Anterra Capital (VC)"
    ],
    "APAC (Asia-Pacific)": [
        "• H&H Group (Swisse/Zesty Paws)",
        "• CP Foods (Agri-Giant)",
        "• Godrej Agrovet (Agri-Giant)",
        "• Rumin8 (Methane - Australia)",
        "• Sea6 Energy (Seaweed - India)",
        "• Gamhol Pet Group (Manufacturing)",
        "• Shandong Lushang (Feed)"
    ]
}

# Coordinates for text placement (approximate based on standard world map layout)
# Inspecting the image dimensions will be crucial, but we'll start with relative positions if possible, or fixed guesses.
# Assuming a standard 1080p or 4k landscape map.
COORDINATES = {
    "North America": (130, 150),  # Top Left
    "EMEA (Europe)": (700, 100),  # Top Center-Right (Europe is usually higher up)
    "APAC (Asia-Pacific)": (1100, 250), # Right side
    "LATAM": (250, 600)           # Bottom Left
}

def extract_map_image(pdf_path, output_image_path):
    print(f"Extracting image from {pdf_path}...")
    try:
        reader = PdfReader(pdf_path)
        page = reader.pages[0]
        
        # Check for images in the page
        if not page.images:
            print("No images found in PDF!")
            return False
        
        # Extract the first image found (assuming it's the map)
        image_file_object = page.images[0]
        print(f"Found image: {image_file_object.name}")
        
        with open(output_image_path, "wb") as fp:
            fp.write(image_file_object.data)
            
        print(f"Saved base map to {output_image_path}")
        return True
    except Exception as e:
        print(f"Error extracting image: {e}")
        return False

def overlay_entities(base_image_path, output_path):
    print(f"Overlaying entities onto {base_image_path}...")
    try:
        # Load image
        img = Image.open(base_image_path)
        draw = ImageDraw.Draw(img)
        
        # Get dimensions
        width, height = img.size
        print(f"Image dimensions: {width}x{height}")
        
        # Recalculate coordinates based on image size if needed
        # We'll stick to percentage-based relative positioning for better robustness
        coords_relative = {
            "North America": (0.05, 0.15),
            "EMEA (Europe)": (0.48, 0.10),
            "APAC (Asia-Pacific)": (0.75, 0.25),
        }
        
        # Load Font
        try:
            # Try to load a standard font
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=24) # Mac standard
        except:
            try: 
                 font = ImageFont.truetype("arial.ttf", 24)
            except:
                print("Could not load custom font, using default.")
                font = ImageFont.load_default()

        # Colors
        text_color = (0, 0, 0) # Black
        
        for region, lines in ENTITIES.items():
            if region not in coords_relative:
                continue
                
            rx, ry = coords_relative[region]
            x = int(rx * width)
            y = int(ry * height)
            
            # Draw Region Title
            draw.text((x, y), region.upper(), fill=(0, 0, 139), font=font) # Dark Blue title
            
            # Draw spacing
            y += 30
            
            # Draw entities
            # Use smaller font for list
            try:
                list_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=18)
            except:
                list_font = font
                
            for line in lines:
                draw.text((x, y), line, fill=text_color, font=list_font)
                y += 22
                
        img.save(output_path)
        print(f"Final map saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing image: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    pdf_input = "report/20260121_new input/MapChart_Map .pdf"
    temp_image = "report/20260121_new input/temp_map_base.png"
    final_output = "Global_Antigravity_Landscape.png"
    
    if extract_map_image(pdf_input, temp_image):
        overlay_entities(temp_image, final_output)
        # Optional: cleanup
        # os.remove(temp_image)

