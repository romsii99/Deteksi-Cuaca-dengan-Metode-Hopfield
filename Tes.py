import streamlit as st
import numpy as np

# Definisikan jaringan Hopfield
class HopfieldNetwork:
    def __init__(self, ukuran):  # Perbaiki kesalahan ketik di sini
        self.ukuran = ukuran
        self.bobot = np.zeros((ukuran, ukuran))

    def latih(self, pola):
        for p in pola:
            self.bobot += np.outer(p, p)
        self.bobot[np.diag_indices(self.ukuran)] = 0

    def prediksi(self, pola, langkah=5):
        for _ in range(langkah):
            for i in range(self.ukuran):
                pola[i] = 1 if np.dot(self.bobot[i], pola) >= 0 else -1
        return pola

# Peta kondisi cuaca ke pola
peta_cuaca = {
    "cerah": [1, -1, 1, -1],
    "berawan": [-1, -1, -1, -1],
    "hujan": [-1, 1, -1, 1]
}

# Peta balik
peta_balik_cuaca = {
    (1, -1, 1, -1): "cerah",
    (-1, -1, -1, -1): "berawan",
    (-1, 1, -1, 1): "hujan"
}

# Inisialisasi jaringan Hopfield
jaringan_hopfield = HopfieldNetwork(ukuran=4)
pola = np.array(list(peta_cuaca.values()))
jaringan_hopfield.latih(pola)

# UI Streamlit
st.title("Prediksi Cuaca menggunakan Jaringan Hopfield")

arah_angin = st.number_input("Arah Angin (derajat)", min_value=0, max_value=360)
suhu = st.number_input("Suhu (°C)", min_value=-50.0, max_value=50.0)
kelembapan = st.number_input("Kelembapan (%)", min_value=0.0, max_value=100.0)
tekanan = st.number_input("Tekanan (mb)", min_value=900.0, max_value=1100.0)

def dapatkan_keadaan_cuaca(arah_angin, suhu, kelembapan, tekanan):
    # Konversi parameter input ke pola
    if arah_angin < 150:
        pola_angin = 1
    elif arah_angin <= 200:
        pola_angin = -1
    else:
        pola_angin = -1
    
    if suhu > 29:
        pola_suhu = -1 
    elif suhu >= 26:
        pola_suhu = 1
    else:
        pola_suhu = -1
    
    if kelembapan < 70:
        pola_kelembapan = 1
    elif kelembapan <= 85:
        pola_kelembapan = -1
    else:
        pola_kelembapan = -1
    
    if tekanan > 1010:
        pola_tekanan = -1
    elif tekanan >= 1007:
        pola_tekanan = 1
    else:
        pola_tekanan = 1
    
    return np.array([pola_angin, pola_suhu, pola_kelembapan, pola_tekanan])

if st.button("Prediksi Cuaca"):
    pola = dapatkan_keadaan_cuaca(arah_angin, suhu, kelembapan, tekanan)
    hasil = jaringan_hopfield.prediksi(pola.copy())
    kondisi_cuaca = peta_balik_cuaca.get(tuple(hasil), "Tidak Diketahui")
    st.write(f"Kondisi Cuaca yang Diprediksi: {kondisi_cuaca}")
