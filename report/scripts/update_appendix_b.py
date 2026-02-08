
import re

file_path = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/Master_WhitePaper_Final.md"

# MAPPING 
country_map = {
    # A
    "AB Vista": "🇬🇧",
    "ADM": "🇺🇸",
    "Adisseo": "🇨🇳", # Bluestar
    "AgriProtein": "🇬🇧",
    "Agrivida": "🇺🇸",
    "Algaebio+": "🇮🇱", # Assuming Israel or similar, will check. Actually Algaebio is often Turkey or others. Let's use 🌍 if unknown. Wait, "Algaebio+" likely AlgaeBio (Turkey)? Or Algaennovation? Let's check context. "Astaxanthin". Algalif is Iceland. Algaebio+ might be startup. I will use 🌍 for unsure.
    "Algalif": "🇮🇸",
    "Alltech": "🇺🇸",
    "Alphia": "🇺🇸", # Alphia, NovaTaste
    "AniMedica": "🇩🇪",
    "Animal Necessity": "🇺🇸",
    "AnimalBiome": "🇺🇸",
    "Anizome": "🇬🇧",
    "Anpario": "🇬🇧",
    "Ark Naturals": "🇺🇸",
    "Aroma NZ": "🇳🇿",
    "Audevard": "🇫🇷",
    "Austin and Kat": "🇺🇸",
    "Aviform": "🇬🇧",
    "Axiota": "🇺🇸",
    # B
    "Balchem": "🇺🇸",
    "Because Animals": "🇺🇸",
    "Beneo": "🇩🇪",
    "Beta Hatch": "🇺🇸",
    "Big Heart Pet Brands": "🇺🇸",
    "BioAtlantis": "🇮🇪",
    "BioFeyn": "🇫🇷",
    "Bioiberica": "🇪🇸",
    "Biome9": "🇬🇧",
    "Bioriginal": "🇨🇦",
    "Boehringer Ingelheim": "🇩🇪",
    "Bond Pet Foods": "🇺🇸",
    "Buitelaar": "🇬🇧", # Buitelaar Group
    "Butternut Box": "🇬🇧", 
    # C
    "CH4 Global": "🇺🇸", # US/Aus
    "Calysta": "🇺🇸",
    "CanBiocin": "🇨🇦",
    "Candioli": "🇮🇹",
    "Canna-Pet": "🇺🇸",
    "Canvit": "🇨🇿",
    "Cargill Animal Nutrition": "🇺🇸",
    "Ceva": "🇫🇷",
    "Ceva Santé Animale": "🇫🇷",
    "Chicoa Fish Farm": "🇲🇿",
    "CompaniCalm": "🇫🇷", # Ceva product? No, "CompaniCalm" isn't a company, it's a product of someone? Wait, "CompaniCalm" listed as company? Ah, let's check product. "AC for Pets". Alpha-Casozepine is Zylkene (Vetoquinol). Wait, maybe Ingredia? "CompaniCalm" might be a typo for a brand. I'll check.
    "DSM-Firmenich": "🇨🇭",
    "Dechra": "🇬🇧",
    "Diamond V": "🇺🇸",
    "Dogswell": "🇺🇸",
    "Dr. Eckel": "🇩🇪",
    "Drools": "🇮🇳",
    # E
    "Earth Animal": "🇺🇸",
    "Edgard & Cooper": "🇧🇪",
    "Elanco": "🇺🇸",
    "ElleVet": "🇺🇸",
    "ElleVet Sciences": "🇺🇸",
    "Enough": "🇬🇧", # Scotland
    "EnsiliTech": "🇬🇧",
    "Enthos": "🇿🇦", # South Africa (Entomology?) 
    "Evonik": "🇩🇪",
    # F
    "FOTP": "🇺🇸",
    "Farmina": "🇮🇹",
    "Farnam": "🇺🇸",
    "Felix Biotechnology": "🇺🇸",
    "Fera Pet Organics": "🇺🇸",
    "Fermentalg": "🇫🇷",
    "Givaudan": "🇨🇭",
    "Finn": "🇺🇸",
    "FoodScience Corp": "🇺🇸",
    "FoodScience Corporation": "🇺🇸",
    "ForFarmers": "🇳🇱",
    "Freshpet": "🇺🇸",
    "Fyto": "🇺🇸", 
    # G
    "Gelita": "🇩🇪",
    "General Mills": "🇺🇸",
    "Gnubiotics": "🇨🇭",
    "Grizzly Pet Products": "🇺🇸",
    # H
    "Hamlet Protein": "🇩🇰",
    "Herbsmith Inc.": "🇺🇸",
    "Hexafly": "🇮🇪",
    "Hill's": "🇺🇸",
    "HolistaPet": "🇺🇸",
    "Honest Paws": "🇺🇸",
    "Hoofprint Biome": "🇺🇸",
    "Huvepharma": "🇧🇬",
    # I
    "Incaptek": "🇨🇭", # Switz
    "Innovafeed": "🇫🇷",
    "Innovet": "🇮🇹", # Innovet Italia
    "Inspired Pet Nutrition": "🇬🇧",
    # K
    "Kaesler Nutrition": "🇩🇪",
    "Kapsera": "🇫🇷",
    "Kemin": "🇺🇸",
    "Kingdom Supercultures": "🇺🇸",
    # L
    "LT Natural Group": "🇮🇹",
    "Lallemand": "🇨🇦",
    "Leiber GmbH": "🇩🇪",
    "Lintbells": "🇬🇧",
    "Lonza": "🇨🇭",
    # M
    "MIAVIT": "🇩🇪",
    "Made by Nacho": "🇺🇸",
    "Majesty’s": "🇺🇸",
    "Mammaly": "🇩🇪",
    "Mars Petcare": "🇺🇸",
    "Merck Animal Health": "🇺🇸",
    "MicroHarvest": "🇩🇪",
    "Millpledge": "🇬🇧",
    "Mixscience": "🇫🇷",
    "Monogram Foods": "🇺🇸",
    "Mootral": "🇨🇭", # Swiss
    "MycoTechnology": "🇺🇸",
    # N
    "Native Pet": "🇺🇸",
    "Nestlé Purina": "🇺🇸", # US HQ for Purina
    "Roquette": "🇫🇷",
    "NextProtein": "🇫🇷", # France/Tunisia
    "Nor-Feed": "🇫🇷",
    "NovoNutrients": "🇺🇸",
    "Novonesis": "🇩🇰",
    "Novus Intl.": "🇺🇸",
    "Nualtis": "🇫🇷",
    "Nulo": "🇺🇸",
    "Nuqo": "🇫🇷",
    "Nutramax": "🇺🇸",
    "Nutramax Laboratories": "🇺🇸",
    "Nutravet": "🇬🇧",
    "Nutreco": "🇳🇱",
    # O
    "Olmix": "🇫🇷",
    # P
    "Peptobiotics": "🇸🇬",
    "Perstorp": "🇸🇪", # Sweden
    "Petco": "🇺🇸",
    "PetHonesty": "🇺🇸",
    "PetLab Co.": "🇬🇧",
    "Phibro": "🇺🇸",
    "Phytobiotics": "🇩🇪",
    "Pintaluba": "🇪🇸",
    "Pond Technologies": "🇨🇦",
    "Precision Microbes": "🇮🇪",
    "Protenga": "🇸🇬",
    "Proteon": "🇵🇱",
    "Protix": "🇳🇱",
    "PupGrade": "🇺🇸",
    "Purina": "🇺🇸",
    # R
    "Red Mills": "🇮🇪",
    "Rumin8": "🇦🇺",
    "Rx Vitamins": "🇺🇸",
    # S
    "Sea6 Energy": "🇮🇳",
    "Seaqure Labs": "🇬🇧", # Likely UK or EU
    "Smalls": "🇺🇸",
    "SmartPak": "🇺🇸",
    "Solid Gold": "🇺🇸",
    "Springtide Seaweed": "🇺🇸",
    "String Bio": "🇮🇳",
    "Swedencare": "🇸🇪",
    "Symbrosia": "🇺🇸",
    "Symrise": "🇩🇪",
    "Symrise (Diana)": "🇩🇪",
    # T
    "Taiyo Kagaku": "🇯🇵",
    "Techna Vet": "🇫🇷",
    "The Nutriment Company": "🇸🇪",
    "The QRILL Company": "🇳🇴",
    "Treatibles": "🇺🇸",
    # U
    "Untamed": "🇬🇧",
    # V
    "VAFO": "🇨🇿",
    "Veramaris": "🇳🇱",
    "VetPlus": "🇬🇧",
    "Vetark": "🇬🇧",
    "Vetnique": "🇺🇸",
    "Vetnique Labs": "🇺🇸",
    "Vetoquinol": "🇫🇷",
    "Vetra Animal Health": "🇺🇸",
    "VetriScience": "🇺🇸",
    "Virbac": "🇫🇷",
    # W
    "Wellness Pet Company": "🇺🇸",
    "Wholistic Pet Organics": "🇺🇸",
    "Wild Earth": "🇺🇸",
    # Y
    "YuMOVE": "🇬🇧",
    "YuMOVE (Lintbells)": "🇬🇧",
    # Z
    "Zesty Paws": "🇺🇸",
    "Zinpro": "🇺🇸"
}

# Add default for missing
def get_flag(name):
    # Try exact match
    if name in country_map:
        return country_map[name]
    # Try partial
    for key, val in country_map.items():
        if key in name or name in key:
            return val
    return "🌍"

with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
in_table = False
header_processed = False

for line in lines:
    stripped = line.strip()
    
    # Detect Table Start
    if "| Company | Category |" in line:
        in_table = True
        # Add Country column to header
        parts = [p.strip() for p in line.split('|')]
        # parts[0] is empty str, parts[1] is Company, etc.
        # Expected: ['', 'Company', 'Category', 'Key Product/Focus', 'Target Species', 'Strategic Summary', '']
        parts.insert(2, "Country") 
        new_line = " | ".join(parts) + "\n"
        new_lines.append(new_line)
        header_processed = True
        continue
    
    # Detect separator row
    if in_table and set(stripped.replace('|', '').replace(' ', '')) == {'-'}:
         # Separator line: | --- | --- | ...
         # Need to add one more column separator
         parts = [p.strip() for p in line.split('|')]
         parts.insert(2, "---")
         new_line = " | ".join(parts) + "\n"
         new_lines.append(new_line)
         continue

    if in_table and stripped.startswith('|') and stripped.endswith('|'):
        # Table Row
        # Split by pipe
        # Note: simplistic split, assumes no pipes in content. 
        # Markdown tables usually escape pipes or don't use them in content. Use regex to be safer?
        # Actually split('|') is risky if empty cells.
        parts = line.split('|')
        
        # parts[0] is usually empty (before first pipe).
        # parts[1] is Company
        # We need to insert country at parts[2]
        
        if len(parts) >= 3:
            company_name = parts[1].strip()
            if company_name:
                flag = get_flag(company_name)
                parts.insert(2, f" {flag} ")
                new_line = "|".join(parts)
                new_lines.append(new_line)
            else:
                # Empty row or formatting
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    else:
        # Not a table row or end of table
        if in_table and not stripped.startswith('|'):
            in_table = False
        new_lines.append(line)

with open(file_path, 'w') as f:
    f.writelines(new_lines)

print("Appendix B updated with Country flags.")
