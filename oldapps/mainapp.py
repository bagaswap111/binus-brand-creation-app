# app.py
import streamlit as st
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Page configuration
st.set_page_config(
    page_title="YouTube AI Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🎬 YouTube Video AI Analysis</div>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_provider = st.selectbox(
        "Choose AI Provider",
        ["Groq (Recommended)", "OpenRouter", "Hugging Face"]
    )
    
    # Set default values based on environment variables or placeholders
    default_api_key = os.getenv('DEFAULT_API_KEY', '')
    
    if api_provider == "Groq (Recommended)":
        print("Loaded API Key:", os.getenv('DEFAULT_API_KEY'))

        api_key = st.text_input(
            "Groq API Key",
            value=default_api_key,
            type="password",
            placeholder="gsk-...",
            help="Get free key from https://console.groq.com"
        )
        model_name = "llama-3.1-8b-instant"
        
    elif api_provider == "OpenRouter":
        api_key = st.text_input(
            "OpenRouter API Key", 
            value=default_api_key,
            type="password",
            placeholder="sk-or-...",
            help="Get free credits from https://openrouter.ai"
        )
        model_name = "google/gemma-2-2b-it"
        
    else:  # Hugging Face
        api_key = st.text_input(
            "Hugging Face Token",
            value=default_api_key, 
            type="password",
            placeholder="hf_...",
            help="Get token from https://huggingface.co"
        )
        model_name = "mistralai/Mistral-7B-Instruct-v0.1"
    
    st.markdown("---")
    st.header("📖 Instructions")
    st.markdown("""
    1. Paste YouTube URL
    2. Fill out the form
    3. Enter API key
    4. Get AI analysis!
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # YouTube section
    st.header("📺 YouTube Video")
    default_youtube_key = os.getenv('DEFAULT_YOUTUBE_KEY', '')
    youtube_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        key="youtube_url",
        value=default_youtube_key
    )
    
    if youtube_url:
        try:
            if "youtube.com/watch?v=" in youtube_url:
                video_id = youtube_url.split("v=")[1].split("&")[0]
            elif "youtu.be/" in youtube_url:
                video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
            else:
                video_id = None
                
            if video_id:
                st.video(f"https://www.youtube.com/watch?v={video_id}")
        except:
            st.error("Please enter a valid YouTube URL")

with col2:
    # Quick info
    st.header("ℹ️ App Info")
    st.markdown("""
    **Features:**
    - 📹 Embed YouTube videos
    - 📝 Analysis forms
    - 🤖 AI-powered insights
    - ☁️ Free API options
    
    **Free APIs Available:**
    - Groq: 5,000+ requests/day
    - OpenRouter: 10,000 free tokens
    - Hugging Face: Free access
    """)

# Analysis form
st.header("📝 Analysis Form")

with st.form("analysis_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name", placeholder="Optional")
        video_topic = st.text_input("Video Topic", placeholder="What is the video about?")
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Summary", "Critical Review", "Educational Content", "Technical Analysis"]
        )
    
    with col2:
        rating = st.slider("Rating (1-5 stars)", 1, 5, 3)
        urgency = st.select_slider("Urgency Level", options=["Low", "Medium", "High"])
        focus_area = st.selectbox(
            "Focus Area", 
            ["Content", "Presentation", "Technical", "Entertainment", "Educational"]
        )
    
    questions = st.text_area(
        "Your Questions",
        placeholder="What would you like to know about this video?",
        height=100
    )
    
    submitted = st.form_submit_button("🚀 Get AI Analysis")

# API functions
def call_groq_api(api_key, prompt):
    """Call Groq API"""
    if not api_key.startswith('gsk-'):
        return {"error": "Invalid Groq API key format"}
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-8b-instant",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

# Handle form submission
if submitted:
    if not api_key:
        st.error("❌ Please enter your API key")
    elif not questions:
        st.error("❌ Please enter your analysis questions")
    else:
        with st.spinner("🤖 Analyzing with AI... This may take a few seconds"):
            # Prepare prompt
            prompt = f"""
            Analyze the YouTube video based on this request:
            
            Video: {youtube_url or 'Not specified'}
            Topic: {video_topic or 'Not specified'}
            Analysis Type: {analysis_type}
            Focus Area: {focus_area}
            Rating: {rating}/5 stars
            Urgency: {urgency}
            
            User Questions: {questions}
            
            Please provide a comprehensive analysis.
            """
            
            # Call API based on provider
            if api_provider == "Groq (Recommended)":
                response = call_groq_api(api_key, prompt)
            else:
                response = {"error": "Only Groq API implemented for demo. Check code for other providers."}
            
            # Display results
            if response and "error" in response:
                st.error(f"❌ {response['error']}")
            elif response:
                st.success("✅ Analysis Complete!")
                
                try:
                    if api_provider == "Groq (Recommended)":
                        content = response['choices'][0]['message']['content']
                        st.markdown("### 🤖 AI Analysis Result")
                        st.write(content)
                        
                        # Show usage info
                        if 'usage' in response:
                            st.info(f"Tokens used: {response['usage']['total_tokens']}")
                except Exception as e:
                    st.error(f"Error parsing response: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with ❤️ using Streamlit | Deployed on Streamlit Community Cloud"
    "</div>", 
    unsafe_allow_html=True
)