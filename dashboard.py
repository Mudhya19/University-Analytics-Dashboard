import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Dashboard Analitik Universitas",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #2e75b6;
        border-bottom: 2px solid #2e75b6;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        text-align: center;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        text-align: center;
    }
    .metric-card h3 {
        margin: 0.2rem 0;
        font-size: 1.8rem;
        color: #1f4e79;
    }
    .metric-card p {
        margin: 0.2rem 0;
        font-size: 1rem;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🎓 Dashboard Analitik Universitas</h1>', unsafe_allow_html=True)

# Load dataset with error handling
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('./database/data/mahasiswa_simulasi.csv')
        # Convert date columns if they exist
        for col in df.columns:
            if 'tanggal' in col.lower() or 'date' in col.lower() or 'waktu' in col.lower() or 'time' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
        return df
    except FileNotFoundError:
        st.error("File './database/data/mahasiswa_simulasi.csv' tidak ditemukan.")
        return pd.DataFrame() # Return empty DataFrame
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {str(e)}")
        return pd.DataFrame() # Return empty DataFrame

# Function to calculate KPIs
def calculate_kpis(df):
    if df.empty:
        return {
            'total_mahasiswa': 0,
            'total_aktif': 0,
            'total_lulus': 0,
            'persentase_aktif': 0,
            'avg_ipk': 0.0
        }
    
    total_mahasiswa = len(df)
    
    # Find status column
    status_col = None
    for col in df.columns:
        if 'status' in col.lower():
            status_col = col
            break
    
    # Count active and graduated students
    total_aktif = 0
    total_lulus = 0
    if status_col and status_col in df.columns:
        total_aktif = df[df[status_col].str.upper() == 'AKTIF'].shape[0]
        total_lulus = df[df[status_col].str.upper() == 'LULUS'].shape[0]
    
    # Find IPK column
    ipk_col = None
    for col in df.columns:
        if 'ipk' in col.lower() or 'gpa' in col.lower():
            ipk_col = col
            break
    
    # Calculate average IPK
    avg_ipk = 0.0
    if ipk_col and ipk_col in df.columns:
        try:
            ipk_values = pd.to_numeric(df[ipk_col], errors='coerce')
            avg_ipk = ipk_values.mean()
            if pd.isna(avg_ipk):
                avg_ipk = 0.0
        except:
            avg_ipk = 0.0
    
    # Calculate percentage of active students
    persentase_aktif = (total_aktif / total_mahasiswa * 100) if total_mahasiswa > 0 else 0
    
    return {
        'total_mahasiswa': total_mahasiswa,
        'total_aktif': total_aktif,
        'total_lulus': total_lulus,
        'persentase_aktif': persentase_aktif,
        'avg_ipk': avg_ipk
    }

# Load data
df = load_data()

# Tambahkan filter tahun angkatan di sini
st.sidebar.subheader("Filter Tahun Angkatan")
tahun_angkatan_cols = [col for col in df.columns if 'angkatan' in col.lower() or 'tahun' in col.lower() or 'year' in col.lower()]
if tahun_angkatan_cols:
    tahun_angkatan_col = tahun_angkatan_cols[0]  # Gunakan kolom tahun angkatan pertama
    unique_tahun = list(set(df[tahun_angkatan_col].dropna().unique()))
    unique_tahun = sorted([int(year) for year in unique_tahun if pd.notna(year)])  # Pastikan hanya tahun valid dan urut
    selected_tahun_angkatan = st.sidebar.selectbox("Pilih Tahun Angkatan", ["Semua"] + unique_tahun, key="tahun_angkatan_filter")
    
    if selected_tahun_angkatan != "Semua":
        df = df[df[tahun_angkatan_col] == selected_tahun_angkatan]  # Apply filter to main df for KPI calculation
else:
    # If no tahun angkatan column found, use original df
    pass

# Tambahkan filter fakultas di sini
st.sidebar.subheader("Filter Fakultas")
# Mencari kolom yang mungkin berisi informasi fakultas/jurusan
fakultas_prodi_cols = [col for col in df.columns if 'fakultas' in col.lower() or 'faculty' in col.lower() or 'prodi' in col.lower() or 'jurusan' in col.lower() or 'department' in col.lower()]
selected_fakultas_col = None  # Inisialisasi variabel
if fakultas_prodi_cols:
    selected_fakultas_col = fakultas_prodi_cols[0] # Gunakan kolom pertama yang ditemukan
    unique_faculties = list(set(df[selected_fakultas_col].dropna().unique()))
    unique_faculties = [fak for fak in unique_faculties if pd.notna(fak)]  # Pastikan hanya nilai yang tidak null
    
    # Ganti selectbox dengan multiselect untuk multi-filter fakultas
    selected_faculties = st.sidebar.multiselect(f"Pilih {selected_fakultas_col}", unique_faculties, default=unique_faculties)
    
    if selected_fakultas_col and selected_fakultas_col in df.columns and selected_faculties:
        df = df[df[selected_fakultas_col].isin(selected_faculties)]  # Apply filter to main df for KPI calculation

# Check if data is loaded successfully
if df.empty:
    st.error("Dataset kosong atau tidak dapat dimuat. Menampilkan KPI default.")
    kpis = {
        'total_mahasiswa': 0,
        'total_aktif': 0,
        'total_lulus': 0,
        'persentase_aktif': 0,
        'avg_ipk': 0.0
    }
else:
    # Calculate KPIs
    kpis = calculate_kpis(df)

# Display KPIs at the top of the dashboard
st.markdown('<h2 class="section-header">1. KPI Utama</h2>', unsafe_allow_html=True)

# Create KPI cards with guaranteed display
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_mahasiswa = kpis.get('total_mahasiswa', 0)
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{total_mahasiswa:,}</h3>
            <p>Total Mahasiswa</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    total_aktif = kpis.get('total_aktif', 0)
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{total_aktif:,}</h3>
            <p>Mahasiswa Aktif</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    total_lulus = kpis.get('total_lulus', 0)
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{total_lulus:,}</h3>
            <p>Mahasiswa Lulus</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    persentase_aktif = kpis.get('persentase_aktif', 0)
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{persentase_aktif:.1f}%</h3>
            <p>Persen Aktif</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    avg_ipk = kpis.get('avg_ipk', 0.0)
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{avg_ipk:.2f}</h3>
            <p>Rata-rata IPK</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display additional information about the data
if not df.empty:
    st.success(f"Dataset berhasil dimuat dengan {len(df)} baris data")
    # st.write("### Informasi Dataset")
    # st.write(f"- Jumlah kolom: {len(df.columns)}")
    # st.write(f"- Nama kolom: {', '.join(df.columns.tolist())}")

# Sidebar filters
st.sidebar.header("Filter Data")

# Date range filter
date_columns = []
for col in df.columns:
    if pd.api.types.is_datetime64_any_dtype(df[col]):
        date_columns.append(col)

selected_date_col = None
if date_columns:
    selected_date_col = st.sidebar.selectbox("Pilih Kolom Tanggal", ["Tidak Ada"] + date_columns)
    
    if selected_date_col != "Tidak Ada":
        min_date = df[selected_date_col].min()
        max_date = df[selected_date_col].max()
        
        # Multi-select date filter
        date_option = st.sidebar.radio("Pilih Jenis Filter Tanggal", ["Rentang Tunggal", "Multi-Tanggal"])
        
        if date_option == "Rentang Tunggal":
            date_range = st.sidebar.date_input(
                "Pilih Rentang Tanggal",
                value=(min_date.date(), max_date.date()),
                min_value=min_date.date(),
                max_value=max_date.date()
            )
            
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                # Convert to datetime for comparison
                start_datetime = pd.Timestamp(start_date)
                end_datetime = pd.Timestamp(end_date)
                mask = (df[selected_date_col] >= start_datetime) & (df[selected_date_col] <= end_datetime)
                df_filtered = df.loc[mask]
            else:
                df_filtered = df
        elif date_option == "Multi-Tanggal":
            # Convert datetime column to date for comparison
            df_dates = pd.to_datetime(df[selected_date_col]).dt.date
            unique_dates = sorted(df_dates.dropna().unique())
            selected_dates = st.sidebar.multiselect(
                "Pilih Tanggal",
                options=unique_dates,
                default=[min_date.date(), max_date.date()]
            )
            
            if selected_dates:
                # Create a mask using the date-only version
                mask = df_dates.isin(selected_dates)
                df_filtered = df.loc[mask]
            else:
                df_filtered = df
    else:
        df_filtered = df
else:
    df_filtered = df

# Column selection for analysis
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

# Now df is already filtered based on sidebar selections, so we use it directly for visualization
df_filtered_visual = df

df_cleaned_visual = df_filtered_visual.copy()
original_shape = df_cleaned_visual.shape

# Isi nilai hilang dengan mean/median
for col in numeric_columns:
    if df_cleaned_visual[col].isnull().any():
        if col in ['age', 'semester', 'ipk', 'nilai']:
            df_cleaned_visual[col].fillna(df_cleaned_visual[col].median(), inplace=True)
        else:
            df_cleaned_visual[col].fillna(df_cleaned_visual[col].mean(), inplace=True)

for col in categorical_columns:
    if df_cleaned_visual[col].isnull().any():
        mode_val = df_cleaned_visual[col].mode()
        if not mode_val.empty:
            df_cleaned_visual[col].fillna(mode_val[0], inplace=True)
        else:
            df_cleaned_visual[col].fillna('Tidak Diketahui', inplace=True)
            
st.sidebar.success("Proses pengisian nilai hilang selesai")

# Hapus baris duplikat
original_len = len(df_cleaned_visual)
df_cleaned_visual = df_cleaned_visual.drop_duplicates()
removed_count = original_len - len(df_cleaned_visual)
st.sidebar.success(f"Hapus {removed_count} baris duplikat")

# Update dataframe yang digunakan untuk visualisasi
df_filtered_visual = df_cleaned_visual
st.sidebar.success("Pembersihan data selesai!")
st.sidebar.metric(label="Ukuran Dataset yang Dibersihkan", value=f"{len(df_cleaned_visual):,} rekaman", delta=f"-{original_shape[0] - len(df_cleaned_visual)} dari ukuran awal")

# Display dashboard section
st.markdown('<h2 class="section-header">2. Dashboard Visualisasi</h2>', unsafe_allow_html=True)

# Visualisasi 1: Bar Chart
st.markdown("### 📊 Bar Chart - Distribusi Mahasiswa per Jurusan/Fakultas")
categorical_cols_for_bar = [col for col in categorical_columns if 'jurusan' in col.lower() or 'fakultas' in col.lower() or 'prodi' in col.lower()]
gender_cols = [col for col in categorical_columns if 'gender' in col.lower() or 'jk' in col.lower() or 'kelamin' in col.lower()]
if categorical_cols_for_bar:
    if categorical_cols_for_bar:
        selected_cat_col = categorical_cols_for_bar[0] # Gunakan kolom pertama
    else:
        selected_cat_col = None
        
    # Check if gender column is available for grouping
    if gender_cols:
        selected_gender_col = gender_cols[0] # Gunakan kolom gender pertama
        # Group by both selected category and gender
        bar_data = df_filtered_visual.groupby([selected_cat_col, selected_gender_col]).size().reset_index()
        bar_data.columns = [selected_cat_col, selected_gender_col, 'Jumlah Mahasiswa']
        
        fig_bar = px.bar(bar_data, x=selected_cat_col, y='Jumlah Mahasiswa', color=selected_gender_col,
                        labels={'x': selected_cat_col, 'y': 'Jumlah Mahasiswa', 'color': selected_gender_col},
                        title=f"Distribusi Mahasiswa per {selected_cat_col} (Berdasarkan {selected_gender_col})")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        # Fallback if no gender column is available
        # Jumlahkan mahasiswa per prodi/jurusan/fakultas
        bar_data = df_filtered_visual[selected_cat_col].value_counts().reset_index()
        bar_data.columns = [selected_cat_col, 'Jumlah Mahasiswa']
        
        fig_bar = px.bar(bar_data, x=selected_cat_col, y='Jumlah Mahasiswa',
                        labels={'x': selected_cat_col, 'y': 'Jumlah Mahasiswa'},
                        title=f"Distribusi Mahasiswa per {selected_cat_col}")
        st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("Tidak ditemukan kolom jurusan/fakultas. Menggunakan kolom kategorikal pertama sebagai contoh.")
    if categorical_columns:
        selected_cat_col = categorical_columns[0]
        gender_cols = [col for col in categorical_columns if 'gender' in col.lower() or 'jk' in col.lower() or 'kelamin' in col.lower()]
        if gender_cols:
            selected_gender_col = gender_cols[0]
            # Group by both selected category and gender
            bar_data = df_filtered_visual.groupby([selected_cat_col, selected_gender_col]).size().reset_index()
            bar_data.columns = [selected_cat_col, selected_gender_col, 'Jumlah Mahasiswa']
            
            fig_bar = px.bar(bar_data, x=selected_cat_col, y='Jumlah Mahasiswa', color=selected_gender_col,
                            labels={'x': selected_cat_col, 'y': 'Jumlah Mahasiswa', 'color': selected_gender_col},
                            title=f"Distribusi Mahasiswa per {selected_cat_col} (Berdasarkan {selected_gender_col})")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            bar_data = df_filtered_visual[selected_cat_col].value_counts().reset_index()
            bar_data.columns = [selected_cat_col, 'Jumlah Mahasiswa']
            
            fig_bar = px.bar(bar_data, x=selected_cat_col, y='Jumlah Mahasiswa',
                            labels={'x': selected_cat_col, 'y': 'Jumlah Mahasiswa'},
                            title=f"Distribusi Mahasiswa per {selected_cat_col}")
            st.plotly_chart(fig_bar, use_container_width=True)

# Visualisasi 2: Line Chart
st.markdown("### 📈 Line Chart - Tren Mahasiswa per Tahun Angkatan")
tahun_angkatan_cols = [col for col in df.columns if 'angkatan' in col.lower() or 'tahun' in col.lower() or 'year' in col.lower()]
if tahun_angkatan_cols:
    selected_tahun_col = tahun_angkatan_cols[0]  # Gunakan kolom tahun angkatan pertama
    if selected_tahun_col:
        line_data = df_filtered_visual.groupby(selected_tahun_col).size().reset_index()
        line_data.columns = [selected_tahun_col, 'Jumlah Mahasiswa']
        fig_line = px.line(line_data, x=selected_tahun_col, y='Jumlah Mahasiswa',
                          title=f"Tren Jumlah Mahasiswa per {selected_tahun_col}")
        st.plotly_chart(fig_line, use_container_width=True)
else:
    st.warning("Tidak ditemukan kolom tahun angkatan untuk line chart.")

# Visualisasi 3: Pie Charts
st.markdown("### 🥧 Pie Chart - Proporsi Mahasiswa berdasarkan Status dan Gender")

# Mencari kolom status
status_cols = [col for col in categorical_columns if 'status' in col.lower() or 'aktif' in col.lower()]
if status_cols:
    selected_status_col = status_cols[0]  # Gunakan kolom status pertama
    if selected_status_col:
        status_data = df_filtered_visual[selected_status_col].value_counts()
        fig_status = px.pie(status_data, values=status_data.values, names=status_data.index,
                           title=f"Proporsi Mahasiswa berdasarkan Status")
        st.plotly_chart(fig_status, use_container_width=True)
else:
    st.warning("Tidak ditemukan kolom status untuk pie chart.")

# Mencari kolom gender
gender_cols = [col for col in categorical_columns if 'gender' in col.lower() or 'jk' in col.lower() or 'kelamin' in col.lower()]
if gender_cols:
    selected_gender_col = gender_cols[0]  # Gunakan kolom gender pertama
    if selected_gender_col:
        gender_data = df_filtered_visual[selected_gender_col].value_counts()
        fig_gender = px.pie(gender_data, values=gender_data.values, names=gender_data.index,
                           title=f"Proporsi Mahasiswa berdasarkan Jenis Kelamin")
        st.plotly_chart(fig_gender, use_container_width=True)
else:
    st.warning("Tidak ditemukan kolom gender untuk pie chart.")

# Visualisasi 4: Histogram
st.markdown("### 📊 Histogram - Distribusi IPK Mahasiswa")
ipk_cols = [col for col in numeric_columns if 'ipk' in col.lower() or 'gpa' in col.lower() or 'indeks' in col.lower()]
if ipk_cols:
    selected_ipk_col = ipk_cols[0]  # Gunakan kolom IPK pertama
    if selected_ipk_col:
        fig_hist = px.histogram(df_filtered_visual, x=selected_ipk_col, nbins=20,
                               title=f"Distribusi {selected_ipk_col} Mahasiswa",
                               labels={selected_ipk_col: selected_ipk_col, 'count': 'Frekuensi'})
        st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.warning("Tidak ditemukan kolom IPK. Menggunakan kolom numerik pertama sebagai contoh.")
    if numeric_columns:
        selected_ipk_col = numeric_columns[0]
        fig_hist = px.histogram(df_filtered_visual, x=selected_ipk_col, nbins=20,
                               title=f"Distribusi {selected_ipk_col} Mahasiswa",
                               labels={selected_ipk_col: selected_ipk_col, 'count': 'Frekuensi'})
        st.plotly_chart(fig_hist, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Dashboard Analitik Universitas © 2025</p>", unsafe_allow_html=True)