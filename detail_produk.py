import streamlit as st
from session_storage import save_form_data_to_session

def run():
    st.header("Detail Produk yang Anda Jual")

    # Initialize session state for form data if not exists
    if 'detail_produk' not in st.session_state:
        st.session_state.detail_produk = {}

    # Load existing data if available
    existing_data = st.session_state.detail_produk

    jenis_options = ["Kafe / restoran", "Frozen Food / Makanan Siap Saji", "Street Food", "Makanan Kekinian",
         "Makanan Tradisional", "Roti & Pastry", "Katering",
          "Retail", "Grosir", "Fashion brand", "Penjahit", "Thrift (baju bekas)", "Lainnya"]
    
    jenis = st.multiselect(
        "Jenis Produk/Usaha",
        jenis_options,
        default=existing_data.get('jenis_produk', [])
    )
    
    katalog_file = st.file_uploader("Upload Katalog Produk", type=["jpg", "png", "pdf"])
    
    kategori_options = ["Premium", "Sehat dan natural", "Mudah dan Terjangkau", "Homemade / Rumahan",
         "Modern dan kekinian", "Praktis", "Tradisional dan Otentik"]
    
    kategori = st.multiselect(
        "Kategori / Karakter Produk",
        kategori_options,
        default=existing_data.get('kategori_karakter', [])
    )

    st.subheader("Target Pembeli")
    groups = ["Anak-anak", "Siswa/Mahasiswa", "Pegawai/Karyawan/Guru", "Keluarga Muda", "Orang Tua (di atas 50 tahun)"]
    target_pembeli = existing_data.get('target_pembeli', {})
    
    # Initialize target_pembeli if empty
    for g in groups:
        if g not in target_pembeli:
            target_pembeli[g] = "Tidak ada"
    
    for g in groups:
        current_value = target_pembeli.get(g, "Tidak ada")
        options = ["Tidak ada", "Sedikit", "Cukup banyak", "Sangat banyak"]
        target_pembeli[g] = st.radio(
            f"{g}", 
            options, 
            index=options.index(current_value) if current_value in options else 0, 
            horizontal=True,
            key=f"target_{g}"  # Add unique key untuk setiap radio
        )

    pantangan_options = ["Ya", "Tidak"]
    current_pantangan = existing_data.get('pantangan_khusus', "Tidak")
    pantangan_khusus = st.radio(
        "Apakah produk ini khusus untuk orang dengan penyakit atau pantangan tertentu?",
        pantangan_options,
        index=pantangan_options.index(current_pantangan) if current_pantangan in pantangan_options else 1,
        key="pantangan_khusus"
    )

    if st.button("Selanjutnya"):
        # Validasi data
        if not jenis:
            st.error("Pilih minimal satu jenis produk/usaha!")
            return
            
        if not kategori:
            st.error("Pilih minimal satu kategori produk!")
            return

        data = {
            "jenis_produk": jenis,
            "kategori_karakter": kategori,
            "target_pembeli": target_pembeli,
            "pantangan_khusus": pantangan_khusus,
            "katalog_uploaded": katalog_file is not None
        }

        # Debug: Show data before saving
        st.write("Data yang akan disimpan:", data)

        # Simpan data ke session
        save_form_data_to_session("detail_produk", data)

        st.success("✅ Data detail produk tersimpan!")
        
        # Debug: Verify data saved
        st.write("Data setelah disimpan:", st.session_state.get('detail_produk', {}))
        
        # Pindah ke halaman berikutnya
        st.session_state.page = "Karakter Merk"
        st.rerun()

    # Debug section
    with st.expander("🔍 Debug - Session Data"):
        st.write("Current detail_produk in session:", st.session_state.get('detail_produk', {}))
        st.write("All session state:", dict(st.session_state))