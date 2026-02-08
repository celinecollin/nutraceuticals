import pandas as pd
import xlsxwriter
import os

# --- 1. DEFINE DATASETS ---

# FIG 1: Mobility (Stacked Area)
df_mobility = pd.DataFrame({
    'Year': [2015, 2018, 2020, 2022, 2024, 2026, 2028, 2030],
    'Generic Glucosamine': [70, 64, 60, 52, 45, 42, 38, 35],
    'UC-II Collagen': [5, 11, 15, 19, 25, 27, 28, 30],
    'Green Lipped Mussel': [15, 15, 15, 16, 17, 18, 19, 20],
    'Premium Combos': [10, 10, 10, 13, 13, 13, 15, 15]
})
src_mobility = "Source: Euromonitor, Market Projection Model 2030."

# FIG 2: Internal Composition (Stacked Bar)
df_composition = pd.DataFrame({
    'Sector': ['Gut Health', 'Delivery', 'Immunity', 'Performance', 'Mobility', 'Sustainability', 'Nutrigenomics', 'Niches', 'Cognition', 'Calming', 'Ectoparasite'],
    'Top 1': [50, 35, 55, 29, 39, 67, 66, 77, 35, 46, 74],
    'Top 2': [13, 24, 27, 18, 36, 19, 19, 10, 27, 30, 20],
    'Top 3': [9, 23, 8, 15, 7, 8, 9, 7, 23, 9, 6],
    'Others': [28, 18, 10, 38, 18, 6, 6, 6, 15, 15, 0]
})
src_composition = "Source: R&D Pipeline Analysis; Ingredient Supplier Interviews."

# FIG 3: Risk Heatmap (Data Only for Formatting)
df_risk = pd.DataFrame({
    'Risk Factor': ['Regulatory', 'Scientific', 'Commercial', 'Currency'],
    'North America': [4, 3, 5, 3],
    'Europe': [3, 4, 6, 5],
    'Asia-Pacific': [5, 5, 4, 6],
    'LATAM': [5, 6, 7, 8],
    'Middle East': [6, 7, 8, 7]
})
src_risk = "Source: Global Risk Matrix 2025."

# FIG 4: Segmentation (Pareto)
df_segmentation = pd.DataFrame({
    'Segment': ['Premium (Spare No Expense)', 'Value (Pragmatic)', 'Basic (Price Sensitive)'],
    'Market Share (%)': [20, 50, 30],
    'Revenue Contribution (%)': [48, 42, 10]
})
src_seg = "Source: Consumer Survey N=2,500."

# FIG 5, 6, 7: Conceptual Data (Timeline, Venn, Tradeoff)
df_timeline = pd.DataFrame({'Year': [2006, 2017, 2019, 2022, 2024, 2025], 'Event': ['EU Bans AGP', 'FDA VFD', 'EU Vet Meds', 'Zinc Ban', 'China Tightening', 'UK Reform']})
df_venn = pd.DataFrame({'Circle': ['Pharma', 'Nutrition', 'Preventative'], 'Definition': ['Curative', 'Feed', 'Wellness']})
df_tradeoff = pd.DataFrame({'Stage': ['Material', 'Additive', 'Drug'], 'Cost': ['Low', 'Med', 'High'], 'Claims': ['None', 'Function', 'Cure']})


# --- 2. INITIALIZE WRITER ---
output_filename = 'Master_Dynamic_Report.xlsx'
writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
workbook = writer.book

# --- 3. GENERATION FUNCTIONS ---
def create_native_chart(df, sheet_name, chart_type, source_text, subtype=None):
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]

    # Create Chart Object
    options = {'type': chart_type}
    if subtype:
        options['subtype'] = subtype
    chart = workbook.add_chart(options)
    
    # Add Series dynamically based on columns
    num_rows = len(df)
    num_cols = len(df.columns)

    # Assuming Col A (0) is categories, B+ (1+) are series
    for i in range(1, num_cols):
        # col_letter = chr(ord('A') + i) # not strictly needed for the list syntax below
        chart.add_series({
            'name':       [sheet_name, 0, i],
            'categories': [sheet_name, 1, 0, num_rows, 0],
            'values':     [sheet_name, 1, i, num_rows, i],
        })

    # Formatting
    chart.set_title({'name': f'{sheet_name} (Editable)'})
    chart.set_size({'x_scale': 2, 'y_scale': 1.5})
    worksheet.insert_chart('E2', chart)
    
    worksheet.write(num_rows + 2, 0, source_text, workbook.add_format({'italic': True, 'font_color': 'gray'}))

# --- 4. BUILD SHEETS ---

# A. Mobility (Area Chart)
create_native_chart(df_mobility, 'Mobility', 'area', src_mobility, subtype='stacked')

# B. Internal Composition (Stacked Bar)
create_native_chart(df_composition, 'Internal_Comp', 'bar', src_composition, subtype='stacked')

# C. Segmentation (Column)
create_native_chart(df_segmentation, 'Segmentation', 'column', src_seg)

# D. Risk Heatmap (Conditional Formatting)
df_risk.to_excel(writer, sheet_name='Risk_Matrix', index=False)
ws_risk = writer.sheets['Risk_Matrix']

# Apply 3-Color Scale (Green-Yellow-Red)
# Range B2:F6 covers the numeric data for 5 regions (cols B-F) and 4 rows of data (2-5, or chart logic)
# Let's verify data shape: 4 rows of data (after header). 5 numeric columns (North America...Middle East).
# Rows 2 to 5. Cols B to F.
ws_risk.conditional_format('B2:F5', {
    'type': '3_color_scale',
    'min_color': '#63BE7B', # Green
    'mid_color': '#FFEB84', # Yellow
    'max_color': '#F8696B'  # Red
})
ws_risk.write(8, 0, src_risk, workbook.add_format({'italic': True, 'font_color': 'gray'}))

# E. Conceptual Figures (Static Images)
figures_dir = '/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/report/master_report/figures'

conceptual_items = [
    ('Timeline', df_timeline, 'Regulatory_Timeline_RightArrow.png'),
    ('Venn', df_venn, 'Nutraceuticals_Venn_Centered.png'),
    ('TradeOff', df_tradeoff, 'Regulatory_Tradeoff_FixedArrows.png')
]

for name, df, img_file in conceptual_items:
    df.to_excel(writer, sheet_name=name, index=False)
    ws = writer.sheets[name]
    ws.write(len(df)+2, 0, "Source: Concept Analysis")
    
    image_path = os.path.join(figures_dir, img_file)
    print(f"Processing image for {name}: {image_path}")
    
    if os.path.exists(image_path):
        try:
            ws.insert_image('E2', image_path)
            print(f"Inserted {img_file}")
        except Exception as e:
            print(f"Error inserting {img_file}: {e}")
            ws.write('E2', f"[Error: {e}]")
    else:
        print(f"Image not found: {image_path}")
        ws.write('E2', "[Image file not found in directory]")

# --- 5. SAVE ---
writer.close()
print(f"Success: '{output_filename}' created. Financial charts are fully editable/dynamic.")
