import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines



def create_summary_map():
    # Setup the figure layout
    fig = plt.figure(figsize=(20, 12)) 
    # fig.patch.set_facecolor('#f0f0f0') # Light grey background to frame the map
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    # Load Real Map Image
    try:
        img = plt.imread('report/master_report/figures/base_world_map.png')
        # Equirectangular projection corresponds to these coordinates
        ax.imshow(img, extent=[-180, 180, -90, 90]) 
    except Exception as e:
        print(f"Error loading map: {e}")
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.text(0, 0, "Map Image Not Found", ha='center')

    # Title Banner (Top)
    rect_title = patches.Rectangle((-180, 70), 360, 20, facecolor='white', alpha=0.9)
    ax.add_patch(rect_title)
    
    # TITLE
    ax.text(-170, 82, 'GLOBAL ANIMAL NUTRACEUTICALS: 2025-2035 STRATEGIC MAP', 
            ha='left', va='center', fontsize=32, fontweight='bold', color='#003057') # Increased from 28
    ax.text(-170, 75, 'Market Inflection: $13B \u2192 $24B • "Humanization" & "Post-Antibiotic" Transition', 
            ha='left', va='center', fontsize=20, color='#0089cf', style='italic') # Increased from 18

    # Color Palette
    col_na = '#003057'   # Navy
    col_eu = '#0089cf'   # Blue
    col_asia = '#d04a02' # Orange
    col_latam = '#28a745'# Green
    
    # Common text box style
    box_style = dict(boxstyle="round,pad=0.5", fc="white", alpha=0.9, ec="none") # Increased alpha for readability
    font_size_text = 10 # Increased from 7.5
    font_size_title = 18 # Increased from 16
    
    # === DATA CARDS (Semi-transparent overlays) ===
    
    # NORTH AMERICA
    text_na = (
        "MARKET: ~$6.2B (48% of Global)\n"
        "GROWTH: 5.5% CAGR\n"
        "──────────────────────────────\n"
        "RETAILERS:\n"
        "• PetSmart, Chewy, Petco\n"
        "• Amazon, Walmart\n"
        "NUTRA/PHARMA MAJORS:\n"
        "• Zoetis, Elanco, Nutramax\n"
        "• Zesty Paws, VetriScience\n"
        "• Axiota, Native Pet\n"
        "• ElleVet, Earth Animal\n"
        "FOOD/FEED MAJORS:\n"
        "• Mars, Nestlé, General Mills\n"
        "STARTUPS:\n"
        "• Bond Pet Foods, BiomEdit\n"
        "• Hoofprint Biome, Rumin8\n"
        "STRATEGIC INVESTORS (VC/PE):\n"
        "• Digitalis, Gryphon, S2G\n"
        "• Paine Schwartz"
    )
    # Box position - West Coast / Pacific
    box_x, box_y = -150, 20 
    title_x, title_y = -150, 65
    pin_x, pin_y = -100, 45 # Central US (approx)
    
    ax.text(title_x, title_y, "NORTH AMERICA", fontsize=font_size_title, fontweight='bold', color=col_na, ha='left',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=col_na, alpha=1.0))
    ax.text(box_x, box_y, text_na, fontsize=font_size_text, va='top', ha='left', family='sans-serif', weight='bold',
            bbox=dict(boxstyle="round,pad=0.6", fc="white", ec=col_na, alpha=0.9, lw=2))
    ax.plot([title_x + 60, pin_x], [title_y - 5, pin_y], color=col_na, marker='o', markersize=8, linewidth=2)


    # EUROPE (EU)
    text_eu = (
        "MARKET: ~$3.3B (Excl. UK)\n"
        "GROWTH: 4.5% CAGR\n"
        "──────────────────────────────\n"
        "RETAILERS:\n"
        "• Zooplus, Fressnapf\n"
        "• Musti Group, Arcaplanet\n"
        "PHARMA/NUTRA/INGRED:\n"
        "• Boehringer Ingelheim, DSM\n"
        "• Ceva, Virbac, Vetoquinol\n"
        "• Evonik, Phytobiotics\n"
        "FOOD/FEED MAJORS:\n"
        "• Royal Canin, Affinity Petcare\n"
        "STARTUPS/SCALEUPS:\n"
        "• MicroHarvest, Proteon\n"
        "• Gnubiotics, Veramaris\n"
        "KEY INVESTORS (EU):\n"
        "• EQT, Aqua-Spark\n"
        "• Astanor, Five Seasons"
    )
    # Moved EU box South (Med/Africa) to clear crowded Europe
    box_x, box_y = 10, 10
    title_x, title_y = 10, 55
    pin_x, pin_y = 15, 50 # Central Europe

    ax.text(title_x, title_y, "EUROPE (EU)", fontsize=font_size_title, fontweight='bold', color=col_eu, ha='left',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=col_eu, alpha=1.0))
    ax.text(box_x, box_y, text_eu, fontsize=font_size_text, va='top', ha='left', family='sans-serif', weight='bold',
            bbox=dict(boxstyle="round,pad=0.6", fc="white", ec=col_eu, alpha=0.9, lw=2))
    ax.plot([title_x + 10, pin_x], [title_y - 2, pin_y], color=col_eu, marker='o', markersize=8, linewidth=2)


    # UNITED KINGDOM
    col_uk = '#6f42c1' # Purple specifically for UK
    text_uk = (
        "MARKET: ~$0.8B (Advanced)\n"
        "GROWTH: 5.0% CAGR\n"
        "──────────────────────────────\n"
        "RETAILERS:\n"
        "• Pets at Home (Services)\n"
        "NUTRA/MAJORS:\n"
        "• IVC Evidensia, Dechra\n"
        "• Lintbells (YuMOVE)\n"
        "STARTUPS: Folium, Biome9\n"
        "INVESTORS: BC Partners,\n"
        "Cinven, Ocean 14"
    )
    # Moved UK box North-West (Atlantic)
    box_x_uk, box_y_uk = -45, 85
    title_x_uk, title_y_uk = -45, 115
    pin_x_uk, pin_y_uk = -2, 55 # UK

    ax.text(title_x_uk, title_y_uk, "UNITED KINGDOM", fontsize=font_size_title, fontweight='bold', color=col_uk, ha='left',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=col_uk, alpha=1.0))
    ax.text(box_x_uk, box_y_uk, text_uk, fontsize=font_size_text, va='top', ha='left', family='sans-serif', weight='bold',
            bbox=dict(boxstyle="round,pad=0.6", fc="white", ec=col_uk, alpha=0.9, lw=2))
    ax.plot([title_x_uk + 60, pin_x_uk], [box_y_uk - 5, pin_y_uk], color=col_uk, marker='o', markersize=8, linewidth=2)


    # ASIA-PACIFIC
    text_asia = (
        "MARKET: ~$2.5B (15% Growth)\n"
        "FOCUS: Aqua + Swine + Pet\n"
        "──────────────────────────────\n"
        "RETAILERS:\n"
        "• Pet Circle, HuFT (India)\n"
        "• Aeon Pet, Shopee\n"
        "NUTRA/PREMIX MFRS:\n"
        "• CJ CheilJedang, Nutreco\n"
        "• Zhejiang Medicine\n"
        "FOOD/FEED MAJORS:\n"
        "• Thai Union, CP Foods\n"
        "STARTUPS: Sea6, Drools\n"
        "INVESTORS: Temasek"
    )
    # Box in West Pacific (Right side)
    box_x, box_y = 120, 10
    title_x, title_y = 120, 55
    pin_x, pin_y = 105, 35 # China/SE Asia overlap
    
    ax.text(title_x, title_y, "ASIA-PACIFIC", fontsize=font_size_title, fontweight='bold', color=col_asia, ha='left',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=col_asia, alpha=1.0))
    ax.text(box_x, box_y, text_asia, fontsize=font_size_text, va='top', ha='left', family='sans-serif', weight='bold',
            bbox=dict(boxstyle="round,pad=0.6", fc="white", ec=col_asia, alpha=0.9, lw=2))
    ax.plot([title_x + 10, pin_x], [title_y - 2, pin_y], color=col_asia, marker='o', markersize=8, linewidth=2)


    # LATAM
    text_latam = (
        "MARKET: ~$1.2B (Agri-Focus)\n"
        "FOCUS: Feed Efficiency\n"
        "──────────────────────────────\n"
        "RETAILERS:\n"
        "• Petz, Cobasi, Sodimac\n"
        "NUTRA/PREMIX MFRS:\n"
        "• Ourofino, Vetnil\n"
        "FOOD/FEED MAJORS:\n"
        "• BRF, Cargill, ADM, JBS\n"
        "STARTUPS:\n"
        "• Pasture Bio, Omeat\n"
        "INVESTORS: Riverwood, Softbank"
    )
    # Box in South Atlantic (East of Brazil)
    box_x, box_y = -35, -50
    title_x, title_y = -35, -5
    pin_x, pin_y = -55, -15 # Brazil
    
    ax.text(title_x, title_y, "LATAM", fontsize=font_size_title, fontweight='bold', color=col_latam, ha='left',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=col_latam, alpha=1.0))
    ax.text(box_x, box_y, text_latam, fontsize=font_size_text, va='top', ha='left', family='sans-serif', weight='bold',
            bbox=dict(boxstyle="round,pad=0.6", fc="white", ec=col_latam, alpha=0.9, lw=2))
    ax.plot([title_x, pin_x], [title_y - 2, pin_y], color=col_latam, marker='o', markersize=8, linewidth=2)


    # === GLOBAL STATS FOOTER ===
    rect_footer = patches.Rectangle((-180, -90), 360, 18, facecolor='#003057', alpha=1.0) # Increased height
    ax.add_patch(rect_footer)
    
    ax.text(-120, -82, "VC/PE ACTIVITY\nHigh Velocity in Pet Health", ha='center', va='center', color='white', fontweight='bold', fontsize=16)
    ax.text(0, -82, "GLOBAL CONSOLIDATION\nStrategics Acquiring Clinical Brands", ha='center', va='center', color='white', fontweight='bold', fontsize=16)
    ax.text(120, -82, "REGULATORY TAILWINDS\nUS (Innovative FEED) & EU (Green Deal)", ha='center', va='center', color='white', fontweight='bold', fontsize=16)

    # Save
    output_path = 'report/master_report/figures/Global_Map_V11_Final.png'
    plt.savefig(output_path, dpi=400, bbox_inches='tight') # Increased DPI
    print(f"Figure saved to {output_path}")

if __name__ == "__main__":
    create_summary_map()

