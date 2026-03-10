## 🚲 Bike Sharing Data Analytics Dashboard

Proyek ini merupakan submission untuk tugas akhir analisis data. Tujuan dari proyek ini adalah untuk menganalisis dataset Bike Sharing guna memahami pola penggunaan sepeda berdasarkan tipe hari (hari kerja vs hari libur), membedah pengaruh kondisi cuaca terhadap perilaku penyewaan di jam sibuk, serta menerapkan teknik analisis lanjutan berupa Clustering (Binning) suhu udara.

## 🚀 Fitur Dashboard
- Filter Rentang Waktu: Pengguna dapat memfilter data metrik harian berdasarkan tanggal tertentu.
- Visualisasi Pola Jam Sibuk: Membandingkan tren penyewaan antara pengguna Casual dan Registered pada hari kerja dan akhir pekan.
- Visualisasi Dampak Cuaca: Menganalisis bagaimana perubahan cuaca memengaruhi loyalitas pengguna komuter (Registered) di jam-jam sibuk.
- Analisis Lanjutan (Clustering): Mengelompokkan suhu udara ke dalam 4 kategori kenyamanan (Dingin, Sejuk, Hangat, Panas) untuk melihat performa penyewaan.

## 🛠️ Cara Menjalankan Dashboard Secara Lokal
- Masuk ke direktori proyek:
Buka terminal dan arahkan ke folder proyek ini.

- Instal semua library yang dibutuhkan:
Jalankan perintah berikut di terminal:
```
pip install -r requirements.txt
```
- Jalankan aplikasi Streamlit:
Masuk ke dalam folder dashboard dan jalankan aplikasinya:
```
cd dashboard
streamlit run dashboard.py
```
(Atau jika menggunakan Windows PowerShell: python -m streamlit run dashboard.py)

## 📝 Kesimpulan Analisis
Berdasarkan hasil pengolahan dan eksplorasi data yang telah dilakukan pada dataset Bike Sharing, dapat ditarik beberapa simpulan utama sebagai berikut:
- Karakteristik Pengguna Berdasarkan Waktu: Terdapat polarisasi perilaku yang cukup linier antara segmentasi pengguna dengan tipe hari operasional. Pada hari kerja (Working Day), kurva distribusi didominasi oleh pengguna registered yang membentuk pola bimodal, dengan puncak aktivitas sinkron terhadap jam komuter (08.00 pagi dan 17.00-18.00 sore). Sebaliknya, pada akhir pekan atau hari libur, komposisi bergeser merata di siang hingga sore hari, yang mengindikasikan peralihan fungsi armada menjadi sarana rekreasi bagi pengguna casual.
- Sensitivitas Permintaan Terhadap Cuaca: Analisis pada jendela waktu komuter menunjukkan bahwa demand bersifat sangat elastis terhadap cuaca. Pergeseran cuaca menuju hujan ringan hingga badai terbukti mendisrupsi stabilitas penyewaan pengguna registered secara signifikan.
- Optimasi Operasional Berbasis Suhu Udara: Melalui metode clustering (Binning) terhadap atribut suhu, ditemukan bahwa sweet spot penyewaan maksimal terjadi pada klaster suhu "Hangat". Sebagai implikasi manajerial, periode dengan dominasi klaster suhu "Dingin" dapat diutilisasi sebagai momentum optimal untuk melakukan perawatan unit skala besar.
