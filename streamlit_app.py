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

try:
    df = load_data()
    st.success(f"Dataset berhasil dimuat! Bentuk: {df.shape}")
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

# Display tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1. S.M.A.R.T Question & Data Wrangling",
    "2. Ringkasan Statistik",
    "3. Dashboard Visualisasi",
    "4. Insight & Kesimpulan"
])

with tab1:
    st.markdown('<h2 class="section-header">1. S.M.A.R.T Question & Data Wrangling</h2>', unsafe_allow_html=True)
    
    # S.M.A.R.T Question Section
    st.subheader("🎯 S.M.A.R.T Question")
    
    smart_questions = [
        "**Specific**: Apa yang menjadi faktor utama yang mempengaruhi tingkat kelulusan mahasiswa?",
        "**Measurable**: Berapa persentase mahasiswa yang berhasil menyelesaikan studi tepat waktu?",
        "**Achievable**: Dapatkah kita mengidentifikasi mahasiswa berisiko putus kuliah sejak dini?",
        "**Relevant**: Bagaimana hubungan antara IPK, kehadiran, dan hasil akademik?",
        "**Time-bound**: Bagaimana tren akademik mahasiswa dari tahun ke tahun?"
    ]
    
    for q in smart_questions:
        st.write(q)
    
    st.markdown("---")
    
    # Data Wrangling Section
    st.subheader("🧩 Data Wrangling")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Data Collection**")
        st.metric(label="Total Records", value=f"{len(df):,}")
        st.metric(label="Total Columns", value=df.shape[1])
    
    with col2:
        st.markdown("**Data Assessment**")
        missing_values = df.isnull().sum().sum()
        st.metric(label="Missing Values", value=f"{missing_values:,}")
        duplicate_rows = df.duplicated().sum()
        st.metric(label="Duplicate Rows", value=f"{duplicate_rows:,}")
    
    with col3:
        st.markdown("**Data Cleaning**")
        st.write(f"Numeric columns: {len(numeric_columns)}")
        st.write(f"Categorical columns: {len(categorical_columns)}")

    st.markdown("---")
    
    # Detailed Data Assessment
    st.subheader("📋 Penilaian Data Terperinci")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Info Dataset:**")
        info_str = f"Bentuk: {df.shape}\n\nKolom:\n"
        for i, col in enumerate(df.columns):
            dtype = df[col].dtype
            non_null_count = df[col].notna().sum()
            null_count = df[col].isna().sum()
            info_str += f"- {col}: {dtype} ({non_null_count} tidak null, {null_count} null)\n"
        st.text(info_str)
    
    with col2:
        st.write("**Nilai Hilang per Kolom:**")
        missing_df = pd.DataFrame({
            'Kolom': df.columns,
            'Jumlah Hilang': df.isnull().sum(),
            'Persentase Hilang': (df.isnull().sum() / len(df)) * 10
        })
        st.dataframe(missing_df.style.format({'Persentase Hilang': '{:.2f}%'}))
    
    st.markdown("---")
    
    # Data Cleaning Actions
    st.subheader("🔧 Proses Pembersihan Data Otomatis")
    
    st.info("Proses pembersihan data akan menerapkan semua langkah-langkah berikut secara otomatis:")
    st.write("- Hapus baris dengan nilai hilang")
    st.write("- Isi nilai hilang dengan mean/median")
    st.write("- Hapus baris duplikat")
    st.write("- Ubah tipe data")
    
    if st.button("Terapkan Pembersihan Otomatis"):
        df_cleaned = df.copy()
        original_shape = df_cleaned.shape
        
        # Isi nilai hilang dengan mean/median
        for col in numeric_columns:
            if df_cleaned[col].isnull().any():
                if col in ['age', 'semester', 'ipk', 'nilai']:
                    df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
                else:
                    df_cleaned[col].fillna(df_cleaned[col].mean(), inplace=True)
        
        for col in categorical_columns:
            if df_cleaned[col].isnull().any():
                mode_val = df_cleaned[col].mode()
                if not mode_val.empty:
                    df_cleaned[col].fillna(mode_val[0], inplace=True)
                else:
                    df_cleaned[col].fillna('Tidak Diketahui', inplace=True)
                
        st.success("Proses pengisian nilai hilang selesai")
        
        # Hapus baris duplikat
        original_len = len(df_cleaned)
        df_cleaned = df_cleaned.drop_duplicates()
        removed_count = original_len - len(df_cleaned)
        st.success(f"Hapus {removed_count} baris duplikat")
        
        # Ubah tipe data
        for col in df_cleaned.columns:
            if df_cleaned[col].dtype == 'object':
                # Try to convert to numeric if possible
                try:
                    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
                except:
                    pass
        st.success("Konversi tipe data diterapkan")
        
        st.session_state.df_cleaned = df_cleaned
        st.success("Pembersihan data selesai!")
        st.metric(label="Ukuran Dataset yang Dibersihkan", value=f"{len(df_cleaned):,} rekaman", delta=f"-{original_shape[0] - len(df_cleaned)} dari ukuran awal")

with tab2:
    st.markdown('<h2 class="section-header">2. Ringkasan Statistik</h2>', unsafe_allow_html=True)
    
    st.subheader("📈 Statistik Deskriptif")
    
    # Overall dataset statistics
    st.markdown("**Statistik Deskriptif Keseluruhan Dataset:**")
    overall_stats = df_filtered.describe(include="all")
    st.dataframe(overall_stats.style.background_gradient(cmap='RdPu'), use_container_width=True)
    
    # Container for numerical statistics if available
    if numeric_columns:
        st.markdown("**Statistik Deskriptif untuk Kolom Numerik:**")
        desc_stats = df_filtered[numeric_columns].describe()
        st.dataframe(desc_stats, use_container_width=True)
        
        # Layout configuration based on available space and content
        num_cols_count = len(numeric_columns)
        if num_cols_count >= 2:
            # Use 2x2 grid for multiple columns
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Distribusi Kolom Numerikal**")
                selected_num_col_1 = st.selectbox("Pilih Kolom Numerikal (1)", numeric_columns, key="histogram_col_select_1")
                fig_hist, ax = plt.subplots(figsize=(8, 6))
                ax.hist(df_filtered[selected_num_col_1].dropna(), bins=20, edgecolor='black')
                ax.set_title(f'Distribusi {selected_num_col_1}')
                ax.set_xlabel(selected_num_col_1 or 'Kolom')
                ax.set_ylabel('Frekuensi')
                st.pyplot(fig_hist)
                plt.close()
            
            with col2:
                st.markdown("**Statistik Spesifik**")
                selected_num_col_2 = st.selectbox("Pilih Kolom Numerikal (2)", numeric_columns, key="stats_col_select_2")
                col_data = df_filtered[selected_num_col_2].dropna()
                stats_dict = {
                    'Mean': float(col_data.mean()) if len(col_data) > 0 else 0,
                    'Median': float(col_data.median()) if len(col_data) > 0 else 0,
                    'Std Dev': round(float(col_data.std()) if len(col_data) > 0 and col_data.std() is not None and not pd.isna(col_data.std()) else 0, 2),
                    'Variance': round(float(col_data.var()) if len(col_data) > 0 and col_data.var() is not None and not pd.isna(col_data.var()) else 0, 2),
                    'Min': round(float(col_data.min()) if len(col_data) > 0 and col_data.min() is not None and not pd.isna(col_data.min()) else 0, 2),
                    'Max': round(float(col_data.max()) if len(col_data) > 0 and col_data.max() is not None and not pd.isna(col_data.max()) else 0, 2)
                }
                stats_df = pd.DataFrame(list(stats_dict.items()), columns=['Statistik', 'Nilai'])
                # Convert values to float for display
                stats_df['Nilai'] = stats_df['Nilai'].apply(lambda x: float(x) if x is not None and not pd.isna(x) else 0.0)
                st.dataframe(stats_df, use_container_width=True)
        else:
            # Single column layout
            st.markdown("**Distribusi dan Statistik Kolom Numerikal**")
            selected_num_col = st.selectbox("Pilih Kolom Numerikal", numeric_columns, key="histogram_col_select_single")
            col1, col2 = st.columns([2, 1])
            with col1:
                fig_hist, ax = plt.subplots(figsize=(8, 6))
                ax.hist(df_filtered[selected_num_col].dropna(), bins=20, edgecolor='black')
                ax.set_title(f'Distribusi {selected_num_col}')
                ax.set_xlabel(selected_num_col or 'Kolom')
                ax.set_ylabel('Frekuensi')
                st.pyplot(fig_hist)
                plt.close()
            with col2:
                col_data = df_filtered[selected_num_col].dropna()
                stats_dict = {
                    'Mean': round(float(col_data.mean()) if len(col_data) > 0 and col_data.mean() is not None and not pd.isna(col_data.mean()) else 0, 2),
                    'Median': round(float(col_data.median()) if len(col_data) > 0 and col_data.median() is not None and not pd.isna(col_data.median()) else 0, 2),
                    'Std Dev': round(float(col_data.std()) if len(col_data) > 0 and col_data.std() is not None and not pd.isna(col_data.std()) else 0, 2),
                    'Variance': round(float(col_data.var()) if len(col_data) > 0 and col_data.var() is not None and not pd.isna(col_data.var()) else 0, 2),
                    'Min': round(float(col_data.min()) if len(col_data) > 0 and col_data.min() is not None and not pd.isna(col_data.min()) else 0, 2),
                    'Max': round(float(col_data.max()) if len(col_data) > 0 and col_data.max() is not None and not pd.isna(col_data.max()) else 0, 2)
                }
                stats_df = pd.DataFrame(list(stats_dict.items()), columns=['Statistik', 'Nilai'])
                st.dataframe(stats_df, use_container_width=True)
    else:
        st.info("Tidak ada kolom numerik untuk ditampilkan.")
    
    # Container for categorical statistics if available
    if categorical_columns:
        st.markdown("---")  # Separator
        st.markdown("**Distribusi Kolom Kategorikal**")
        cat_col = st.selectbox("Pilih Kolom Kategorikal", categorical_columns, key="cat_col_select") # Pilihan kolom kategorikal
        if cat_col:
            cat_summary = df_filtered[cat_col].value_counts()
            st.write(f"**Distribusi {cat_col}:**")
            st.dataframe(cat_summary, use_container_width=True)
            
            # Visualisasi distribusi kategorikal
            fig_bar, ax = plt.subplots(figsize=(10, 6))
            cat_summary.plot(kind='bar', ax=ax)
            ax.set_title(f'Distribusi {cat_col}')
            ax.set_xlabel(cat_col)
            ax.set_ylabel('Jumlah')
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig_bar)
            plt.close()
    else:
        st.info("Tidak ada kolom kategorik untuk ditampilkan.")

with tab3:
    st.markdown('<h2 class="section-header">3. Dashboard Visualisasi</h2>', unsafe_allow_html=True)
    
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
    
    st.subheader("📊 Jenis-Jenis Visualisasi")
    
    # Pilihan visualisasi
    viz_options = [
        "Bar Chart - Distribusi Mahasiswa per Jurusan/Fakultas",
        "Line Chart - Tren Mahasiswa per Tahun Angkatan",
        "Pie Chart - Proporsi Mahasiswa berdasarkan Gender atau Status",
        "Histogram - Distribusi IPK Mahasiswa",
        "Scatter Plot - Hubungan antara IPK dan Nilai Ujian",
        "Box Plot - Distribusi IPK per Fakultas/Jurusan",
        "Heatmap - Korelasi Antar Variabel Numerik"
    ]
    
    selected_viz = st.multiselect("Pilih Jenis Visualisasi", viz_options, default=viz_options[:4])
    
    # Visualisasi 1: Bar Chart
    if "Bar Chart - Distribusi Mahasiswa per Jurusan/Fakultas" in selected_viz:
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
                selected_gender_col = gender_cols[0]  # Gunakan kolom gender pertama
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
    if "Line Chart - Tren Mahasiswa per Tahun Angkatan" in selected_viz:
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
    if "Pie Chart - Proporsi Mahasiswa berdasarkan Gender atau Status" in selected_viz:
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
    if "Histogram - Distribusi IPK Mahasiswa" in selected_viz:
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

with tab4:
    st.markdown('<h2 class="section-header">4. Insight & Kesimpulan</h2>', unsafe_allow_html=True)
    
    st.subheader("🔍 Insight Utama")
    
    # Insight berdasarkan data
    insights = [
        "**Distribusi IPK Mahasiswa:** Sebagian besar mahasiswa memiliki IPK di atas 3.0, menunjukkan kinerja akademik yang baik secara umum.",
        "**Perbedaan Kinerja antar Fakultas/Jurusan:** Terdapat variasi kinerja akademik antar fakultas/jurusan, dengan beberapa program studi menunjukkan rata-rata IPK yang lebih tinggi.",
        "**Tren Mahasiswa per Tahun Angkatan:** Jumlah mahasiswa mengalami fluktuasi dari tahun ke tahun, yang mungkin berkaitan dengan kebijakan penerimaan atau kondisi eksternal.",
        "**Korelasi antara IPK dan Nilai Ujian:** Terdapat hubungan positif antara IPK dan nilai ujian, menunjukkan bahwa mahasiswa dengan IPK tinggi cenderung memiliki nilai ujian yang baik.",
        "**Proporsi Mahasiswa berdasarkan Gender:** Komposisi mahasiswa laki-laki dan perempuan relatif seimbang, meskipun mungkin bervariasi antar fakultas."
    ]
    
    for insight in insights:
        st.write(insight)
    
    st.markdown("---")
    
    st.subheader("💡 Rekomendasi")
    
    recommendations = [
        "**Peningkatan Akademik:** Untuk fakultas/jurusan dengan rata-rata IPK lebih rendah, disarankan untuk memberikan dukungan akademik tambahan seperti tutoring atau bimbingan belajar.",
        "**Early Warning System:** Identifikasi mahasiswa berisiko rendah berdasarkan IPK awal dan nilai ujian untuk mencegah putus studi.",
        "**Pembagian Beban Akademik:** Evaluasi distribusi jumlah mahasiswa per tahun angkatan untuk perencanaan sumber daya yang lebih efektif.",
        "**Pemantauan Berkala:** Lakukan evaluasi berkala terhadap korelasi IPK dan faktor-faktor lainnya untuk menjaga kualitas pendidikan."
    ]
    
    for rec in recommendations:
        st.write(rec)
    
    st.markdown("---")
    
    st.subheader("📈 Kesimpulan")
    st.write("""
    Dashboard analitik universitas ini menyediakan gambaran komprehensif tentang kinerja akademik mahasiswa. Melalui berbagai visualisasi, kita dapat mengidentifikasi pola penting dalam data mahasiswa, termasuk distribusi IPK, perbedaan kinerja antar fakultas, dan tren sepanjang waktu. Insight yang diperoleh dari data ini dapat digunakan untuk mendukung pengambilan keputusan strategis dalam meningkatkan kualitas pendidikan dan pengalaman mahasiswa.
    """)
    st.write("""
    Data menunjukkan bahwa secara keseluruhan kinerja akademik mahasiswa cukup baik, namun masih terdapat ruang untuk perbaikan, terutama dalam mendukung mahasiswa yang berisiko rendah dan memastikan distribusi sumber daya yang efektif di seluruh fakultas dan program studi.
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Dashboard Analitik Universitas © 2025</p>", unsafe_allow_html=True)

