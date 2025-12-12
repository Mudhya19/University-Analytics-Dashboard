import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Set page config
st.set_page_config(
    page_title="Dashboard Pasien BPJS Add Antroll",
    page_icon="🏥",
    layout="wide"
)

# Title
st.title("🏥 Dashboard Pasien BPJS Add Antroll")
st.markdown("---")

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. S.M.A.R.T Question & Data Wrangling",
    "2. Ringkasan Statistik Deskriptif",
    "3. Exploratory Data Analysis (Deskriptif)",
    "4. Exploratory Data Analysis (Lanjutan)",
    "5. Insight & Kesimpulan"
])

# Define the load_data function first
@st.cache_data
def load_data():
    """
    Load BPJS antrol data with error handling
    """
    try:
        # Load the dataset
        df = pd.read_csv('database/data/bpjs antrol.csv', low_memory=False)
        
        # Convert date columns to datetime
        df['tgl_registrasi'] = pd.to_datetime(df['tgl_registrasi'], format='%d/%m/%Y', errors='coerce')
        df['tanggal_periksa'] = pd.to_datetime(df['tanggal_periksa'], format='%d/%m/%Y', errors='coerce')
        
        # Convert time column to time format
        df['jam_reg'] = pd.to_datetime(df['jam_reg'], format='%H:%M:%S', errors='coerce').dt.time
        
        # Create a unified status column
        df['status'] = df['status_kirim'].apply(lambda x: 'Sudah' if x == 'Sudah' else 
                                               'Gagal' if x == 'Gagal' else 
                                               'Ambil Antrian' if x == 'Ambil Antrian' else 
                                               'Belum' if x == 'Belum' else 'Tidak Diketahui')
        
        # Create age column if birth date is available (not in this dataset, so we'll skip)
        # Calculate age based on registration date and birth date if available
        
        return df
    except FileNotFoundError:
        st.error("File 'database/data/bpjs antrol.csv' tidak ditemukan. Harap pastikan file tersebut ada di direktori yang benar.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error saat membaca file: {str(e)}")
        return pd.DataFrame()

# Load data
df = load_data()

if df.empty:
    st.error("Tidak dapat memuat data. Silakan periksa file dataset.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

# Date range filter
if not df.empty and 'tgl_registrasi' in df.columns:
    min_date = df['tgl_registrasi'].min()
    max_date = df['tgl_registrasi'].max()
    
    # Default date range: last 30 days
    default_end = min(max_date, datetime.now())
    default_start = max(min_date, default_end - timedelta(days=30))
    
    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        value=(default_start.date(), default_end.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['tgl_registrasi'] >= pd.Timestamp(start_date)) &
                (df['tgl_registrasi'] <= pd.Timestamp(end_date))]

# Poli filter
if 'nm_poli' in df.columns:
    poli_options = df['nm_poli'].unique()
    selected_poli = st.sidebar.multiselect("Pilih Poliklinik", options=poli_options, default=poli_options)
    if selected_poli:
        df = df[df['nm_poli'].isin(selected_poli)]

# Status filter
if 'status' in df.columns:
    status_options = df['status'].unique()
    selected_status = st.sidebar.multiselect("Pilih Status", options=status_options, default=status_options)
    if selected_status:
        df = df[df['status'].isin(selected_status)]

# EDA Mode selector (will be used in tab 4)
# Note: This variable is defined here but the actual selector is in tab 4
eda_mode = "Deskriptif" # Default value, will be set based on tab selection later

# Tab 1: S.M.A.R.T Question & Data Wrangling
with tab1:
    st.subheader("🎯 Tujuan Penelitian & Pertanyaan S.M.A.R.T")
    st.markdown("""
    Aplikasi ini dibuat untuk menganalisis data registrasi pasien BPJS Add Antroll.
    Berikut adalah beberapa pertanyaan S.M.A.R.T yang menjadi dasar analisis ini:

    1. **Berapa jumlah total registrasi pasien BPJS per hari?**
       - *Specific*: Mengukur jumlah registrasi harian
       - *Measurable*: Dapat dihitung dari data tanggal registrasi
       - *Achievable*: Data tersedia di dataset
       - *Relevant*: Penting untuk mengetahui volume layanan
       - *Time-bound*: Dapat dianalisis per hari, minggu, atau bulan

    2. **Berapa persentase keberhasilan registrasi BPJS per poliklinik?**
       - *Specific*: Mengukur efektivitas registrasi per poliklinik
       - *Measurable*: Dihitung sebagai rasio registrasi sukses terhadap total
       - *Achievable*: Status registrasi tersedia di dataset
       - *Relevant*: Penting untuk evaluasi kinerja layanan
       - *Time-bound*: Dapat dianalisis dalam periode tertentu

    3. **Apa poliklinik dengan jumlah kunjungan tertinggi dan terendah?**
       - *Specific*: Identifikasi poliklinik berdasarkan volume kunjungan
       - *Measurable*: Dihitung berdasarkan jumlah registrasi per poliklinik
       - *Achievable*: Nama poliklinik tersedia di dataset
       - *Relevant*: Penting untuk alokasi sumber daya
       - *Time-bound*: Dapat dianalisis dalam periode tertentu

    4. **Apa penyebab utama kegagalan registrasi BPJS?**
       - *Specific*: Mengidentifikasi faktor-faktor yang menyebabkan kegagalan
       - *Measurable*: Dihitung berdasarkan kategori keterangan error
       - *Achievable*: Data keterangan error tersedia di dataset
       - *Relevant*: Penting untuk perbaikan sistem
       - *Time-bound*: Dapat dianalisis dalam periode tertentu

    5. **Bagaimana pola distribusi waktu registrasi pasien?**
       - *Specific*: Mengidentifikasi jam-jam sibuk pendaftaran
       - *Measurable*: Dihitung berdasarkan jam registrasi
       - *Achievable*: Jam registrasi tersedia di dataset
       - *Relevant*: Penting untuk manajemen antrian
       - *Time-bound*: Dapat dianalisis harian/mingguan
    """)
    st.markdown("---")
    
    # Data Wrangling Process
    st.subheader("🔍 Proses Data Wrangling")
    st.markdown("#### Gathering Data")
    st.info(f"Jumlah data awal: {len(df):,} baris dan {df.shape[1]} kolom")

    # Data Quality Assessment
    st.markdown("#### Assessing Data Quality")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Jumlah Baris", value=f"{df.shape[0]:,}")
        
    with col2:
        st.metric(label="Jumlah Kolom", value=df.shape[1])
        
    with col3:
        st.metric(label="Jumlah Missing Values", value=f"{df.isnull().sum().sum():,}")

    # Detailed data info
    st.markdown("#### Informasi Detail Dataset")
    data_info = pd.DataFrame({
        'Kolom': df.columns,
        'Tipe Data': [str(df[col].dtype) for col in df.columns],
        'Missing Values': [df[col].isnull().sum() for col in df.columns],
        'Unique Values': [df[col].nunique() for col in df.columns]
    })
    st.dataframe(data_info, width='stretch')

    # Missing values handling
    st.markdown("#### Cleaning Data - Penanganan Missing Values")
    missing_values_cols = df.columns[df.isnull().any()].tolist()

    if missing_values_cols:
        st.write("Kolom-kolom dengan missing values:")
        for col in missing_values_cols:
            missing_pct = (df[col].isnull().sum() / len(df)) * 10  # Fixed calculation to multiply by 10
            st.write(f"- **{col}**: {df[col].isnull().sum()} missing values ({missing_pct:.2f}%)")
        
        # Automatically fill all missing values with 'Unknown'
        st.info("Mengisi semua missing values dengan 'Unknown'...")
        df.fillna('Unknown', inplace=True)
        st.success("✅ Semua missing values telah diisi dengan 'Unknown'")
                        
    else:
        st.success("🎉 Tidak ada missing values dalam dataset!")

    # Duplicate data handling
    st.markdown("#### Cleaning Data - Penanganan Data Duplikat")

    # Show information about the data before removing duplicates
    st.info(f"Jumlah data sebelum membersihkan duplikat: {len(df)}")

    # Identify duplicates before removing them
    duplicate_mask = df.duplicated(subset=['no_rawat'], keep=False)
    duplicate_count = duplicate_mask.sum()

    if duplicate_count > 0:
        st.warning(f"⚠️ Ditemukan {duplicate_count} baris data duplikat berdasarkan no_rawat dari total {len(df)} baris.")
        
        # Show duplicate information BEFORE removing them
        duplicate_rows = df[duplicate_mask].sort_values('no_rawat')
        st.write(f"Data duplikat berdasarkan no_rawat:")
    else:
        st.success("🎉 Tidak ada data duplikat berdasarkan no_rawat dalam dataset!")

    # Remove duplicates, keeping the first occurrence
    df = df.drop_duplicates(subset=['no_rawat'], keep='first')

    st.success(f"✅ Berhasil memastikan setiap pasien hanya memiliki satu nomor registrasi (no_rawat). Jumlah data sekarang: {len(df)}")
    st.dataframe(df, width='stretch')


    # Expandable section for detailed data types
    with st.expander("📋 Info Tipe Data Pasien BPJS Add Antroll"):
        buffer = pd.io.common.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)
        
        # Add describe with all columns and styled
        st.subheader("Statistik Deskriptif Semua Kolom")
        st.dataframe(df.describe(include="all").style.background_gradient(cmap='RdPu'), width='stretch')

# Tab 2: Ringkasan Statistik Deskriptif
with tab2:
    st.subheader("📈 Ringkasan Statistik Deskriptif")
    st.markdown("#### Statistik Deskriptif untuk Kolom Numerik")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if numeric_cols:
        st.dataframe(df[numeric_cols].describe(), width='stretch')
    else:
        st.info("Tidak ada kolom numerik dalam dataset untuk ditampilkan statistik deskriptifnya.")

    # Additional descriptive statistics for categorical columns
    st.markdown("#### Statistik Deskriptif untuk Kolom Kategorikal")
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    if categorical_cols:
        for col in categorical_cols[0:3]:  # Display first 3 categorical columns to avoid clutter
            st.markdown(f"##### Kolom: {col}")
            value_counts = df[col].value_counts().head(10)  # Top 10 values
            st.dataframe(value_counts, width='stretch')
    else:
        st.info("Tidak ada kolom kategorikal dalam dataset.")

    # Frequency tables for important categorical variables
    st.subheader("📊 Tabel Frekuensi untuk Variabel Kategorikal")

    # Define important categorical columns to display
    important_categorical_cols = ['status', 'nm_poli', 'jk', 'nm_pasien']  # Adjust based on actual dataset
    available_categorical_cols = [col for col in important_categorical_cols if col in df.columns]

    if available_categorical_cols:
        for col in available_categorical_cols:
            with st.expander(f"Tabel Frekuensi: {col}"):
                freq_table = df[col].value_counts().reset_index()
                freq_table.columns = [col, 'Frekuensi']
                freq_table['Persentase'] = (freq_table['Frekuensi'] / freq_table['Frekuensi'].sum()) * 100
                st.dataframe(freq_table, width='stretch')
    else:
        st.info("Tidak ada variabel kategorikal penting yang ditemukan dalam dataset.")

    # Correlation Analysis
    st.subheader("🔗 Analisis Korelasi Antar Variabel")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) >= 2:
        # Create correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Display correlation matrix as heatmap using Plotly
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Heatmap Korelasi Antar Variabel Numerik",
            color_continuous_scale='RdBu',
            zmin=-1, zmax=1
        )
        fig_corr.update_layout(height=500)
        st.plotly_chart(fig_corr, width='stretch')
        
        # Show top correlations
        st.markdown("#### Korelasi Tertinggi")
        # Unstack the correlation matrix to find top correlations
        corr_pairs = corr_matrix.abs().unstack()
        # Sort the correlation pairs and remove self-correlations
        sorted_corr_pairs = corr_pairs.sort_values(kind="quicksort", ascending=False)
        # Remove self-correlations (correlations of variables with themselves)
        top_corr_pairs = sorted_corr_pairs[sorted_corr_pairs < 1.0]
        
        if len(top_corr_pairs) > 0:
            top_5_corr = top_corr_pairs.head(5)
            top_corr_df = pd.DataFrame({
                'Pasangan Variabel': top_5_corr.index.map(lambda x: f"{x[0]} - {x[1]}"),
                'Korelasi': top_5_corr.values
            })
            st.dataframe(top_corr_df, width='stretch')
        else:
            st.info("Tidak ada korelasi yang dapat dihitung antar variabel numerik.")
    else:
        st.info("Tidak cukup variabel numerik dalam dataset untuk melakukan analisis korelasi.")

    # Main KPIs
    st.subheader("📊 KPI Utama")

    col1, col2, col3, col4 = st.columns(4)

    total_records = len(df)
    total_success = len(df[df['status'] == 'Sudah'])
    total_failed = len(df[df['status'] == 'Gagal'])
    success_rate = (total_success / total_records * 10) if total_records > 0 else 0

    with col1:
        st.metric(label="Total Registrasi", value=f"{total_records:,}")

    with col2:
        st.metric(label="Sukses", value=f"{total_success:,}", delta=f"{success_rate:.1f}%")

    with col3:
        st.metric(label="Gagal", value=f"{total_failed:,}")

    with col4:
        st.metric(label="Rata-rata Kunjungan/Hari", 
                  value=f"{df.groupby(df['tgl_registrasi'].dt.date).size().mean():.1f}")

    # Charts
    st.subheader("📈 Visualisasi Data")

    # Chart 1: Status Distribution
    col1, col2 = st.columns(2)

    with col1:
        status_counts = df['status'].value_counts()
        fig_status = px.bar(
            x=status_counts.index, 
            y=status_counts.values,
            title="Distribusi Status Registrasi",
            labels={'x': 'Status', 'y': 'Jumlah'},
            color=status_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_status.update_layout(showlegend=False)
        st.plotly_chart(fig_status, width='stretch')

    with col2:
        # Top 5 Poli by Total Registrations
        top_poli = df['nm_poli'].value_counts().head(5)
        fig_poli = px.bar(
            x=top_poli.values, 
            y=top_poli.index,
            title="Top 5 Poliklinik",
            labels={'x': 'Jumlah Registrasi', 'y': 'Poliklinik'},
            orientation='h',
            color=top_poli.index,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_poli.update_layout(showlegend=False)
        st.plotly_chart(fig_poli, width='stretch')

    # Chart 2: Daily Trend
    st.subheader("📅 Tren Kunjungan Harian")
    daily_trend = df.groupby(df['tgl_registrasi'].dt.date).size().reset_index(name='count')
    fig_trend = px.line(
        daily_trend, 
        x='tgl_registrasi', 
        y='count',
        title="Tren Kunjungan Harian",
        labels={'tgl_registrasi': 'Tanggal', 'count': 'Jumlah Kunjungan'}
    )
    st.plotly_chart(fig_trend, width='stretch')

    # Chart 3: Status by Poli
    st.subheader("🏥 Status Registrasi per Poliklinik")
    status_poli = df.groupby(['nm_poli', 'status']).size().reset_index(name='count')
    fig_status_poli = px.bar(
        status_poli, 
        x='nm_poli', 
        y='count', 
        color='status',
        title="Status Registrasi per Poliklinik",
        labels={'nm_poli': 'Poliklinik', 'count': 'Jumlah'},
        barmode='group'
    )
    fig_status_poli.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_status_poli, width='stretch')

    # Chart 4: Age Distribution (if age column exists) or Patient Distribution
    st.subheader("👥 Distribusi Pasien")
    if 'umur' in df.columns:
        fig_age = px.histogram(df, x='umur', nbins=30, title="Distribusi Umur Pasien")
        st.plotly_chart(fig_age, width='stretch')
    else:
        # Distribution by gender if available
        if 'jk' in df.columns or 'jenis_kelamin' in df.columns:
            gender_col = 'jk' if 'jk' in df.columns else 'jenis_kelamin'
            gender_counts = df[gender_col].value_counts()
            fig_gender = px.pie(
                values=gender_counts.values, 
                names=gender_counts.index,
                title="Distribusi Jenis Kelamin Pasien"
            )
            st.plotly_chart(fig_gender, width='stretch')
        else:
            # Show registration time distribution with 10-minute intervals
            # Convert time column to string format for grouping
            df['jam_reg_str'] = df['jam_reg'].astype(str)
            
            # Convert time strings to datetime and group into 10-minute intervals
            time_series = pd.to_datetime(df['jam_reg_str'], format='%H:%M:%S', errors='coerce')
            df['jam_reg_10min'] = time_series.dt.floor('10min').dt.time.astype(str)
            
            # Count occurrences of each 10-minute interval and sort by time
            time_counts = df['jam_reg_10min'].value_counts().sort_index()
            
            # Create line chart showing time distribution
            fig_time = px.line(
                x=time_counts.index,
                y=time_counts.values,
                title="Distribusi Waktu Registrasi (Interval 10 Menit)",
                labels={'x': 'Waktu', 'y': 'Jumlah Registrasi'}
            )
            
            # Rotate x-axis labels for better readability and adjust layout
            fig_time.update_layout(xaxis_tickangle=-45)
            
            # Display the chart in Streamlit
            st.plotly_chart(fig_time, width='stretch')

# Tab 3: Exploratory Data Analysis (Deskriptif)
with tab3:
    st.subheader("🔍 Visualisasi Pola dan Tren yang Lebih Kompleks")

    # Create tabs for different complex visualizations
    tab3a, tab3b, tab3c = st.tabs(["Distribusi Waktu", "Status vs Poli", "Tren Berdasarkan Hari"])

    with tab3a:
        st.markdown("#### Distribusi Registrasi Berdasarkan Waktu")
        if 'jam_reg' in df.columns:
            # Group by hour
            df['hour'] = pd.to_datetime(df['jam_reg'], format='%H:%M:%S', errors='coerce').dt.hour
            df_hourly = df.groupby('hour').size().reset_index(name='count')
            
            fig_hourly = px.bar(
                df_hourly,
                x='hour',
                y='count',
                title="Distribusi Jumlah Registrasi Berdasarkan Jam",
                labels={'hour': 'Jam', 'count': 'Jumlah Registrasi'},
                color='count',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig_hourly, width='stretch')
        else:
            st.info("Kolom waktu registrasi tidak tersedia dalam dataset.")

    with tab3b:
        st.markdown("#### Status Registrasi Berdasarkan Poliklinik (Heatmap)")
        if 'nm_poli' in df.columns and 'status' in df.columns:
            # Create a pivot table for heatmap
            heatmap_data = df.groupby(['nm_poli', 'status']).size().reset_index(name='count')
            heatmap_pivot = heatmap_data.pivot(index='nm_poli', columns='status', values='count').fillna(0)
            
            fig_heatmap = px.imshow(
                heatmap_pivot,
                text_auto=True,
                aspect="auto",
                title="Heatmap Status Registrasi per Poliklinik",
                color_continuous_scale='Blues'
            )
            fig_heatmap.update_layout(height=500)
            st.plotly_chart(fig_heatmap, width='stretch')
        else:
            st.info("Kolom poliklinik atau status tidak tersedia dalam dataset.")

    with tab3c:
        st.markdown("#### Tren Harian dengan Indikator Status")
        if 'tgl_registrasi' in df.columns and 'status' in df.columns:
            # Group by date and status
            daily_status = df.groupby([df['tgl_registrasi'].dt.date, 'status']).size().reset_index(name='count')
            
            fig_daily_status = px.line(
                daily_status,
                x='tgl_registrasi',
                y='count',
                color='status',
                title="Tren Harian Berdasarkan Status Registrasi",
                labels={'tgl_registrasi': 'Tanggal', 'count': 'Jumlah Registrasi'}
            )
            st.plotly_chart(fig_daily_status, width='stretch')
        else:
            st.info("Kolom tanggal registrasi atau status tidak tersedia dalam dataset.")

# Tab 4: Exploratory Data Analysis (Lanjutan)
with tab4:
    st.subheader("🔍 EDA Lanjutan")
    
    # Patients with high visit count (>=10 visits)
    st.subheader("📈 Pasien dengan Banyak Kunjungan")
    patient_counts = df['nm_pasien'].value_counts()
    high_visitors = patient_counts[patient_counts >= 10]
    
    if len(high_visitors) > 0:
        st.write(f"Jumlah pasien dengan ≥10 kunjungan: {len(high_visitors)}")
        fig_high_visitors = px.bar(
            x=high_visitors.index[:10], 
            y=high_visitors.values[:10],
            title="Top 10 Pasien dengan Kunjungan Terbanyak",
            labels={'x': 'Nama Pasien', 'y': 'Jumlah Kunjungan'}
        )
        fig_high_visitors.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_high_visitors, width='stretch')
    else:
        st.write("Tidak ada pasien dengan ≥10 kunjungan dalam periode ini.")
    
    # Error analysis
    st.subheader("⚠️ Analisis Keterangan Error")
    error_counts = df[df['status'] == 'Gagal']['keterangan'].value_counts()
    if len(error_counts) > 0:
        fig_errors = px.bar(
            x=error_counts.values[:10], 
            y=error_counts.index[:10],
            title="Top 10 Alasan Kegagalan",
            labels={'x': 'Jumlah', 'y': 'Keterangan Error'},
            orientation='h'
        )
        st.plotly_chart(fig_errors, width='stretch')
    else:
        st.write("Tidak ada data error dalam periode ini.")

# Tab 5: Insight & Kesimpulan
with tab5:
    # Failed patients table
    st.subheader("❌ Daftar Pasien Gagal")
    failed_patients = df[df['status'] == 'Gagal'][['tgl_registrasi', 'nm_pasien', 'nm_poli', 'keterangan', 'USER']]
    if not failed_patients.empty:
        st.dataframe(failed_patients, width='stretch')
        
        # Download button for failed patients
        csv = failed_patients.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Pasien Gagal",
            data=csv,
            file_name="pasien_gagal_bpjs_antrol.csv",
            mime="text/csv"
        )
    else:
        st.write("Tidak ada pasien gagal dalam periode ini.")
    
    # Raw data table (optional)
    with st.expander("📋 Lihat Data"):
        st.dataframe(df, width='stretch')
        
        # Download button for raw data
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Data Pasien BPJS Add Antroll",
            data=csv,
            file_name="bpjs_antrol_raw_data.csv",
            mime="text/csv"
        )
    
    # Insights and Conclusions
    st.subheader("💡 Insight & Kesimpulan")
    st.markdown("""
    ### Temuan Utama Berdasarkan Analisis Data:
    1. **Tren Registrasi**: Pola registrasi pasien BPJS dapat dianalisis berdasarkan waktu, hari, dan poliklinik yang paling banyak dikunjungi.
    2. **Tingkat Keberhasilan**: Persentase keberhasilan registrasi dapat diidentifikasi dan dianalisis penyebab kegagalannya.
    3. **Pola Waktu**: Jam-jam sibuk pendaftaran dapat diidentifikasi untuk membantu manajemen antrian.
    4. **Distribusi Poliklinik**: Poliklinik mana yang paling banyak digunakan dan perlu diberikan perhatian lebih.
    
    ### Rekomendasi:
    1. **Optimalisasi Pelayanan**: Berdasarkan pola waktu registrasi, dapat diatur penjadwalan petugas yang lebih efisien.
    2. **Perbaikan Sistem**: Analisis keterangan error dapat digunakan untuk mengidentifikasi dan memperbaiki masalah teknis dalam sistem registrasi.
    3. **Pengalokasian Sumber Daya**: Berdasarkan distribusi poliklinik, dapat dilakukan pengalokasian sumber daya yang lebih merata sesuai kebutuhan.
    4. **Peningkatan Kualitas Data**: Dengan pemeriksaan kualitas data yang telah dilakukan, dapat diusulkan perbaikan dalam pengumpulan dan pencatatan data.
    """)
    
    # Executive Summary
    st.subheader("📋 Ringkasan Eksekutif")
    st.markdown("""
    Dashboard ini menyediakan analisis komprehensif terhadap data registrasi pasien BPJS Add Antroll.
    Dengan menggunakan berbagai teknik eksplorasi data, visualisasi, dan analisis statistik,
    dashboard ini membantu dalam memahami pola penggunaan layanan, tingkat keberhasilan registrasi,
    dan faktor-faktor yang mempengaruhi kegagalan sistem.
    
    Melalui fitur interaktif yang disediakan, pengguna dapat melakukan filtering data berdasarkan tanggal,
    poliklinik, dan status registrasi untuk mendapatkan insight yang lebih spesifik sesuai kebutuhan.
    Dashboard ini diharapkan dapat mendukung pengambilan keputusan yang lebih baik dalam
    pengelolaan layanan kesehatan dan sistem informasi rumah sakit.
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("*Dashboard ini menampilkan analisis pendaftaran BPJS (Add Antroll) - Data diperbarui secara real-time dari database*")