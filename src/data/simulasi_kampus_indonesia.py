import numpy as np
import pandas as pd

# ============================================================
# 1. DAFTAR KAMPUS (GANTI SENDIRI DENGAN KAMPUS INDONESIA)
# ============================================================

campuses = [
    "Universitas Islam Indonesia",
]

# ============================================================
# 2. SIMULASI DATA MAHASISWA
# ============================================================

np.random.seed(42)  # supaya hasil konsisten

n_students = 42000  # total mahasiswa simulasi (termasuk S1-S3 dan profesi) - 30000 sekarang + 6000 baru (2024-2025)

prodi_rumpun = [
    # Fakultas Teknologi Industri
    "Teknik Informatika",
    "Teknik Elektro",
    "Teknik Industri",
    "Teknik Kimia",
    "Teknik Sipil",
    "Arsitektur",
    "Teknik Mesin",
    
    # Fakultas Ekonomi & Bisnis
    "Manajemen",
    "Akuntansi",
    "Ekonomi Syariah",
    "Bisnis Digital",
    
    # Fakultas Kedokteran
    "Kedokteran",
    "Farmasi",
    "Profesi Apoteker",
    
    # Fakultas Keguruan & Ilmu Pendidikan
    "Pendidikan Teknik Elektro",
    "Pendidikan Teknik Informatika",
    "Pendidikan Bahasa Inggris",
    "Pendidikan Guru PAUD",
    "Pendidikan Guru SD",
    
    # Fakultas Hukum
    "Ilmu Hukum",
    
    # Fakultas Ilmu Sosial & Humaniora
    "Ilmu Komunikasi",
    "Hubungan Internasional",
    "Sastra Arab",
    "Sastra Inggris",
    
    # Fakultas Matematika & Ilmu Pengetahuan Alam
    "Matematika",
    "Fisika",
    "Biologi",
    "Kimia",
    "Farmasi",
    
    # Fakultas Agama Islam
    "Komunikasi dan Penyiaran Islam",
    "Pendidikan Agama Islam",
    "Perbankan Syariah",
    "Ilmu Al-Quran dan Tafsir",
    "Sejarah Kebudayaan Islam",
    
    # Fakultas Psikologi
    "Psikologi",
    
    # Fakultas Ilmu Budaya
    "Ilmu Perpustakaan",
]

angkatan_choices = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
status_choices = ["AKTIF", "CUTI", "LULUS", "DO"]
jalur_masuk_choices = ["Mandiri", "Beasiswa", "Transfer", "Alih Jenjang"]
jenjang_choices = ["D3", "D4", "S1", "S2", "S3", "Profesi"]
kelamin_choices = ["L", "P"]

status_probs = [0.55, 0.03, 0.37, 0.05]
jalur_probs = [0.45, 0.25, 0.20, 0.10]
jenjang_probs = [0.08, 0.05, 0.75, 0.07, 0.01, 0.04]
kelamin_probs = [0.48, 0.52]

# Generate angkatan choices first so we can use them for both ID and angkatan field
angkatan_values = np.random.choice(angkatan_choices, size=n_students)

students = pd.DataFrame({
    "id_mahasiswa": [
        int(f"{angkatan}{str(i).zfill(6)}")
        for angkatan, i in zip(
            angkatan_values,
            range(1, n_students + 1)
        )
    ],
    "kampus": np.random.choice(campuses, size=n_students),
    "prodi": np.random.choice(prodi_rumpun, size=n_students),
    "angkatan": angkatan_values,
    "status": np.random.choice(status_choices, p=status_probs, size=n_students),
    "jalur_masuk": np.random.choice(jalur_masuk_choices, p=jalur_probs, size=n_students),
    "jenjang": np.random.choice(jenjang_choices, p=jenjang_probs, size=n_students),
    "jenis_kelamin": np.random.choice(kelamin_choices, p=kelamin_probs, size=n_students),
})
students = students.sort_values(['angkatan', 'prodi', 'id_mahasiswa']).reset_index(drop=True)

# IPK realistis
base_gpa = np.random.normal(loc=3.15, scale=0.25, size=n_students)
students["ipk"] = base_gpa.clip(2.0, 4.0)

mask_lulus = students["status"] == "LULUS"
students.loc[mask_lulus, "ipk"] = (
    students.loc[mask_lulus, "ipk"] + np.random.normal(0.15, 0.10, mask_lulus.sum())
).clip(2.5, 4.0)

# Menambahkan noise dan anomali ke data agar lebih realistis
np.random.seed(42)  # untuk konsistensi

# 1. Menambahkan missing values (data hilang)
missing_fraction = 0.05  # 5% data akan hilang
for col in students.columns:
    if col not in ['id_mahasiswa', 'angkatan']:  # jangan hapus ID dan angkatan
        mask = np.random.rand(len(students)) < missing_fraction
        students.loc[mask, col] = np.nan

# 2. Menambahkan beberapa data duplikat
n_duplicates = int(n_students * 0.02)  # 2% data akan diduplikat
duplicate_indices = np.random.choice(students.index, size=n_duplicates, replace=True)
duplicate_rows = students.loc[duplicate_indices].copy()
students = pd.concat([students, duplicate_rows], ignore_index=True)

# 3. Menambahkan beberapa outliers pada IPK
outlier_fraction = 0.005  # 0.5% data IPK akan menjadi outlier
outlier_indices = np.random.choice(students.index, size=int(len(students) * outlier_fraction), replace=False)
students.loc[outlier_indices, 'ipk'] = np.random.uniform(0, 1, size=len(outlier_indices))

# 4. Menambahkan beberapa data dengan nilai tidak valid
# Beberapa jenis kelamin dengan nilai tidak valid
invalid_gender_indices = np.random.choice(students.index, size=int(len(students) * 0.005), replace=False)
students.loc[invalid_gender_indices, 'jenis_kelamin'] = np.random.choice(['L', 'P'], size=len(invalid_gender_indices))

# 5. Menambahkan beberapa nilai IPK di luar rentang normal (di atas 4.0)
high_gpa_indices = np.random.choice(students.index, size=int(len(students) * 0.002), replace=False)
students.loc[high_gpa_indices, 'ipk'] = np.random.uniform(4.1, 5.0, size=len(high_gpa_indices))

# 6. Menambahkan whitespace dan formatting tidak konsisten
whitespace_indices = np.random.choice(students.index, size=int(len(students) * 0.03), replace=False)
students.loc[whitespace_indices, 'prodi'] = students.loc[whitespace_indices, 'prodi'].apply(lambda x: f" {x} " if pd.notna(x) else x)

# 7. Menambahkan beberapa nilai status yang tidak valid
invalid_status_indices = np.random.choice(students.index, size=int(len(students) * 0.003), replace=False)
students.loc[invalid_status_indices, 'status'] = np.random.choice(['AKTIF', 'LULUS', 'DO', 'CUTI'], size=len(invalid_status_indices))

# 8. Menambahkan beberapa jalur masuk yang tidak valid
invalid_jalur_indices = np.random.choice(students.index, size=int(len(students) * 0.003), replace=False)
students.loc[invalid_jalur_indices, 'jalur_masuk'] = np.random.choice(["Mandiri", "Beasiswa", "Transfer", "Alih Jenjang"], size=len(invalid_jalur_indices))


# ============================================================
# 3. SIMULASI DATA MATA KULIAH & KRS
# ============================================================

# Duplicate definition removed - already defined earlier in the file

n_courses = 150

courses = pd.DataFrame({
    "kode_mk": [f"MK{str(i).zfill(3)}" for i in range(1, n_courses + 1)],
    "nama_mk": [f"Mata Kuliah {i}" for i in range(1, n_courses + 1)],
    "sks": np.random.choice([2, 3], size=n_courses, p=[0.3, 0.7]),
    "prodi": np.random.choice(prodi_rumpun, size=n_courses),
})

# Menambahkan noise dan anomali ke data mata kuliah
np.random.seed(42)

# 1. Menambahkan missing values ke data mata kuliah
missing_fraction_courses = 0.03  # 3% data akan hilang
for col in courses.columns:
    if col != 'kode_mk':  # jangan hapus kode_mk karena itu ID
        mask = np.random.rand(len(courses)) < missing_fraction_courses
        courses.loc[mask, col] = np.nan

# 2. Menambahkan beberapa data duplikat
n_duplicates_courses = int(n_courses * 0.01)  # 1% data akan diduplikat
duplicate_indices_courses = np.random.choice(courses.index, size=n_duplicates_courses, replace=True)
duplicate_rows_courses = courses.loc[duplicate_indices_courses].copy()
courses = pd.concat([courses, duplicate_rows_courses], ignore_index=True)

# 3. Menambahkan beberapa nilai SKS yang tidak valid
invalid_sks_indices = np.random.choice(courses.index, size=int(len(courses) * 0.005), replace=False)
courses.loc[invalid_sks_indices, 'sks'] = np.random.choice([0, 1, 4, 5, 6], size=len(invalid_sks_indices))

# 4. Menambahkan whitespace dan formatting tidak konsisten
whitespace_indices_courses = np.random.choice(courses.index, size=int(len(courses) * 0.02), replace=False)
courses.loc[whitespace_indices_courses, 'nama_mk'] = courses.loc[whitespace_indices_courses, 'nama_mk'].apply(lambda x: f" {x} " if pd.notna(x) else x)

n_krs = 45000

krs = pd.DataFrame({
    "id_krs": range(1, n_krs + 1),
    "id_mahasiswa": np.random.choice(students["id_mahasiswa"], size=n_krs),
    "kode_mk": np.random.choice(courses["kode_mk"], size=n_krs),
    "semester_akademik": np.random.choice(
        ["202/2023 Ganjil", "2022/2023 Genap", "2023/2024 Ganjil"],
        size=n_krs,
    ),
})

nilai_angka = np.random.normal(loc=78, scale=8, size=n_krs).clip(40, 100)
krs["nilai_angka"] = nilai_angka

# Menambahkan noise dan anomali ke data KRS
np.random.seed(42)

# 1. Menambahkan missing values ke data KRS
missing_fraction_krs = 0.04  # 4% data akan hilang
for col in krs.columns:
    if col != 'id_krs':  # jangan hapus ID
        mask = np.random.rand(len(krs)) < missing_fraction_krs
        krs.loc[mask, col] = np.nan

# 2. Menambahkan beberapa data duplikat
n_duplicates_krs = int(n_krs * 0.03)  # 3% data akan diduplikat
duplicate_indices_krs = np.random.choice(krs.index, size=n_duplicates_krs, replace=True)
duplicate_rows_krs = krs.loc[duplicate_indices_krs].copy()
krs = pd.concat([krs, duplicate_rows_krs], ignore_index=True)

# 3. Menambahkan beberapa nilai nilai_angka yang tidak valid (outliers)
outlier_fraction = 0.005  # 0.5% data nilai_angka akan menjadi outlier
outlier_indices = np.random.choice(krs.index, size=int(len(krs) * outlier_fraction), replace=False)
krs.loc[outlier_indices, 'nilai_angka'] = np.random.uniform(0, 39, size=len(outlier_indices))

# 4. Menambahkan beberapa nilai nilai_angka yang di atas rentang normal
high_nilai_indices = np.random.choice(krs.index, size=int(len(krs) * 0.005), replace=False)
krs.loc[high_nilai_indices, 'nilai_angka'] = np.random.uniform(101, 150, size=len(high_nilai_indices))

# 5. Menambahkan beberapa semester yang tidak valid
invalid_semester_indices = np.random.choice(krs.index, size=int(len(krs) * 0.01), replace=False)
krs.loc[invalid_semester_indices, 'semester_akademik'] = np.random.choice(['2021/2022 Ganjil', '2021/2022 Genap', '2024/2025 Ganjil'], size=len(invalid_semester_indices))


def konversi_huruf(x: float) -> str:
    if x >= 85:
        return "A"
    if x >= 75:
        return "B"
    if x >= 65:
        return "C"
    if x >= 55:
        return "D"
    return "E"


krs["nilai_huruf"] = krs["nilai_angka"].apply(konversi_huruf)


# ============================================================
# 4. AGREGASI UNTUK DASHBOARD (ALA MUS, VERSI KAMPUS INDONESIA)
# ============================================================

# a. Jumlah mahasiswa aktif per kampus
aktif_per_kampus = (
    students[students["status"] == "AKTIF"]
    .groupby("kampus")
    .size()
    .reset_index(name="jumlah_mahasiswa_aktif")
    .sort_values("jumlah_mahasiswa_aktif", ascending=False)
)

# b. Tren angkatan per kampus
angkatan_trend = (
    students
    .groupby(["angkatan", "kampus"])
    .size()
    .reset_index(name="jumlah_mhs")
    .sort_values(["angkatan", "kampus"])
)

# c. Distribusi status studi
status_dist = (
    students
    .groupby(["kampus", "status"])
    .size()
    .reset_index(name="jumlah")
    .sort_values(["kampus", "status"])
)

# d. Rata-rata IPK per kampus dan jenjang
ipk_summary = (
    students
    .groupby(["kampus", "jenjang"])
    .agg(
        jumlah_mhs=("id_mahasiswa", "count"),
        rata2_ipk=("ipk", "mean"),
    )
    .reset_index()
    .sort_values(["kampus", "jenjang"])
)

# e. Distribusi mahasiswa per prodi
prodi_dist = (
    students
    .groupby(["kampus", "prodi"])
    .size()
    .reset_index(name="jumlah_mhs")
    .sort_values("jumlah_mhs", ascending=False)
)

# f. Jalur masuk per kampus
jalur_masuk_dist = (
    students
    .groupby(["kampus", "jalur_masuk"])
    .size()
    .reset_index(name="jumlah_mhs")
    .sort_values(["kampus", "jalur_masuk"])
)

# ============================================================
# 5. CONTOH OUTPUT RINGKAS DI TERMINAL
# ============================================================

if __name__ == "__main__":
    print("==== CONTOH DATA MAHASISWA ====")
    print(students.head(), "\n")

    print("==== JUMLAH MAHASISWA AKTIF PER KAMPUS ====")
    print(aktif_per_kampus, "\n")

    print("==== TREN ANGKATAN (5 TAHUN TERAKHIR) ====")
    print(angkatan_trend.head(15), "\n")

    print("==== DISTRIBUSI STATUS STUDI PER KAMPUS ====")
    print(status_dist.head(20), "\n")

    print("==== RATA-RATA IPK PER KAMPUS & JENJANG ====")
    print(ipk_summary.head(20), "\n")

    print("==== DISTRIBUSI MAHASISWA PER PRODI ====")
    print(prodi_dist.head(20), "\n")

    print("==== DISTRIBUSI JALUR MASUK PER KAMPUS ====")
    print(jalur_masuk_dist.head(20), "\n")

    # ============================================================
    # 6. SIMPAN DATASET KE FOLDER database/dataset
    # ============================================================
    
    # Membuat folder jika belum ada
    import os
    os.makedirs("database/data", exist_ok=True)
    
    # Menyimpan data ke file CSV
    students.to_csv("database/data/mahasiswa_simulasi.csv", index=False)
    courses.to_csv("database/data/mata_kuliah_simulasi.csv", index=False)
    krs.to_csv("database/data/krs_simulasi.csv", index=False)
    
    
    print("==== DATASET TELAH DISIMPAN ====")
    print("File disimpan di folder: database/data/")
    print(f"Jumlah mahasiswa: {len(students)}")
    print(f"Jumlah mata kuliah: {len(courses)}")
    print(f"Jumlah KRS: {len(krs)}")
    
    # Menampilkan ringkasan data cleaning yang bisa dilakukan
    print("\n==== RINGKASAN ANOMALI DATA ====")
    print(f"Jumlah missing values di data mahasiswa: {students.isnull().sum().sum()}")
    print(f"Jumlah data duplikat di data mahasiswa: {students.duplicated().sum()}")
    print(f"Jumlah missing values di data mata kuliah: {courses.isnull().sum().sum()}")
    print(f"Jumlah data duplikat di data mata kuliah: {courses.duplicated().sum()}")
    print(f"Jumlah missing values di data KRS: {krs.isnull().sum().sum()}")
    print(f"Jumlah data duplikat di data KRS: {krs.duplicated().sum()}")
    
    # Menampilkan contoh outlier IPK
    ipk_outliers = students[(students['ipk'] < 0) | (students['ipk'] > 4.0)]
    print(f"Jumlah outlier IPK (di luar rentang 0-4.0): {len(ipk_outliers)}")
    
    # Menampilkan contoh nilai-nilai yang tidak valid
    invalid_gender = students[students['jenis_kelamin'].isin(['Laki-laki', 'Perempuan', 'M', 'F', 'X'])]
    print(f"Jumlah jenis kelamin dengan format tidak valid: {len(invalid_gender)}")

