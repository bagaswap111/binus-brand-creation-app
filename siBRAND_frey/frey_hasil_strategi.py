import streamlit as st

def run():
    st.header("Hasil Strategi Branding")

    st.markdown("""
    **Karakter Brand yang cocok untuk merk Anda adalah**
    **teman muda yang percaya diri dan stylish, tapi tetap ramah dan mudah didekati.**

    #### Elemen Visual: Maskot, Avatar dan Ikon
    Gunakan ilustrasi sederhana, gaya minimalis, dengan warna lembut dan hangat.

    #### Cara Interaksi dengan Pelanggan
    - **Ramah:** Bahasa kasual, seperti ngobrol dengan teman.  
    - **Percaya diri:** Pesan singkat, jelas, dan berwibawa.  
    - **Stylish:** Gunakan kata kekinian dan positif.

    #### Kepuasan
    Seberapa puas Anda dengan hasil rekomendasi di atas?
    """)
    st.radio("", ["Sangat tidak puas", "Tidak puas", "Cukup puas", "Puas", "Sangat puas"], horizontal=True)

    st.info("Untuk hasil yang lebih mendalam, Anda dapat bekerja sama dengan desainer atau agensi kreatif untuk pengembangan strategi lebih lanjut.")

    st.download_button("Download Strategi", data="Rekomendasi strategi branding Anda.", file_name="strategi_branding.txt")
