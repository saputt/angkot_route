from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import numpy as np

def clean_text(t):
    if not t: return ""
    t = t.replace('\u00a0', ' ').replace('\u2013', '-').replace('\u2014', '-').replace('\u2015', '-')
    return " ".join(t.split()).strip()

def clean_jurusan_full(text):
    text = re.sub(r'\s*\(\d+[A-Z]?\)', '', text)
    text = re.sub(r'\s*-\s*\d+\s*jam', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*\(.*\d+.*\)', '', text)
    return clean_text(text)

def get_terminal_key(text):
    text_fixed = clean_text(text).upper().replace('-', ' ')
    words = re.findall(r'\b[A-Z]{4,}\b', text_fixed)
    return frozenset(words) if len(words) >= 2 else text_fixed

def scrape_angkot_to_v2(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    content = soup.find('div', class_='entry-content')
    lines = [clean_text(l) for l in content.get_text(separator="\n").split('\n') if clean_text(l)]

    raw_data = []
    c_warna = "N/A"

    for i, line in enumerate(lines):
        h_match = re.search(r'^([A-Za-z\s-]+)\s*\((\d+[A-Z]?)\)$', line)
        if h_match:
            c_warna = clean_text(h_match.group(1))
            continue
        elif len(line.split()) <= 4 and "-" in line and "Jl." not in line:
            c_warna = clean_text(line)
            continue

        if "Jl." in line or "Terminal" in line:
            jurusan_raw = lines[i-1] if i > 0 else "N/A"
            roads = [r.strip() for r in re.split(r' – | - | -', line) if r.strip()]
            
            raw_data.append({
                "warna": c_warna,
                "jurusan_raw": jurusan_raw,
                "jurusan_clean": clean_jurusan_full(jurusan_raw),
                "key": get_terminal_key(jurusan_raw),
                "rute": roads
            })

    df = pd.DataFrame(raw_data)
    processed = np.zeros(len(df), dtype=bool)
    final_list = []
    current_id = 1

    for i in range(len(df)):
        if processed[i]: continue
        
        row_a = df.iloc[i]
        match_idx = -1
        
        for j in range(i + 1, len(df)):
            if processed[j]: continue
            row_b = df.iloc[j]
            if row_a['key'] == row_b['key'] and isinstance(row_a['key'], frozenset):
                match_idx = j
                break
        
        forward_streets = row_a['rute']
        
        forward_geometry = [[None, None] for _ in forward_streets]
        
        if match_idx != -1:
            backward_streets = df.iloc[match_idx]['rute']
            backward_geometry = [[None, None] for _ in backward_streets]
            processed[match_idx] = True
        else:
            backward_streets = forward_streets[::-1]
            backward_geometry = forward_geometry[::-1]

        final_list.append({
            "id_angkot": current_id,
            "warna": row_a['warna'],
            "jurusan": row_a['jurusan_clean'],
            "forward": {
                "lintasan_jalan": forward_streets,
                "geometry": forward_geometry
            },
            "backward": {
                "lintasan_jalan": backward_streets,
                "geometry": backward_geometry
            }
        })
        
        processed[i] = True
        current_id += 1

    return final_list

data_v2 = scrape_angkot_to_v2('maranatha.html')

json_filename = 'data_angkot_v2_clean.json'
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(data_v2, f, indent=4, ensure_ascii=False)

print(f"File disimpan di: {json_filename}")