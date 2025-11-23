import streamlit as st
import pandas as pd
from PIL import Image
import io

# Konfigurasi halaman
st.set_page_config(
    page_title="SIBRAND - Strategi Branding untuk UMKM",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2E86AB;
        margin-bottom: 1rem;
    }
    .welcome-text {
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: justify;
        margin-bottom: 2rem;
    }
    .section-box {
        background-color: #f0f8ff;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin-bottom: 2rem;
    }
    .stButton button {
        background-color: #2E86AB;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #1a5d7a;
    }
</style>
""", unsafe_allow_html=True)

# Session state untuk menyimpan data
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'business_profile' not in st.session_state:
    st.session_state.business_profile = {}

def home_page():
    st.markdown('<div class="main-header">SIBRAND - Strategi Branding untuk UMKM</div>', unsafe_allow_html=True)
    
    # Sidebar untuk navigasi
    with st.sidebar:
        st.markdown("### Navigasi")
        if st.button("🏠 Profil Usaha", use_container_width=True):
            st.session_state.page = 'home'
        if st.button("📊 Buat Strategi Branding", use_container_width=True):
            st.session_state.page = 'branding_strategy'
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.page = 'logout'
    
    # Konten utama
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Selamat datang di SIBRAND!</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-text">', unsafe_allow_html=True)
        st.write("""
        Aplikasi ini dirancang khusus untuk membantu UMKM menyusun strategi promosi dan branding yang efektif.
        
        **Branding** adalah serangkaian kegiatan yang membuat konsumen dan masyarakat mempunyai persepsi yang baik terhadap produk dan usaha Anda.
        
        Melalui aplikasi ini, Anda akan dibimbing untuk membuat strategi branding yang berguna memperkuat kesan baik terhadap usaha Anda.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Lengkapi Profil Usaha untuk Memulai", use_container_width=True):
            st.session_state.page = 'business_profile'
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #e6f7ff; padding: 2rem; border-radius: 10px; text-align: center;'>
            <h3>💡 Tips Branding</h3>
            <p>Mulailah dengan memahami profil usaha Anda untuk membuat strategi branding yang tepat sasaran.</p>
        </div>
        """, unsafe_allow_html=True)

def business_profile_page():
    st.markdown('<div class="main-header">Profil Usaha Anda</div>', unsafe_allow_html=True)
    
    # Sidebar untuk navigasi
    with st.sidebar:
        st.markdown("### Navigasi")
        if st.button("🏠 Beranda", use_container_width=True):
            st.session_state.page = 'home'
        if st.button("📊 Buat Strategi Branding", use_container_width=True):
            st.session_state.page = 'branding_strategy'
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.page = 'logout'
    
    # Form profil usaha
    with st.form("business_profile_form"):
        st.markdown("### Informasi Dasar Usaha")
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input("Nama Usaha*", placeholder="Isikan nama merk Anda")
            business_address = st.text_area("Alamat Usaha*", placeholder="Isikan alamat usaha Anda")
            city = st.text_input("Kota*", placeholder="Isikan kota tempat usaha Anda")
            
            # Lokasi toko/platform penjualan
            st.markdown("**Lokasi Toko / Platform Penjualan***")
            location_options = ["Ruko", "Pasar", "Pinggir jalan raya", "Mall", "Online"]
            location_type = st.radio("Pilih jenis lokasi:", location_options, horizontal=True)
            
            employees = st.number_input("Jumlah Karyawan*", min_value=0, step=1, placeholder="Jumlah karyawan")
        
        with col2:
            # Media sosial
            st.markdown("### Media Sosial")
            instagram = st.text_input("Akun Media Sosial Instagram", placeholder="@username")
            tiktok = st.text_input("Akun Media Sosial Tiktok", placeholder="@username")
            facebook = st.text_input("Akun Media Sosial Facebook", placeholder="Nama halaman Facebook")
            
            # Logo
            st.markdown("### Logo Merk (jika ada)")
            logo_file = st.file_uploader("Unggah logo Anda", type=['png', 'jpg', 'jpeg'])
            
            if logo_file is not None:
                image = Image.open(logo_file)
                st.image(image, caption="Logo Preview", width=150)
        
        # Bidang usaha
        st.markdown("### Bidang Usaha*")
        business_field = st.radio(
            "Pilih bidang usaha utama:",
            ["Fesyen (Pakaian, Tas, Sepatu, Aksesoris)", "FnB (Makanan, Minuman, Camilan)", "Lainnya"],
            horizontal=True
        )
        
        # Jika memilih lainnya
        if business_field == "Lainnya":
            other_field = st.text_input("Sebutkan bidang usaha Anda")
        
        # Tombol submit
        submitted = st.form_submit_button("💾 Simpan dan Lanjut")
        
        if submitted:
            # Validasi field wajib
            if not business_name or not business_address or not city or not location_type or employees == 0:
                st.error("Harap lengkapi semua field yang wajib diisi (*)")
            else:
                # Simpan data ke session state
                st.session_state.business_profile = {
                    'business_name': business_name,
                    'business_address': business_address,
                    'city': city,
                    'location_type': location_type,
                    'employees': employees,
                    'instagram': instagram,
                    'tiktok': tiktok,
                    'facebook': facebook,
                    'logo_file': logo_file,
                    'business_field': business_field if business_field != "Lainnya" else other_field
                }
                
                st.success("✅ Profil usaha berhasil disimpan!")
                st.info("Silakan lanjutkan ke halaman Buat Strategi Branding")
                
                # Tampilkan preview data
                st.markdown("### Preview Profil Usaha")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Nama Usaha:** {business_name}")
                    st.write(f"**Alamat:** {business_address}")
                    st.write(f"**Kota:** {city}")
                    st.write(f"**Lokasi:** {location_type}")
                
                with col2:
                    st.write(f"**Jumlah Karyawan:** {employees}")
                    st.write(f"**Bidang Usaha:** {business_field if business_field != 'Lainnya' else other_field}")
                    if instagram:
                        st.write(f"**Instagram:** {instagram}")
                    if tiktok:
                        st.write(f"**TikTok:** {tiktok}")

def branding_strategy_page():
    st.markdown('<div class="main-header">Buat Strategi Branding</div>', unsafe_allow_html=True)
    
    # Sidebar untuk navigasi
    with st.sidebar:
        st.markdown("### Navigasi")
        if st.button("🏠 Beranda", use_container_width=True):
            st.session_state.page = 'home'
        if st.button("👤 Profil Usaha", use_container_width=True):
            st.session_state.page = 'business_profile'
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.page = 'logout'
    
    # Cek apakah profil usaha sudah diisi
    if not st.session_state.business_profile:
        st.warning("⚠️ Silakan lengkapi Profil Usaha terlebih dahulu sebelum membuat strategi branding.")
        if st.button("Lengkapi Profil Usaha"):
            st.session_state.page = 'business_profile'
            st.rerun()
        return
    
    business_profile = st.session_state.business_profile
    
    st.markdown(f"""
    <div class="section-box">
        <h3>Strategi Branding untuk {business_profile['business_name']}</h3>
        <p>Berdasarkan profil usaha Anda, berikut adalah rekomendasi strategi branding:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rekomendasi strategi berdasarkan bidang usaha
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #e6f7ff; padding: 1.5rem; border-radius: 10px; height: 300px;'>
            <h4>🎯 Target Audience</h4>
            <p>Tentukan target pasar yang spesifik berdasarkan:</p>
            <ul>
                <li>Usia</li>
                <li>Jenis kelamin</li>
                <li>Lokasi</li>
                <li>Minat dan gaya hidup</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #f0f8ff; padding: 1.5rem; border-radius: 10px; height: 300px;'>
            <h4>📱 Strategi Media Sosial</h4>
            <p>Optimalkan platform media sosial:</p>
            <ul>
                <li>Konten visual menarik</li>
                <li>Interaksi dengan followers</li>
                <li>Promosi terarah</li>
                <li>Storytelling brand</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #e6f7ff; padding: 1.5rem; border-radius: 10px; height: 300px;'>
            <h4>🎨 Identitas Visual</h4>
            <p>Kembangkan identitas brand yang konsisten:</p>
            <ul>
                <li>Logo dan warna brand</li>
                <li>Tipografi</li>
                <li>Gaya fotografi</li>
                <li>Packaging design</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Form untuk mengembangkan strategi lebih lanjut
    st.markdown("### Kembangkan Strategi Branding Anda")
    
    with st.form("branding_strategy_form"):
        st.markdown("#### Value Proposition")
        value_prop = st.text_area("Apa nilai unik yang ditawarkan brand Anda?", 
                                 placeholder="Contoh: Produk handmade berkualitas dengan harga terjangkau...")
        
        st.markdown("#### Target Pasar Spesifik")
        target_market = st.text_area("Jelaskan target pasar Anda secara detail",
                                   placeholder="Contoh: Wanita usia 20-35 tahun, tinggal di perkotaan, menyukai fashion sustainable...")
        
        st.markdown("#### Strategi Konten")
        content_strategy = st.text_area("Rencana konten untuk media sosial",
                                      placeholder="Jenis konten, frekuensi posting, tema konten...")
        
        submitted = st.form_submit_button("💾 Simpan Strategi Branding")
        
        if submitted:
            st.success("✅ Strategi branding berhasil disimpan!")
            st.balloons()

def logout_page():
    st.markdown('<div class="main-header">Logout</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background-color: #f0f8ff; border-radius: 10px;'>
            <h3>👋 Terima kasih telah menggunakan SIBRAND!</h3>
            <p>Anda telah berhasil logout dari aplikasi.</p>
            <p>Kami harap strategi branding yang telah Anda buat dapat membantu mengembangkan usaha Anda.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Masuk Kembali"):
            st.session_state.page = 'home'
            st.session_state.business_profile = {}
            st.rerun()

# Routing halaman berdasarkan session state
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'business_profile':
    business_profile_page()
elif st.session_state.page == 'branding_strategy':
    branding_strategy_page()
elif st.session_state.page == 'logout':
    logout_page()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>SIBRAND - Strategi Branding untuk UMKM © 2024</div>", 
    unsafe_allow_html=True
)