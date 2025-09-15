# Dashboard Visualisasi Data: Analisis dan Pemantauan Tren Banjir di Kota Bima

import streamlit as st
import pandas as pd
import plotly.express as px

# Judul
st.title(" Visualisasi Tren Banjir di Kota Bima")
st.markdown("""
Dashboard ini bertujuan untuk memberikan wawasan visual terkait tren banjir di Kota Bima berdasarkan data curah hujan, kejadian banjir, dan validasi dari berita daring.
 Data ini bersumber dari BMKG, BNPB, BPBD, dan media terpercaya.""")

# Load dataset
rain = pd.read_csv("../data/curah_hujan_bima.csv")
banjir = pd.read_csv("../data/kejadian_banjir_bima.csv")
berita = pd.read_csv("../data/berita_banjir_bima.csv")

# Sidebar filter
st.sidebar.header("Filter Wilayah")
lokasi = st.sidebar.multiselect("Pilih Lokasi Curah Hujan", rain['lokasi'].unique(), default=rain['lokasi'].unique())
filtered_rain = rain[rain['lokasi'].isin(lokasi)]

list_kelurahan = sorted(banjir['kelurahan'].unique())
selected_kelurahan = st.sidebar.multiselect("Pilih Kelurahan", list_kelurahan, default=list_kelurahan)

# Line Graph - Curah Hujan
st.subheader("1. Tren Curah Hujan Harian (2019–2023)")
rain_perday = filtered_rain.groupby('tanggal').mean(numeric_only=True).reset_index()
fig_rain = px.line(rain_perday, x='tanggal', y='curah_hujan', title='Curah Hujan Harian di Kota Bima')
st.plotly_chart(fig_rain, use_container_width=True)

# Mapping kelurahan ke lokasi curah hujan (harus disesuaikan dengan data aslinya)
kelurahan_to_lokasi = {
    "Paruga": "Paruga",
    "Kodo": "Kodo",
    "Sarae": "Sarae",
    "Penatoi": "Penatoi",
    "Monggonao": "Monggonao",
    # Tambah jika ada kelurahan/lokasi lain
}

# Ambil nama lokasi dari kelurahan yang dipilih
lokasi_terpilih = [kelurahan_to_lokasi[kel] for kel in selected_kelurahan if kel in kelurahan_to_lokasi]

# Filter semua dataset
filtered_rain = rain[rain['lokasi'].isin(lokasi_terpilih)]
filtered_banjir = banjir[banjir['kelurahan'].isin(selected_kelurahan)]
filtered_berita = berita[berita['lokasi'].isin(lokasi_terpilih)] if 'lokasi' in berita.columns else berita


# 2. Bar Chart - Kejadian Banjir Tahunan
st.subheader("2. Jumlah Kejadian Banjir per Tahun")
if not filtered_banjir.empty:
    filtered_banjir['tahun'] = pd.to_datetime(filtered_banjir['tanggal']).dt.year
    banjir_tahunan = filtered_banjir.groupby('tahun').size().reset_index(name='jumlah_banjir')
    fig_banjir = px.bar(banjir_tahunan, x='tahun', y='jumlah_banjir',
                        title=f"Kejadian Banjir: {', '.join(selected_kelurahan)}")
    st.plotly_chart(fig_banjir, use_container_width=True)
else:
    st.warning("Tidak ada data kejadian banjir untuk kelurahan yang dipilih.")

# 3. Heatmap - Wilayah Rawan Banjir
st.subheader("3. Heatmap Wilayah yang Paling Sering Terkena Banjir")
if not filtered_banjir.empty:
    kelurahan_count = filtered_banjir['kelurahan'].value_counts().reset_index()
    kelurahan_count.columns = ['Kelurahan', 'Frekuensi']
    fig_heat = px.density_heatmap(kelurahan_count, x='Kelurahan', y='Frekuensi',
                                  color_continuous_scale='OrRd')
    st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.info("Tidak ada data untuk membuat heatmap.")

# Scatter Plot - Korelasi Curah Hujan dan Korban
st.subheader("4. Korelasi antara Curah Hujan dan Jumlah Korban")
merged = pd.merge(rain, banjir, on='tanggal', how='inner')
fig_scatter = px.scatter(merged, x='curah_hujan', y='korban_terdampak', color='kelurahan',
                         title='Curah Hujan vs Korban Terdampak')
st.plotly_chart(fig_scatter, use_container_width=True)
# 4. Tambahan: Scatter jika kamu ingin menampilkan korelasi (opsional)
# st.subheader("Korelasi Curah Hujan & Kejadian Banjir (opsional)")
# ... (bisa ditambahkan nanti)

# Map - Visualisasi Lokasi Banjir
st.subheader("5. Peta Sebaran Kejadian Banjir di Kota Bima")
fig_map = px.scatter_mapbox(
    banjir, lat="latitude", lon="longitude",
    hover_name="kelurahan", hover_data=["tanggal", "korban_terdampak"],
    color="korban_terdampak", size="korban_terdampak",
    zoom=11, height=500, mapbox_style="open-street-map"
)
st.plotly_chart(fig_map, use_container_width=True)

