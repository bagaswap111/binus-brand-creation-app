import streamlit as st

def run():
    st.header("Karakter Merk dan Gaya Komunikasi")

    st.subheader("Jika merk Anda adalah seseorang, bagaimana karakternya?")
    st.multiselect("Pilih 2 karakter", ["Ceria dan humoris", "Sederhana dan lugu", "Elegan dan berkelas", "Hangat dan dapat dipercaya", "Inovatif dan enerjik"])

    st.subheader("Bagaimana merk Anda berkomunikasi di media sosial?")
    st.multiselect("Pilih 2 gaya komunikasi", ["Lucu dan santai", "Trendi dan cepat tanggap", "Akrab dan ramah", "Profesional dan sopan", "Hangat dan penuh empati"])

    st.radio("Gaya visual yang menggambarkan brand Anda",
             ["Ceria dan humoris", "Tradisional dan berwarna-warni", "Natural", "Gelap dan elegan", "Minimalis dan rapi"])

    st.radio("Apakah merk Anda sudah memiliki maskot atau ikon?",
             ["Ya", "Belum, tapi tertarik membuat", "Tidak tertarik"])

    st.subheader("Hubungan dengan pelanggan")
    st.multiselect("Pilih maksimal 2", [
        "Memberikan pelayanan ramah dan cepat",
        "Menceritakan kisah di balik menu",
        "Interaksi di media sosial seperti kuis/challenge",
        "Memberi promo dan diskon",
        "Melibatkan pelanggan dalam inovasi produk"
    ])

    st.subheader("Nilai yang ditonjolkan dari produk Anda")
    st.multiselect("Pilih maksimal 2", [
        "Cita rasa otentik",
        "Kebersamaan dan kehangatan",
        "Kreativitas dan inovasi rasa",
        "Kesehatan dan kesegaran",
        "Kenyamanan tempat dan pelayanan"
    ])

    st.button("Lihat Strategi")
