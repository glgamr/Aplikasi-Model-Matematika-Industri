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

    # Fungsi tujuan: Maksimalkan Z = 50.000x + 40.000y
    c = [-50000, -40000]  # dikali -1 karena linprog meminimalkan

    # Kendala:
    A = [
        [2, 3],   # 2x + 3y <= 100 (jam kerja tukang kayu)
        [4, 1]    # 4x +  y <= 80 (papan kayu)
    ]
    b = [100, 80]
    bounds = [(0, None), (0, None)]

    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if res.success:
        x, y = res.x
        st.success("Solusi ditemukan:")
        st.write(f"Jumlah Meja (x): {x:.2f}")
        st.write(f"Jumlah Kursi (y): {y:.2f}")
        st.write(f"Maksimum Keuntungan: Rp {abs(res.fun):,.0f}")
    else:
        st.error("Solusi tidak ditemukan.")

# ---------------------------------------------
# 2. EOQ
# ---------------------------------------------
elif "EOQ" in menu:
    st.header("2. EOQ – Economic Order Quantity")

    D = 1000    # permintaan tahunan
    S = 50000   # biaya pemesanan
    H = 2000    # biaya penyimpanan per unit

    eoq = sqrt((2 * D * S) / H)

    st.write(f"Permintaan tahunan (D): {D}")
    st.write(f"Biaya pemesanan per order (S): Rp {S:,}")
    st.write(f"Biaya penyimpanan per unit per tahun (H): Rp {H:,}")
    st.success(f"Jumlah Pemesanan Ekonomis (EOQ): {eoq:.2f} unit")

# ---------------------------------------------
# 3. Antrian M/M/1
# ---------------------------------------------
elif "Antrian" in menu:
    st.header("3. Antrian M/M/1 – Sistem Layanan Pelanggan")

    λ = 2  # pelanggan per jam
    μ = 4  # layanan per jam

    if λ >= μ:
        st.error("Sistem tidak stabil (λ harus < μ).")
    else:
        ρ = λ / μ
        L = λ / (μ - λ)
        W = 1 / (μ - λ)

        st.write(f"Tingkat Kedatangan (λ): {λ} pelanggan/jam")
        st.write(f"Tingkat Pelayanan (μ): {μ} pelanggan/jam")
        st.success(f"Utilisasi Teknisi (ρ): {ρ:.2f} atau {ρ*100:.0f}%")
        st.success(f"Rata-rata pelanggan dalam sistem (L): {L:.2f} orang")
        st.success(f"Rata-rata waktu dalam sistem (W): {W*60:.2f} menit")

# ---------------------------------------------
# 4. Regresi Linier
# ---------------------------------------------
elif "Regresi" in menu:
    st.header("4. Regresi Linier – Prediksi Permintaan Bulanan")

    bulan = np.array([1, 2, 3, 4, 5])
    permintaan = np.array([100, 120, 130, 150, 170])

    n = len(bulan)
    sum_x = bulan.sum()
    sum_y = permintaan.sum()
    sum_xy = (bulan * permintaan).sum()
    sum_x2 = (bulan ** 2).sum()

    b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    a = (sum_y - b * sum_x) / n

    def predict(x): return a + b * x
    bulan_ke6 = predict(6)

    st.write(f"Persamaan regresi: Y = {a:.2f} + {b:.2f}X")
    st.success(f"Prediksi permintaan bulan ke-6: {bulan_ke6:.2f} unit")

    # Plot grafik
    plt.figure()
    plt.scatter(bulan, permintaan, color='blue', label='Data Aktual')
    plt.plot(bulan, predict(bulan), color='red', label='Regresi Linier')
    plt.xlabel("Bulan")
    plt.ylabel("Permintaan")
    plt.title("Prediksi Permintaan dengan Regresi Linier")
    plt.legend()
    st.pyplot(plt)
