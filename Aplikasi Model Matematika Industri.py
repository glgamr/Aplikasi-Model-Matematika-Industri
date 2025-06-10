# Aplikasi Model Matematika Industri
# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Aplikasi Model Matematika Industri", layout="wide")

st.sidebar.title("Instruksi")
st.sidebar.info("""
1. Pilih tab di atas untuk model yang diinginkan.
2. Masukkan parameter model.
3. Lihat hasil dan grafik visualisasi.
""")

# Tab Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Optimasi Produksi",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Break-even Analysis"
])

# === TAB 1: Linear Programming ===
with tab1:
    st.header("Optimasi Produksi (Linear Programming)")

    st.write("Masukkan data model:")
    c1 = st.number_input("Keuntungan produk A", value=20)
    c2 = st.number_input("Keuntungan produk B", value=30)

    a11 = st.number_input("Waktu mesin (jam) produk A", value=1)
    a12 = st.number_input("Waktu mesin (jam) produk B", value=2)
    b1 = st.number_input("Total waktu mesin tersedia (jam)", value=40)

    a21 = st.number_input("Tenaga kerja produk A", value=2)
    a22 = st.number_input("Tenaga kerja produk B", value=1)
    b2 = st.number_input("Total tenaga kerja tersedia", value=50)

    if st.button("Hitung Optimasi"):
        c = [-c1, -c2]  # Maximize
        A = [[a11, a12], [a21, a22]]
        b = [b1, b2]
        x_bounds = (0, None)

        res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, x_bounds], method='highs')

        if res.success:
            st.success(f"Jumlah Produk A: {res.x[0]:.2f}, Produk B: {res.x[1]:.2f}")
            st.info(f"Total Keuntungan Maksimum: {-res.fun:.2f}")
        else:
            st.error("Optimasi gagal.")

# === TAB 2: EOQ ===
with tab2:
    st.header("Model Persediaan (EOQ)")

    D = st.number_input("Permintaan tahunan (D)", value=1000)
    S = st.number_input("Biaya pemesanan (S)", value=100)
    H = st.number_input("Biaya penyimpanan per unit/tahun (H)", value=10)

    if st.button("Hitung EOQ"):
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ: {EOQ:.2f} unit per pemesanan")

        fig, ax = plt.subplots()
        Q = np.linspace(1, 2*EOQ, 100)
        TC = (D/Q)*S + (Q/2)*H
        ax.plot(Q, TC, label='Total Cost')
        ax.axvline(EOQ, color='red', linestyle='--', label='EOQ')
        ax.set_title("Total Biaya vs Jumlah Pesanan")
        ax.set_xlabel("Jumlah Pesanan (Q)")
        ax.set_ylabel("Total Biaya")
        ax.legend()
        st.pyplot(fig)

# === TAB 3: Antrian (M/M/1) ===
with tab3:
    st.header("Model Antrian (M/M/1)")

    lam = st.number_input("Rata-rata kedatangan (λ)", value=2.0)
    mu = st.number_input("Rata-rata pelayanan (μ)", value=5.0)

    if lam >= mu:
        st.error("Sistem tidak stabil. λ harus lebih kecil dari μ.")
    else:
        rho = lam / mu
        L = rho / (1 - rho)
        Lq = (rho**2) / (1 - rho)
        W = 1 / (mu - lam)
        Wq = rho / (mu - lam)

        st.success(f"Utilisasi Sistem (ρ): {rho:.2f}")
        st.write(f"Jumlah rata-rata dalam sistem (L): {L:.2f}")
        st.write(f"Jumlah rata-rata dalam antrian (Lq): {Lq:.2f}")
        st.write(f"Waktu rata-rata dalam sistem (W): {W:.2f}")
        st.write(f"Waktu rata-rata dalam antrian (Wq): {Wq:.2f}")

        fig, ax = plt.subplots()
        traffic = np.linspace(0.01, 0.99, 100)
        ax.plot(traffic, traffic / (1 - traffic), label='L')
        ax.set_title("L vs Utilisasi")
        ax.set_xlabel("ρ (λ/μ)")
        ax.set_ylabel("L")
        st.pyplot(fig)

# === TAB 4: Break-even Analysis ===
with tab4:
    st.header("Model Tambahan: Break-even Analysis")

    FC = st.number_input("Fixed Cost", value=10000)
    VC = st.number_input("Variable Cost per unit", value=50)
    P = st.number_input("Selling Price per unit", value=100)

    if VC >= P:
        st.error("Harga jual harus lebih besar dari biaya variabel.")
    else:
        BEQ = FC / (P - VC)
        st.success(f"Titik impas (Break-even Quantity): {BEQ:.2f} unit")

        Q = np.linspace(0, BEQ*2, 100)
        TR = P * Q
        TC = FC + VC * Q

        fig, ax = plt.subplots()
        ax.plot(Q, TR, label='Total Revenue')
        ax.plot(Q, TC, label='Total Cost')
        ax.axvline(BEQ, color='red', linestyle='--', label='Break-even Point')
        ax.set_title("Break-even Analysis")
        ax.set_xlabel("Quantity")
        ax.set_ylabel("Cost / Revenue")
        ax.legend()
        st.pyplot(fig)
