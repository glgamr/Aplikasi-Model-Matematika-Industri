import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Aplikasi Model Matematika Industri", layout="wide")

with st.sidebar:
    st.title("📘 Petunjuk Aplikasi")
    st.write("Aplikasi ini terdiri dari 4 model matematika industri:")
    st.markdown("""
    1. **Optimasi Produksi (Linear Programming)**
    2. **Model Persediaan (EOQ)**
    3. **Model Antrian (M/M/1)**
    4. **Prediksi Permintaan (Regresi Linier)**
    
    Masukkan parameter pada tiap tab dan lihat hasil visualisasi serta outputnya.
    """)

tabs = st.tabs(["Optimasi Produksi", "Model EOQ", "Model Antrian", "Prediksi Permintaan"])

# Tab 1: Linear Programming
with tabs[0]:
    st.header("Optimasi Produksi (Linear Programming)")
    st.write("Gunakan Linear Programming untuk memaksimalkan keuntungan.")

    c1 = st.number_input("Keuntungan produk A", value=5)
    c2 = st.number_input("Keuntungan produk B", value=4)

    A = [[2, 3], [4, 1]]  # Koefisien kendala
    b = [100, 80]  # Batasan sumber daya
    c = [-c1, -c2]  # Negatif karena linprog melakukan minimisasi

    bounds = [(0, None), (0, None)]
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if res.success:
        st.success("Solusi ditemukan!")
        st.write(f"Produksi Produk A: {res.x[0]:.2f} unit")
        st.write(f"Produksi Produk B: {res.x[1]:.2f} unit")

        fig, ax = plt.subplots()
        ax.bar(['Produk A', 'Produk B'], res.x, color=['blue', 'orange'])
        ax.set_ylabel('Jumlah Produksi')
        st.pyplot(fig)
    else:
        st.error("Solusi tidak ditemukan.")

# Tab 2: EOQ
with tabs[1]:
    st.header("Model Persediaan (EOQ)")
    D = st.number_input("Permintaan Tahunan (D)", value=1000)
    S = st.number_input("Biaya Pemesanan per Order (S)", value=50)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=2)

    if H > 0:
        eoq = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ (Jumlah Pemesanan Ekonomis): {eoq:.2f} unit")

        fig, ax = plt.subplots()
        q = np.linspace(1, 2*eoq, 100)
        tc = (D/q)*S + (q/2)*H
        ax.plot(q, tc)
        ax.set_xlabel('Jumlah Pemesanan (Q)')
        ax.set_ylabel('Total Biaya')
        ax.set_title('Kurva Total Biaya vs EOQ')
        st.pyplot(fig)

# Tab 3: M/M/1 Queue
with tabs[2]:
    st.header("Model Antrian (M/M/1)")
    lambd = st.number_input("Rata-rata Kedatangan (λ)", value=2.0)
    mu = st.number_input("Rata-rata Pelayanan (μ)", value=4.0)

    if mu > lambd:
        rho = lambd / mu
        L = rho / (1 - rho)
        W = 1 / (mu - lambd)
        st.success(f"Utilisasi: {rho:.2f}")
        st.write(f"Jumlah rata-rata dalam sistem (L): {L:.2f}")
        st.write(f"Waktu rata-rata dalam sistem (W): {W:.2f} jam")

        fig, ax = plt.subplots()
        ax.bar(['Utilisasi', 'L', 'W'], [rho, L, W], color='green')
        st.pyplot(fig)
    else:
        st.error("μ harus lebih besar dari λ agar sistem stabil.")

# Tab 4: Regresi Linier
with tabs[3]:
    st.header("Prediksi Permintaan (Regresi Linier)")
    st.write("Masukkan data bulan dan permintaan.")
    months = st.text_input("Bulan (pisahkan dengan koma)", "1,2,3,4,5")
    demand = st.text_input("Permintaan (pisahkan dengan koma)", "100,120,130,150,170")

    try:
        x = np.array([int(i) for i in months.split(',')])
        y = np.array([int(i) for i in demand.split(',')])

        if len(x) == len(y) and len(x) >= 2:
            coef = np.polyfit(x, y, 1)
            trend = np.poly1d(coef)

            st.success(f"Model: permintaan = {coef[0]:.2f} * bulan + {coef[1]:.2f}")

            fig, ax = plt.subplots()
            ax.scatter(x, y, color='blue', label='Data')
            ax.plot(x, trend(x), color='red', label='Regresi')
            ax.set_xlabel('Bulan')
            ax.set_ylabel('Permintaan')
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("Data bulan dan permintaan harus sama panjang dan minimal 2 data.")
    except:
        st.error("Format input tidak valid. Gunakan angka dan koma.")
