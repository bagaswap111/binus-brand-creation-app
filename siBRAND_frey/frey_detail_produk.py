import streamlit as st

def run():
    st.header("Detail Produk yang Anda Jual")

    jenis = st.multiselect(
        "Jenis Produk/Usaha",
        ["Kafe / restoran", "Frozen Food / Makanan Siap Saji", "Street Food", "Makanan Kekinian",
         "Makanan Tradisional", "Roti & Pastry", "Katering", "Lainnya"]
    )
    st.file_uploader("Upload Katalog Produk", type=["jpg", "png", "pdf"])
    kategori = st.multiselect(
        "Kategori / Karakter Produk",
        ["Premium", "Sehat dan natural", "Mudah dan Terjangkau", "Homemade / Rumahan",
         "Modern dan kekinian", "Praktis", "Tradisional dan Otentik"]
    )

    st.subheader("Target Pembeli")
    groups = ["Anak-anak", "Siswa/Mahasiswa", "Pegawai/Karyawan/Guru", "Keluarga Muda", "Orang Tua (di atas 50 tahun)"]
    for g in groups:
        st.radio(f"{g}", ["Tidak ada", "Sedikit", "Cukup banyak", "Sangat banyak"], horizontal=True)

    st.radio("Apakah produk ini khusus untuk orang dengan penyakit atau pantangan tertentu?",
             ["Ya", "Tidak"])

    st.button("Selanjutnya")
