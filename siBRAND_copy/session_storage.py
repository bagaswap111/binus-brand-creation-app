import streamlit as st
import streamlit.components.v1 as components
import json

def save_to_session_storage(key: str, value: dict):
    """
    Simpan dictionary ke sessionStorage browser.
    """
    js = f"""
    <script>
    const data = {json.dumps(value)};
    sessionStorage.setItem("{key}", JSON.stringify(data));
    console.log("✅ Data '{key}' disimpan ke sessionStorage:", data);
    </script>
    """
    components.html(js, height=0)

def save_form_data_to_session(key: str, data: dict):
    """
    Simpan data form ke session state dan session storage
    """
    # Simpan ke Streamlit session state
    st.session_state[key] = data
    
    # Simpan ke browser session storage
    save_to_session_storage(key, data)
    
    # Debug log
    print(f"✅ Data {key} saved:")
    print(f"  - Session state: {st.session_state[key]}")
    print(f"  - Type: {type(st.session_state[key])}")

def load_form_data_from_session(key: str):
    """
    Load data from session state
    """
    return st.session_state.get(key, {})

def collect_all_form_data():
    """
    Kumpulkan semua data form dari session state
    """
    all_data = {}
    
    form_keys = ["profil_usaha", "detail_produk", "karakter_merk"]
    
    for key in form_keys:
        if key in st.session_state:
            all_data[key] = st.session_state[key]
            print(f"📦 Collected {key}: {st.session_state[key]}")
        else:
            print(f"⚠️  {key} not found in session state")
    
    print(f"🎯 All collected data: {all_data}")
    return all_data