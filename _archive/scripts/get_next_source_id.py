import pandas as pd
import re

def get_next_s_id():
    registry_path = '/Users/celinecollin/Library/CloudStorage/OneDrive-Personal/Nutraceuticals/_registry/source_registry.xlsx'
    try:
        df = pd.read_excel(registry_path, sheet_name='Sources')
        # Extract numbers from S001, S002, etc.
        # Assuming column 'source_id' exists
        ids = df['source_id'].dropna().astype(str).tolist()
        max_id = 0
        for s_id in ids:
            match = re.search(r'S(\d+)', s_id)
            if match:
                num = int(match.group(1))
                if num > max_id:
                    max_id = num
        
        print(f"Max Source ID: S{max_id:03d}")
        print(f"Next Source ID: S{max_id+1:03d}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_next_s_id()
