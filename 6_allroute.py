import json

def generate_lookup(soi_final_file, output_file):
    with open(soi_final_file, 'r') as f:
        soi_list = json.load(f)

    route_lookup = {}

    for asal in soi_list:
        asal_id = asal['nama'] 
        route_lookup[asal_id] = {}

        for tujuan in soi_list:
            tujuan_id = tujuan['nama']
            
            if asal_id == tujuan_id:
                continue

            angkot_asal = set(asal['id_angkot_lewat'])
            angkot_tujuan = set(tujuan['id_angkot_lewat'])
            
            angkot_nyambung = list(angkot_asal.intersection(angkot_tujuan))

            if angkot_nyambung:
                route_lookup[asal_id][tujuan_id] = angkot_nyambung
            else:
                route_lookup[asal_id][tujuan_id] = None 

    with open(output_file, 'w') as f:
        json.dump(route_lookup, f, indent=4)
    
    print(f"✅ File Lookup Berhasil Dibuat: {output_file}")

generate_lookup('soi_final.json', 'rute_lookup.json')