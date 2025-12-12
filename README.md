# University Analytics Dashboard

## 📋 Deskripsi Project

Dashboard analytics untuk universitas yang menampilkan insights tentang:

- Student enrollment dan demographics
- Academic program performance
- Faculty statistics
- Financial metrics
- Course statistics

## 🎯 Objectives

Sesuai dengan tugas mata kuliah Data Insight:

1. Evaluasi kritis dashboard existing (Montana University System)
2. Perancangan dan implementasi dashboard universitas sendiri
3. Menggunakan Python dengan framework modern (Streamlit/Dash)

## 🚀 Quick Start

### Prasyarat

- Python 3.9+
- pip atau conda
- Git (optional)

### Installation

```bash
# Clone atau download project ini
git clone https://github.com/Mudhya19/University-Analytics-Dashboard.git
cd University-Analytics-Dashboard

# Run setup script
chmod +x setup.sh
./setup.sh

# Atau manual setup
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# atau
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Running the Dashboard

```bash
# Activate virtual environment
source .venv/bin/activate

# Run Streamlit app
streamlit run src/dashboard/app.py
```

Aplikasi akan berjalan di: `http://localhost:8501`

## 📁 Project Structure

```
University-Analytics-Dashboard/
├── .venv/                      # Virtual environment
├── src/                        # Source code
│   ├── dashboard/              # Dashboard applications
│   │   └── app.py             # Main Streamlit app
│   ├── data/                  # Data processing
│   │   ├── loader.py          # Data loading utilities
│   │   └── simulasi_kampus_indonesia.py  # Data simulation script
│   └── utils/                 # Utility functions
├── notebooks/                 # Jupyter notebooks
├── docs/                      # Documentation
├── database/                  # Database files
│   ├── data/                  # Data files (.csv, .xlsx)
│   └── schemas/               # Database schemas
├── images/                    # Project images
│   ├── screenshots/           # Dashboard screenshots
│   └── mockups/              # UI mockups
├── output/                    # Generated outputs
│   ├── reports/              # Reports
│   └── exports/              # Data exports
├── tests/                     # Unit tests
├── config/                    # Configuration files
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
├── setup.sh                  # Setup script
└── README.md                 # This file
```

## 📊 Dashboard Pages

1. **Home** - Landing page
2. **Overview** - High-level KPIs and metrics
3. **Student Analytics** - Student enrollment and demographics
4. **Academic Programs** - Program performance and statistics
5. **Finance** - Financial metrics and budgets
6. **Settings** - Dashboard configuration

## 📚 Data Sources

- Local CSV/Excel files
- Kaggle datasets
- Public university APIs
- Simulated data
- Realistic Indonesian university data generated through simulation program

## 🛠 Technologies Used

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Database**: SQLite, SQLAlchemy
- **Testing**: Pytest
- **Version Control**: Git

## 📝 Tasks

- [ ] Complete data exploration
- [ ] Design dashboard layouts
- [ ] Implement core visualizations
- [ ] Add interactive filters
- [ ] Performance optimization
- [ ] Testing & QA
- [ ] Deployment

## 🔗 Links

- [Project Repository](https://github.com/Mudhya19/University-Analytics-Dashboard.git)
- [Montana University Dashboard](https://mus.edu)

## 📄 Laporan Analisis

Untuk informasi lebih lengkap tentang evaluasi kritis dashboard existing (Montana University System), silakan merujuk ke laporan analisis lengkap:

- [Laporan Analisis Dashboard MUS](docs/Laporan%20Analisis%20Dashboard%20MUS.pdf)
- [Streamlit Web App](https://university-analytics-dashboard.streamlit.app/)

Laporan ini berisi analisis mendalam tentang:

- Analisis pengguna (User Analysis)
- Evaluasi UX/UI dan fitur-fitur dashboard
- Analisis konten data yang ditampilkan
- Rekomendasi perbaikan dan pengembangan

## 📄 License

This project is for educational purposes (Data Insight Course).

---

## 🎲 Program Simulasi Dataset

Program ini menyediakan simulasi data universitas Indonesia yang realistis untuk keperluan analisis dan visualisasi dashboard. Source code untuk mendapatkan dataset dapat ditemukan di file `src/data/simulasi_kampus_indonesia.py`.

### Program Simulasi

Program simulasi dibuat untuk menghasilkan data mahasiswa, mata kuliah, dan KRS (Kartu Rencana Studi) secara otomatis. Simulasi ini mencakup berbagai faktor realistis seperti:

- **Data Mahasiswa**: Terdiri dari 42,000 record mahasiswa dari berbagai program studi dan angkatan
- **Program Studi**: Melibatkan berbagai fakultas termasuk Teknologi Industri, Ekonomi & Bisnis, Kedokteran, Keguruan & Ilmu Pendidikan, Hukum, Ilmu Sosial & Humaniora, Matematika & Ilmu Pengetahuan Alam, Agama Islam, Psikologi, dan Ilmu Budaya
- **Jenjang Pendidikan**: D3, D4, S1, S2, S3, dan Profesi
- **Anomali Data**: Program juga menyisipkan data anomali seperti missing values, duplikat, outliers, dan format tidak konsisten untuk merepresentasikan kondisi data nyata

### Struktur Dataset

Dataset terdiri dari tiga tabel utama:

- **mahasiswa_simulasi.csv**:
  - id_mahasiswa: ID unik mahasiswa berdasarkan angkatan
  - kampus: Nama kampus (Universitas Islam Indonesia dalam simulasi ini)
  - prodi: Program studi mahasiswa
  - angkatan: Tahun masuk mahasiswa
  - status: Status mahasiswa (AKTIF, CUTI, LULUS, DO)
  - jalur_masuk: Jalur penerimaan (Mandiri, Beasiswa, Transfer, Alih Jenjang)
  - jenjang: Jenjang pendidikan (D3, S1, S2, dll.)
  - jenis_kelamin: Jenis kelamin (L/P)
  - ipk: Indeks Prestasi Kumulatif

### Smart Questions & Insights

Dashboard ini dirancang untuk menjawab pertanyaan-pertanyaan cerdas (smart questions) mengenai kinerja universitas, antara lain:

1. Specific: Apa yang menjadi faktor utama yang mempengaruhi tingkat kelulusan mahasiswa?
2. Measurable: Berapa persentase mahasiswa yang berhasil menyelesaikan studi tepat waktu?
3. Achievable: Dapatkah kita mengidentifikasi mahasiswa berisiko putus kuliah sejak dini?
4. Relevant: Bagaimana hubungan antara IPK, kehadiran, dan hasil akademik?
5. Time-bound: Bagaimana tren akademik mahasiswa dari tahun ke tahun?

### Fitur dan Visualisasi

Dashboard ini menyediakan berbagai fitur dan visualisasi penting untuk menganalisis kinerja universitas:

#### Fitur Utama:

- **Dashboard Interaktif**: Antarmuka berbasis web yang mudah digunakan
- **Filter Dinamis**: Filter berdasarkan kampus, prodi, angkatan, dan kriteria lainnya
- **Visualisasi Real-time**: Grafik yang langsung diperbarui saat filter diubah
- **Export Data**: Kemampuan mengekspor data dan grafik ke berbagai format
- **Data Cleaning Tools**: Fitur untuk mengidentifikasi dan membersihkan data anomali

#### Visualisasi yang Tersedia:

- **Tren Mahasiswa**: Grafik garis menunjukkan jumlah mahasiswa per angkatan
- **Distribusi Prodi**: Pie chart dan bar chart distribusi mahasiswa per program studi
- **IPK Analysis**: Box plot dan histogram distribusi IPK
- **Status Mahasiswa**: Donut chart distribusi status mahasiswa (aktif, cuti, lulus, DO)
- **Jalur Masuk**: Bar chart distribusi jalur masuk mahasiswa
- **Nilai Akademik**: Heatmap dan scatter plot hubungan antara nilai dan IPK
- **Kinerja Mata Kuliah**: Grafik distribusi nilai per mata kuliah

#### Komponen Utama:

- **Frontend**: Streamlit untuk antarmuka dashboard interaktif
- **Backend**: Python dengan pandas, numpy untuk pemrosesan data
- **Visualisasi**: Plotly untuk grafik interaktif, Matplotlib/Seaborn untuk grafik statistik
- **Data Processing**: Modul untuk membersihkan dan memproses data sebelum visualisasi
- **Configuration**: Sistem konfigurasi untuk mengatur parameter dashboard

### Kesimpulan

Program simulasi ini memberikan dataset yang realistis dengan berbagai kompleksitas dan anomali yang sering ditemui dalam data nyata. Hal ini memungkinkan analis data untuk:

- Melatih kemampuan data cleaning dan preprocessing
- Menguji berbagai teknik visualisasi dan analisis
- Mengidentifikasi pola dan insight penting dari data universitas
- Menyediakan dasar yang kuat untuk pengambilan keputusan berbasis data di lingkungan universitas

Dashboard ini merupakan alat yang komprehensif untuk menganalisis dan memvisualisasikan data universitas, dengan fokus pada kinerja akademik, demografi mahasiswa, dan efektivitas program pendidikan.

---

**Last Updated**: December 2025
**Version**: 1.0
