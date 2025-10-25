import os
import json
import requests
import streamlit as st

def generate_branding_strategy(form_data):
    """
    Generate branding strategy menggunakan API AI
    """
    # Debug: Show what data we're sending
    st.write("📤 Data yang dikirim ke AI:", form_data)
    
    # Buat prompt dari data form
    prompt = create_prompt_from_form_data(form_data)
    
    # Coba Groq dulu, jika tidak ada coba DeepSeek
    try:
        return call_groq_api(prompt)
    except Exception as e:
        st.error(f"❌ Groq API gagal: {str(e)}")
        try:
            return call_deepseek_api(prompt)
        except Exception as e2:
            raise Exception(f"Semua API gagal:\n- Groq: {str(e)}\n- DeepSeek: {str(e2)}")

def create_prompt_from_form_data(form_data):
    """
    Buat prompt yang terstruktur dari semua data form
    """
    profil = form_data.get('profil_usaha', {})
    produk = form_data.get('detail_produk', {})
    karakter = form_data.get('karakter_merk', {})
    
    # Debug: Check if all data exists
    if not profil:
        st.warning("⚠️ Data profil usaha kosong")
    if not produk:
        st.warning("⚠️ Data detail produk kosong") 
    if not karakter:
        st.warning("⚠️ Data karakter merk kosong")
    
    prompt = f"""
Buatkan strategi branding yang komprehensif untuk usaha berikut:

**PROFIL USAHA:**
- Nama Usaha: {profil.get('nama', 'Tidak diisi')}
- Bidang: {profil.get('bidang', 'Tidak diisi')}
- Lokasi: {profil.get('kota', 'Tidak diisi')} - {', '.join(profil.get('lokasi', []))}
- Jumlah Karyawan: {profil.get('karyawan', 'Tidak diisi')}
- Media Sosial: IG: {profil.get('ig', 'Tidak ada')}, TikTok: {profil.get('tiktok', 'Tidak ada')}, FB: {profil.get('fb', 'Tidak ada')}

**DETAIL PRODUK:**
- Jenis Produk: {', '.join(produk.get('jenis_produk', []))}
- Kategori Karakter: {', '.join(produk.get('kategori_karakter', []))}
- Target Pembeli: {json.dumps(produk.get('target_pembeli', {}), ensure_ascii=False)}
- Khusus Pantangan: {produk.get('pantangan_khusus', 'Tidak diisi')}

**KARAKTER BRAND:**
- Karakter: {', '.join(karakter.get('karakter_orang', []))}
- Gaya Komunikasi: {', '.join(karakter.get('gaya_komunikasi', []))}
- Gaya Visual: {karakter.get('gaya_visual', 'Tidak diisi')}
- Status Maskot: {karakter.get('maskot', 'Tidak diisi')}
- Nilai Utama: {', '.join(karakter.get('nilai_utama', []))}
- Hubungan Pelanggan: {', '.join(karakter.get('hubungan_pelanggan', []))}

Buat strategi branding yang mencakup:
1. **Karakter Brand** - deskripsikan persona brand
2. **Elemen Visual** - rekomendasi warna, typography, style  
3. **Gaya Komunikasi** - tone of voice, cara berinteraksi
4. **Strategi Konten** - ide konten untuk media sosial
5. **Hubungan dengan Pelanggan** - cara membangun loyalitas

Berikan dalam format yang mudah dipahami dan actionable untuk UMKM.
"""
    return prompt

def call_groq_api(prompt):
    """
    Panggil Groq API
    """
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    
    if not api_key:
        raise Exception("Groq API key tidak ditemukan. Silakan tambahkan GROQ_API_KEY di secrets.toml")
    
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
        st.success("✅ Response dari AI berhasil diterima!")
        return result
    else:
        raise Exception(f"Groq API Error {response.status_code}: {response.text}")

def call_deepseek_api(prompt):
    """
    Panggil DeepSeek API
    """
    api_key = st.secrets.get("DEEPSEEK_API_KEY", os.getenv("DEEPSEEK_API_KEY"))
    
    if not api_key:
        raise Exception("DeepSeek API key tidak ditemukan. Silakan tambahkan DEEPSEEK_API_KEY di secrets.toml")
    
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
        st.success("✅ Response dari AI berhasil diterima!")
        return result
    else:
        raise Exception(f"DeepSeek API Error {response.status_code}: {response.text}")