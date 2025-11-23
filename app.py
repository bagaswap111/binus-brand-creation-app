import streamlit as st
from streamlit_option_menu import option_menu
import home
import profil_usaha
import detail_produk
import karakter_merk
import hasil_strategi
import memory

st.set_page_config(page_title="SiBRAND - Strategi Branding untuk UMKM", layout="wide")

# --- 1️⃣ Inisialisasi halaman default ---
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

menu_items = [
    "Beranda", 
    "Profil Usaha", 
    "Detail Produk",  # This should match st.session_state.page
    "Karakter Merk", 
    "Hasil Strategi", 
    "Logout"
]

# Safe default index handling
def get_default_index():
    page_mapping = {
        "Beranda": 0,
        "Profil Usaha": 1,
        "Detail Produk": 2, 
        "Karakter Merk": 3,
        "Hasil Strategi": 4,
        "Logout": 5
    }
    current_page = st.session_state.get('page', 'Beranda')
    return page_mapping.get(current_page, 0)

with st.sidebar:
    selected = option_menu(
        "SiBRAND - Strategi Branding untuk UMKM",
        menu_items,
        icons=["house", "building", "cart", "lightbulk", "file-text", "box-arrow-right"],
        menu_icon="app-indicator",
        default_index=get_default_index(),
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
    home.run()
elif st.session_state.page == "Profil Usaha":
    profil_usaha.run()
elif st.session_state.page == "Detail Produk":
    detail_produk.run()
elif st.session_state.page == "Memory":
    memory.run()
elif selected == "Karakter Merk":
    karakter_merk.run()
elif selected == "Hasil Strategi":
    hasil_strategi.run()
elif st.session_state.page == "Logout":
    st.warning("Anda telah keluar dari aplikasi.")

