
import matplotlib.pyplot as plt
import os
import textwrap

# Define output directory
output_dir = "report/master_report/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- STYLE SETTINGS (Journal Quality) ---
HEADER_COLOR = '#2c3e50' # Dark Blue/Grey
ROW_EVEN_COLOR = '#ffffff'
ROW_ODD_COLOR = '#f8f9fa' # Very light grey
TEXT_COLOR = '#333333'
FONT_FAMILY = 'DejaVu Sans' # Robust sans-serif

# Column Width Ratios (Approximate relative weights)
# Standard Columns: Family, Species, Target, Results, Evidence, Refs, Usage%, UsageGen%, Rev
COL_WIDTHS = [0.12, 0.15, 0.12, 0.12, 0.18, 0.10, 0.07, 0.07, 0.07]

def clean_text(text):
    return text.replace('  ', ' ').strip()

def render_table(title, columns, data, filename):
    """
    Renders a list of rows as a matplotlib table image.
    """
    # Calculate height based on roughly estimated text wrapping
    # A base height plus some per-row factor
    
    # We need to figure out how tall each row is. 
    # For simplicity in this script, we'll use a fixed wide aspect ratio 
    # and let matplotlib auto-layout handle some of it, but manual wrapping is safer for "beautiful".
    
    # Manual constraints
    fig_width = 16 # Wide to fit 9 columns
    # Estimate height: Header + Rows. 
    # Assume average row takes 1 inch if dense, 0.5 if sparse.
    fig_height = 1.0 + (len(data) * 0.8) 
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')
    
    # Create the table
    table = ax.table(cellText=data,
                     colLabels=columns,
                     cellLoc='left',
                     loc='center',
                     colColours=[HEADER_COLOR] * len(columns),
                     cellColours=[[ROW_ODD_COLOR if i % 2 else ROW_EVEN_COLOR for _ in columns] for i in range(len(data))])

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 4) # Stretch height padding

    # formatting
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#dddddd')
        cell.set_linewidth(0.5)
        
        # Header Styling
        if row == 0:
            cell.set_text_props(weight='bold', color='white', ha='center', wrap=True)
            cell.set_height(0.15) # Taller header
        else:
            # Body Styling
            cell.set_text_props(color=TEXT_COLOR, wrap=True)
            # Custom height adjustment for dense text
            content_len = len(str(data[row-1][col]))
            if content_len > 100:
                cell.set_height(0.25) # Make tall rows taller
            elif content_len > 50:
                cell.set_height(0.18)

    # Title
    plt.title(title, pad=20, fontsize=14, weight='bold', color=HEADER_COLOR)
    
    # Save
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.2)
    print(f"Generated {output_path}")
    plt.close()

# --- DATA ---

cols_main = ["Nutraceutical Family", "Primary Species/Use Case", "Target/Mechanism", "Results", "Evidence Level & Takeaway", "Key Refs", "Use % (Segment)", "Use % (General)", "Est. Revenue"]

# II.1 Mobility
data_mobility = [
    ["Omega-3 (EPA/DHA)", "Dogs, cats (OA pain); Equine (adjunct)", "Adjunct to NSAIDs; Anti-inflammatory", "Pain scores, mobility, weight bearing", "A: Controlled canine OA data supports analgesia; adjunct usage.", "(Roush 2010)", "25-30%", "18-20%", "$1.2-1.4B"],
    ["UC-II Collagen", "Dogs (OA pain); Equine", "Adjunct to NSAIDs; Oral Tolerance", "Owner reported function, pain measures", "B to A: Positioning as 'maintenance + symptom reduction'.", "(Gupta 2009)", "10-15%", "3-5%", "$170-250M"],
    ["Eggshell Membrane", "Dogs (stiffness)", "Adjunct to NSAIDs", "Mobility questionnaires, stiffness", "B: Supports mobility; outcomes vary by formula.", "(Ragetly 2025)", "2-5%", "-", "$50-80M"],
    ["Green Lipped Mussel", "Dogs (joint function)", "Adjunct to NSAIDs", "Lameness, mobility scoring", "B: Supportive, but stabilized lipid processing is critical.", "(Carmona 2009)", "8-12%", "2-4%", "$170-200M"],
    ["Glucosamine/Chondroitin", "Dogs, Horses (Legacy)", "Adjunct to NSAIDs", "Mobility scores", "B to C: widely used but systematic reviews show mixed efficacy.", "(Vandeweerd 2012)", "45-55%", "12-15%", "$1.1-1.3B"],
    ["MSM", "Horses, Dogs", "Soreness recovery", "Comfort, lameness scoring", "C: Supportive equine evidence; thinner veterinary data.", "(Barshick 2025)", "15-20%", "4-6%", "$230-250M"],
    ["Boswellia/Curcumin", "Dogs, Horses", "Inflammation support", "Pain measures", "C: Plausible mechanism; acceptable secondary stack.", "(Aguado 2021)", "5-8%", "1-2%", "$100-150M"]
]

# II.2 Gut Health
data_gut = [
    ["Probiotics", "Dogs (Diarrhea); Swine/Poultry (Perform)", "Reduce antibiotics; Stabilize gut", "Stool quality, ADG, FCR", "A: Strong canine acute diarrhea data; context-dependent livestock ROI.", "(Shmalberg 2019)", "40-50%", "30-38%", "$5.6-7.5B"],
    ["Prebiotics (MOS/FOS)", "Broilers, Swine", "Pathogen binding", "FCR, morbidity, shedding", "B: Production-relevant meta-analytic support.", "(Hooge 2004)", "25-35%", "10-15%", "$500-800M"],
    ["Synbiotics", "Dogs (Shelters); Production", "Resilience, Diarrhea reduction", "Diarrhea incidence", "B: Controlled shelter work supports reduced diarrhea.", "(Rose 2017)", "~25%", "~8%", "$1.25B"],
    ["Postbiotics", "Piglets (Weaning)", "Enteric stability", "Gut morphology, growth", "B: Supports morphology/growth in piglets.", "(Zeng 2015)", "10-15%", "3-5%", "$0.2-1.2B"],
    ["Organic Acids", "Swine, Poultry", "Feed hygiene, pH modulation", "Microbial counts, FCR", "B: Broad base; 'toolbox' component.", "(Khan 2016)", "60-70%", "25-30%", "$10-12B"],
    ["Digestive Enzymes", "Poultry, Swine", "Digestibility (P, Protein)", "FCR, litter quality, P excretion", "A: Mature evidence for Phytase/Xylanase.", "(Selle 2007)", "80-90%", "3-5%", "$1.4-2.1B"]
]

# II.3 Immunity
data_immunity = [
    ["Beta-Glucans", "Aqua (Shrimp/Fish); Poultry", "Resilience, Mortality reduction", "Survival, immune markers", "B: Established immunostimulants in aquaculture.", "(Meena 2013)", "-", "-", "$38M"],
    ["Plasma / Ig-Fractions", "Piglets (Weaning)", "Reduce diarrhea, medication", "ADG, gut integrity", "B to A: Widely supported in early life nutrition.", "(Torrallardona 2010)", "-", "-", "$2.20B"],
    ["Nucleotides", "Poultry, Aqua", "Growth under stress", "Immune readouts", "B: Controlled studies support growth/immune parameters.", "(Abdel Moneim 2020)", "-", "-", "$622M"],
    ["Seaweed/Polysaccharides", "Ruminants, Monogastrics", "Oxidative stress, Immune support", "Metabolic indicators", "B to C: Variable endpoints but high volume.", "(Sweeney 2022)", "-", "-", "$4.46B"],
    ["Selenium / Vit E", "All Species", "Antioxidant defense", "Biomarkers, fertility", "B: Essential prevention of deficiency states.", "(Calik 2022)", "-", "-", "$280M"]
]

# II.4 Cognition
data_cognition = [
    ["MCTs (6.5% Diet)", "Senior Dogs", "Cognitive dysfunction (CCD)", "Cognitive tasks (DISHAA)", "A: Controlled evidence for brain energy metabolism.", "(Pan 2010)", "34.9%", "-", "$450M"],
    ["DHA", "Dogs, Cats", "Brain aging", "Cognitive measures", "B: Biologically strong; design-dependent outcomes.", "(Pan 2010)", "27.1%", "-", "$350M"],
    ["Antioxidant Blends", "Senior Dogs", "Oxidative stress", "Learning, memory tasks", "B to A: Strong literature base for antioxidant intervention.", "(Cotman 2002)", "23.3%", "-", "$300M"],
    ["SAMe", "Aging Animals", "Liver/Brain support", "Clinical signs", "C: Stronger liver data than cognition.", "(Reme 2008)", "7.8%", "-", "$100M"],
    ["Phosphatidylserine", "Senior Pets", "Cognition", "Behavior endpoints", "C: Limited veterinary-specific trials.", "(Finno 2020)", "1.2%", "-", "$15M"]
]

# II.5 Calming
data_calming = [
    ["L-Theanine", "Dogs, Cats", "Anxiety support", "Anxiety scales", "B: Supportive evidence, some heterogeneity.", "(Pike 2015)", "4.5%", "-", "$50M"],
    ["Alpha-Casozepine", "Dogs, Cats", "Stress modulation", "Behavior outcomes", "B: Controlled evidence supports calming.", "(Beata 2007)", "2.7%", "-", "$30M"],
    ["Tryptophan", "Dogs", "Behavior modulation", "Aggression/Stress", "B to C: Context matters; serotonin precursor.", "(DeNapoli 2000)", "7.3%", "-", "$80M"],
    ["Botanicals (Valerian...)", "Dogs, Cats, Horses", "Situational anxiety", "Behavioral outcomes", "C: Variable; safety review needed.", "(Robinson 2025)", "9.1%", "-", "$100M"],
    ["CBD/Hemp", "Dogs", "Pain/Anxiety", "Pain/Anxiety endpts", "C to B: Growing base, regulatory variance.", "(Mulder 2025)", "30.0%", "-", "$330M"],
    ["Multi-Complexes", "All Species", "Adjunct support", "Owner reported signs", "C: Depends on lead active.", "(Finno 2020)", "45.5%", "-", "$500M"]
]

# II.6 Performance
data_performance = [
    ["Phytase", "Poultry, Swine", "Phosphorus digestibility", "FCR, P Excretion", "A: Established standard of care.", "(Selle 2007)", "8.5%", "1.4%", "$600M"],
    ["Xylanase", "Poultry, Swine", "Fiber digestibility", "FCR, Litter quality", "A: Mature ROI logic.", "(Selle 2007)", "14.1%", "2.3%", "$1.0B"],
    ["Protease", "Poultry", "Protein utilization", "Digestibility", "A to B: Meta-analysis support.", "(Cowieson 2020)", "2.8%", "-", "$200M"],
    ["Yeast Culture", "Ruminants", "Rumen efficiency", "Milk yield / FCR", "B: Meta-analysis support.", "(Desnoyers 2009)", "28.2%", "4.6%", "$2.0B"],
    ["Protected Amino Acids", "Ruminants", "Nitrogen efficiency", "Yield, Milk Protein", "B: Mature technology.", "(Fleming 2019)", "16.9%", "2.8%", "$1.2B"]
]

# II.7 Niches
data_niches = [
    ["Derm: Omega-6", "Dogs, Cats", "Skin barrier", "Coat, pruritus scores", "B: Strong for barrier/deficiency.", "(Saevik 2004)", "6.8%", "-", "$120M"],
    ["Derm: Zinc Methionine", "Dogs", "Skin integrity", "Skin outcomes", "B to C: Supportive.", "(Finno 2020)", "10.0%", "-", "$175M"],
    ["Pigment: Astaxanthin", "Aqua", "Flesh color", "Color fan score", "B: Established economic necessity.", "(Shah 2016)", "77.1%", "-", "$1.35B"]
]

# II.8 Ectoparasite
data_ecto = [
    ["Natural Repellents", "Dogs", "Flea/Tick avoidance", "Bite incidence", "C: High variability; safety/regulatory risk.", "(Robinson 2025)", "55.0%", "-", "$550M"],
    ["Garlic", "Dogs", "Parasite control", "Counts", "C: Anecdotal; safety concerns.", "(Robinson 2025)", "4.0%", "-", "$40M"],
    ["Skin Barrier Stacks", "Dogs", "Flea Allergy Dermatitis", "Pruritus", "C: Defensible as derm support.", "(Finno 2020)", "15.0%", "-", "$150M"]
]

# II.9 Nutrigenomics
data_nutrigenomics = [
    ["Biomarker Validation", "Livestock, Premium Pet", "Defensibility/IP", "Biomarker movement", "B: Differentiation layer.", "(Asmelash 2018)", "17.5%", "-", "$613M"],
    ["Nrf2 Activators", "Multi-species", "Antioxidant narrative", "Oxidative markers", "C to B: Strong mechanism.", "(Deon 2025)", "5.7%", "-", "$200M"],
    ["Gut Integrity Tools", "Swine, Poultry", "Antibiotic alternative", "Lesion scores", "B to A: Strong ROI link.", "(Kiarie 2012)", "62.0%", "-", "$2.17B"]
]

# II.10 Delivery
cols_delivery = ["Technology", "Species", "Problem Solved", "Results/ROI", "Evidence & Takeaway", "Refs", "Use %", "Gen %", "Revenue"]
data_delivery = [
    ["Rumen Protection", "Ruminants", "Bypass rumen fermentation", "Biomass/Yield", "B: Mature for Amino Acids.", "(Fleming 2019)", "49.2%", "19.6%", "$3.80B"],
    ["Soft Chews", "Dogs, Cats", "Compliance / Palatability", "Repeat purchase", "Commercial Criticality.", "(Sirio 2026)", "31.7%", "12.6%", "$2.45B"],
    ["Aqua Coatings", "Aqua", "Nutrient leaching", "Biomass preservation", "B: Key for stability.", "(Hauton 2021)", "14.5%", "5.8%", "$1.12B"],
    ["Smart Boluses", "Cattle", "Disease detection", "Antibiotic reduction", "B: Enables precision.", "(smaXtec 2025)", "4.2%", "2.1%", "$2.58B"]
]

# II.11 Sustainability
cols_green = ["Wedge", "Species", "Additive Family", "Measurable KPI", "Evidence Level", "Refs", "Use % (Green)", "Use % (Gen)", "Revenue"]
data_green = [
    ["Methane Mitigation", "Ruminants", "Asparagopsis", "Methane reduction", "B: Large reductions; scaling hard.", "(Roque 2021)", "0.8%", "<0.1", "$25M"],
    ["Methane Mitigation", "Ruminants", "3-NOP", "Methane reduction", "A to B: Consistent ~30% reduction.", "(Hristov 2015)", "1.9%", "0.1%", "$60M"],
    ["Phosphorus Mgmt", "Monogastrics", "Phytase", "P excretion", "A: Established Standard.", "(Afsharmanesh 2023)", "20.7%", "1.5%", "$640M"],
    ["N Efficiency", "Ruminants", "AA / Urease inhibitors", "N excretion", "A: Mature tools.", "(IPCC 2021)", "60%+", "5%+", "$2.25B"]
]


if __name__ == "__main__":
    render_table("Table II.1: Mobility and Joint Health Targets", cols_main, data_mobility, "Figure_Table_II_1.png")
    render_table("Table II.2: Gut Health and Microbiome Targets", cols_main, data_gut, "Figure_Table_II_2.png")
    render_table("Table II.3: Immunity and Resilience Targets", cols_main, data_immunity, "Figure_Table_II_3.png")
    render_table("Table II.4: Cognitive Support Targets", cols_main, data_cognition, "Figure_Table_II_4.png")
    render_table("Table II.5: Calming and Behavioral Targets", cols_main, data_calming, "Figure_Table_II_5.png")
    render_table("Table II.6: Performance and Efficiency Targets", cols_main, data_performance, "Figure_Table_II_6.png")
    render_table("Table II.7: Special Niches Targets", cols_main, data_niches, "Figure_Table_II_7.png")
    render_table("Table II.8: Ectoparasite Defense Targets", cols_main, data_ecto, "Figure_Table_II_8.png")
    render_table("Table II.9: Nutrigenomics Targets", cols_main, data_nutrigenomics, "Figure_Table_II_9.png")
    render_table("Table II.10: Advanced Delivery Systems", cols_delivery, data_delivery, "Figure_Table_II_10.png")
    render_table("Table II.11: Sustainability Targets", cols_green, data_green, "Figure_Table_II_11.png")
