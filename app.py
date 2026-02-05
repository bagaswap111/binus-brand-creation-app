import streamlit as st
from streamlit_option_menu import option_menu
import time
import home
import profil_usaha
import detail_produk
import karakter_merk
import hasil_strategi
import memory

st.set_page_config(
    page_title="SiBRAND - Strategi Branding untuk UMKM", 
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1️⃣ Inisialisasi halaman default ---
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

if "last_page" not in st.session_state:
    st.session_state.last_page = "Beranda"


# --- 2️⃣ Sidebar Navigation ---
menu_items = [
    "Beranda", 
    "Profil Usaha", 
    "Detail Produk", 
    "Karakter Merk", 
    "Hasil Strategi",
    "Keluar"
]

# Mapping icons ke menu
menu_icons = {
    "Beranda": "house",
    "Profil Usaha": "building", 
    "Detail Produk": "cart",
    "Karakter Merk": "lightbulb",
    "Hasil Strategi": "file-text",
    "Keluar": "box-arrow-right"
}

# Default index handling
def get_default_index():
    page_mapping = {page: idx for idx, page in enumerate(menu_items)}
    current_page = st.session_state.get('page', 'Beranda')
    return page_mapping.get(current_page, 0)

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 5px; background: linear-gradient(135deg, #367d7a 0%, #8fd1d1 100%); border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">🎨 SiBRAND</h2>
        <p style="color: white; margin: 5px 0 0 0; font-size: 14px;">Strategi Branding untuk UMKM</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,  # No title, kita pakai image
        options=menu_items,
        icons=[menu_icons[item] for item in menu_items],
        menu_icon="app-indicator",
        default_index=get_default_index(),
        styles={
            "container": {
                "padding": "5px",
                "background-color": "#f0f2f6",
                "border-radius": "10px",
                "margin-bottom": "20px"
            },
            "icon": {"color": "#367d7a", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px 0",
                "border-radius": "5px",
                "color": "#2c3e50",
                "padding": "10px"
            },
            "nav-link-selected": {
                "background-color": "#367d7a",
                "color": "white",
                "font-weight": "bold",
            },
        },
    )

# --- 3️⃣ Update session_state jika halaman berubah ---
if selected != st.session_state.page:
    # Simpan halaman sebelumnya untuk tracking scroll
    st.session_state.last_page = st.session_state.page
    st.session_state.page = selected
    
    # Scroll to top JavaScript
    st.markdown("""
    <script>
        window.scrollTo({top: 0, behavior: 'instant'});
    </script>
    """, unsafe_allow_html=True)
    
    # Delay kecil lalu rerun
    time.sleep(0.05)
    st.rerun()

# --- 4️⃣ Routing yang KONSISTEN ---
current_page = st.session_state.page

if current_page == "Beranda":
    home.run()
elif current_page == "Profil Usaha":
    profil_usaha.run()
elif current_page == "Detail Produk":
    detail_produk.run()
elif current_page == "Karakter Merk":
    karakter_merk.run()
elif current_page == "Hasil Strategi":
    hasil_strategi.run()
# elif current_page == "Memory":
#     memory.run()
elif current_page == "Logout":
    # Clear session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.success("✅ Anda telah berhasil keluar!")
    st.info("Silakan refresh halaman untuk masuk kembali.")
    st.stop()


# Info current page di sidebar bawah
with st.sidebar:
    st.markdown("---")
    st.caption(f"📄 Halaman: **{current_page}**")
    st.caption("SiBRAND © 2025")

