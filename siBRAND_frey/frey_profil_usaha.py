import streamlit as st

def run():
    st.header("Profil Usaha Anda")

    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Usaha")
        alamat = st.text_input("Alamat Usaha")
        kota = st.text_input("Kota")
        lokasi = st.multiselect(
            "Lokasi Toko / Platform Penjualan",
            ["Ruko", "Toko Online", "Pasar", "Whatsapp, Instagram", "Pinggir jalan raya", "Mall"]
        )
        karyawan = st.text_input("Jumlah Karyawan")
    with col2:
        ig = st.text_input("Akun Media Sosial Instagram")
        tiktok = st.text_input("Akun Media Sosial Tiktok")
        fb = st.text_input("Akun Media Sosial Facebook")
        st.file_uploader("Logo Merk (jika ada)", type=["jpg", "png"])
        bidang = st.radio("Bidang Usaha", ["Fesyen (Pakaian, Tas, Sepatu, Aksesoris)", "FnB (Makanan, Minuman, Camilan)"])

    st.button("Simpan dan Lanjut")
