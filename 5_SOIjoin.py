import json
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

def spatial_join_soi(angkot_file, soi_file, output_file, radius_meter=200):
    with open(angkot_file, 'r') as f:
        angkot_data = json.load(f)
    with open(soi_file, 'r') as f:
        soi_data = json.load(f)

    for place in soi_data:
        id_angkot_lewat = []
        p_lat, p_lng = place['lat'], place['lng']

        for angkot in angkot_data:
            found = False
            for arah in ['forward', 'backward']:
                if found: break
                for coord in angkot[arah]['geometry']:
                    dist = calculate_distance(p_lat, p_lng, coord[0], coord[1])
                    if dist <= radius_meter:
                        id_angkot_lewat.append(angkot['id_angkot'])
                        found = True
                        break
        
        place['id_angkot_lewat'] = list(set(id_angkot_lewat))

    with open(output_file, 'w') as f:
        json.dump(soi_data, f, indent=4)

spatial_join_soi('data_angkot_v2_FINAL.json', 'soi.json', 'soi_final.json')