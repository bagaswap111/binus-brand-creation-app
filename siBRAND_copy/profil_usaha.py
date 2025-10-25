import streamlit as st
import streamlit.components.v1 as components
from session_storage import save_form_data_to_session

def run():
    st.header("Profil Usaha Anda")

    # Initialize session state for form data if not exists
    if 'profil_usaha' not in st.session_state:
        st.session_state.profil_usaha = {}

    # Load existing data if available
    existing_data = st.session_state.profil_usaha

    # --- FORM ---
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Usaha", value=existing_data.get('nama', ''))
        alamat = st.text_input("Alamat Usaha", value=existing_data.get('alamat', ''))
        kota = st.text_input("Kota", value=existing_data.get('kota', ''))
        
        lokasi_options = ["Ruko", "Toko Online", "Pasar", "Whatsapp, Instagram", "Pinggir jalan raya", "Mall"]
        default_lokasi = existing_data.get('lokasi', [])
        lokasi = st.multiselect(
            "Lokasi Toko / Platform Penjualan",
            lokasi_options,
            default=default_lokasi
        )
        
        karyawan = st.text_input("Jumlah Karyawan", value=existing_data.get('karyawan', ''))

    with col2:
        ig = st.text_input("Akun Media Sosial Instagram", value=existing_data.get('ig', ''))
        tiktok = st.text_input("Akun Media Sosial Tiktok", value=existing_data.get('tiktok', ''))
        fb = st.text_input("Akun Media Sosial Facebook", value=existing_data.get('fb', ''))
        
        logo_file = st.file_uploader("Logo Merk (jika ada)", type=["jpg", "png"])
        
        bidang_options = ["Fesyen (Pakaian, Tas, Sepatu, Aksesoris)", "FnB (Makanan, Minuman, Camilan)"]
        default_bidang = existing_data.get('bidang', bidang_options[0])
        bidang = st.radio(
            "Bidang Usaha",
            bidang_options,
            index=bidang_options.index(default_bidang) if default_bidang in bidang_options else 0
        )

    # --- BUTTON ---
    if st.button("💾 Simpan dan Lanjut"):
        # Validate required fields
        if not nama:
            st.error("Nama Usaha harus diisi!")
            return
            
        data = {
            "nama": nama,
            "alamat": alamat,
            "kota": kota,
            "lokasi": lokasi,
            "karyawan": karyawan,
            "ig": ig,
            "tiktok": tiktok,
            "fb": fb,
            "bidang": bidang,
            "logo_uploaded": logo_file is not None
        }

        # Simpan data ke session
        save_form_data_to_session("profil_usaha", data)

        st.success("✅ Data profil usaha tersimpan!")
        
        # Debug: Show where we're going
        st.write(f"Moving to: Detail Produk yang Anda Jual")
        
        # Pindah ke halaman berikutnya - USE EXACT MATCHING NAME
        st.session_state.page = "Detail Produk"  # Make sure this matches your menu_items exactly
        st.rerun()

    # Show current session state for debugging
    with st.expander("Debug Info"):
        st.write("Current session state:", dict(st.session_state))
        st.write("Current profil_usaha data:", st.session_state.get('profil_usaha', {}))