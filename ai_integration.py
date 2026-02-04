import os
import json
import requests
import streamlit as st
from huggingface_hub import InferenceClient, InferenceTimeoutError
import time

def generate_branding_strategy(form_data, api_priority="Groq → HuggingFace → DeepSeek"):
    """
    Generate branding strategy menggunakan API AI dengan prioritas yang bisa dipilih
    """
    # Debug: Show what data we're sending
    st.write("📤 Data yang dikirim ke AI:", form_data)
    
    # Buat prompt dari data form
    prompt = create_prompt_from_form_data(form_data)
    
    # Tentukan urutan API berdasarkan priority
    if "Groq → HuggingFace → DeepSeek" in api_priority:
        return try_apis_in_order(prompt, ["groq", "huggingface", "deepseek"], form_data)
    elif "HuggingFace (Free) → Groq → DeepSeek" in api_priority:
        return try_apis_in_order(prompt, ["huggingface", "groq", "deepseek"], form_data)
    elif "Hanya HuggingFace (100% Gratis)" in api_priority:
        return try_apis_in_order(prompt, ["huggingface"], form_data)
    else:
        return try_apis_in_order(prompt, ["groq", "huggingface", "deepseek"], form_data)

def try_apis_in_order(prompt, api_order, form_data):
    """
    Coba API sesuai urutan yang diberikan
    """
    for api_name in api_order:
        try:
            if api_name == "groq":
                st.info("🔄 Mencoba Groq API...")
                return call_groq_api(prompt)
            elif api_name == "huggingface":
                st.info("🤗 Mencoba Hugging Face API (gratis)...")
                return call_huggingface_api_simple(prompt)
            elif api_name == "deepseek":
                st.info("🧠 Mencoba DeepSeek API...")
                return call_deepseek_api(prompt)
        except Exception as e:
            st.warning(f"⚠️ {api_name.capitalize()} API gagal: {str(e)[:100]}...")
            if api_name != api_order[-1]:  # Bukan API terakhir
                st.info(f"🔄 Mencoba API berikutnya...")
                time.sleep(1)  # Tunggu sebentar
    
    # Semua API gagal
    st.error("❌ Semua API gagal, menggunakan fallback strategy...")
    return generate_fallback_strategy(form_data)

def call_huggingface_api_simple(prompt):
    """
    Versi SIMPLE Hugging Face API yang pasti bekerja
    """
    try:
        # PAKAI GPT-2 SAJA (paling reliable)
        model = "gpt2"
        
        # Buat prompt yang lebih singkat dan spesifik
        short_prompt = f"""Anda adalah ahli strategi branding untuk UMKM.

Berdasarkan data berikut:
{prompt[:800]}

Buat strategi branding dengan format:

## 🎯 **KARAKTER BRAND**
[Deskripsi persona brand]

## 🎨 **IDENTITAS VISUAL** 
[Warna, typography, logo]

## 💬 **GAYA KOMUNIKASI**
[Tone of voice, cara berinteraksi]

## 📱 **STRATEGI KONTEN**
[Ide konten media sosial]

## 🤝 **HUBUNGAN PELANGGAN**
[Cara bangun loyalitas]

Berikan rekomendasi praktis dan mudah diimplementasikan."""
        
        # Pakai InferenceClient basic
        client = InferenceClient()
        
        with st.spinner("🤗 Generating dengan Hugging Face API..."):
            response = client.text_generation(
                prompt=short_prompt,
                model=model,
                max_new_tokens=800,
                temperature=0.7,
                do_sample=True,
                wait_for_model=True,
                max_wait_time=60
            )
        
        # Validasi response
        if not response or len(response.strip()) < 100:
            raise Exception("Response terlalu pendek")
        
        # Format response
        formatted_response = format_huggingface_response(response, short_prompt)
        
        return formatted_response
        
    except Exception as e:
        # Coba fallback ke model yang lebih kecil
        try:
            return call_huggingface_fallback_simple(prompt)
        except Exception as e2:
            raise Exception(f"Hugging Face API gagal: {str(e)[:150]}")

def call_huggingface_fallback_simple(prompt):
    """
    Fallback untuk Hugging Face dengan model alternatif
    """
    models = [
        "distilgpt2",  # Lebih ringan dari GPT-2
        "microsoft/DialoGPT-small",
        "EleutherAI/gpt-neo-125M"
    ]
    
    short_prompt = f"Buat strategi branding singkat untuk UMKM: {prompt[:500]}"
    
    for model in models:
        try:
            client = InferenceClient()
            response = client.text_generation(
                prompt=short_prompt,
                model=model,
                max_new_tokens=500,
                temperature=0.8,
                wait_for_model=True,
                max_wait_time=30
            )
            
            if response and len(response) > 50:
                return f"## Strategi Branding (via {model})\n\n{response}"
                
        except Exception:
            continue
    
    raise Exception("Semua model Hugging Face gagal")

def format_huggingface_response(response, original_prompt):
    """
    Format response dari Hugging Face agar lebih rapi
    """
    # Hapus prompt dari response jika ada
    if response.startswith(original_prompt[:100]):
        response = response[len(original_prompt):].strip()
    
    # Pastikan ada formatting yang cukup
    if response.count('#') < 2:
        # Tambahkan section headers
        sections = [
            "## 🎯 **KARAKTER BRAND**",
            "## 🎨 **IDENTITAS VISUAL**",
            "## 💬 **GAYA KOMUNIKASI**",
            "## 📱 **STRATEGI KONTEN**",
            "## 🤝 **HUBUNGAN PELANGGAN**"
        ]
        
        lines = response.split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            if i < len(sections):
                formatted_lines.append(sections[i])
            formatted_lines.append(line)
        
        response = '\n'.join(formatted_lines)
    
    return response

def create_prompt_from_form_data(form_data):
    """
    Buat prompt yang terstruktur dari semua data form
    """
    profil = form_data.get('profil_usaha', {})
    produk = form_data.get('detail_produk', {})
    karakter = form_data.get('karakter_merk', {})
    
    prompt = f"""
**PROFIL USAHA:**
- Nama Usaha: {profil.get('nama', 'Tidak diisi')}
- Bidang: {profil.get('bidang', 'Tidak diisi')}
- Lokasi: {profil.get('kota', 'Tidak diisi')} - {', '.join(profil.get('lokasi', []))}

**DETAIL PRODUK:**
- Jenis Produk: {', '.join(produk.get('jenis_produk', []))}
- Target Pembeli: {json.dumps(produk.get('target_pembeli', {}), ensure_ascii=False)}

**KARAKTER BRAND:**
- Karakter: {', '.join(karakter.get('karakter_orang', []))}
- Gaya Komunikasi: {', '.join(karakter.get('gaya_komunikasi', []))}
- Nilai Utama: {', '.join(karakter.get('nilai_utama', []))}

Buat strategi branding komprehensif yang mencakup:
1. Karakter Brand
2. Elemen Visual  
3. Gaya Komunikasi
4. Strategi Konten
5. Hubungan dengan Pelanggan
"""
    return prompt

def call_groq_api(prompt):
    """
    Panggil Groq API
    """
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    
    if not api_key:
        raise Exception("Groq API key tidak ditemukan")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {
                "role": "system", 
                "content": "Anda adalah ahli strategi branding dan marketing yang berpengalaman. Berikan rekomendasi yang praktis dan mudah diimplementasikan untuk UMKM."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "llama-3.1-8b-instant",
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    with st.spinner("🔄 Mengirim request ke Groq API..."):
        response = requests.post(url, headers=headers, json=data, timeout=60)
    
    if response.status_code == 200:
        result = response.json()["choices"][0]["message"]["content"]
        return result
    else:
        raise Exception(f"Groq API Error {response.status_code}: {response.text[:200]}")

def call_deepseek_api(prompt):
    """
    Panggil DeepSeek API
    """
    api_key = st.secrets.get("DEEPSEEK_API_KEY", os.getenv("DEEPSEEK_API_KEY"))
    
    if not api_key:
        raise Exception("DeepSeek API key tidak ditemukan")
    
    url = "https://api.deepseek.com/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah ahli strategi branding dan marketing yang berpengalaman. Berikan rekomendasi yang praktis dan mudah diimplementasikan untuk UMKM."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "model": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    with st.spinner("🔄 Mengirim request ke DeepSeek API..."):
        response = requests.post(url, headers=headers, json=data, timeout=60)
    
    if response.status_code == 200:
        result = response.json()["choices"][0]["message"]["content"]
        return result
    else:
        raise Exception(f"DeepSeek API Error {response.status_code}: {response.text[:200]}")

def generate_fallback_strategy(form_data):
    """
    Generate fallback strategy jika semua API gagal
    """
    profil = form_data.get('profil_usaha', {})
    produk = form_data.get('detail_produk', {})
    karakter = form_data.get('karakter_merk', {})
    
    fallback_strategy = f"""
# 🎯 Strategi Branding untuk {profil.get('nama', 'Usaha Anda')}

## 📊 Analisis Data Usaha
- **Bidang:** {profil.get('bidang', 'Tidak diisi')}
- **Lokasi:** {profil.get('kota', 'Tidak diisi')}
- **Target:** {json.dumps(produk.get('target_pembeli', {}), ensure_ascii=False)}

## 🎨 Rekomendasi Branding Dasar

### 1. Karakter Brand
- Persona: {', '.join(karakter.get('karakter_orang', ['Ramah', 'Profesional']))}
- Tone of Voice: {', '.join(karakter.get('gaya_komunikasi', ['Santai', 'Informal']))}

### 2. Elemen Visual
- **Warna:** Pilih 2-3 warna utama yang sesuai dengan karakter {', '.join(karakter.get('karakter_orang', []))}
- **Typography:** Gunakan font yang mudah dibaca dan konsisten
- **Logo:** Sederhana namun memorable

### 3. Strategi Media Sosial
- **Instagram:** Posting visual menarik 3-4x seminggu
- **TikTok:** Buat konten edukasi atau behind-the-scenes
- **Facebook:** Fokus pada komunitas dan testimonial

### 4. Tips Praktis untuk UMKM
1. Konsisten dalam visual dan komunikasi
2. Responsif terhadap pelanggan
3. Gunakan cerita (storytelling) dalam konten
4. Minta feedback dan testimonial

## 📈 Action Plan Minggu Pertama
1. Buat schedule posting media sosial
2. Desain template konten sederhana
3. Siapkan respons standar untuk customer service
4. Kumpulkan testimonial pertama

*Catatan: Ini adalah strategi dasar. Untuk analisis lebih detail, coba lagi API nanti.*
"""
    
    return fallback_strategy

# Fungsi untuk UI Streamlit
def show_api_selection():
    """
    Tampilkan pilihan API di sidebar
    """
    st.sidebar.markdown("### 🔧 Konfigurasi API")
    
    # API Keys input
    with st.sidebar.expander("🔑 API Keys (opsional)"):
        groq_key = st.text_input("Groq API Key", type="password", 
                                help="Dapatkan di console.groq.com")
        hf_key = st.text_input("Hugging Face Token", type="password",
                             help="Dapatkan di huggingface.co/settings/tokens (opsional)")
        deepseek_key = st.text_input("DeepSeek API Key", type="password",
                                   help="Dapatkan di platform.deepseek.com")
        
        if st.button("Simpan ke Session"):
            if groq_key:
                st.session_state['GROQ_API_KEY'] = groq_key
            if hf_key:
                st.session_state['HF_API_KEY'] = hf_key
            if deepseek_key:
                st.session_state['DEEPSEEK_API_KEY'] = deepseek_key
            st.success("API keys disimpan di session!")
    
    # API Priority selection
    st.sidebar.markdown("### 🎯 Prioritas API")
    api_priority = st.sidebar.radio(
        "Pilih urutan API:",
        [
            "Groq → HuggingFace → DeepSeek (Recommended)",
            "HuggingFace (Free) → Groq → DeepSeek",
            "Hanya HuggingFace (100% Gratis)"
        ],
        index=0
    )
    
    # Tampilkan status API keys
    with st.sidebar.expander("🔍 Status API Keys"):
        keys_status = {
            "Groq": "✅ Tersedia" if st.secrets.get("GROQ_API_KEY") or st.session_state.get('GROQ_API_KEY') else "❌ Tidak ada",
            "Hugging Face": "✅ Tersedia" if st.secrets.get("HF_API_KEY") or st.session_state.get('HF_API_KEY') else "ℹ️ Akan gunakan public access",
            "DeepSeek": "✅ Tersedia" if st.secrets.get("DEEPSEEK_API_KEY") or st.session_state.get('DEEPSEEK_API_KEY') else "❌ Tidak ada"
        }
        for api, status in keys_status.items():
            st.write(f"{api}: {status}")
    
    return api_priority

# Fungsi debug untuk testing
def show_debug_info():
    """
    Tampilkan info debug
    """
    with st.sidebar.expander("🐛 Debug Info"):
        st.write("Session keys:", list(st.session_state.keys()))
        
        if st.button("Test Hugging Face Connection"):
            try:
                client = InferenceClient()
                test = client.text_generation(
                    prompt="Test",
                    model="gpt2",
                    max_new_tokens=10
                )
                st.success(f"✅ Hugging Face OK: {test}")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Contoh penggunaan dalam app Streamlit
def main():
    st.title("🤖 Branding Strategy Generator")
    
    # Tampilkan API selection
    api_priority = show_api_selection()
    
    # Tampilkan debug info (opsional)
    show_debug_info()
    
    # Form input
    with st.form("branding_form"):
        st.subheader("📋 Data Usaha")
        
        col1, col2 = st.columns(2)
        with col1:
            nama_usaha = st.text_input("Nama Usaha*", placeholder="Contoh: Toko ABC")
            bidang = st.selectbox("Bidang Usaha*", 
                                ["Makanan & Minuman", "Fashion", "Jasa", "Retail", 
                                 "Teknologi", "Kesehatan", "Pendidikan", "Lainnya"])
        
        with col2:
            kota = st.text_input("Kota*", placeholder="Jakarta")
            lokasi = st.multiselect("Lokasi Operasi*",
                                  ["Online", "Offline", "Kedua-duanya"],
                                  default=["Online"])
        
        st.subheader("🎯 Target Pasar")
        target_umur = st.selectbox("Usia Target", 
                                 ["18-25", "25-35", "35-45", "45-55", "Semua usia"])
        target_gender = st.selectbox("Gender Target",
                                   ["Pria", "Wanita", "Semua gender"])
        
        st.subheader("🎨 Karakter Brand")
        karakter_brand = st.multiselect("Karakter Brand",
                                      ["Ramah", "Profesional", "Modern", "Tradisional",
                                       "Lucu", "Serius", "Eksklusif", "Terjangkau"],
                                      default=["Ramah", "Profesional"])
        
        submitted = st.form_submit_button("🚀 Generate Strategy")
        
        if submitted and nama_usaha:
            # Validasi input
            if not all([nama_usaha, bidang, kota]):
                st.error("❌ Harap isi semua field yang wajib (*)")
                return
            
            # Siapkan form data
            form_data = {
                'profil_usaha': {
                    'nama': nama_usaha,
                    'bidang': bidang,
                    'kota': kota,
                    'lokasi': lokasi,
                    'karyawan': '1-5',
                    'ig': '@' + nama_usaha.lower().replace(' ', ''),
                    'tiktok': '@' + nama_usaha.lower().replace(' ', ''),
                    'fb': nama_usaha.replace(' ', '')
                },
                'detail_produk': {
                    'jenis_produk': ['Produk Fisik' if 'Offline' in lokasi else 'Digital'],
                    'kategori_karakter': karakter_brand,
                    'target_pembeli': {'umur': target_umur, 'gender': target_gender},
                    'pantangan_khusus': 'Tidak ada'
                },
                'karakter_merk': {
                    'karakter_orang': karakter_brand,
                    'gaya_komunikasi': ['Santai', 'Edukatif'],
                    'gaya_visual': 'Minimalis',
                    'maskot': 'Tidak ada',
                    'nilai_utama': ['Kualitas', 'Kecepatan'],
                    'hubungan_pelanggan': ['Teman', 'Konsultan']
                }
            }
            
            # Generate strategy
            with st.spinner("🤖 Membuat strategi branding..."):
                try:
                    strategy = generate_branding_strategy(form_data, api_priority)
                    
                    # Tampilkan hasil
                    st.markdown("## 📋 Hasil Strategi Branding")
                    st.markdown(strategy)
                    
                    # Info API yang digunakan
                    st.info(f"✅ Strategi berhasil dibuat menggunakan {api_priority.split(' ')[0]} API")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Strategi (MD)",
                        data=strategy,
                        file_name=f"strategi_{nama_usaha.lower().replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                    
                    # Export as text juga
                    st.download_button(
                        label="📥 Download Strategi (TXT)",
                        data=strategy,
                        file_name=f"strategi_{nama_usaha.lower().replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Tips: Coba pilih API priority lain di sidebar")

if __name__ == "__main__":
    main()