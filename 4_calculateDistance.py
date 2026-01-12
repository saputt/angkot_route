import json
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def hitung_total_lintasan(coords):
    if not coords or len(coords) < 2:
        return 0.0
    
    total_jarak = 0.0
    for i in range(len(coords) - 1):
        lat1, lon1 = coords[i]
        lat2, lon2 = coords[i+1]
        total_jarak += haversine(lat1, lon1, lat2, lon2)
    
    return round(total_jarak, 2)

def main():
    input_file = './hasil_json/data_angkot_v2_FINAL_CLEAN(4).json'
    output_file = 'data_angkot_v2_WITH_DISTANCE.json'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        dist_f = hitung_total_lintasan(item['forward']['geometry'])
        item['forward']['jarak_km'] = dist_f
        
        dist_b = hitung_total_lintasan(item['backward']['geometry'])
        item['backward']['jarak_km'] = dist_b
        
        print(f"ID {item['id_angkot']} - {item['jurusan']}: {dist_f} km (F) / {dist_b} km (B)")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()