import streamlit as st
import numpy as np
from scipy.optimize import linprog
from math import sqrt
import matplotlib.pyplot as plt

st.set_page_config(page_title="Model Matematika Industri", layout="centered")

st.title("📊 Aplikasi Model Matematika Industri")
menu = st.sidebar.selectbox("Pilih Model", [
    "1. Linear Programming – Optimasi Produksi",
    "2. EOQ – Economic Order Quantity",
    "3. Antrian M/M/1 – Layanan Pelanggan",
    "4. Regresi Linier – Prediksi Permintaan"
])

# 1. Linear Programming
if "Linear Programming" in menu:
    st.header("1. Linear Programming – Optimasi Produksi")

    profit_A = st.number_input("Keuntungan per unit Produk A (Meja)", value=50000)
    profit_B = st.number_input("Keuntungan per unit Produk B (Kursi)", value=40000)

    jam_A = st.number_input("Jam kerja tukang untuk Produk A", value=2.0)
    jam_B = st.number_input("Jam kerja tukang untuk Produk B", value=3.0)
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
            st.success(f"Meja: {x:.2f}, Kursi: {y:.2f}, Keuntungan: Rp {abs(res.fun):,.0f}")

            # Visualisasi grafik
            x_vals = np.linspace(0, 60, 400)
            y1 = (max_jam - jam_A * x_vals) / jam_B
            y2 = (max_papan - papan_A * x_vals) / papan_B

            plt.figure()
            plt.plot(x_vals, y1, label="Kendala Jam Kerja")
            plt.plot(x_vals, y2, label="Kendala Papan Kayu")
            plt.fill_between(x_vals, 0, np.minimum(y1, y2), where=(np.minimum(y1, y2) > 0), color='lightgreen', alpha=0.5)
            plt.plot(x, y, 'ro', label="Solusi Optimal")
            plt.xlabel("Jumlah Meja (x)")
            plt.ylabel("Jumlah Kursi (y)")
            plt.title("Wilayah Feasible & Solusi")
            plt.legend()
            st.pyplot(plt)
        else:
            st.error("Tidak ada solusi yang memenuhi.")

# 2. EOQ
elif "EOQ" in menu:
    st.header("2. EOQ – Economic Order Quantity")

    D = st.number_input("Permintaan Tahunan (unit)", value=1000)
    S = st.number_input("Biaya Pemesanan per Order (Rp)", value=50000)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", value=2000)

    if st.button("Hitung EOQ"):
        EOQ = sqrt((2 * D * S) / H)
        st.success(f"EOQ: {EOQ:.2f} unit")

        Q = np.linspace(1, 2 * EOQ, 500)
        TC = (D / Q) * S + (Q / 2) * H

        plt.figure()
        plt.plot(Q, TC, label='Total Cost')
        plt.axvline(EOQ, color='r', linestyle='--', label='EOQ')
        plt.title("Total Cost vs. Quantity")
        plt.xlabel("Order Quantity (Q)")
        plt.ylabel("Total Cost")
        plt.legend()
        st.pyplot(plt)

# 3. Antrian M/M/1
elif "Antrian" in menu:
    st.header("3. Antrian M/M/1 – Sistem Layanan")

    λ = st.number_input("Tingkat Kedatangan λ (pelanggan/jam)", value=2.0)
    μ = st.number_input("Tingkat Pelayanan μ (pelanggan/jam)", value=4.0)

    if st.button("Hitung Antrian"):
        if λ >= μ:
            st.error("Sistem tidak stabil: λ harus < μ")
        else:
            ρ = λ / μ
            L = λ / (μ - λ)
            W = 1 / (μ - λ)
            st.success(f"Utilisasi (ρ): {ρ*100:.2f}%")
            st.write(f"Rata-rata pelanggan (L): {L:.2f}")
            st.write(f"Rata-rata waktu dalam sistem (W): {W*60:.2f} menit")

            # Grafik: Utilisasi terhadap L dan W
            lam_vals = np.linspace(0.01, μ - 0.01, 500)
            L_vals = lam_vals / (μ - lam_vals)
            W_vals = 1 / (μ - lam_vals)

            fig, ax = plt.subplots(2, 1, figsize=(6, 8))
            ax[0].plot(lam_vals, L_vals, label='L (Pelanggan dalam sistem)')
            ax[0].axvline(λ, color='r', linestyle='--', label='λ Sekarang')
            ax[0].legend()
            ax[0].set_title("λ vs L")
            ax[0].set_xlabel("λ")
            ax[0].set_ylabel("L")

            ax[1].plot(lam_vals, W_vals, label='W (Waktu dalam sistem)', color='green')
            ax[1].axvline(λ, color='r', linestyle='--', label='λ Sekarang')
            ax[1].legend()
            ax[1].set_title("λ vs W")
            ax[1].set_xlabel("λ")
            ax[1].set_ylabel("W (jam)")

            st.pyplot(fig)

# 4. Regresi Linier
elif "Regresi" in menu:
    st.header("4. Regresi Linier – Prediksi Permintaan")

    n = st.number_input("Jumlah Bulan", min_value=2, max_value=12, value=5)
    bulan = []
    permintaan = []

    for i in range(int(n)):
        col1, col2 = st.columns(2)
        with col1:
            x = st.number_input(f"Bulan ke-{i+1}", value=i+1, key=f"x_{i}")
        with col2:
            y = st.number_input(f"Permintaan ke-{i+1}", value=100 + i * 20, key=f"y_{i}")
        bulan.append(x)
        permintaan.append(y)

    bulan = np.array(bulan)
    permintaan = np.array(permintaan)

    if st.button("Hitung Regresi dan Prediksi"):
        a, b = np.polyfit(bulan, permintaan, 1)

        def predict(x): return a * x + b
        next_month = int(max(bulan) + 1)
        prediksi = predict(next_month)

        st.success(f"Persamaan: Y = {a:.2f}X + {b:.2f}")
        st.write(f"Prediksi Bulan ke-{next_month}: {prediksi:.2f} unit")

        # Grafik
        plt.figure()
        plt.scatter(bulan, permintaan, label="Data Aktual")
        plt.plot(bulan, predict(bulan), color="red", label="Regresi Linier")
        plt.axvline(next_month, color='gray', linestyle='--')
        plt.scatter(next_month, prediksi, color='green', label=f"Prediksi Bulan {next_month}")
        plt.title("Prediksi Permintaan Bulanan")
        plt.xlabel("Bulan")
        plt.ylabel("Permintaan")
        plt.legend()
        st.pyplot(plt)
