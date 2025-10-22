import streamlit as st
import streamlit.components.v1 as components
from session_storage import save_to_session_storage  # pakai fungsi buatanmu

def run():
    st.header("Profil Usaha Anda")

    # --- FORM ---
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
        bidang = st.radio(
            "Bidang Usaha",
            ["Fesyen (Pakaian, Tas, Sepatu, Aksesoris)", "FnB (Makanan, Minuman, Camilan)"]
        )

    # --- BUTTON ---
    if st.button("💾 Simpan dan Lanjut"):
        data = {
            "nama": nama,
            "alamat": alamat,
            "kota": kota,
            "lokasi": lokasi,
            "karyawan": karyawan,
            "ig": ig,
            "tiktok": tiktok,
            "fb": fb,
            "bidang": bidang
        }

        # Simpan data langsung ke browser sessionStorage
        save_to_session_storage("profil_usaha", data)

        st.success("✅ Data tersimpan di sessionStorage browser!")

        # Simpan juga nama page untuk pindah halaman
        st.session_state.page = "Buat Strategi Branding"
        st.rerun()

    # --- OPSIONAL: Auto-load dari sessionStorage (restore data form) ---
    components.html("""
        <script>
        const saved = sessionStorage.getItem("profil_usaha");
        if (saved) {
            const data = JSON.parse(saved);
            // Isi kembali form input di Streamlit
            for (const key in data) {
                const val = data[key];
                if (!val) continue;
                const input = window.parent.document.querySelector(`input[aria-label='${key}']`);
                if (input) input.value = val;
            }
        }
        </script>
    """, height=0)
