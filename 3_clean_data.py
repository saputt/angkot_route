import pandas as pd
import numpy as np
import json

def clean_with_pandas(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for angkot in data:
        for arah in ['forward', 'backward']:
            coords = angkot[arah]['geometry']
            
            if len(coords) > 0:
                df = pd.DataFrame(coords, columns=['lat', 'lng'])
                
                mask = (df.lat != df.lat.shift()) | (df.lng != df.lng.shift())
                df_clean = df[mask]
                
                angkot[arah]['geometry'] = df_clean.values.tolist()
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
clean_with_pandas('hasil_json/data_angkot_v2_HALUS(3).json', 'data_angkot_v2_FINAL_PANDAS.json')