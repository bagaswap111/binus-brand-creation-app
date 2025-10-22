import streamlit as st
from session_storage import save_to_session_storage

def run():
    st.title("🧾 Profil Usaha Anda")

    # --- Input field ---
    nama = st.text_input("Nama Usaha")
    jenis = st.text_input("Jenis Usaha")
    deskripsi = st.text_area("Deskripsi Singkat")

    # --- Simpan ke sessionStorage ---
    if st.button("💾 Simpan ke Browser"):
        save_to_session_storage("profil_usaha", f"{nama}|{jenis}|{deskripsi}")
        st.success("✅ Profil usaha disimpan di sessionStorage browser!")

    # --- Ambil data dari sessionStorage (opsional) ---
    if st.button("📦 Ambil Data dari Browser"):
        save_to_session_storage("profil_usaha")
        st.info("Data diambil dari sessionStorage (lihat console browser).")

    st.markdown("Cek di browser console → Application → Session Storage → localhost")
