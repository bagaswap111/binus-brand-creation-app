import streamlit as st
from streamlit_option_menu import option_menu
import frey_home
import frey_profil_usaha
import frey_detail_produk
import frey_karakter_merk
import frey_hasil_strategi

st.set_page_config(page_title="SiBRAND - Strategi Branding untuk UMKM", layout="wide")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "SiBRAND - Strategi Branding untuk UMKM",
        ["Beranda", "Profil Usaha", "Buat Strategi Branding", "Logout"],
        icons=["house", "building", "lightbulb", "box-arrow-right"],
        menu_icon="app-indicator",
        default_index=0,
        styles={
            "container": {"background-color": "#8fd1d1"},
            "nav-link": {"font-size": "16px", "color": "black"},
            "nav-link-selected": {"background-color": "#367d7a", "color": "white"},
        },
    )

# Routing ke halaman
if selected == "Beranda":
    frey_home.run()
elif selected == "Profil Usaha":
    frey_profil_usaha.run()
elif selected == "Buat Strategi Branding":
    frey_detail_produk.run()
elif selected == "Logout":
    st.write("Anda telah keluar dari aplikasi.")
