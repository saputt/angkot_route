===========================================================
   PROJECT TUBES: SISTEM INFORMASI RUTE ANGKOT BANDUNG
===========================================================

---
[ 1. ALUR PENGOLAHAN DATA ]
---

Seluruh data rute dalam proyek ini telah melalui empat tahapan utama:

1. Tahap Scraping (Sumber: Maranatha Website):
   - Pengambilan data mentah trayek dilakukan melalui website resmi Universitas 
     Kristen Maranatha (https://www.maranatha.edu/en/trayek-angkot-bandung/).
   - Metode: Ekstraksi data dilakukan langsung dari Source Code HTML halaman 
     tersebut untuk mendapatkan daftar jalan yang dilewati oleh setiap trayek.

2. Tahap Manual Mapping:
   - Berdasarkan daftar jalan hasil scraping, dilakukan penentuan titik koordinat 
     kunci (Latitude & Longitude) secara manual.
   - Penentuan titik manual bertujuan untuk memastikan setiap persimpangan 
     jalan utama pada rute angkot terdata dengan presisi.

3. Tahap Perhalus (Integrasi OSRM API):
   - Koordinat hasil input manual diproses menggunakan OSRM API (Open Source 
     Routing Machine).
   - Fungsi: Melakukan snapping koordinat ke geometri jalan yang tersedia pada 
     peta, sehingga rute tidak berupa garis lurus melainkan mengikuti kontur 
     jalan yang sebenarnya.

4. Tahap Data Cleaning (Pandas & NumPy):
   - Optimasi data dilakukan menggunakan library Pandas dan NumPy di Python.
   - Tujuan: Mengidentifikasi dan menghapus koordinat duplikat atau bertumpuk 
     hasil dari pemrosesan OSRM dan penggabungan manual.
   - Output: File JSON akhir yang optimal, ringan, dan stabil saat diakses 
     oleh aplikasi web dashboard.

---
[ 2. PANDUAN PENGISIAN DATA SOI (POINTS OF INTEREST) ]
---

Langkah-langkah pengisian koordinat fasilitas publik (SOI):

1. Identifikasi lokasi berdasarkan daftar yang telah disediakan (Mall, RS, dll).
2. Tentukan koordinat melalui Google Maps dengan cara klik kanan pada titik 
   lokasi untuk mendapatkan Latitude dan Longitude.
3. Masukkan angka tersebut ke dalam file JSON SOI pada atribut "lat" dan "lng".
4. Pastikan angka koordinat akurat agar integrasi spasial tidak meleset.

---
[ 3. TAHAPAN SELANJUTNYA ]
---

Setelah data SOI lengkap, akan dilakukan proses "Spatial Join" untuk menghubungkan 
titik fasilitas publik dengan jalur angkot terdekat secara otomatis berdasarkan 
radius tertentu (Buffer Analysis).

===========================================================