import json
import requests
import time

INPUT_FILE = 'data_angkot_v2.json'
OUTPUT_FILE = 'data_angkot_v2_HALUS.json'
MAX_POINTS_PER_CHUNK = 40  
DELAY = 1.5 

def get_osrm_route_chunked(coords):
    if not coords or len(coords) < 2:
        return coords

    all_smoothed_coords = []
    
    for i in range(0, len(coords) - 1, MAX_POINTS_PER_CHUNK - 1):
        chunk = coords[i : i + MAX_POINTS_PER_CHUNK]
        if len(chunk) < 2: continue
        
        coord_str = ";".join([f"{c[1]},{c[0]}" for c in chunk if c[0] is not None])
        url = f"http://router.project-osrm.org/route/v1/driving/{coord_str}"
        
        try:
            response = requests.get(url, params={"overview": "full", "geometries": "geojson"}, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'Ok':
                    new_points = [[c[1], c[0]] for c in data['routes'][0]['geometry']['coordinates']]
                    if all_smoothed_coords:
                        all_smoothed_coords.extend(new_points[1:])
                    else:
                        all_smoothed_coords.extend(new_points)
            else:
                print(f" (Chunk error {response.status_code}) ", end="")
        except Exception as e:
            print(f" (Conn error) ", end="")
        
        time.sleep(0.5) 

    return all_smoothed_coords if all_smoothed_coords else coords

def main():
    print("Mulai Snapping dengan sistem Chunking (Anti-Error 414)...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for index, item in enumerate(data):
        print(f"[{index+1}/{len(data)}] {item['jurusan']}")
        
        print("   - Forward...", end="", flush=True)
        item['forward']['geometry'] = get_osrm_route_chunked(item['forward']['geometry'])
        time.sleep(DELAY)
        
        print("   - Backward...", end="", flush=True)
        item['backward']['geometry'] = get_osrm_route_chunked(item['backward']['geometry'])
        print(" Done.")
        time.sleep(DELAY)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\nSelesai! File disimpan di: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()