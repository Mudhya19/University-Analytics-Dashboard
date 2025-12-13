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
        font-size: 1.5rem;
        color: #2e75b6;
        border-bottom: 2px solid #2e75b6;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🎓 Dashboard Analitik Universitas</h1>', unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('./database/data/mahasiswa_simulasi.csv')
    # Convert date columns if they exist
    for col in df.columns:
        if 'tanggal' in col.lower() or 'date' in col.lower() or 'waktu' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
    return df

# Function to calculate KPIs
def calculate_kpis(df):
    total_mahasiswa = len(df)
    
    # KPI untuk mahasiswa aktif
    aktif_mask = df['status'].str.upper() == 'AKTIF'
    total_aktif = df[aktif_mask]['status'].count()
    
    # KPI untuk mahasiswa lulus
    lulus_mask = df['status'].str.upper() == 'LULUS'
    total_lulus = df[lulus_mask]['status'].count()
    
    # KPI untuk IPK rata-rata
    avg_ipk = df['ipk'].mean()
    
    # KPI untuk distribusi jalur masuk
    jalur_masuk_dist = df['jalur_masuk'].value_counts()
    
    # KPI untuk distribusi jenjang
    jenjang_dist = df['jenjang'].value_counts()
    
    # KPI untuk jumlah mahasiswa per angkatan
    angkatan_dist = df['angkatan'].value_counts().sort_index()
    
    return {
        'total_mahasiswa': total_mahasiswa,
        'total_aktif': total_aktif,
        'total_lulus': total_lulus,
        'persentase_aktif': (total_aktif / total_mahasiswa * 10) if total_mahasiswa > 0 else 0,
        'persentase_lulus': (total_lulus / total_mahasiswa * 100) if total_mahasiswa > 0 else 0,
        'avg_ipk': avg_ipk,
        'jalur_masuk_dist': jalur_masuk_dist,
        'jenjang_dist': jenjang_dist,
        'angkatan_dist': angkatan_dist
    }

try:
    df = load_data()
    st.success(f"Dataset berhasil dimuat! Bentuk: {df.shape}")
    
    # Calculate KPIs
    kpis = calculate_kpis(df)
except FileNotFoundError:
    st.error("Dataset 'mahasiswa_simulasi.csv' tidak ditemukan. Pastikan file tersebut ada.")
    st.stop()

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
    else:
        df_filtered = df
else:
    df_filtered = df

# Column selection for analysis
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

selected_columns = st.sidebar.multiselect("Pilih Kolom untuk Analisis", numeric_columns + categorical_columns, default=numeric_columns + categorical_columns)

# Filter functionality - allow filtering by a single numeric column if only one is selected
if selected_columns and len(selected_columns) == 1:
    selected_single_column = selected_columns[0]
    if selected_single_column in numeric_columns:
        # Filter based on selected column
        col_min, col_max = float(df_filtered[selected_single_column].min()), float(df_filtered[selected_single_column].max())
        col_range = st.sidebar.slider(
            f"Rentang untuk {selected_single_column}",
            min_value=col_min,
            max_value=col_max,
            value=(col_min, col_max)
        )
        df_filtered = df_filtered[
            (df_filtered[selected_single_column] >= col_range[0]) &
            (df_filtered[selected_single_column] <= col_range[1])
        ]
# If multiple columns are selected, no numeric filtering is applied

# Display KPIs at the top of the dashboard
st.markdown('<h2 class="section-header">KPI Utama</h2>', unsafe_allow_html=True)

# Create KPI cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{kpis['total_mahasiswa']:,}</h3>
            <p>Total Mahasiswa</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{kpis['total_aktif']:,}</h3>
            <p>Mahasiswa Aktif</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{kpis['total_lulus']:,}</h3>
            <p>Mahasiswa Lulus</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{kpis['persentase_aktif']:.1f}%</h3>
            <p>Persen Aktif</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{kpis['avg_ipk']:.2f}</h3>
            <p>Rata-rata IPK</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display dashboard directly without tabs
st.markdown('<h2 class="section-header">Dashboard Visualisasi</h2>', unsafe_allow_html=True)

# Tambahkan filter tahun angkatan di sini
st.sidebar.subheader("Filter Tahun Angkatan")
tahun_angkatan_cols = [col for col in df.columns if 'angkatan' in col.lower() or 'tahun' in col.lower() or 'year' in col.lower()]
if tahun_angkatan_cols:
    selected_tahun_angkatan_tab3 = st.sidebar.selectbox("Pilih Tahun Angkatan", ["Semua"] + tahun_angkatan_cols, key="tab3_year_filter")
    
    if selected_tahun_angkatan_tab3 != "Semua":
        unique_years = df[selected_tahun_angkatan_tab3].unique()
        selected_year_tab3 = st.sidebar.selectbox(f"Pilih Tahun dari {selected_tahun_angkatan_tab3}", ["Semua"] + list(unique_years), key="tab3_selected_year")
        
        if selected_year_tab3 != "Semua" and selected_year_tab3:
            df_filtered_visual = df[df[selected_tahun_angkatan_tab3] == selected_year_tab3]
        else:
            df_filtered_visual = df
    else:
        df_filtered_visual = df
else:
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

# st.subheader("📊 Jenis-Jenis Visualisasi")

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
                        title=f"Distribusi Mahasiswa per {selected_cat_col} (Berdsarkan {selected_gender_col})")
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
                            title=f"Distribusi Mahasiswa per {selected_cat_col} (Berdsarkan {selected_gender_col})")
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

# Visualisasi 3: Pie Chart
st.markdown("### 🥧 Pie Chart - Proporsi Mahasiswa berdasarkan Gender atau Status")
gender_status_cols = [col for col in categorical_columns if 'gender' in col.lower() or 'jk' in col.lower() or 'kelamin' in col.lower() or 'status' in col.lower() or 'aktif' in col.lower()]
if gender_status_cols:
    selected_pie_col = st.selectbox("Pilih Kolom untuk Pie Chart", gender_status_cols, key="pie_chart_select")
    if selected_pie_col:
        pie_data = df_filtered_visual[selected_pie_col].value_counts()
        fig_pie = px.pie(pie_data, values=pie_data.values, names=pie_data.index,
                        title=f"Proporsi Mahasiswa berdasarkan {selected_pie_col}")
        st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.warning("Tidak ditemukan kolom gender atau status untuk pie chart. Menggunakan kolom kategorikal pertama sebagai contoh.")
    if categorical_columns:
        selected_pie_col = categorical_columns[0]
        pie_data = df_filtered_visual[selected_pie_col].value_counts()
        fig_pie = px.pie(pie_data, values=pie_data.values, names=pie_data.index,
                        title=f"Proporsi Mahasiswa berdasarkan {selected_pie_col}")
        st.plotly_chart(fig_pie, use_container_width=True)

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

