import streamlit as st
from session_storage import save_form_data_to_session, collect_all_form_data
from ai_integration import generate_branding_strategy

def run():
    st.header("Karakter Merk dan Gaya Komunikasi")

    # Initialize session state for form data if not exists
    if 'karakter_merk' not in st.session_state:
        st.session_state.karakter_merk = {}

    # Load existing data if available
    existing_data = st.session_state.karakter_merk

    st.subheader("Jika merk Anda adalah seseorang, bagaimana karakternya?")
    karakter_options = ["Ceria dan humoris", "Sederhana dan lugu", "Elegan dan berkelas", "Hangat dan dapat dipercaya", "Inovatif dan enerjik"]
    karakter_orang = st.multiselect(
        "Pilih 2 karakter", 
        karakter_options,
        default=existing_data.get('karakter_orang', []),
        max_selections=2
    )

    st.subheader("Bagaimana merk Anda berkomunikasi di media sosial?")
    komunikasi_options = ["Lucu dan santai", "Trendi dan cepat tanggap", "Akrab dan ramah", "Profesional dan sopan", "Hangat dan penuh empati"]
    gaya_komunikasi = st.multiselect(
        "Pilih 2 gaya komunikasi", 
        komunikasi_options,
        default=existing_data.get('gaya_komunikasi', []),
        max_selections=2
    )

    visual_options = ["Ceria dan humoris", "Tradisional dan berwarna-warni", "Natural", "Gelap dan elegan", "Minimalis dan rapi"]
    current_visual = existing_data.get('gaya_visual', visual_options[0])
    gaya_visual = st.radio(
        "Gaya visual yang menggambarkan brand Anda",
        visual_options,
        index=visual_options.index(current_visual) if current_visual in visual_options else 0,
        key="gaya_visual"
    )

    maskot_options = ["Ya", "Belum, tapi tertarik membuat", "Tidak tertarik"]
    current_maskot = existing_data.get('maskot', maskot_options[1])
    maskot = st.radio(
        "Apakah merk Anda sudah memiliki maskot atau ikon?",
        maskot_options,
        index=maskot_options.index(current_maskot) if current_maskot in maskot_options else 1,
        key="maskot"
    )

    st.subheader("Hubungan dengan pelanggan")
    hubungan_options = [
        "Memberikan pelayanan ramah dan cepat",
        "Menceritakan kisah di balik menu",
        "Interaksi di media sosial seperti kuis/challenge", 
        "Memberi promo dan diskon",
        "Melibatkan pelanggan dalam inovasi produk"
    ]
    hubungan_pelanggan = st.multiselect(
        "Pilih maksimal 2", 
        hubungan_options,
        default=existing_data.get('hubungan_pelanggan', []),
        max_selections=2
    )

    st.subheader("Nilai yang ditonjolkan dari produk Anda")
    nilai_options = [
        "Cita rasa otentik",
        "Kebersamaan dan kehangatan", 
        "Kreativitas dan inovasi rasa",
        "Kesehatan dan kesegaran",
        "Kenyamanan tempat dan pelayanan"
    ]
    nilai_utama = st.multiselect(
        "Pilih maksimal 2", 
        nilai_options,
        default=existing_data.get('nilai_utama', []),
        max_selections=2
    )

    if st.button("Lihat Strategi"):
        # Validasi data
        if len(karakter_orang) != 2:
            st.error("Pilih tepat 2 karakter untuk brand Anda!")
            return
            
        if len(gaya_komunikasi) != 2:
            st.error("Pilih tepat 2 gaya komunikasi!")
            return
            
        if len(hubungan_pelanggan) == 0:
            st.error("Pilih minimal 1 hubungan dengan pelanggan!")
            return
            
        if len(nilai_utama) == 0:
            st.error("Pilih minimal 1 nilai utama produk!")
            return

        data = {
            "karakter_orang": karakter_orang,
            "gaya_komunikasi": gaya_komunikasi,
            "gaya_visual": gaya_visual,
            "maskot": maskot,
            "hubungan_pelanggan": hubungan_pelanggan,
            "nilai_utama": nilai_utama
        }

        # Simpan data ke session
        save_form_data_to_session("karakter_merk", data)

        # Kumpulkan semua data form
        all_form_data = collect_all_form_data()
        
        # Debug: Show collected data
        st.write("📊 Semua data yang terkumpul:", all_form_data)
        
        # Simpan semua data ke session state untuk digunakan di halaman hasil
        st.session_state.all_form_data = all_form_data
        
        # Generate strategi branding menggunakan AI
        with st.spinner("🤖 Membuat strategi branding khusus untuk Anda..."):
            try:
                ai_response = generate_branding_strategy(all_form_data)
                st.session_state.ai_response = ai_response
                st.success("✅ Strategi branding berhasil dibuat!")
                
                # Pindah ke halaman hasil
                st.session_state.page = "Hasil Strategi"
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Gagal membuat strategi: {str(e)}")
                st.info("💡 Pastikan Anda sudah menambahkan API key di file secrets.toml")

    # Debug section
    with st.expander("🔍 Debug - Session Data"):
        st.write("Current karakter_merk in session:", st.session_state.get('karakter_merk', {}))
        st.write("Current detail_produk in session:", st.session_state.get('detail_produk', {}))
        st.write("Current profil_usaha in session:", st.session_state.get('profil_usaha', {}))