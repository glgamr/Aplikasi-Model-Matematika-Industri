import streamlit as st
import numpy as np
from scipy.optimize import linprog
from math import sqrt
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aplikasi Model Matematika Industri", layout="centered")

st.title("📊 Aplikasi Model Matematika Industri")
menu = st.sidebar.selectbox("Pilih Model", [
    "1. Linear Programming – Optimasi Produksi",
    "2. EOQ – Economic Order Quantity",
    "3. Antrian M/M/1 – Layanan Pelanggan",
    "4. Regresi Linier – Prediksi Permintaan"
])

# ---------------------------------------------
# 1. Linear Programming
# ---------------------------------------------
if "Linear Programming" in menu:
    st.header("1. Linear Programming – Optimasi Produksi")

    st.subheader("Masukkan parameter:")
    profit_A = st.number_input("Keuntungan per unit Produk A (Meja)", value=50000)
    profit_B = st.number_input("Keuntungan per unit Produk B (Kursi)", value=40000)

    jam_A = st.number_input("Jam tukang untuk Produk A", value=2.0)
    jam_B = st.number_input("Jam tukang untuk Produk B", value=3.0)
    papan_A = st.number_input("Papan kayu untuk Produk A", value=4.0)
    papan_B = st.number_input("Papan kayu untuk Produk B", value=1.0)

    max_jam = st.number_input("Total jam kerja tersedia", value=100.0)
    max_papan = st.number_input("Total papan kayu tersedia", value=80.0)

    if st.button("Hitung Optimasi Produksi"):
        c = [-profit_A, -profit_B]
        A = [[jam_A, jam_B], [papan_A, papan_B]]
        b = [max_jam, max_papan]
        bounds = [(0, None), (0, None)]

        res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
        if res.success:
            x, y = res.x
            st.success("Solusi ditemukan:")
            st.write(f"Jumlah Produk A (Meja): {x:.2f}")
            st.write(f"Jumlah Produk B (Kursi): {y:.2f}")
            st.write(f"Maksimum Keuntungan: Rp {abs(res.fun):,.0f}")
        else:
            st.error("Solusi tidak ditemukan.")

# ---------------------------------------------
# 2. EOQ
# ---------------------------------------------
elif "EOQ" in menu:
    st.header("2. EOQ – Economic Order Quantity")

    D = st.number_input("Permintaan Tahunan (unit)", value=1000)
    S = st.number_input("Biaya Pemesanan per Order (Rp)", value=50000)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", value=2000)

    if st.button("Hitung EOQ"):
        eoq = sqrt((2 * D * S) / H)
        st.success(f"Jumlah Pemesanan Ekonomis (EOQ): {eoq:.2f} unit")

# ---------------------------------------------
# 3. Antrian M/M/1
# ---------------------------------------------
elif "Antrian" in menu:
    st.header("3. Antrian M/M/1 – Sistem Layanan Pelanggan")

    λ = st.number_input("Tingkat Kedatangan (λ) pelanggan/jam", value=2.0)
    μ = st.number_input("Tingkat Pelayanan (μ) pelanggan/jam", value=4.0)

    if st.button("Hitung Antrian"):
        if λ >= μ:
            st.error("Sistem tidak stabil. λ harus lebih kecil dari μ.")
        else:
            ρ = λ / μ
            L = λ / (μ - λ)
            W = 1 / (μ - λ)
            st.success(f"Utilisasi Teknisi: {ρ*100:.2f}%")
            st.write(f"Rata-rata pelanggan dalam sistem (L): {L:.2f}")
            st.write(f"Waktu rata-rata pelanggan dalam sistem (W): {W*60:.2f} menit")

# ---------------------------------------------
# 4. Regresi Linier
# ---------------------------------------------
elif "Regresi" in menu:
    st.header("4. Regresi Linier – Prediksi Permintaan Bulanan")

    st.write("Masukkan data bulan dan permintaan:")
    jumlah_data = st.number_input("Jumlah Bulan", min_value=2, max_value=12, value=5)

    bulan = []
    permintaan = []

    for i in range(int(jumlah_data)):
        col1, col2 = st.columns(2)
        with col1:
            x = st.number_input(f"Bulan ke-{i+1}", value=i+1, key=f"x_{i}")
        with col2:
            y = st.number_input(f"Permintaan bulan ke-{i+1}", value=100 + i*20, key=f"y_{i}")
        bulan.append(x)
        permintaan.append(y)

    bulan = np.array(bulan)
    permintaan = np.array(permintaan)

    if st.button("Hitung Regresi dan Prediksi"):
        n = len(bulan)
        sum_x = bulan.sum()
        sum_y = permintaan.sum()
        sum_xy = (bulan * permintaan).sum()
        sum_x2 = (bulan ** 2).sum()

        b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        a = (sum_y - b * sum_x) / n

        def predict(x): return a + b * x
        bulan_next = int(max(bulan) + 1)
        prediksi = predict(bulan_next)

        st.write(f"Persamaan regresi: Y = {a:.2f} + {b:.2f}X")
        st.success(f"Prediksi permintaan bulan ke-{bulan_next}: {prediksi:.2f} unit")

        # Grafik
        plt.figure()
        plt.scatter(bulan, permintaan, color='blue', label='Data Aktual')
        plt.plot(bulan, predict(bulan), color='red', label='Regresi Linier')
        plt.xlabel("Bulan")
        plt.ylabel("Permintaan")
        plt.title("Prediksi Permintaan")
        plt.legend()
        st.pyplot(plt)
