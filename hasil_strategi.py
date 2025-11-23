import streamlit as st
from session_storage import collect_all_form_data

def run():
    st.header("Hasil Strategi Branding")

    # Cek apakah ada response AI di session state
    if "ai_response" not in st.session_state:
        st.warning("Silakan lengkapi semua form terlebih dahulu untuk mendapatkan strategi branding.")
        
        # Optional: Tampilkan data yang sudah terkumpul
        all_data = collect_all_form_data()
        if all_data:
            with st.expander("Data yang sudah terkumpul"):
                st.json(all_data)
        return

    # Tampilkan hasil dari AI
    st.markdown(st.session_state.ai_response)

    st.markdown("---")
    st.subheader("Kepuasan")
    st.radio(
        "Seberapa puas Anda dengan hasil rekomendasi di atas?",
        ["Sangat tidak puas", "Tidak puas", "Cukup puas", "Puas", "Sangat puas"], 
        horizontal=True
    )

    st.info("Untuk hasil yang lebih mendalam, Anda dapat bekerja sama dengan desainer atau agensi kreatif untuk pengembangan strategi lebih lanjut.")

    # Download button
    st.download_button(
        "📥 Download Strategi", 
        data=st.session_state.ai_response, 
        file_name="strategi_branding.txt",
        mime="text/plain"
    )

    # Tombol untuk mulai lagi
    if st.button("🔄 Isi Form Lagi"):
        # Clear session data
        keys_to_clear = ["profil_usaha", "detail_produk", "karakter_merk", "all_form_data", "ai_response"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.page = "Profil Usaha"
        st.rerun()