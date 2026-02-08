
import re

# File paths
INPUT_FILE = "/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/Master_WhitePaper_Final.md"
# We will write to the same file, but strictly it's safer to write to a temp one first or just overwrite if confident.
# For this task, I'll overwrite as I will verify immediately.

# The Master Plan: Mapping New ID -> {ImageFile, TriggerPhrase, NewCaption}
# Note: The TriggerPhrase must be unique enough to find the insertion point.
# "ImageFile" will be used to harvest the "Source" line from the original text before deleting it.

FIGURE_MAP = [
    {
        "id": 1,
        "filename": "Table_US_vs_EU.png",
        "trigger": "navigating the stark divergence between the US focus on Safety (GRAS) and the EU mandate for Efficacy (Zootechnical).",
        "caption": "Regulatory Divergence creates structural barriers to entry for non-compliant actors."
    },
    {
        "id": 2,
        "filename": "Timeline_Regulations.png",
        "trigger": "Two seismic regulatory events have reshaped the competitive landscape, transforming nutraceuticals from discretionary additives into non-negotiable sanitary infrastructure",
        "caption": "Regulatory accelerators like AGP bans have historically driven volume adoption."
    },
    {
        "id": 3,
        "filename": "Figure_I_3_Regulatory_Matrix.png",
        "trigger": "A product's regulatory pathway determines its pricing power",
        "caption": "Regulatory pathways dictate unit economics and allowable claims."
    },
    {
        "id": 4,
        "filename": "Figure_TAM_Reconciliation.png",
        "trigger": "This strict scoping reveals a **$13 billion** high-quality revenue pool comprising **Pet Supplements (~$6B)** and **Livestock Functional Additives (~$7B)**.",
        "caption": "Market reconciliation excludes commodities to define the investable high-value universe."
    },
    {
        "id": 5,
        "filename": "Matrix_Species_Functional.png",
        "trigger": "## I.2. Economic Physics: Clinical Evidence is the Primary Driver of Pricing Power", # Placing right before this section as it summarizes section I.1/Transition
        "placement": "before", # Special flag to place before the line if needed, but default is after. Let's stick to "follow paragraph". 
        # Actually plan says: "End of 'Defining the Investable Universe'". The last sentence is the one used in Figure 4 trigger. 
        # Let's use the start of I.2 as the anchor and insert BEFORE it.
        "caption": "Functional architecture maps biological needs to commercial opportunities."
    },
    {
        "id": 6,
        "filename": "Figure_II_0_1_Innovation_Matrix.png",
        "trigger": "Financial data (2024/2025) confirms that companies investing **>5% of revenue in R&D** and publishing **Clinical Data** command superior EBITDA margins (>25%) versus traditional feed players (<10%)",
        "caption": "R&D intensity correlates directly with EBITDA margin expansion/premium."
    },
    {
        "id": 7,
        "filename": "Figure_II_0_2_Market_Bifurcation.png",
        "trigger": "Here, R&D is a **Defensive Necessity** to protect market share.",
        "caption": "Structural bifurcation splits the market into Emotional (Pet) and ROI (Livestock) economies."
    },
    {
        "id": 8,
        "filename": "Figure_II_1_Matrix.png",
        "trigger": "low-dose, immune-modulating collagens offer superior compliance and validated pain reduction.",
        "caption": "Efficacy levels in Mobility define market positioning and pricing power."
    },
    {
        "id": 9,
        "filename": "Figure_II_2_Matrix.png",
        "trigger": "proving that bio-efficacy eventually becomes a volume standard.",
        "caption": "Gut Health strategy shifts from generic digestion to precision microbiome modulation."
    },
    {
        "id": 10,
        "filename": "Figure_II_3_Matrix.png",
        "trigger": "In this sector, efficacy is measured by survival rates and reduction in veterinary interventions.",
        "caption": "Immunity solutions build biological resilience for the post-antibiotic era."
    },
    {
        "id": 11,
        "filename": "Figure_II_4_Matrix.png",
        "trigger": "This category represents the purest play on the \"Life Extension\" thesis.",
        "caption": "Cognitive support monetizes the Silver Economy via neuro-preservation."
    },
    {
        "id": 12,
        "filename": "Figure_II_5_Matrix.png",
        "trigger": "L-Theanine are driving growth by offering verifiable calmness without the pharmaceutical hangover.",
        "caption": "Non-sedative anxiolysis replaces pharmacological interventions in behavior management."
    },
    {
        "id": 13,
        "filename": "Figure_II_6_Matrix.png",
        "trigger": "minimizing metabolic waste—a critical value proposition as feed costs rise.",
        "caption": "Enzymes and yeast cultures drive Feed Conversion Ratios (FCR) in livestock."
    },
    {
        "id": 14,
        "filename": "Figure_II_7_Matrix.png",
        "trigger": "proving that efficacy that can be *seen* commands a premium.",
        "caption": "Visual health attributes like pigmentation and dermatology command functional premiums."
    },
    {
        "id": 15,
        "filename": "Figure_II_8_Matrix.png",
        "trigger": "trading absolute efficacy for safety appeal",
        "caption": "Safety appeal drives the adoption of natural repellents over chemical actives."
    },
    {
        "id": 16,
        "filename": "Figure_II_9_Matrix.png",
        "trigger": "creating a \"Moat of Data\" around natural ingredients.",
        "caption": "Gene-expression data constructs a defensible moat of validation around ingredients."
    },
    {
        "id": 17,
        "filename": "Figure_II_10_Matrix.png",
        "trigger": "proving that the format is as valuable as the active.",
        "caption": "Advanced delivery formats ensure bioavailability and maximize compliance."
    },
    {
        "id": 18,
        "filename": "Figure_II_11_Matrix.png",
        "trigger": "with **Methane Mitigation** (3-NOP) emerging as a regulatory imperative.",
        "caption": "Sustainability metrics like methane reduction are becoming non-negotiable procurement specs."
    },
    {
        "id": 19,
        "filename": "Figure1_Pet_Ownership.png",
        "trigger": "forecast to double to **~$10.5B by 2030**. Growth here is decoupled from volume; it is driven by **Premiumization**, where innovation creates new pricing tiers.",
        "caption": "Developed markets prioritize 'Value over Volume' in pet ownership trends."
    },
    {
        "id": 20,
        "filename": "Figure2_EU_Pet_Pop.png",
        "trigger": "The cat segment, growing at **+11%**, outpaces the dog segment due to urbanization constraints",
        "caption": "European demographics show a structural dominance of the feline segment."
    },
    {
        "id": 21,
        "filename": "Figure3_EU_Growth.png",
        "trigger": "France and Germany act as the twin engines of this high-value, pharmacy-led market.",
        "caption": "Feline segment growth outpaces canine due to urbanization constraints."
    },
    {
        "id": 22,
        "filename": "Figure4_Regional_Market.png",
        "trigger": "creating a specialized demand for stress and urinary health solutions in dense urban environments.",
        "caption": "APAC emerging as the primary volume engine for the next decade."
    },
    {
        "id": 23,
        "filename": "Figure5_Probiotics_Share.png",
        "trigger": "Poultry absorbs the majority of the **$6.8B feed additive** spend.",
        "caption": "Probiotics volume share reflects the dominance of poultry and swine sectors."
    },
    {
        "id": 24,
        "filename": "Figure6_Poultry_HPAI.png",
        "trigger": "frequent disease outbreaks (HPAI) have engaged a permanent demand for immune-modulating additives",
        "caption": "Disease outbreaks act as catalysts for immune-modulating additive demand."
    },
    {
        "id": 25,
        "filename": "Figure7_Swine_Decline.png",
        "trigger": "forcing a pivot to \"Quality over Quantity\" strategies where efficiency tools (enzymes) are mandatory to survive thin margins.",
        "caption": "Regulatory pressures drive structural contraction in Western swine herds."
    },
    {
        "id": 26,
        "filename": "Figure8_Cattle_Inventory.png",
        "trigger": "The market is shrinking in headcount but expanding in value-per-head.",
        "caption": "Western de-ruminization shifts value from herd size to efficiency-per-head."
    },
    {
        "id": 27,
        "filename": "Figure9_Livestock_Trends.png",
        "trigger": "**Western Contraction** driven by climate policy vs. **Global Expansion** driven by protein demand.", # Better trigger for general trends
        "caption": "Global protein production shifts favor poultry and aquaculture over ruminants."
    },
    {
        "id": 28,
        "filename": "Figure11_Aquaculture_Production.png",
        "trigger": "The **$250M Probiotics** market in aqua is non-discretionary; it is the biological life-support system for high-density RAS (Recirculating Aquaculture Systems).",
        "caption": "The 'Blue Transformation' drives industrialization and functional additive needs in aqua."
    },
    {
        "id": 29,
        "filename": "Figure14_Psychology.png",
        "trigger": "**\"Fear of Loss\" (50%)** outweighs \"Aspiration\" (30%).",
        "caption": "Purchasing psychology is driven more by the fear of loss than aspirational health."
    },
    {
        "id": 30,
        "filename": "Figure11_Formats.png",
        "trigger": "**Pet Owners Buy \"Fear Reduction\":**", # Wait, 30 is Palatability. 
        # Plan says: Move text to be descriptive. 
        "trigger": "Format Strategy: Palatability Dictates Compliance",
        "caption": "Palatability and format dictate compliance, which is a key efficacy driver."
    },
    {
        "id": 31,
        "filename": "Figure12_Wallet.png",
        "trigger": "supplements are now considered essential maintenance, not discretionary luxuries.",
        "caption": "Nutraceuticals have captured a dominant share of the preventive care wallet."
    },
    {
        "id": 32,
        "filename": "Figure13_Segmentation.png",
        "trigger": "For a proactive US pet owner spending **$1,500/year**", 
        "caption": "High-spending households drive the majority of revenue in the pet wellness category."
    },
    {
        "id": 33,
        "filename": "Figure15_Mobility_Evo.png",
        "trigger": "expanding the total category value even as volume growth stabilizes.",
        "caption": "Category premiumization evolves from generic ingredients to IP-backed solutions."
    },
    {
        "id": 34,
        "filename": "Figure16_Senior_Growth.png",
        "trigger": "By initiating cognitive and joint support earlier, brands convert a 3-year geriatric purchase cycle into a 7-year wellness regimen.",
        "caption": "Determining validity of 'Pre-Senior' segment expands Customer Lifetime Value."
    },
    {
        "id": 35,
        "filename": "Figure17_Value_Chain.png",
        "trigger": "Generic commodity suppliers are trapped in low-margin (5-12%) volatility.",
        "caption": "Margin capture shifts upstream to IP holders and downstream to specialized CDMOs."
    },
    {
        "id": 36,
        "filename": "Figure18_Channel_Economics.png",
        "trigger": "While DTC looks attractive, customer acquisition costs compress margins to **20-25%**.",
        "caption": "Channel economics favor omnichannel dominance but penalize pure-play DTC."
    },
    {
        "id": 37,
        "filename": "Figure19_Value_Waterfall.png",
        "trigger": "The value chain is not a monolith; it is split between the \"Speed\" of Pet/Consumer and the \"Scale\" of Livestock/Industrial models.", # Trigger for waterfall
        "caption": "Pricing power erodes as products move from IP owners to generic retailers."
    },
    {
        "id": 38,
        "filename": "Figure20_Risk_Reward.png",
        "trigger": "This \"Cradle-to-Grave\" monetization denies competitors access to the veterinary channel.",
        "caption": "Strategic categorization defines the risk-reward profile for market entrants."
    },
    {
        "id": 39,
        "filename": "Figure21_Pharma_Funnel.png",
        "trigger": "Major incumbents (Zoetis, Elanco) use nutraceuticals strategically as a \"Customer Acquisition Funnel\"",
        "caption": "Incumbents utilize nutraceuticals as a low-cost acquisition funnel for future banking."
    },
    {
        "id": 40,
        "filename": "Figure_MA_Matrix.png",
        "trigger": "Titans are paying **\"Time-to-Market Premiums\"** to acquire de-risked, clinically validated assets rather than building from scratch.",
        "caption": "M&A valuation matrix favors de-risked assets over internal R&D development."
    }
]

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def clean_figures(content, figure_map):
    # Map of filename -> source_text
    sources = {}
    
    # Regex to find figures blocks
    # Format typically:
    # **Figure I.1: Title**
    # ![Alt](path)
    # *Source: ...*
    
    # We want to capture the source line for each filename to preserve it.
    # Structure might vary slightly, so we iterate line by line to build extracting logic.
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    # Build a quick lookup set
    filenames = set(f['filename'] for f in figure_map)
    
    while i < len(lines):
        line = lines[i]
        
        # Check if line contains an image from our list
        img_match = re.search(r'!\[.*?\]\((.*?)\)', line)
        if img_match:
            path = img_match.group(1)
            # Normalize path (sometimes it has figures/ prefix)
            fname = path.split('/')[-1]
            
            if fname in filenames:
                # This is one of our target figures.
                # Look ahead for Source
                source_line = ""
                # Look up to 2 lines ahead for source
                for offset in range(1, 3):
                    if i + offset < len(lines) and lines[i+offset].strip().startswith('*Source'):
                        source_line = lines[i+offset].strip()
                        break
                
                # Store source
                sources[fname] = source_line
                
                # Now we need to remove this block.
                # The block might include a preceding "**Figure ...**" line
                # Look behind 1-2 lines
                start_remove = i
                if i > 0 and lines[i-1].strip().startswith('**Figure'):
                    start_remove = i - 1
                
                # Valid lines to keep are BEFORE start_remove
                # But we might have already added them to new_lines?
                # No, we are building new_lines as we go.
                
                # We need to pop the previous line if it was the Figure title
                if len(new_lines) > 0 and new_lines[-1].strip().startswith('**Figure') and (i - start_remove >= 1):
                   new_lines.pop()

                # Skip the Source line if found
                end_remove = i
                found_source = False
                for offset in range(1, 3):
                    if i + offset < len(lines) and lines[i+offset].strip().startswith('*Source'):
                        end_remove = i + offset
                        found_source = True
                        break
                
                i = end_remove + 1
                continue

        new_lines.append(line)
        i += 1
        
    return '\n'.join(new_lines), sources

def insert_new_figures(content, figure_map, sources):
    
    final_content = content
    
    # Sort map by ID so we don't mess up if multiple insertions happen? 
    # Actually, python string replace is not good for multiple inserts as offsets shift.
    # Better to split the string by trigger? 
    # Or just replace trigger with trigger + \n\nFIGURE
    
    summary_table = []
    
    for item in figure_map:
        fname = item['filename']
        trigger = item['trigger']
        new_id = item['id']
        caption = item['caption']
        
        # Construct new block
        # Check if we have a source captured, else use generic
        src = sources.get(fname, "*Source: Internal Analysis*") 
        
        # Check if image path needs 'figures/' prefix
        # In the original file they were 'figures/Filename.png'
        # We should probably keep that relative path
        img_path = f"figures/{fname}"
        
        block = f"\n\n**Figure {new_id}: {caption}**\n![{caption}]({img_path})\n{src}\n"
        
        if item.get('placement') == 'before':
             # Insert before trigger
             if trigger not in final_content:
                 print(f"WARNING: Trigger not found for Figure {new_id}: '{trigger[:30]}...'")
             final_content = final_content.replace(trigger, block + "\n" + trigger)
        else:
             # Insert after trigger
             if trigger not in final_content:
                 # fuzzy match? 
                 # Try removing markdown bold **
                 clean_trigger = trigger.replace('**', '')
                 if clean_trigger in final_content:
                     trigger = clean_trigger
                 else:
                     print(f"WARNING: Trigger not found for Figure {new_id}: '{trigger[:30]}...'")
                     
             final_content = final_content.replace(trigger, trigger + block)

        summary_table.append(f"| {fname} | Figure {new_id} | {caption} |")
        
    return final_content, summary_table

def update_references(content, figure_map):
    # This is the tricky part. 
    # The user wants "Standardized format in parentheses, such as (see Figure 1)"
    # We need to find old references.
    # Old references look like: (see Figure I.1), (see Figure 2), see Figure I.4, etc.
    
    # We can try to replace them based on the OLD ID if we knew it.
    # But we didn't map Old ID explicitly in the script, only implicitly by filename in the plan table?
    # Actually the plan has "Original File".
    # We can rely on the fact that we are placing Figure X right after its mention.
    # So if there is a "(see Figure ...)" right before where we placed Figure X, we should update it to (see Figure X).
    
    # Alternative:
    # Just generic replace all `(see Figure .*?)` with a placeholder `(see Figure ???)` 
    # and then assume they are in order? No, unsafe.
    
    # Better:
    # Use the triggers!
    # The trigger text often contains the reference " (see Figure I.2)" or similar.
    # Since we are inserting the figure right after the trigger, we can modify the trigger text provided in the map
    # to include the NEW reference.
    
    # Strategy:
    # 1. Update the references WITHIN the triggers in our loop.
    pass # logic will be inside the loop
    
    return content

# Main Execution Flow

content = read_file(INPUT_FILE)

# 1. Clean old figures
clean_content, sources = clean_figures(content, FIGURE_MAP)

# 2. Insert new figures AND update their references in the trigger text
final_content = clean_content
summary_rows = []

for item in FIGURE_MAP:
    fname = item['filename']
    trigger = item['trigger']
    new_id = item['id']
    caption = item['caption']
    
    # Look for reference in trigger
    # Regex to find (see Figure ...) or (Figure ...) inside the trigger text
    # e.g. "market... (see Figure I.2):"
    
    updated_trigger = trigger
    
    # Pattern: (see Figure X) or (refer to Figure X) or (Figure X)
    # We want to force format "(see Figure X)"
    
    # Check if trigger has a reference
    ref_match = re.search(r'\((see |refer to )?Figure.*?\)', updated_trigger, re.IGNORECASE)
    if ref_match:
        # Replace it
        updated_trigger = re.sub(r'\((see |refer to )?Figure.*?\)', f'(see Figure {new_id})', updated_trigger, flags=re.IGNORECASE)
    else:
        # If no reference exists in trigger, check if we should add one?
        # User said "Update all 'figure calls' within the prose." 
        # If the trigger didn't have one, maybe it's not needed, or maybe it was just outside the trigger snippet.
        pass

    # Now replace the OLD trigger in the content with the NEW trigger (with updated ref) -> Then add figure
    # BUT wait, the clean_content still has the OLD trigger.
    # We need to find the OLD trigger in clean_content.
    
    # Issue: The `trigger` string in my map might contain markdown `**` which might be slightly different or stripped.
    # I'll try to match exact first.
    
    found_trigger = False
    
    # Try exact match
    if trigger in final_content:
        final_content = final_content.replace(trigger, updated_trigger)
        found_trigger = True
    else:
        # Try finding it without bold markers
        clean_trig = trigger.replace('**', '')
        if clean_trig in final_content:
            final_content = final_content.replace(clean_trig, updated_trigger)
            trigger = clean_trig # update so insertion works
            found_trigger = True
    
    if not found_trigger:
        print(f"Skipping ref update for Figure {new_id} - text not matched exactly.")
        # Proceed with insertion using the original finding method
    
    # Now Insert Figure Block
    src = sources.get(fname, "*Source: Internal Analysis*")
    img_path = f"figures/{fname}"
    block = f"\n\n**Figure {new_id}: {caption}**\n![{caption}]({img_path})\n{src}\n"
    
    if item.get('placement') == 'before':
        final_content = final_content.replace(updated_trigger, block + "\n" + updated_trigger)
    else:
        final_content = final_content.replace(updated_trigger, updated_trigger + block)

    summary_rows.append(f"| {fname} | Figure {new_id} | {caption} |")


# 3. Last sweep for any remaining unformatted references?
# Iterate 1..40 and ensure (see Figure X) is compliant?
# Actually script above only updates references if they were IN the trigger.
# Many references might be outside the trigger string (e.g. prev sentence).
# I should do a regex pass for `Figure I.X` and `Figure II.X` to warn or try to fix.
# But mapping is hard without context.
# However, I have logic. 
# Figure I.1 -> Figure 1
# Figure I.2 -> Figure 2
# ...
# If I assume the user's current numbering "I.1, I.2" generally maps to my new order, I could try. 
# But the reordering is significant.
# E.g. Figure I.21 (Pet Ownership) moved to Figure 19.
# Figure I.3 became Figure 3.
# The previous document had I.1, I.2... up to I.41?
# It's safest to manually check the diff or rely on my trigger-based updates.

# Add summary table at the end
final_content += "\n\n# Summary of Figure Adjustments\n\n"
final_content += "| Original File | New Number | Key Takeaway |\n| :--- | :--- | :--- |\n"
final_content += "\n".join(summary_rows)

print(f"Write updated content to {INPUT_FILE}")
write_file(INPUT_FILE, final_content)

