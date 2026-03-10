import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Mengatur tema seaborn
sns.set_theme(style="darkgrid")

# ==============================
# 1. SETUP PAGE & LAYOUT
# ==============================
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
st.title("🚲 Bike Sharing Data Analytics Dashboard")
st.markdown("**Proyek Analisis Data: Bike Sharing Dataset**")

# ==============================
# 2. LOAD & STANDARDIZE DATA (ANTI-ERROR)
# ==============================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    main_df = pd.read_csv(file_path)
    
    # 1. Standarisasi nama kolom otomatis
    rename_dict = {}
    if 'dteday' in main_df.columns: rename_dict['dteday'] = 'date'
    if 'hr' in main_df.columns: rename_dict['hr'] = 'hour'
    if 'weathersit' in main_df.columns: rename_dict['weathersit'] = 'weather_condition'
    if 'cnt' in main_df.columns: rename_dict['cnt'] = 'total_count'
    main_df.rename(columns=rename_dict, inplace=True)
    
    # 2. Standarisasi isi data (Mapping otomatis jika masih berupa angka)
    if main_df['workingday'].dtype in ['int64', 'float64', 'int32']:
        main_df['workingday'] = main_df['workingday'].map({0: 'Holiday/Weekend', 1: 'Working Day'})
        
    if main_df['weather_condition'].dtype in ['int64', 'float64', 'int32']:
        main_df['weather_condition'] = main_df['weather_condition'].map({1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain'})
    
    # Memastikan format tanggal
    main_df['date'] = pd.to_datetime(main_df['date'])
    
    # Bining untuk Clustering Suhu 
    bins = [0, 0.25, 0.50, 0.75, 1.0]
    labels = ['Dingin (Cold)', 'Sejuk (Mild)', 'Hangat (Warm)', 'Panas (Hot)']
    main_df['temp_cluster'] = pd.cut(main_df['temp'], bins=bins, labels=labels, include_lowest=True)
    
    return main_df

main_df = load_data()

# ==============================
# 3. SIDEBAR (FILTER)
# ==============================
st.sidebar.title("🚴‍♂️ Navigasi Data")
st.sidebar.markdown("Gunakan filter di bawah untuk mengeksplorasi data.")

min_date = main_df["date"].min()
max_date = main_df["date"].max()

# PENANGANAN ERROR TANGGAL: Menggunakan variabel penampung sementara
date_range = st.sidebar.date_input(
    label="Rentang Waktu",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Mengecek apakah user sudah memilih 2 tanggal (awal dan akhir)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

# Memfilter dataset berdasarkan input sidebar
filtered_df = main_df[(main_df["date"] >= pd.to_datetime(start_date)) & 
                      (main_df["date"] <= pd.to_datetime(end_date))]

# Menampilkan metrik utama di sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Total Penyewaan (Periode Terpilih)")
st.sidebar.metric("Total Count", value=f"{filtered_df['total_count'].sum():,}")
st.sidebar.metric("Registered Users", value=f"{filtered_df['registered'].sum():,}")
st.sidebar.metric("Casual Users", value=f"{filtered_df['casual'].sum():,}")

# ==============================
# 4. MAIN DASHBOARD CONTENT (TABS)
# ==============================
tab1, tab2, tab3 = st.tabs(["🕒 Pola Jam Sibuk (Q1)", "⛈️ Dampak Cuaca (Q2)", "🌡️ Analisis Lanjutan (Clustering)"])

# ----- TAB 1: Pola Waktu -----
with tab1:
    st.header("Perbandingan Jam Sibuk: Hari Kerja vs Akhir Pekan")
    
    # SUDAH DIGANTI MENJADI 'hour'
    hourly_trend = filtered_df.groupby(['workingday', 'hour'])[['casual', 'registered']].mean().reset_index()
    
    # Cek apakah data kosong setelah difilter
    if hourly_trend.empty:
        st.warning("Data tidak tersedia untuk rentang tanggal ini.")
    else:
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6), sharey=True)

        working_data = hourly_trend[hourly_trend['workingday'] == 'Working Day']
        axes[0].plot(working_data['hour'], working_data['registered'], label='Registered', color='#1f77b4', marker='o', linewidth=2)
        axes[0].plot(working_data['hour'], working_data['casual'], label='Casual', color='#ff7f0e', marker='o', linewidth=2)
        axes[0].set_title('Hari Kerja (Working Day)', fontsize=14)
        axes[0].set_xlabel('Jam (0-23)', fontsize=12)
        axes[0].set_ylabel('Rata-rata Penyewaan', fontsize=12)
        axes[0].legend()
        axes[0].grid(True, alpha=0.4)

        holiday_data = hourly_trend[hourly_trend['workingday'] == 'Holiday/Weekend']
        axes[1].plot(holiday_data['hour'], holiday_data['registered'], label='Registered', color='#1f77b4', marker='o', linewidth=2)
        axes[1].plot(holiday_data['hour'], holiday_data['casual'], label='Casual', color='#ff7f0e', marker='o', linewidth=2)
        axes[1].set_title('Akhir Pekan/Libur (Holiday/Weekend)', fontsize=14)
        axes[1].set_xlabel('Jam (0-23)', fontsize=12)
        axes[1].legend()
        axes[1].grid(True, alpha=0.4)

        st.pyplot(fig)
        
        with st.expander("Lihat Insight/Kesimpulan"):
            st.write("- **Hari Kerja:** Didominasi pelanggan *registered* pada jam komuter (08:00 dan 17:00-18:00).")
            st.write("- **Hari Libur:** Pola berubah merata di siang hari (12:00-16:00) dengan peningkatan drastis pengguna *casual*.")

# ----- TAB 2: Dampak Cuaca -----
with tab2:
    st.header("Dampak Cuaca Terhadap Penyewaan di Jam Komuter")
    
    commuter_hours = [7, 8, 9, 17, 18, 19]
    # SUDAH DIGANTI MENJADI 'hour'
    commuter_data = filtered_df[(filtered_df['hour'].isin(commuter_hours)) & (filtered_df['workingday'] == 'Working Day')]
    
    if commuter_data.empty:
        st.warning("Data tidak tersedia untuk rentang tanggal ini.")
    else:
        weather_impact = commuter_data.groupby('weather_condition')['registered'].mean().reset_index().sort_values(by='registered', ascending=False)
        
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.barplot(x='weather_condition', y='registered', data=weather_impact, palette='viridis', ax=ax2)
        ax2.set_title('Rata-rata Penyewaan (Registered) per Kondisi Cuaca di Jam Komuter', fontsize=14)
        ax2.set_xlabel('Kondisi Cuaca')
        ax2.set_ylabel('Rata-rata Penyewaan')
        
        for index, row in enumerate(weather_impact['registered']):
            ax2.text(index, row + 5, f'{round(row)}', color='black', ha="center", fontsize=10, fontweight='bold')
        
        st.pyplot(fig2)

# ----- TAB 3: Analisis Lanjutan -----
with tab3:
    st.header("Clustering Manual: Tingkat Kenyamanan Suhu Udara")
    
    cluster_summary = filtered_df.groupby('temp_cluster')[['casual', 'registered', 'total_count']].mean().reset_index()
    
    if cluster_summary.empty:
        st.warning("Data tidak tersedia untuk rentang tanggal ini.")
    else:
        fig3, axes3 = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
        
        sns.barplot(x='temp_cluster', y='total_count', data=cluster_summary, palette='coolwarm', ax=axes3[0])
        axes3[0].set_title('Total Penyewaan per Cluster Suhu', fontsize=14)
        axes3[0].set_xlabel('Cluster Suhu')
        axes3[0].set_ylabel('Total Penyewaan')
        
        cluster_summary_melted = cluster_summary.melt(id_vars='temp_cluster', value_vars=['casual', 'registered'], 
                                                      var_name='User Type', value_name='Average Count')
        sns.barplot(x='temp_cluster', y='Average Count', hue='User Type', data=cluster_summary_melted, palette=['#ff7f0e', '#1f77b4'], ax=axes3[1])
        axes3[1].set_title('Proporsi Tipe Pengguna per Cluster Suhu', fontsize=14)
        axes3[1].set_xlabel('Cluster Suhu')
        axes3[1].set_ylabel('Rata-rata Penyewaan')
        
        st.pyplot(fig3)

st.caption("Jacky Sakti Pratama (c) 2026 - Bike Sharing Data Analysis ")