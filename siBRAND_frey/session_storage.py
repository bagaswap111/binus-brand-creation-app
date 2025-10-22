import streamlit as st
import streamlit.components.v1 as components
import json

def save_to_session_storage(key: str, value: dict):
    """
    Simpan dictionary ke sessionStorage browser.
    """
    js = f"""
    <script>
    sessionStorage.setItem("{key}", JSON.stringify({json.dumps(value)}));
    console.log("✅ Data '{key}' disimpan ke sessionStorage:", {json.dumps(value)});
    </script>
    """
    components.html(js, height=0)


def load_from_session_storage(key: str):
    """
    Ambil data dari sessionStorage browser (hanya untuk logging di console).
    Catatan: tidak bisa dikembalikan langsung ke Python.
    """
    js = f"""
    <script>
    const data = sessionStorage.getItem("{key}");
    if (data) {{
        console.log("📦 Data '{key}' dari sessionStorage:", JSON.parse(data));
    }} else {{
        console.log("⚠️ Tidak ada data '{key}' di sessionStorage");
    }}
    </script>
    """
    components.html(js, height=0)
