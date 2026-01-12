import json
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    if lat1 is None or lat2 is None: return float('inf') 
    R = 6371000 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

def spatial_join_soi(angkot_file, soi_file, output_file, radius_meter=300): 
    with open(angkot_file, 'r') as f:
        angkot_data = json.load(f)
    with open(soi_file, 'r') as f:
        soi_data = json.load(f)

    # List baru untuk menampung hasil yang sudah "FLAT" (Rata)
    soi_final_flat = []

    # FIX: Loop Kategori dulu, baru Loop Titik
    for category in soi_data:
        kategori_name = category['kategori']
        
        for place in category['titik']:
            # Copy data tempat biar aman
            place_final = place.copy()
            place_final['kategori'] = kategori_name # Simpan info kategori di tiap item
            
            id_angkot_lewat = set() # Pakai set biar gak ada duplikat ID
            p_lat, p_lng = place['lat'], place['lng']

            # Skip kalau koordinat masih kosong (belum diisi temanmu)
            if p_lat is None or p_lng is None:
                continue 

            for angkot in angkot_data:
                found_in_angkot = False
                for arah in ['forward', 'backward']:
                    if found_in_angkot: break
                    # Cek geometry ada atau tidak
                    if 'geometry' in angkot[arah]:
                        for coord in angkot[arah]['geometry']:
                            dist = calculate_distance(p_lat, p_lng, coord[0], coord[1])
                            if dist <= radius_meter:
                                id_angkot_lewat.add(angkot['id_angkot'])
                                found_in_angkot = True
                                break
            
            place_final['id_angkot_lewat'] = list(id_angkot_lewat)
            soi_final_flat.append(place_final)

    # Simpan hasil sebagai List Flat
    with open(output_file, 'w') as f:
        json.dump(soi_final_flat, f, indent=4)
    
spatial_join_soi('data_angkot_v2_WITH_DISTANCE.json', 'SOI.json', 'soi_final.json')