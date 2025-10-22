import streamlit as st
from streamlit_option_menu import option_menu
import frey_home
import frey_profil_usaha
import frey_detail_produk
import frey_karakter_merk
import frey_hasil_strategi
import frey_memory

st.set_page_config(page_title="SiBRAND - Strategi Branding untuk UMKM", layout="wide")

# --- 1️⃣ Inisialisasi halaman default ---
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

menu_items = ["Beranda", "Profil Usaha", "Buat Strategi Branding", "Memory", "Logout"]

# --- 2️⃣ Sidebar menu (sinkron dengan session_state) ---
with st.sidebar:
    selected = option_menu(
        "SiBRAND - Strategi Branding untuk UMKM",
        menu_items,
        icons=["house", "building", "lightbulb", "box-arrow-right"],
        menu_icon="app-indicator",
        default_index=menu_items.index(st.session_state.page),
        styles={
            "container": {"background-color": "#8fd1d1"},
            "nav-link": {"font-size": "16px", "color": "black"},
            "nav-link-selected": {"background-color": "#367d7a", "color": "white"},
        },
    )

# --- 3️⃣ Update session_state kalau user klik di sidebar ---
if selected != st.session_state.page:
    st.session_state.page = selected
    st.rerun()

# --- 4️⃣ Routing berdasarkan halaman aktif ---
if st.session_state.page == "Beranda":
    frey_home.run()
elif st.session_state.page == "Profil Usaha":
    frey_profil_usaha.run()
elif st.session_state.page == "Buat Strategi Branding":
    frey_detail_produk.run()
elif st.session_state.page == "Memory":
    frey_memory.run()
elif st.session_state.page == "Logout":
    st.warning("Anda telah keluar dari aplikasi.")
