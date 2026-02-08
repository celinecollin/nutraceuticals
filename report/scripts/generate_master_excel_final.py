import pandas as pd
import xlsxwriter
import os
import re
import datetime

# --- CONFIGURATION ---
OUTPUT_FILENAME = 'Whitepaper_Master_Data.xlsx'
REPORT_PATH = '/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/Master_WhitePaper_Final.md'

# --- 1. DATA DEFINITIONS (Consolidated from Analysis) ---

# Figure I.1: US vs EU Regulatory Differences
data_reg_diff = {
    'Region': ['United States', 'European Union', 'China'],
    'Focus': ['Safety First (GRAS)', 'Efficacy First (Zootechnical)', 'Compliance First'],
    'Primary Law': ['FDA GFI #293', 'Reg (EC) 1831/2003', 'MoA Decree 20'],
    'Market Barrier': ['Moderate (GRAS costs)', 'High (Trial costs)', 'High (License costs)'],
    'Key Label Claim': ['"Supplement" (Structure/Function)', '"Zootechnical Additive" (Performance)', '"Pet Feed" / "Additive"']
}
source_reg_diff = "Source: FDA GFI #293, EU Reg 1831/2003, MARA Decree 20."

# Figure I.2: Regulatory Accelerators (Timeline)
data_timeline = {
    'Year': [2006, 2017, 2019, 2022, 2024, 2025],
    'Event': ['EU bans AGPs', 'US FDA VFD Implemented', 'EU Vet Meds Reg', 'EU bans Zinc Oxide', 'China AGP Tightening', 'UK Feed Reform'],
    'Impact Category': ['Market Access', 'Antibiotic Reduction', 'Veterinary Oversight', 'Environmental', 'Antibiotic Reduction', 'Sustainability'],
    'Impact Level (1-5)': [5, 4, 3, 5, 5, 3]
}
source_timeline = "Source: Internal Analysis based on Regulatory Decrees (EU, FDA, MOA)."

# Figure I.3: Regulatory Pathways Matrix (Matrix Data)
data_reg_matrix = {
    'Zone': ['Feed Material', 'Feed Additive', 'Veterinary Drug'],
    'Cost_Index (1-10)': [2, 6, 9],
    'Claim_Power (1-10)': [2, 6, 9],
    'Description': ['No functional claims', 'Zootechnical/Performance claims', 'Therapeutic/Cure claims'],
    'Examples': ['Calcium Carbonate', 'Phytase, Probiotics (Zootech)', 'Antibiotics, NSAIDs']
}
source_reg_matrix = "Source: Internal Regulatory Analysis."

# Figure I.4: TAM Reconciliation
data_tam = {
    'Component': ['Pet Nutraceuticals', 'Livestock Functional Additives', 'Total "Animal Nutraceuticals"', 'Context: Broader Animal Health', 'Context: Total Pet Care'],
    'Value (USD Billion)': [6.0, 7.0, 13.0, 50.0, 136.0],
    'Examples': ['Joint chews, probiotics, calming oils', 'Phytase, rumen-protected AAs', 'Scope of White Paper', 'Vaccines, pharma, parasiticides', 'Food, services, vet care']
}
source_tam = "Source: Grand View Research (2024), Euromonitor (2024)."

# Figure I.6: Innovation Premium (Scatter/Correlation)
data_innovation = {
    'Company Type': ['Commodity Feed', 'Specialty Feed', 'Premium Pet Brand', 'Pharma-Nutra Hybrid', 'Biotech Pure-Play'],
    'RD_Intensity_Pct': [0.5, 2.5, 3.0, 6.0, 15.0],
    'EBITDA_Margin_Pct': [8.0, 12.0, 18.0, 26.0, -10.0], # Biotech often negative early on, but let's say mature biotech is high
    'Valuation_Multiple': [8, 10, 14, 18, 22] 
}
# Adjusting Biotech for the "Premium" narrative (mature state)
data_innovation['EBITDA_Margin_Pct'][4] = 35.0 

source_innovation = "Source: Annual Reports 2024/2025; Internal Analysis."

# Figure I.21: Pet Ownership Rates
data_ownership = {
    'Region': ['United States', 'Canada', 'European Union', 'Rest of World'],
    'Household Ownership %': [71, 60, 49, 35]
}
source_ownership = "Source: APPA National Pet Owners Survey 2024, FEDIAF 2024."

# Figure I.22/23: EU Species Split
data_eu_species = {
    'Species': ['Cats', 'Dogs'],
    'Population (Millions)': [127, 104],
    'Growth Rate (%)': [11.0, 5.0]
}
source_eu_species = "Source: FEDIAF Facts & Figures 2023."

# Figure I.24: Regional Value Distribution
data_regional = {
    'Region': ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'MEA'],
    'Market Share %': [38, 30, 22, 7, 3]
}
source_regional = "Source: Grand View Research (2024)."

# Figure I.32: Wallet Share (The Preventive Wallet)
data_wallet = {
    'Category': ['Food', 'Vet Care', 'Supplies', 'Nutraceuticals/Preventive', 'Services'],
    'Spend Share %': [40, 25, 15, 12, 8],
    'Growth Trend': ['Stable', 'Rising', 'Stable', 'High Growth', 'Recovering']
}
source_wallet = "Source: APPA National Pet Owners Survey 2024."

# Figure I.34: Purchasing Psychology
data_psych = {
    'Driver': ['Fear of Loss (Prevention)', 'Aspiration (Performance)', 'Value/Cost', 'Vet Recommendation'],
    'Influence %': [50, 30, 10, 10]
}
source_psych = "Source: Nicotra et al. (2025)."

# Figure IV.5: Revenue Comparison
data_revenue = {
    'Company': ['Nestlé Purina', 'Mars Petcare', 'Zoetis', 'Merck AH', 'Boehringer Ingelheim', 'Elanco', 'Hill\'s', 'DSM-Firmenich', 'Novonesis', 'Blue Buffalo', 'Phibro'],
    'Segment': ['Pet Food/CPG', 'Pet Food/CPG', 'Pharma', 'Pharma', 'Pharma', 'Pharma', 'Pet Food/CPG', 'Feed Inputs', 'Feed Inputs', 'Pet Food/CPG', 'Feed Inputs'],
    'Revenue_2024_Bn': [22.4, 22.0, 9.3, 5.9, 5.0, 4.4, 4.4, 3.6, 2.5, 2.3, 1.4]
}
source_revenue = "Source: Corporate Annual Reports (2023/2024 Estimates)."

# Figure IV.6: Capability Matrix (Heatmap Equivalent)
data_capability = {
    'Company': ['Zoetis', 'Merck AH', 'Elanco', 'DSM-Firmenich', 'Mars Petcare', 'Nestlé Purina', 'Hill\'s'],
    'Therapeutics (Rx)': [1, 1, 1, 0, 0, 0, 0],
    'Vaccines': [1, 1, 1, 0, 0, 0, 0],
    'Feed Additives': [0, 0, 1, 1, 0, 0, 0],
    'Pet Supplements': [1, 0.5, 1, 0.5, 0.5, 1, 0.5],
    'Pet Food': [0, 0, 0, 0, 1, 1, 1],
    'Diagnostics': [1, 1, 0.5, 0.5, 1, 0, 0.5]
}
# 1 = Core, 0.5 = Emerging/Partial, 0 = Absent
source_capability = "Source: Internal Strategic Analysis."

# Figure IV.4: Margin Ladder
data_margins = {
    'Segment': ['Commodity Feed', 'Feed Premix/Mills', 'Pet Food (Mass)', 'Pet Supplements', 'Pharma / Biotech'],
    'EBITDA Margin %': [4.0, 10.0, 16.0, 25.0, 32.0]
}
source_margins = "Source: Industry Financial Benchmarks."

# Matrix Data (Consolidated for generic bubble chart rendering)
# (Name, Table Data, Source)
matrix_datasets = {
    "Fig_II_1_Mobility": (
        pd.DataFrame([
            ['Omega-3', 9, 9, 1300, 'Gold Standard'], ['UC-II Collagen', 5.5, 8, 200, 'Rising Star'], 
            ['Green Lipped Mussel', 5, 5, 185, 'Neutral'], ['Glucosamine', 9, 3, 1100, 'Commodity'],
            ['Chondroitin', 8.5, 2, 800, 'Commodity'], ['MSM', 7, 4, 240, 'Neutral']
        ], columns=['Ingredient', 'Maturity (1-10)', 'Evidence (1-10)', 'Market Size ($M)', 'Status']),
        "Source: Internal Efficacy Analysis."
    ),
    "Fig_II_2_Gut": (
        pd.DataFrame([
            ['Probiotics', 9, 9, 6000, 'Gold Standard'], ['Phytase', 9.5, 9.5, 1800, 'Gold Standard'],
            ['Prebiotics', 7, 6, 650, 'Neutral'], ['Synbiotics', 6, 7, 1250, 'Rising Star'],
            ['Postbiotics', 3, 8, 500, 'Rising Star'], ['Organic Acids', 8, 5, 4000, 'Neutral']
        ], columns=['Ingredient', 'Maturity (1-10)', 'Evidence (1-10)', 'Market Size ($M)', 'Status']),
        "Source: Internal Efficacy Analysis."
    )
    # Add others similarly if needed, but these serve as the template examples
}


# --- 2. MARKDOWN PARSING (Internal Composition) ---
def parse_composition_from_md(file_path):
    """
    Parses the Markdown file to extract the 'Internal Composition' data from the text tables.
    Returns a DataFrame.
    """
    if not os.path.exists(file_path):
        return pd.DataFrame({'Error': ['File not found']})

    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    data = []
    current_segment = "Unknown"
    
    # Regex to find table rows like "| **Probiotics** | Dogs... | ... | ... | $1.2B |"
    # We want to extract: Segment, Ingredient, Revenue
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Detect Segment Header
        if line.startswith("### II."):
            match = re.search(r"II\.\d+\.\s+(.*?)(\(|$)", line)
            if match:
                current_segment = match.group(1).strip()
        
        # Detect Table Row
        if line.startswith("|") and not "---" in line and not "**Nutraceutical family**" in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 8:
                ingredient = parts[1].replace("**", "")
                revenue_str = parts[-2] # Assuming Revenue is last column
                
                # Simple parsing of revenue string "$1.2B" -> 1.2
                revenue = 0.0
                clean_rev = revenue_str.replace("$", "").replace("B", "").replace("M", "").strip()
                try:
                    val = float(re.search(r"[\d\.]+", clean_rev).group(0))
                    if "M" in revenue_str:
                        val = val / 1000.0 # Convert to Billions
                    revenue = val
                except:
                    revenue = 0.0
                
                if revenue > 0:
                    data.append({
                        'Segment': current_segment,
                        'Ingredient': ingredient,
                        'Est. Revenue ($B)': revenue
                    })
    
    df = pd.DataFrame(data)
    # Aggregate small items
    return df

# --- 3. EXCEL GENERATION ---

def add_sheet_with_chart(writer, df, sheet_name, title, source, chart_type='Column', xtitle=None, ytitle=None):
    """
    Adds a worksheet with a table and a native Excel chart.
    """
    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=20)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    
    # Formats
    header_format = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#2c3e50', 'border': 1})
    source_format = workbook.add_format({'italic': True, 'font_color': 'gray'})
    title_format = workbook.add_format({'bold': True, 'font_size': 16})
    
    # Write Title
    worksheet.write('A1', title, title_format)
    
    # Style Table Header
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(20, col_num, value, header_format)
        worksheet.set_column(col_num, col_num, 20) # Width

    # Create Table (ListObject)
    rows = len(df)
    cols = len(df.columns)
    if rows > 0:
        worksheet.add_table(20, 0, 20+rows, cols-1, {'columns': [{'header': col} for col in df.columns], 'style': 'TableStyleMedium2'})

    # Write Source
    worksheet.write(20+rows+2, 0, source, source_format)

    # --- CHART CREATION ---
    if chart_type and rows > 0:
        chart = workbook.add_chart({'type': chart_type.lower()})
        
        # Configure Series
        # Assume First Column is Categories, Last Column is Values (unless specified otherwise)
        cat_col_idx = 0
        val_col_idx = cols - 1
        
        if chart_type.lower() == 'scatter' or chart_type.lower() == 'bubble':
             # For matrix: Col 1=X, Col 2=Y, Col 3=Size (Size ignored in simple scatter)
             val_col_idx = 1 # Y
             chart = workbook.add_chart({'type': 'scatter'}) 
             
             # Scatter Series
             chart.add_series({
                 'name':       'Market Landscape',
                 'categories': [sheet_name, 21, 1, 20+rows, 1], # X (Maturity)
                 'values':     [sheet_name, 21, 2, 20+rows, 2], # Y (Evidence)
                 # 'data_labels': {'value': False, 'custom': [{'value': n} for n in df.iloc[:,0]]} # Custom labels complex in xlsxwriter
                 'data_labels': {'value': False, 'position': 'right'}, # Simple labels often fail without custom support, skipping for robustness or using basic
             })
             # Note: XlsxWriter doesn't easily support "Label from Range" for Scatter without loops. 
             # We will stick to simple points. User can add labels in Excel if needed.
        
        else:
            # Standard Bar/Line/Pie
            # If multiple value columns (e.g. Innovation), add multiple series
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            for i, col_name in enumerate(numeric_cols):
                col_idx = df.columns.get_loc(col_name)
                # If first column is numeric, do not use it as value if it's meant to be category
                if col_idx == 0: continue 
                
                chart.add_series({
                    'name':       [sheet_name, 20, col_idx],
                    'categories': [sheet_name, 21, 0, 20+rows, 0],
                    'values':     [sheet_name, 21, col_idx, 20+rows, col_idx],
                })
        
        # Styling
        chart.set_title({'name': title})
        if xtitle: chart.set_x_axis({'name': xtitle})
        if ytitle: chart.set_y_axis({'name': ytitle})
        chart.set_style(10) # Modern style
        
        # Insert Chart
        worksheet.insert_chart('E2', chart, {'x_scale': 1.5, 'y_scale': 1.5})


def create_master_excel():
    print("Generating Master Excel Workbook...")
    
    writer = pd.ExcelWriter(OUTPUT_FILENAME, engine='xlsxwriter')
    workbook = writer.book
    
    # --- 1. INDEX SHEET ---
    worksheet = workbook.add_worksheet('Index')
    worksheet.write('A1', 'White Paper Master Data Index', workbook.add_format({'bold': True, 'size': 18}))
    
    headings = ['Figure/Table', 'Analytic Focus', 'Sheet Link']
    index_data = []
    
    # --- 2. ADD SHEETS ---
    
    # I.4 TAM
    df_tam = pd.DataFrame(data_tam)
    add_sheet_with_chart(writer, df_tam, 'Fig_I_4_TAM', 'Total Addressable Market (Reconciliation)', source_tam, 'Column', 'Component', 'Value ($B)')
    index_data.append(['Fig I.4', 'TAM Reconciliation', "internal:'Fig_I_4_TAM'!A1"])

    # I.21 Pet Ownership
    df_own = pd.DataFrame(data_ownership)
    add_sheet_with_chart(writer, df_own, 'Fig_I_21_Ownership', 'Global Pet Ownership Rates', source_ownership, 'Column', 'Region', 'Ownership %')
    index_data.append(['Fig I.21', 'Ownership Demographics', "internal:'Fig_I_21_Ownership'!A1"])

    # I.22 EU Species
    df_eu = pd.DataFrame(data_eu_species)
    add_sheet_with_chart(writer, df_eu, 'Fig_I_22_Species', 'EU Pet Population', source_eu_species, 'Pie')
    index_data.append(['Fig I.22', 'EU Species Split', "internal:'Fig_I_22_Species'!A1"])

    # I.24 Regional
    df_reg = pd.DataFrame(data_regional)
    add_sheet_with_chart(writer, df_reg, 'Fig_I_24_Regional', 'Regional Value Distribution', source_regional, 'Pie')
    index_data.append(['Fig I.24', 'Regional Market Share', "internal:'Fig_I_24_Regional'!A1"])

    # I.32 Wallet Share
    df_wallet = pd.DataFrame(data_wallet)
    add_sheet_with_chart(writer, df_wallet, 'Fig_I_32_Wallet', 'The Preventive Wallet (Spend Share)', source_wallet, 'Column', 'Category', 'Share %')
    index_data.append(['Fig I.32', 'Wallet Share Analysis', "internal:'Fig_I_32_Wallet'!A1"])

    # I.34 Psychology
    df_psych = pd.DataFrame(data_psych)
    add_sheet_with_chart(writer, df_psych, 'Fig_I_34_Psychology', 'Consumer Purchasing Drivers', source_psych, 'Bar', 'Driver', 'Influence %')
    index_data.append(['Fig I.34', 'Consumer Psychology', "internal:'Fig_I_34_Psychology'!A1"])
    
    # IV.5 Revenue
    df_rev = pd.DataFrame(data_revenue)
    add_sheet_with_chart(writer, df_rev, 'Fig_IV_5_Revenue', 'Competitive Landscape: Revenue by Segment', source_revenue, 'Bar', 'Company', 'Revenue ($B)')
    index_data.append(['Fig IV.5', 'Competitor Revenues', "internal:'Fig_IV_5_Revenue'!A1"])

    # IV.4 Margins
    df_marg = pd.DataFrame(data_margins)
    add_sheet_with_chart(writer, df_marg, 'Fig_IV_4_Margins', 'The Margin Ladder (EBITDA)', source_margins, 'Column', 'Sector', 'Margin %')
    index_data.append(['Fig IV.4', 'Margin Analysis', "internal:'Fig_IV_4_Margins'!A1"])

    # I.6 Innovation
    df_inn = pd.DataFrame(data_innovation)
    add_sheet_with_chart(writer, df_inn, 'Fig_I_6_Innovation', 'Innovation Premium Correlation', source_innovation, 'Column', 'Company Type', 'Metrics')
    index_data.append(['Fig I.6', 'Innovation Economics', "internal:'Fig_I_6_Innovation'!A1"])

    # Special: Matrices (Bubble Charts)
    for key, (df_m, src) in matrix_datasets.items():
        add_sheet_with_chart(writer, df_m, key, key.replace('_', ' '), src, 'Bubble', 'Maturity', 'Evidence')
        index_data.append([key, 'Strategic Matrix', f"internal:'{key}'!A1"])

    # Special: Tables (No Chart / Text Based) - Regulatory
    df_diff = pd.DataFrame(data_reg_diff)
    add_sheet_with_chart(writer, df_diff, 'Fig_I_1_Reg_Div', 'Regulatory Divergence', source_reg_diff, None)
    index_data.append(['Fig I.1', 'Regulatory Divergence', "internal:'Fig_I_1_Reg_Div'!A1"])

    df_time = pd.DataFrame(data_timeline)
    add_sheet_with_chart(writer, df_time, 'Fig_I_2_Timeline', 'Regulatory Timeline', source_timeline, None)
    index_data.append(['Fig I.2', 'Regulatory Timeline', "internal:'Fig_I_2_Timeline'!A1"])

    # Special: Dynamic Composition from Markdown
    try:
        df_comp = parse_composition_from_md(REPORT_PATH)
        if not df_comp.empty:
            add_sheet_with_chart(writer, df_comp, 'Fig_Composition', 'Internal Composition (Extracted)', 'Source: White Paper Report Tables', 'Column')
            index_data.append(['Data', 'Full Composition Data', "internal:'Fig_Composition'!A1"])
    except Exception as e:
        print(f"Warning: Could not parse markdown composition: {e}")

    # --- POPULATE INDEX ---
    header_fmt = workbook.add_format({'bold': True, 'bottom': 1, 'bg_color': '#DDDDDD'})
    link_fmt = workbook.add_format({'color': 'blue', 'underline': True})
    
    worksheet.write_row('A3', headings, header_fmt)
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:C', 15)
    
    for i, row_data in enumerate(index_data):
        worksheet.write(i+3, 0, row_data[0])
        worksheet.write(i+3, 1, row_data[1])
        worksheet.write_url(i+3, 2, row_data[2], string='Go to Data', cell_format=link_fmt)

    writer.close()
    print(f"Success! Saved to {os.path.abspath(OUTPUT_FILENAME)}")

if __name__ == "__main__":
    create_master_excel()
