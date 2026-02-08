
import matplotlib.pyplot as plt
import os
import textwrap

# Define output directory
output_dir = "report/master_report/figures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Helper function to wrap text
def wrap_text(text, width=30):
    return "\n".join(textwrap.wrap(text, width=width))

# Data for the table with wrapped text where necessary to avoid super width
# We will rely on column width + wrapping
data_raw = [
    ["A. Pet Nutraceuticals", "~$6.0 B", "Joint chews, probiotics, calming oils"],
    ["B. Livestock Functional Additives", "~$7.0 B", "Phytase, rumen-protected amino acids, probiotics"],
    ["= Total \"Animal Nutraceuticals\"", "~$13.0 B", "The Scope of this White Paper"],
    ["Context: Broader Animal Health", "~$50.0 B", "Includes vaccines, pharma, parasiticides"],
    ["Context: Total Pet Care", "~$136.0 B", "Includes food, services, vet care"]
]

# Wrap the text in the first and last columns
data = []
for row in data_raw:
    new_row = [
        wrap_text(row[0], 35), # First column wrap
        row[1],
        wrap_text(row[2], 45)  # Last column wrap
    ]
    data.append(new_row)

columns = ["Component", "Value (USD Billions)", "Examples"]

# Colors (Corporate Palette)
COLORS = {
    'primary': '#003057',    # Navy Blue
    'secondary': '#0089cf',  # Bright Blue
    'light_bg': '#f0f4f8',   # Very light blue/grey
    'white': '#ffffff',
    'text_dark': '#333333',
    'context_bg': '#f9f9f9', # Very light grey for context
}

# Create figure - widened to fit content better
# Increased height to accommodate wrapped text
fig, ax = plt.subplots(figsize=(14, 5)) 
ax.axis('off')

# Create table
table = ax.table(cellText=data, colLabels=columns, cellLoc='left', loc='center', bbox=[0, 0, 1, 1])

# Styling
table.auto_set_font_size(False)
table.set_fontsize(12)

# Column widths (relative) - Adjusted to give more space to text columns
col_widths = [0.32, 0.20, 0.48] 
for i, width in enumerate(col_widths):
    for j in range(len(data) + 1): # +1 for header
        table[j, i].set_width(width)

# Cell styling loop
for (row, col), cell in table.get_celld().items():
    # Dynamic row height based on line count?
    # Basic height 0.15 is good for single line, maybe 0.2 for safety with wrapping
    cell.set_height(0.18) 
    
    cell.set_edgecolor('#dddddd') # Light grey grid
    
    # Padding settings
    cell.set_text_props(va='center')
    
    if row == 0:
        # Header Styling
        cell.set_facecolor(COLORS['primary'])
        cell.set_text_props(color='white', weight='bold', fontsize=13, va='center')
    elif row == 3: # Total Row (index 2 in data -> row 3 in table)
        cell.set_facecolor(COLORS['light_bg'])
        cell.set_text_props(weight='bold', color=COLORS['text_dark'])
        if col == 2:
            cell.set_text_props(weight='bold', color=COLORS['primary']) # Scope text
    elif row >= 4: # Context Rows
        cell.set_facecolor(COLORS['context_bg'])
        cell.set_text_props(style='italic', color='#555555')
    else:
        cell.set_facecolor('white')
        cell.set_text_props(color=COLORS['text_dark'])
        if col == 0:
            cell.set_text_props(weight='bold')
    
    # Specific Alignment for Value Column
    if col == 1:
        cell.set_text_props(ha='center') # Center the values
    else:
        # Indent left text slightly "virtually" by ensuring wrapping doesn't hit edge?
        # Matplotlib doesn't support padding easily, usually handled by leading space in string
        pass 

# Add manual padding to strings in the actual table cells to prevent edge touching
for (row, col), cell in table.get_celld().items():
    text = cell.get_text().get_text()
    if col != 1: # Don't pad centered values
        cell.set_text_props(ha='left')
        cell.get_text().set_text(f"  {text}") # Add explicit spaces for padding

# Save
output_path = os.path.join(output_dir, "Figure_TAM_Reconciliation.png")
# Tight layout with padding to ensure no clipping at figure edges
plt.savefig(output_path, bbox_inches='tight', dpi=300, pad_inches=0.1)
print(f"Table figure saved to: {output_path}")
