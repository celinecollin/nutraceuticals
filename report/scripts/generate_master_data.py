import pandas as pd
import xlsxwriter
import os

# --- 1. DEFINE ALL DATASETS ---

# Figure 13: Segmentation (Pareto)
data_seg = {
    'Segment': ['Spare No Expense', 'Value-Conscious', 'Basic Care'],
    'Households_Pct': [20, 50, 30],
    'Revenue_Pct': [48, 42, 10]
}
df_seg = pd.DataFrame(data_seg)
source_seg = "Source: Consumer Survey 2024; Internal ERP Data."

# Mobility Premiumization (Time Series) - Figure 15? (Based on context of mobility)
years = [2015, 2018, 2020, 2022, 2024, 2026, 2028, 2030]
data_mob = {
    'Year': years,
    'Generic Glucosamine': [70, 64, 60, 52, 45, 42, 38, 35],
    'UC-II Collagen': [5, 11, 15, 19, 25, 27, 28, 30],
    'Green Lipped Mussel': [15, 15, 15, 16, 17, 18, 19, 20],
    'Premium Combos': [10, 10, 10, 13, 13, 13, 15, 15]
}
df_mob = pd.DataFrame(data_mob)
source_mob = "Source: Market Reports (Euromonitor) & Projected Estimates."

# Risk Heatmap - Figure 20?
data_risk = {
    'Region': ['North America', 'Europe', 'Asia-Pacific', 'LATAM', 'Middle East'],
    'Regulatory': [4, 3, 5, 5, 6],
    'Scientific': [3, 4, 5, 6, 7],
    'Commercial': [5, 6, 4, 7, 8],
    'Macro': [3, 5, 6, 8, 7]
}
df_risk = pd.DataFrame(data_risk)
source_risk = "Source: Expert Interviews & Regional Risk Assessment Matrix."

# Internal Composition (Top 3 Drivers)
data_comp = {
    'Sector': ['Gut Health', 'Delivery', 'Immunity', 'Performance', 'Mobility', 'Sustainability', 'Nutrigenomics'],
    'Top_Ingredient': ['Probiotics', 'Rumen Prot.', 'Seaweed', 'Yeast Culture', 'Omega-3', 'N-Efficiency', 'Gut Infrastr.'],
    'Top_Share_%': [50, 35, 55, 29, 39, 67, 66],
    'Second_Ingredient': ['Enzymes', 'Smart Bolus', 'Plasma', 'Amino Acids', 'Glucosamine', 'P-Mgmt', 'Biomarkers'],
    'Second_Share_%': [13, 24, 27, 18, 36, 19, 19]
}
df_comp = pd.DataFrame(data_comp)
source_comp = "Source: R&D Pipeline Analysis 2025."

# Regulatory Timeline
data_time = {
    'Year': [2006, 2017, 2019, 2022, 2024, 2025],
    'Event': ['EU bans AGPs', 'US FDA VFD', 'EU Vet Meds Reg', 'EU bans Zinc Oxide', 'China AGP Tightening', 'UK Feed Reform'],
    'Impact_Level': ['High', 'High', 'Medium', 'High', 'High', 'Medium']
}
df_time = pd.DataFrame(data_time)
source_time = "Source: Official Regulatory Gazettes (EU, FDA, MOA China)."


# --- 2. INITIALIZE EXCEL WRITER ---
output_filename = 'Whitepaper_Master_Data.xlsx'
writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
workbook = writer.book

# --- 3. HELPER FUNCTION ---
def add_sheet(df, sheet_name, source_text, fig_filename):
    # Write Data
    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1, startcol=1)
    
    worksheet = writer.sheets[sheet_name]
    
    # Formatting
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#DCE6F1', 'border': 1})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(1, col_num + 1, value, header_fmt)
    
    worksheet.set_column(1, len(df.columns), 20) # Widen columns
    
    # Write Source
    source_fmt = workbook.add_format({'italic': True, 'font_color': '#555555'})
    worksheet.write(len(df) + 3, 1, source_text, source_fmt)
    
    # Insert Image
    # Define absolute path to figures directory
    figures_dir = '/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/figures'
    image_path = os.path.join(figures_dir, fig_filename)
    
    print(f"Attempting to insert image: {image_path}")
    
    if os.path.exists(image_path):
        try:
            worksheet.insert_image('H2', image_path, {'x_scale': 0.6, 'y_scale': 0.6})
            print(f"Successfully inserted {fig_filename}")
        except Exception as e:
            print(f"Error inserting image {fig_filename}: {e}")
            worksheet.write('H2', f"[Error inserting image: {e}]")
    else:
        print(f"Image not found: {image_path}")
        worksheet.write('H2', "[Image Not Found - Please check figures directory]")


# --- 4. EXECUTE WRITING ---

# Mappings (Data, Sheet Name, Source, Filename)
# Note: Filenames are based on what was found in the figures directory and user request
datasets = [
    (df_seg, 'Fig13_Segmentation', source_seg, 'Figure13_Pareto_With_Note.png'),
    (df_mob, 'Fig_Mobility', source_mob, 'Mobility_Premiumization_Fixed.png'),
    (df_risk, 'Fig_Risk_Heatmap', source_risk, 'Risk_Heatmap_BlackText.png'),
    (df_comp, 'Fig_Ingredients', source_comp, 'Internal_Composition_SmartFit_LargeFont.png'),
    (df_time, 'Fig_Timeline', source_time, 'Regulatory_Timeline_RightArrow.png')
]

for df, sheet_name, source, filename in datasets:
    add_sheet(df, sheet_name, source, filename)

# Close and Save
writer.close()
print(f"Success: '{output_filename}' generated with data, sources, and images.")
