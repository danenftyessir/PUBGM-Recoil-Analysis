# PUBGM_Recoil_Analysis

## Overview

Program ini mengimplementasikan Sistem Persamaan Linear untuk menganalisis dan memprediksi pola recoil senjata dalam PUBG Mobile. Program menggunakan data yang dikumpulkan dari tiga senjata assault rifle populer (AKM, M416, dan SCAR-L) untuk menghasilkan model matematis yang menjelaskan karakteristik recoil vertikal dan horizontal.

## Features

* **Ekstraksi Data**: Mengumpulkan dan memproses data recoil pattern langsung dari PUBG Mobile dengan tingkat akurasi tinggi.

* **Analisis Matematis**: Menerapkan sistem persamaan linear untuk menghasilkan model prediktif yang akurat dari pola recoil.

* **Visualisasi Komprehensif**: Menyajikan representasi visual dari pola recoil dan koefisien untuk pemahaman yang lebih baik.

* **Perbandingan Senjata**: Menyediakan analisis komparatif mendalam antara berbagai jenis assault rifle.

* **Laporan Terperinci**: Menghasilkan dokumentasi lengkap dari hasil analisis untuk referensi dan studi lebih lanjut.

## Requirements

* Python 3.12 atau yang lebih tinggi
* NumPy 2.0.2 atau yang lebih tinggi
* Pandas 2.2.3 atau yang lebih tinggi
* Matplotlib 3.9.3 atau yang lebih tinggi
* Seaborn 0.13.2 atau yang lebih tinggi

## Installation

```bash
# Clone repositori
git clone https://github.com/danenftyessir/PUBGM_Recoil_Analysis.git

# Masuk ke direktori proyek
cd PUBGM_SPL_Recoil_Pattern

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run ekstraksi data
python recoil_extractor.py

# Run pengolahan data
python recoil_processor.py

# Run model recoil
python recoil_model.py

# Run analisis
python recoil_analysis.py
```

## Room for Improvement

* Ekspansi Analisis: Menambahkan dukungan untuk berbagai jenis senjata lainnya dalam game.
* Antarmuka Pengguna: Mengembangkan GUI yang interaktif untuk visualisasi real-time dari pola recoil.
* Sistem Attachment: Mengintegrasikan pengaruh berbagai attachment senjata terhadap pola recoil.
* Peningkatan Akurasi: Mengoptimalkan model prediksi untuk hasil yang lebih akurat.
* Menambah jenis lainnya: Mengembangkan recoil pattern untuk SMG class/LMG class/DMR class.

## Author

* Danendra Shafi Athallah (13523136)
* Institut Teknologi Bandung

