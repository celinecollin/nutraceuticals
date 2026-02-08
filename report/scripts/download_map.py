import urllib.request
import os

def download_map():
    # Standard Equirectangular Projection Map (2000px width)
    # Source: Wikimedia Commons (Blank Map)
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/World_map_blank_without_borders.svg/2000px-World_map_blank_without_borders.svg.png"
    output_path = "report/master_report/figures/base_world_map.png"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Downloading map from {url}...")
    try:
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
            
        print(f"Map saved to {output_path}. Size: {len(data)} bytes")
    except Exception as e:
        print(f"Error downloading map: {e}")
        # Fallback to creating a blank white image if download fails, to prevent crash
        from PIL import Image
        img = Image.new('RGB', (2000, 1000), color='white')
        img.save(output_path)
        print("Created blank fallback image.")

if __name__ == "__main__":
    download_map()
