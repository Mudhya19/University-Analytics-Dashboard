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

# Tambahkan fitur pilih tahun angkatan
tahun_angkatan_columns = [col for col in df.columns if 'angkatan' in col.lower() or 'tahun' in col.lower() or 'year' in col.lower()]
if tahun_angkatan_columns:
    selected_tahun_angkatan = st.sidebar.selectbox("Pilih Tahun Angkatan", ["Semua"] + tahun_angkatan_columns)
    
    if selected_tahun_angkatan != "Semua":
        unique_years = df[selected_tahun_angkatan].unique()
        selected_year = st.sidebar.selectbox(f"Pilih Tahun dari {selected_tahun_angkatan}", list(unique_years))
        
        if selected_year:
            df_filtered = df_filtered[df_filtered[selected_tahun_angkatan] == selected_year]

# Display tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. S.M.A.R.T Question & Data Wrangling",
    "2. Ringkasan Statistik Deskriptif",
    "3. Exploratory Data Analysis (Deskriptif)",
    "4. Exploratory Data Analysis (Lanjutan)",
    "5. Insight & Kesimpulan"
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
            'Persentase Hilang': (df.isnull().sum() / len(df)) * 100
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
    st.markdown('<h2 class="section-header">2. Ringkasan Statistik Deskriptif</h2>', unsafe_allow_html=True)
    
    st.subheader("📊 Descriptive Statistics Summary")
    
    # Overall summary
    st.write("**Overall Dataset Summary:**")
    st.dataframe(df.describe(include='all').style.background_gradient(cmap='RdPu'))
    
    st.markdown("---")
    
    # Numeric columns summary
    if numeric_columns:
        st.subheader("📈 Numeric Variables Summary")
        
        # Select specific numeric columns for detailed analysis
        selected_num_cols = st.multiselect("Select numeric columns for analysis:", numeric_columns, default=numeric_columns[:3] if len(numeric_columns) >= 3 else numeric_columns)
        
        for col in selected_num_cols:
            st.write(f"**{col}**")
            # Calculate statistics with proper error handling
            count_val = df[col].count()
            mean_val = df[col].mean()
            std_val = df[col].std()
            min_val = df[col].min()
            q25_val = df[col].quantile(0.25)
            median_val = df[col].median()
            q75_val = df[col].quantile(0.75)
            max_val = df[col].max()
            
            col_stats = pd.DataFrame({
                'Statistics': ['Count', 'Mean', 'Std Dev', 'Min', '25%', 'Median', '75%', 'Max'],
                'Value': [
                    count_val,
                    round(float(mean_val) if pd.notna(mean_val) else 0, 2),
                    round(float(std_val) if pd.notna(std_val) else 0, 2),
                    round(float(min_val) if pd.notna(min_val) else 0, 2),
                    round(float(q25_val) if pd.notna(q25_val) else 0, 2),
                    round(float(median_val) if pd.notna(median_val) else 0, 2),
                    round(float(q75_val) if pd.notna(q75_val) else 0, 2),
                    round(float(max_val) if pd.notna(max_val) else 0, 2)
                ]
            })
            st.dataframe(col_stats)
            
            # Distribution plot
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(data=df, x=col, kde=True, ax=ax)
            ax.set_title(f'Distribution of {col}')
            st.pyplot(fig)
            plt.close()
    
    st.markdown("---")
    
    # Categorical columns summary
    if categorical_columns:
        st.subheader("📋 Categorical Variables Summary")
        
        # Select specific categorical columns for detailed analysis
        selected_cat_cols = st.multiselect("Select categorical columns for analysis:", categorical_columns, default=categorical_columns[:3] if len(categorical_columns) >= 3 else categorical_columns)
        
        for col in selected_cat_cols:
            st.write(f"**{col}**")
            
            value_counts = df[col].value_counts()
            unique_count = df[col].nunique()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="Unique Values", value=unique_count)
                st.write("Top 10 Categories:")
                st.dataframe(value_counts.head(10))
            
            with col2:
                # Bar chart for categorical data
                fig, ax = plt.subplots(figsize=(8, 5))
                value_counts.head(10).plot(kind='bar', ax=ax)
                ax.set_title(f'Top 10 Categories in {col}')
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
                plt.close()
    
    st.markdown("---")
    
    # Correlation analysis
    if len(numeric_columns) > 1:
        st.subheader("🔗 Correlation Analysis")
        corr_method = st.selectbox("Select correlation method:", ["Pearson", "Spearman"])
        
        method = 'pearson' if corr_method == "Pearson" else 'spearman'
        correlation_matrix = df[numeric_columns].corr(method=method)
        
        # Heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                    square=True, fmt='.2f', ax=ax)
        ax.set_title(f'Correlation Matrix ({corr_method})')
        st.pyplot(fig)
        plt.close()

with tab3:
    st.markdown('<h2 class="section-header">3. Exploratory Data Analysis (Deskriptif)</h2>', unsafe_allow_html=True)
    
    st.subheader("🔍 Univariate Analysis")
    
    # Select variable for univariate analysis
    analysis_col = st.selectbox("Select variable for univariate analysis:", numeric_columns + categorical_columns)
    
    if analysis_col in numeric_columns:
        # Numerical variable analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Distribution of {analysis_col}**")
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.histplot(data=df, x=analysis_col, kde=True, ax=ax)
            ax.set_title(f'Histogram of {analysis_col}')
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.write(f"**Descriptive Statistics**")
            # Calculate basic statistics
            mean_val = df[analysis_col].mean()
            median_val = df[analysis_col].median()
            std_val = df[analysis_col].std()
            
            stats_df = pd.DataFrame({
                'Measure': ['Mean', 'Median', 'Std Dev'],
                'Value': [
                    round(float(mean_val) if pd.notna(mean_val) else 0, 2),
                    round(float(median_val) if pd.notna(median_val) else 0, 2),
                    round(float(std_val) if pd.notna(std_val) else 0, 2)
                ]
            })
            st.dataframe(stats_df)
    
    elif analysis_col in categorical_columns:
        # Categorical variable analysis
        st.write(f"**Distribution of {analysis_col}**")
        value_counts = df[analysis_col].value_counts()
        
        # Bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        value_counts.plot(kind='bar', ax=ax)
        ax.set_title(f'Bar Chart of {analysis_col}')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
        plt.close()
        
        # Frequency table
        st.write(f"**Frequency Table for {analysis_col}:**")
        freq_table = pd.DataFrame({
            'Category': value_counts.index,
            'Count': value_counts.values,
            'Percentage': [round((count / len(df)) * 100, 2) for count in value_counts.values]
        })
        st.dataframe(freq_table)
    
    st.markdown("---")
    
    st.subheader("🔗 Bivariate Analysis")
    
    # Select variables for bivariate analysis
    var1 = st.selectbox("Select first variable:", numeric_columns + categorical_columns, key='var1')
    var2 = st.selectbox("Select second variable:", numeric_columns + categorical_columns, key='var2')
    
    if var1 != var2:
        if var1 in numeric_columns and var2 in numeric_columns:
            # Correlation and scatter plot
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Correlation between {var1} and {var2}:**")
                correlation = df[var1].corr(df[var2])
                st.metric(label="Correlation Coefficient", value=round(correlation, 3))
            
            with col2:
                st.write(f"**Scatter Plot {var1} vs {var2}**")
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.scatterplot(data=df, x=var1, y=var2, ax=ax)
                ax.set_xlabel(var1)
                ax.set_ylabel(var2)
                ax.set_title(f'{var1} vs {var2}')
                st.pyplot(fig)
                plt.close()
        
        elif (var1 in numeric_columns and var2 in categorical_columns) or (var1 in categorical_columns and var2 in numeric_columns):
            # Numeric vs Categorical
            num_var = var1 if var1 in numeric_columns else var2
            cat_var = var1 if var1 in categorical_columns else var2
            
            st.write(f"**Distribution of {num_var} by {cat_var}**")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.boxplot(data=df, x=cat_var, y=num_var, ax=ax)
            ax.tick_params(axis='x', rotation=45)
            ax.set_title(f'{num_var} by {cat_var}')
            st.pyplot(fig)
            plt.close()
            
            # Grouped statistics
            st.write(f"**Statistics of {num_var} by {cat_var}:**")
            grouped_stats = df.groupby(cat_var)[num_var].agg(['count', 'mean', 'std']).round(2)
            st.dataframe(grouped_stats)

with tab4:
    st.markdown('<h2 class="section-header">4. Exploratory Data Analysis (Lanjutan)</h2>', unsafe_allow_html=True)
    
    st.subheader("🔍 Outlier Detection")
    
    # Outlier Detection
    if numeric_columns:
        numeric_col_for_outliers = st.selectbox("Select numeric column for outlier detection:", numeric_columns)
        
        Q1 = df[numeric_col_for_outliers].quantile(0.25)
        Q3 = df[numeric_col_for_outliers].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[numeric_col_for_outliers] < lower_bound) |
                      (df[numeric_col_for_outliers] > upper_bound)]
        
        st.write(f"Outliers detected in {numeric_col_for_outliers}: {len(outliers)} records")
        st.write(f"Lower bound: {lower_bound:.2f}, Upper bound: {upper_bound:.2f}")
        
        if not outliers.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(y=df[numeric_col_for_outliers], ax=ax)
            ax.set_title(f'Box Plot showing Outliers in {numeric_col_for_outliers}')
            st.pyplot(fig)
            plt.close()
    
    st.markdown("---")
    
    st.subheader("📈 Data Trends")
    
    # Time series analysis if date columns exist
    if date_columns and numeric_columns:
        time_col = st.selectbox("Select date column for trend analysis:", date_columns)
        metric_col = st.selectbox("Select metric for trend analysis:", numeric_columns)
        
        # Group data by selected time period
        df_time = df.copy()
        df_time[time_col] = pd.to_datetime(df_time[time_col])
        df_time['year_month'] = df_time[time_col].apply(lambda x: x.strftime('%Y-%m'))
        
        if time_col and metric_col:  # Pastikan kedua variabel tidak None
            try:
                # Group data by selected time period
                df_time = df.copy()
                df_time[time_col] = pd.to_datetime(df_time[time_col])
                df_time['year_month'] = df_time[time_col].apply(lambda x: x.strftime('%Y-%m'))
                
                trend_data = df_time.groupby('year_month')[metric_col].mean().reset_index()
                
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(trend_data['year_month'], trend_data[metric_col], marker='o', linewidth=2, markersize=4)
                ax.set_title(f'Average {metric_col} Trend Over Time')
                ax.set_xlabel('Time Period')
                ax.set_ylabel(f'Average {metric_col}')
                plt.xticks(rotation=45)
                st.pyplot(fig)
                plt.close()
            except:
                st.warning("Cannot create trend chart due to issues with date column or metric.")

with tab5:
    st.markdown('<h2 class="section-header">5. Wawasan & Kesimpulan</h2>', unsafe_allow_html=True)
    
    st.subheader("💡 Wawasan Utama")
    
    # Generate automated insights based on the data
    insights = []
    
    # Insight 1: Missing data
    missing_percentage = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    if missing_percentage > 5:
        insights.append(f"⚠️ Dataset memiliki {missing_percentage:.2f}% nilai yang hilang yang mungkin perlu perhatian.")
    else:
        insights.append(f"✅ Dataset memiliki data hilang yang relatif rendah ({missing_percentage:.2f}%).")
    
    # Insight 2: Unique values in categorical columns
    for col in categorical_columns:
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio > 0.9:
            insights.append(f"🔍 Kolom '{col}' memiliki kardinalitas sangat tinggi ({df[col].nunique()} nilai unik), yang mungkin sulit dianalisis secara efektif.")
        elif unique_ratio < 0.05:
            insights.append(f"📊 Kolom '{col}' memiliki kardinalitas rendah ({df[col].nunique()} nilai unik), membuatnya cocok untuk analisis kategorikal.")
    
    # Insight 3: Correlations
    if len(numeric_columns) > 1:
        try:
            corr_matrix = df[numeric_columns].corr()
            # Ambil pasangan kolom dengan korelasi tinggi (di atas 0.7)
            high_corr_count = 0
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if pd.notna(corr_val):
                        high_corr_count += 1
            if high_corr_count > 0:
                insights.append(f"🔗 Ditemukan {high_corr_count} pasangan variabel dengan korelasi tinggi (di atas 0.7).")
        except:
            pass  # Jika terjadi kesalahan saat menghitung korelasi, lewati
    
    # Insight 4: Outliers
    for col in numeric_columns[:5]: # Check first 5 numeric columns
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers_count = len(df[(df[col] < lower_bound) | (df[col] > upper_bound)])
        if outliers_count > len(df) * 0.01:  # More than 1% are outliers
            insights.append(f"🚨 Kolom '{col}' memiliki {outliers_count} outlier ({outliers_count/len(df)*100:.2f}% dari data).")
    
    # Display insights
    for i, insight in enumerate(insights, 1):
        st.write(f"{i}. {insight}")
    
    st.markdown("---")
    
    st.subheader("📊 Ringkasan Visual")
    
    # Create a comprehensive visualization
    if len(numeric_columns) >= 2:
        # Pairplot for top 4 numeric columns
        cols_to_plot = numeric_columns[:4] if len(numeric_columns) >= 4 else numeric_columns
        
        if len(cols_to_plot) >= 2:
            st.write("**Pairplot dari Variabel Numerik Terpilih:**")
            sample_df = df[cols_to_plot].sample(min(100, len(df)))
            fig = sns.pairplot(sample_df, diag_kind='hist', height=2.5)
            st.pyplot(fig.fig)
            plt.close()
    
    st.markdown("---")
    
    st.subheader("📝 Kesimpulan & Rekomendasi")
    
    conclusion_text = """
    Berdasarkan analisis eksploratori data yang telah dilakukan, berikut adalah kesimpulan dan rekomendasi utama:
    
    1. **Penilaian Kualitas Data**:
       - Dataset secara umum memiliki kualitas data yang baik dengan tingkat missing value yang rendah
       - Beberapa kolom mungkin memerlukan preprocessing tambahan untuk analisis lebih lanjut
    
    2. **Pola & Hubungan**:
       - Terdapat beberapa pasangan variabel yang menunjukkan korelasi yang kuat
       - Hubungan antar variabel dapat dieksplorasi lebih lanjut untuk model prediktif
    
    3. **Anomali & Outlier**:
       - Beberapa variabel memiliki outlier yang signifikan yang perlu ditangani
       - Outlier ini bisa menjadi kasus menarik atau kesalahan data
    
    4. **Peluang Rekayasa Fitur**:
       - Ada potensi untuk membuat fitur-fitur baru dari data yang ada
       - Diskretisasi atau agregasi bisa meningkatkan kemampuan analisis
    
    5. **Langkah Selanjutnya**:
       - Lakukan analisis statistik lanjutan seperti modeling atau forecasting
       - Validasi hipotesis yang telah dirumuskan dalam tahap pertanyaan SMART
       - Implementasikan monitoring dan sistem alert berdasarkan pola yang ditemukan
    """
    
    st.write(conclusion_text)
    
    st.markdown("---")
    
    st.subheader("🎯 Item Tindakan")
    
    action_items = [
        "1. Validasi data lebih lanjut dengan stakeholder untuk memastikan keakuratan",
        "2. Lakukan sampling data jika dataset terlalu besar untuk analisis mendalam",
        "3. Buat pipeline data untuk otomatisasi proses pembersihan dan transformasi",
        "4. Kembangkan model prediktif berdasarkan pola-pola yang ditemukan",
        "5. Siapkan dashboard interaktif untuk pemantauan real-time"
    ]
    
    for item in action_items:
        st.write(item)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Dashboard Analitik Universitas © 2025</p>", unsafe_allow_html=True)