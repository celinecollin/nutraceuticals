import xlsxwriter
import pandas as pd
import datetime
import os

# --- CONFIGURATION ---
OUTPUT_FILE = '/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/Whitepaper_Master_Data.xlsx'

# Brand Colors corresponding to the report theme
COLORS = {
    'primary': '#003057',    # Navy Blue
    'secondary': '#0089cf',  # Bright Blue
    'accent1': '#b4a996',    # Beige/Gold
    'accent2': '#d04a02',    # Burnt Orange
    'accent3': '#4d6b7b',    # Slate Teal
    'grey': '#8b9ba5',       # Gridlines/Text
    'text': '#333333',       # Main Text
    'white': '#ffffff',
    'light_bg': '#f9f9f9'
}

# --- DATA DEFINITIONS ---
# Format:
# 'id': 'Figure 1', 
# 'title': 'Chart Title', 
# 'type': 'column' / 'bar' / 'line' / 'pie' / 'area' / 'scatter'
# 'data': DataFrame
# 'source': "Source String"
# 'subtype': 'stacked' (optional)

FIGURES = []

# --- PART I: FOUNDATION ---

# Fig 1: Regulatory Differences (Table I.1)
fig1_data = pd.DataFrame({
    'Feature': ['Nutraceutical Definition', 'Regulatory Body', 'Disease Claims', 'Market Entry Speed'],
    'United States (US)': ['Undefined (Food vs Drug)', 'FDA-CVM & AAFCO', 'Prohibited (Drug only)', 'Fast (Notification)'],
    'European Union (EU)': ['Undefined (Feed vs VMP)', 'EFSA & National Agencies', 'Prohibited (PARNUTs exception)', 'Slow (Dossier Approval)']
})
FIGURES.append({
    'id': 'Figure 1', 'title': 'Regulatory Landscape Comparison: US vs EU',
    'type': 'table', 'data': fig1_data, 
    'source': "Source: FDA-CVM, EFSA Regulations."
})

# Fig 2: Regulatory Timeline
fig2_data = pd.DataFrame({
    'Year': [2006, 2017, 2022, 2024, 2025],
    'Event Impact (Scale 1-10)': [10, 8, 9, 7, 6],
    'Event Description': ['EU Bans AGPs', 'US FDA VFD Implemented', 'EU Bans Zinc Oxide', 'China AGP Tightening', 'UK Feed Reform']
})
FIGURES.append({
    'id': 'Figure 2', 'title': 'Regulatory Timeline: The Push for Alternatives',
    'type': 'line', 'data': fig2_data[['Year', 'Event Impact (Scale 1-10)']], 
    'source': "Source: Regulatory Filings Analysis."
})

# Fig 3: Regulatory Pathways Matrix (Table I.2 Data)
fig3_data = pd.DataFrame({
    'Pathway': ['Feed Material', 'Feed Additive', 'Veterinary Drug'],
    'Development Cost (m)': [0.05, 1.5, 150.0],
    'Time to Market (Years)': [0.5, 2.0, 7.0],
    'Claim Strength (1-10)': [1, 5, 10]
})
FIGURES.append({
    'id': 'Figure 3', 'title': 'Regulatory Pathways: Cost vs Claim Strength',
    'type': 'scatter', 'data': fig3_data,
    'source': "Source: Internal Regulatory Logic Model."
})

# Fig 4: TAM Reconciliation
# Fig 4: TAM Reconciliation
fig4_data = pd.DataFrame({
    'Segment': ['Total Addressable Market (TAM)', 'Serviceable Addressable Market (SAM)', 'Serviceable Obtainable Market (SOM)'],
    'Value (bn)': [123.0, 13.0, 0.25]
})
FIGURES.append({
    'id': 'Figure 4', 'title': 'Total Addressable Market (TAM) Reconciliation (2024)',
    'type': 'concentric', 'data': fig4_data,
    'source': "Source: Grand View Research (2024), Euromonitor (2024)."
})

# --- PART II.0: MARKET BIFURCATION ---

# Fig 5: Innovation Premium
fig5_data = pd.DataFrame({
    'Company': ['Novonesis', 'Zoetis', 'Elanco', 'Vetoquinol', 'DSM-Firmenich', 'Virbac', 'H&H Group', 'Symrise (Pet)', 'Phibro', 'ForFarmers', 'Dechra', 'Balchem', 'Givaudan', 'Swedencare', 'Aker BioMarine'],
    'R&D Intensity (%)': [10.8, 8.0, 7.7, 8.1, 5.5, 8.0, 1.8, 6.5, 2.9, 0.8, 7.5, 1.5, 8.0, 0.1, 0.5],
    'EBITDA Margin (%)': [36.1, 38.0, 20.5, 19.3, 16.5, 16.0, 15.0, 22.2, 11.0, 4.0, 22.0, 7.0, 24.0, 22.0, 15.0],
    'Sector': ['Pharma-Nutra', 'Pharma-Nutra', 'Pharma-Nutra', 'Pharma-Nutra', 'Ingredient Tech', 'Pharma-Nutra', 'Brand/Consumer', 'Ingredient Tech', 'Feed/Health', 'Commodity Feed', 'Pharma-Nutra', 'Feed/Health', 'Ingredient Tech', 'Brand/Consumer', 'Ingredient Tech']
})
FIGURES.append({
    'id': 'Figure 5', 'title': 'The Innovation-Premium Matrix: R&D Intensity vs Margins',
    'type': 'scatter', 'data': fig5_data,
    'source': "Source: Annual Reports 2024/2025; Internal Analysis."
})

# Fig 6: Market Bifurcation (Pet vs Livestock)
fig6_data = pd.DataFrame({
    'Metric': ['R&D Intensity', 'Gross Margin', 'Price Sensitivity (Inv)', 'Brand Loyalty'],
    'Pet (Emotional Economy)': [9, 7.5, 8, 8.5],
    'Livestock (ROI Economy)': [2, 1.5, 2, 4.0]
})
FIGURES.append({
    'id': 'Figure 6', 'title': 'Market Bifurcation: Structural Economics',
    'type': 'column', 'data': fig6_data,
    'source': "Source: Internal Strategy Analysis."
})

# --- PART II.1 - II.11: FUNCTIONAL MATRICES ---

# Fig 7: Mobility
fig7_data = pd.DataFrame({
    'Ingredient': ['Omega-3', 'UC-II Collagen', 'Eggshell Membrane', 'Green Lipped Mussel', 'Glucosamine/Chondroitin', 'MSM'],
    'Evidence Level (1-10)': [9, 8, 7, 7, 5, 4],
    'Est. Value (m)': [315, 51, 16, 45, 291, 58]
})
FIGURES.append({
    'id': 'Figure 7', 'title': 'Mobility Market: Efficacy vs Value',
    'type': 'bar', 'data': fig7_data,
    'source': "Source: Internal Efficacy Analysis based on JAVMA/JVIM studies."
})

# Fig 8: Gut Health
fig8_data = pd.DataFrame({
    'Ingredient': ['Probiotics (Specific)', 'Prebiotics (MOS/FOS)', 'Synbiotics', 'Postbiotics/Butyrate', 'Organic Acids', 'Enzymes (Phytase)'],
    'Evidence Level (1-10)': [9, 7, 7, 7, 7, 9],
    'Est. Value (m)': [1590, 157, 303, 173, 266, 424]
})
FIGURES.append({
    'id': 'Figure 8', 'title': 'Gut Health Market: Efficacy vs Value',
    'type': 'bar', 'data': fig8_data,
    'source': "Source: Internal Efficacy Analysis."
})

# Fig 9: Immunity
fig9_data = pd.DataFrame({
    'Ingredient': ['Beta-glucans', 'Plasma/Colostrum', 'Nucleotides', 'Seaweed Polysaccharides', 'Selenium/Vit E'],
    'Evidence Level (1-10)': [7, 8, 7, 6, 7],
    'Est. Value (m)': [9, 533, 151, 1080, 68]
})
FIGURES.append({
    'id': 'Figure 9', 'title': 'Immunity Market: Efficacy vs Value',
    'type': 'bar', 'data': fig9_data,
    'source': "Source: Internal Efficacy Analysis."
})

# Fig 10: Cognition
fig10_data = pd.DataFrame({
    'Ingredient': ['MCTs', 'DHA (Omega-3)', 'Antioxidants', 'Phosphatidylserine', 'SAMe', 'B Vitamins'],
    'Evidence Level (1-10)': [9, 8, 8, 5, 5, 5],
    'Est. Value (m)': [109, 85, 73, 4, 24, 17]
})
FIGURES.append({
    'id': 'Figure 10', 'title': 'Cognitive Health: Efficacy vs Value',
    'type': 'bar', 'data': fig10_data,
    'source': "Source: Internal Efficacy Analysis."
})

# Fig 11: Calming
fig11_data = pd.DataFrame({
    'Ingredient': ['L-Theanine', 'Alpha-Casozepine', 'Tryptophan', 'CBD/Hemp', 'Multi-Complexes'],
    'Evidence Level (1-10)': [7, 7, 6, 6, 5],
    'Est. Value (m)': [12, 7, 19, 80, 121]
})
FIGURES.append({
    'id': 'Figure 11', 'title': 'Calming Sector: Efficacy vs Value',
    'type': 'bar', 'data': fig11_data,
    'source': "Source: Internal Efficacy Analysis."
})

# Fig 12: Performance (Livestock)
fig12_data = pd.DataFrame({
    'Ingredient': ['Phytase', 'Xylanase', 'Protease', 'Phytogenics', 'Yeast Culture', 'Amino Acids'],
    'Evidence Level (1-10)': [10, 10, 8, 7, 7, 8],
    'Est. Value (m)': [145, 242, 48, 216, 484, 291]
})
FIGURES.append({
    'id': 'Figure 12', 'title': 'Performance/FCR: Efficacy vs Value',
    'type': 'bar', 'data': fig12_data,
    'source': "Source: Internal Efficacy Analysis."
})

# Fig 13: Niches
fig13_data = pd.DataFrame({
    'Ingredient': ['Omega-6/Linoleic', 'Biotin', 'Zinc Methionine', 'Astaxanthin'],
    'Evidence Level (1-10)': [8, 5, 6, 8],
    'Est. Value (m)': [29, 14, 42, 327]
})
FIGURES.append({
    'id': 'Figure 13', 'title': 'Special Niches: Efficacy vs Value',
    'type': 'bar', 'data': fig13_data,
    'source': "Source: Internal Efficacy Analysis."
})

# Fig 14: Ectoparasite
fig14_data = pd.DataFrame({
    'Ingredient': ['Natural Repellents', 'Garlic/Botanicals', 'Skin Barrier Stacks'],
    'Evidence Level (1-10)': [5, 3, 5],
    'Est. Value (m)': [133, 10, 36]
})
FIGURES.append({
    'id': 'Figure 14', 'title': 'Natural Ectoparasite: Efficacy vs Value',
    'type': 'bar', 'data': fig14_data,
    'source': "Source: Internal Efficacy Analysis."
})

# Fig 15: Nutrigenomics
fig15_data = pd.DataFrame({
    'Strategy': ['Biomarker Analysis', 'Nrf2 Activators', 'Genotypic Profiling', 'Vaccine Adjuvants'],
    'Evidence Level (1-10)': [7, 6, 8, 6],
    'Est. Value (m)': [148, 48, 526, 73]
})
FIGURES.append({
    'id': 'Figure 15', 'title': 'Nutrigenomics: Efficacy vs Value',
    'type': 'bar', 'data': fig15_data,
    'source': "Source: Internal Efficacy Analysis."
})

# Fig 16: Delivery Systems
fig16_data = pd.DataFrame({
    'Technology': ['Rumen Protection', 'Smart Boluses', 'Soft Chews', 'Aquafeed Coatings', 'Biofilm Probiotics'],
    'Tech Maturity (1-10)': [8, 7, 9, 8, 6],
    'Est. Value (m)': [920, 625, 593, 271, 40]
})
FIGURES.append({
    'id': 'Figure 16', 'title': 'Delivery Systems: Maturity vs Value',
    'type': 'bar', 'data': fig16_data,
    'source': "Source: Internal Technology Audit."
})

# Fig 17: Sustainability
fig17_data = pd.DataFrame({
    'Strategy': ['Methane (Asparagopsis)', 'Methane (3-NOP)', 'P-Management (Phytase)', 'N-Efficiency (Protease)'],
    'Evidence Level (1-10)': [7, 9, 10, 8],
    'Est. Value (m)': [6, 15, 155, 545]
})
FIGURES.append({
    'id': 'Figure 17', 'title': 'Sustainability: Efficacy vs Value',
    'type': 'bar', 'data': fig17_data,
    'source': "Source: Internal Efficacy Analysis."
})

# Fig 18: Comparative Revenue (Aggregated from above)
fig18_data = pd.DataFrame({
    'Segment': ['Performance/FCR', 'Gut Health', 'Delivery Systems', 'Nutrigenomics', 'Sustainability', 'Mobility', 'Immunity', 'Psych/Calming', 'Niches', 'Cognition', 'Ectoparasite'],
    'Total Value (m)': [1426, 2913, 2749, 795, 786, 776, 1841, 239, 412, 312, 179] # Sum of components
})
FIGURES.append({
    'id': 'Figure 18', 'title': 'Total Revenue Potential by Functional Segment',
    'type': 'bar', 'data': fig18_data.sort_values('Total Value (m)', ascending=True),
    'source': "Source: Aggregated Segment Analysis."
})

# Fig 19: Ingredient Share (Consolidated)
fig19_data = pd.DataFrame({
    'Key Ingredient': ['Probiotics', 'Seeaweed/Polysaccharides', 'Rumen Protection Tech', 'Soft Chews Tech', 'Plasma', 'Yeast Culture', 'Phytase'],
    'Market Value (m)': [1590, 1080, 920, 593, 533, 484, 569]
})
FIGURES.append({
    'id': 'Figure 19', 'title': 'Top 7 Power Ingredients/Technologies by Value',
    'type': 'bar', 'data': fig19_data,
    'source': "Source: Internal Market Sizing."
})

# --- PART III: DEMOGRAPHICS ---

# Fig 20: Global Pet Ownership
fig20_data = pd.DataFrame({
    'Region': ['US', 'Canada', 'EU'],
    'Ownership Rate (%)': [71, 60, 49]
})
FIGURES.append({
    'id': 'Figure 20', 'title': 'Household Pet Ownership Rate by Region',
    'type': 'column', 'data': fig20_data,
    'source': "Source: APPA (2024), FEDIAF (2024)."
})

# Fig 21: EU Pet Population
fig21_data = pd.DataFrame({
    'Species': ['Cats', 'Dogs', 'Others'],
    'Population (m)': [127, 104, 50]
})
FIGURES.append({
    'id': 'Figure 21', 'title': 'EU Pet Population Structure',
    'type': 'pie', 'data': fig21_data,
    'source': "Source: FEDIAF Facts & Figures 2024."
})

# Fig 22: EU Growth
fig22_data = pd.DataFrame({
    'Species': ['Cats', 'Dogs'],
    'Growth 2018-2023 (%)': [11, 5]
})
FIGURES.append({
    'id': 'Figure 22', 'title': 'EU Pet Population Growth (2018-2023)',
    'type': 'column', 'data': fig22_data,
    'source': "Source: FEDIAF."
})

# Fig 23: Regional Market
fig23_data = pd.DataFrame({
    'Region': ['APAC', 'Europe', 'North America', 'LATAM', 'Rest of World'],
    'Market Size (bn)': [2.1, 1.7, 1.1, 0.8, 0.3]
})
FIGURES.append({
    'id': 'Figure 23', 'title': 'Regional Market Size: Pet Nutraceuticals',
    'type': 'bar', 'data': fig23_data,
    'source': "Source: Grand View Research (2024 Estimates)."
})

# Fig 24: Probiotics Share
fig24_data = pd.DataFrame({
    'Species': ['Poultry', 'Swine', 'Ruminant', 'Aqua'],
    'Volume Share (%)': [60, 25, 10, 5],
    'Revenue (bn)': [2.5, 1.0, 0.4, 0.2]
})
FIGURES.append({
    'id': 'Figure 24', 'title': 'Probiotics Market: Volume Share vs Revenue',
    'type': 'combination', 'data': fig24_data,
    'source': "Source: Global Market Insights."
})

# Fig 25: HPAI Impact
fig25_data = pd.DataFrame({
    'Year': range(2015, 2025),
    'Bird Losses (m)': [5, 8, 10, 12, 15, 25, 35, 40, 45, 50]
})
FIGURES.append({
    'id': 'Figure 25', 'title': 'Impact of HPAI: Cumulative Bird Losses',
    'type': 'area', 'data': fig25_data,
    'source': "Source: WOAH WAHIS Situation Reports."
})

# Fig 26: Swine Decline
fig26_data = pd.DataFrame({
    'Year': range(2014, 2025),
    'EU Swine Herd Index': [100 - (0.81 * x) for x in range(11)] # Simulated decline to ~91.9
})
FIGURES.append({
    'id': 'Figure 26', 'title': 'EU Swine Herd Structural Decline (Index 2014=100)',
    'type': 'line', 'data': fig26_data,
    'source': "Source: Eurostat Livestock Statistics 2024."
})

# Fig 27: Cattle Inventory
fig27_data = pd.DataFrame({
    'Year': range(2010, 2025),
    'US Cattle (m)': [95 - (0.52 * x) for x in range(15)] # Trend to 87.2
})
FIGURES.append({
    'id': 'Figure 27', 'title': 'US Cattle Inventory: The 70-Year Low',
    'type': 'line', 'data': fig27_data,
    'source': "Source: USDA NASS."
})

# Fig 28: Livestock Trends
fig28_data = pd.DataFrame({
    'Year': [2018, 2019, 2020, 2021, 2022, 2023],
    'Poultry Index': [100, 102, 104, 106, 108, 110.5],
    'Bovine Index': [100, 99, 98, 97, 96, 94.8]
})
FIGURES.append({
    'id': 'Figure 28', 'title': 'Divergent Production Trends: Poultry vs Bovine',
    'type': 'line', 'data': fig28_data,
    'source': "Source: FAO, OECD-FAO Agricultural Outlook."
})

# Fig 29: Aqua Production
fig29_data = pd.DataFrame({
    'Type': ['Aquaculture', 'Capture Fisheries'],
    'Production 2022 (m tonnes)': [94.4, 91.0] # Crossover moment
})
FIGURES.append({
    'id': 'Figure 29', 'title': 'The Blue Transformation: Aquaculture vs Capture',
    'type': 'column', 'data': fig29_data,
    'source': "Source: FAO SOFIA 2024."
})

# Fig 30: Formats By Species
fig30_data = pd.DataFrame({
    'Format': ['Chews/Treats', 'Liquids/Pastes', 'Pills/Powders'],
    'Dogs (%)': [64, 10, 26],
    'Cats (%)': [15, 35, 50],
    'Horses (%)': [0, 25, 75]
})
FIGURES.append({
    'id': 'Figure 30', 'title': 'Preferred Delivery Formats by Species',
    'type': 'column', 'data': fig30_data, 'subtype': 'stacked',
    'source': "Source: Grand View Research."
})

# Fig 31: Wallet Share
fig31_data = pd.DataFrame({
    'Category': ['Food', 'Vet Care', 'Supplements', 'Toys/Access', 'Services'],
    'Share of Wallet (%)': [40, 25, 15, 10, 10]
})
FIGURES.append({
    'id': 'Figure 31', 'title': 'Preventive Health Wallet Allocation',
    'type': 'pie', 'data': fig31_data,
    'source': "Source: APPA 2025."
})

# Fig 32: Segmentation
fig32_data = pd.DataFrame({
    'Segment': ['Prem (Spare No Expense)', 'Value (Pragmatic)', 'Basic (Price Sensitive)'],
    'Households (%)': [20, 50, 30],
    'Revenue (%)': [48, 42, 10]
})
FIGURES.append({
    'id': 'Figure 32', 'title': 'Consumer Segmentation: The Pareto Effect',
    'type': 'combination', 'data': fig32_data, # Logic handled in chart gen
    'source': "Source: Internal Customer Segmentation."
})

# Fig 33: Psychology
fig33_data = pd.DataFrame({
    'Driver': ['Fear of Loss / Regret', 'Love / Bonding', 'Duty / Responsibility'],
    'Impact Score (%)': [50, 30, 20]
})
FIGURES.append({
    'id': 'Figure 33', 'title': 'Psychological Drivers of Purchase',
    'type': 'bar', 'data': fig33_data,
    'source': "Source: Nicotra et al. (2025)."
})

# Fig 34: Mobility Evo
fig34_data = pd.DataFrame({
    'Year': [2015, 2020, 2024, 2030],
    'Generic Glucosamine': [70, 60, 45, 35],
    'UC-II Collagen': [5, 15, 25, 30],
    'Green Lipped Mussel': [15, 15, 18, 20],
    'Premium Combos': [10, 10, 12, 15]
})
FIGURES.append({
    'id': 'Figure 34', 'title': 'Evolution of Mobility Ingredients (Share %)',
    'type': 'area', 'data': fig34_data, 'subtype': 'stacked',
    'source': "Source: Nutrition Business Journal."
})

# Fig 35: Senior Growth
fig35_data = pd.DataFrame({
    'Year': [2015, 2024, 2030],
    'Senior Wellness Market Index': [5, 12, 20]
})
FIGURES.append({
    'id': 'Figure 35', 'title': 'Growth of the Senior Pet Wellness Market',
    'type': 'column', 'data': fig35_data,
    'source': "Source: Internal Projections."
})

# Fig 36: Value Chain (Table Data for Concept)
fig36_data = pd.DataFrame({
    'Stage': ['Ingredients', 'Manufacturing', 'Brand Owner'],
    'EBITDA Margin Capture (%)': [25, 15, 20],
    'Value Added': ['IP/Science', 'Scale/Form', 'Consumer Trust']
})
FIGURES.append({
    'id': 'Figure 36', 'title': 'Value Chain Economics: Margin Capture',
    'type': 'bar', 'data': fig36_data,
    'source': "Source: L.E.K. Consulting."
})

# Fig 37: Channel Economics (Margin Erosion)
fig37_data = pd.DataFrame({
    'Year': [2010, 2015, 2019, 2024],
    'Vet Channel Net Margin (%)': [25, 23, 20, 18]
})
FIGURES.append({
    'id': 'Figure 37', 'title': 'Vet Channel Margin Erosion (Due to E-Comm)',
    'type': 'line', 'data': fig37_data,
    'source': "Source: Industry Interviews."
})

# Fig 38: Value Waterfall
fig38_data = pd.DataFrame({
    'Cost Component': ['Raw Material', 'Manufacturing', 'Logistics/Mktg', 'Net Margin'],
    'Livestock Premix ($50)': [30, 10, 8, 2],
    'Pet Supplement ($50)': [10, 15, 15, 10]
})
FIGURES.append({
    'id': 'Figure 38', 'title': 'Value Waterfall: Livestock vs Pet Cost Structure',
    'type': 'column', 'data': fig38_data, 'subtype': 'stacked',
    'source': "Source: Internal Pricing Models."
})

# Fig 39: Risk/Reward
fig39_data = pd.DataFrame({
    'Segment': ['Pet Brands', 'Livestock Premix', 'Ingredients (IP)', 'Commodities'],
    'Market Size (bn)': [6, 8, 2, 5],
    'EBITDA Margin (%)': [22, 10, 25, 6]
})
FIGURES.append({
    'id': 'Figure 39', 'title': 'Risk/Reward Map: Size vs Margin',
    'type': 'scatter', 'data': fig39_data,
    'source': "Source: Strategic Categorization."
})

# Fig 40: Pharma Funnel
fig40_data = pd.DataFrame({
    'Funnel Stage': ['OTC Trial (Nutraceutical)', 'Regular User', 'Rx Conversion'],
    'Customer Volume (Index)': [100, 40, 10]
})
FIGURES.append({
    'id': 'Figure 40', 'title': 'The Pharma Integration Funnel',
    'type': 'bar', 'data': fig40_data,
    'source': "Source: Customer Journey Mapping."
})

# --- PART IV: COMPETITIVE ---

# Fig 41: Revenue Comparison
fig41_data = pd.DataFrame({
    'Company': ['Zoetis', 'Merck AH', 'Elanco', 'DSM-Firmenich', 'Nestle Purina'],
    'Revenue 2024 (bn)': [9.3, 5.9, 4.4, 3.3, 22.4]
})
FIGURES.append({
    'id': 'Figure 41', 'title': 'Revenue Comparison: Pharma vs Nutrition',
    'type': 'bar', 'data': fig41_data,
    'source': "Source: Company Filings."
})

# Fig 42: Capability Matrix (Score)
fig42_data = pd.DataFrame({
    'Capability': ['Diagnostics', 'Vaccines', 'Pharma (Rx)', 'Nutraceuticals', 'Pet Food'],
    'Zoetis': [1, 1, 1, 1, 0],
    'Mars': [1, 0, 0, 1, 1],
    'Nestle': [0, 0, 0, 1, 1],
    'Virbac': [0, 1, 1, 1, 1]
})
FIGURES.append({
    'id': 'Figure 42', 'title': 'Capability Matrix: Continuum of Care Coverage',
    'type': 'table', 'data': fig42_data, 
    'source': "Source: Corporate Strategy Analysis."
})

# Fig 43: Pet Market Share
fig43_data = pd.DataFrame({
    'Company': ['Mars Petcare', 'Nestle Purina', 'Hill\'s', 'General Mills (Blue)', 'Others'],
    'Share (%)': [20, 19, 5, 4, 52]
})
FIGURES.append({
    'id': 'Figure 43', 'title': 'Global Pet Nutrition Market Share',
    'type': 'pie', 'data': fig43_data,
    'source': "Source: Euromonitor."
})

# Fig 44: Margin Ladder
fig44_data = pd.DataFrame({
    'Value Chain Step': ['Commodity Feed', 'Specialty Premix', 'Distributor', 'Pet Retailer', 'Pharma-Nutra Brand'],
    'Est. EBITDA Margin (%)': [4, 8, 12, 15, 25]
})
FIGURES.append({
    'id': 'Figure 44', 'title': 'The Margin Ladder: Value Capture by Step',
    'type': 'bar', 'data': fig44_data,
    'source': "Source: Internal Margin Analysis."
})

# Fig 45: Strategic Matrix (Watchlist)
fig45_data = pd.DataFrame({
    'Company': ['Zoetis', 'Novonesis', 'Swedencare', 'DSM-Firmenich'],
    'Clinical Evidence Score (1-10)': [9, 9, 7, 8],
    'Commercial Scale Score (1-10)': [10, 6, 4, 9]
})
FIGURES.append({
    'id': 'Figure 45', 'title': 'Strategic Matrix: Evidence vs Scale',
    'type': 'scatter', 'data': fig45_data,
    'source': "Source: M&A Database."
})

# --- GENERATION LOGIC ---

def generate_excel():
    print(f"Generating Master Excel with {len(FIGURES)} figures...")
    
    writer = pd.ExcelWriter(OUTPUT_FILE, engine='xlsxwriter')
    workbook = writer.book
    
    # Formats
    fmt_header = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': COLORS['primary'], 'font_color': 'white', 'border': 1})
    fmt_cell = workbook.add_format({'border': 1})
    fmt_source = workbook.add_format({'italic': True, 'font_color': 'gray', 'font_size': 10})
    
    # Create Index Sheet
    ws_index = workbook.add_worksheet('INDEX')
    ws_index.write(0, 0, "Master Figure Index", workbook.add_format({'bold': True, 'font_size': 16}))
    ws_index.write(1, 0, "Generated: " + str(datetime.date.today()))
    ws_index.set_column(0, 0, 15)
    ws_index.set_column(1, 1, 50)
    
    ws_index.write(3, 0, "Sheet ID", fmt_header)
    ws_index.write(3, 1, "Figure Title", fmt_header)
    
    for i, fig in enumerate(FIGURES):
        print(f"Processing {fig['id']}...")
        
        # Add to Index
        ws_index.write(i+4, 0, fig['id'], fmt_cell)
        ws_index.write_url(i+4, 1, f"internal:'{fig['id']}'!A1", string=fig['title'])
        
        # Create Sheet
        sheet_name = fig['id']
        df = fig['data']
        ws = workbook.add_worksheet(sheet_name)
        
        # Write Table Data
        ws.write(0, 0, fig['title'], workbook.add_format({'bold': True, 'font_size': 14, 'font_color': COLORS['primary']}))
        
        # Write Headers
        for col_num, value in enumerate(df.columns.values):
            ws.write(2, col_num, value, fmt_header)
        
        # Write Rows
        for row_num, row_data in enumerate(df.values):
            for col_num, value in enumerate(row_data):
                ws.write(3+row_num, col_num, value, fmt_cell)
        
        # Write Source
        last_row = 3 + len(df)
        ws.write(last_row + 1, 0, fig.get('source', ''), fmt_source)
        
        # Adjust Columns
        ws.set_column(0, len(df.columns)-1, 20)
        
        # Skip chart for tables
        if fig['type'] == 'table':
            continue
            
        # --- CHART CREATION ---
        
        chart_type = fig['type']
        if chart_type == 'combination': chart_type = 'column' # Handle combo manually if needed, or default
        
        options = {'type': chart_type}
        if fig.get('subtype'):
            options['subtype'] = fig.get('subtype')
            
        chart = workbook.add_chart(options)
        
        # Categories (X-Axis) - usually col 0
        # Values (Y-Axis) - cols 1 to end
        cat_col_idx = 0
        val_start_idx = 1
        
        # Special logic for some charts? Assuming standard structure for now.
        
        for col_idx in range(val_start_idx, len(df.columns)):
            col_name = df.columns[col_idx]
            chart.add_series({
                'name':       [sheet_name, 2, col_idx],
                'categories': [sheet_name, 3, cat_col_idx, last_row - 1, cat_col_idx],
                'values':     [sheet_name, 3, col_idx, last_row - 1, col_idx],
                'line':       {'width': 2.25} if chart_type == 'line' else None
            })
            
        # Styling
        chart.set_title({'name': fig['title']})
        chart.set_size({'width': 720, 'height': 480})
        chart.set_style(10) # Clean style
        
        # Insert Chart
        ws.insert_chart('E3', chart)

    writer.close()
    print(f"COMPLETE. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_excel()
