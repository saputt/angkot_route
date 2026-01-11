===========================================================
   SISTEM INFORMASI GEOGRAFIS (SIG): RUTE ANGKOT BANDUNG
===========================================================

[ METODOLOGI PENGOLAHAN DATA ]

1. DATA ACQUISITION (Scraping)
   - Sumber: Website Universitas Maranatha (Trayek Angkot Bandung).
   - Teknik: Ekstraksi Source Code HTML untuk mendapatkan list jalan tekstual.

2. MANUAL SPATIAL MAPPING (Input Koordinat Kunci)
   - Penentuan koordinat Latitude/Longitude manual pada titik-titik persimpangan 
     utama rute angkot berdasarkan hasil scraping.

3. GEOMETRY REFINEMENT (Snapping Road via OSRM API)
   - Menggunakan API OSRM untuk memperhalus garis rute agar mengikuti kontur 
     jalan asli di peta (bukan garis lurus).

4. DATA OPTIMIZATION (Pandas & NumPy Cleaning)
   - Pembersihan data koordinat duplikat dan redudansi menggunakan library 
     Pandas untuk menjamin performa aplikasi di sisi klien (Front-End).

5. SPATIAL RELATIONSHIP (POI Integration)
   - Mengintegrasikan data Point of Interest (POI) dengan rute angkot 
     melalui metode Spatial Join berdasarkan radius aksesibilitas.

6. PRE-COMPUTED ROUTE LOOKUP (Feature)
   - Fitur pencarian rute dikembangkan menggunakan tabel lookup hasil 
     pre-computasi untuk mempercepat proses pencarian rute asal-tujuan.
