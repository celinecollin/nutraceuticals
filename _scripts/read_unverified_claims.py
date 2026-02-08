import pandas as pd
import openpyxl

def get_unverified_claims():
    registry_path = '/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/_registry/source_registry.xlsx'
    try:
        # Read Claims tab
        df = pd.read_excel(registry_path, sheet_name='Claims')
        
        # Filter for UNVERIFIED in source_ids
        # We look for strings containing 'UNVERIFIED', handling NaNs
        unverified = df[df['source_ids'].astype(str).str.contains('UNVERIFIED', na=False)]
        
        print(f"Found {len(unverified)} unverified claims.")
        for index, row in unverified.iterrows():
            print(f"ID: {row['claim_id']}")
            print(f"Content: {row['claim_text']}") # Assuming column name is 'claim_text' or similar, strict check needed?
            # Let's check columns first if this fails, but usually it's 'claim_text' or 'claim'
            print("-" * 20)

    except Exception as e:
        print(f"Error reading registry: {e}")
        # Print columns to debug
        try:
            df = pd.read_excel(registry_path, sheet_name='Claims')
            print("Columns found:", df.columns.tolist())
        except:
            pass

if __name__ == "__main__":
    get_unverified_claims()
