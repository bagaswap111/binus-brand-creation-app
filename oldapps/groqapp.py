import streamlit as st
import requests
import json
import time

# Configure the page
st.set_page_config(
    page_title="BINUS AI BRANDING CREATION APP",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 BINUS AI BRANDING CREATION APP")

# API Selection
st.sidebar.header("🔧 API Configuration")
api_provider = st.sidebar.selectbox(
    "Choose FREE AI Provider",
    [
        "Groq (Recommended - Free)", 
        "OpenRouter (Free Credits)", 
        "Hugging Face (With Free Token)"
    ],
    index=0
)

# API Setup
if api_provider == "Groq (Recommended - Free)":
    st.sidebar.info("""
    **Groq Setup:**
    1. Go to https://console.groq.com
    2. Sign up → Get API key FREE
    3. Use model: llama-3.1-8b-instant
    """)
    
    api_key = st.sidebar.text_input("Groq API Key", type="password", help="Get free key from Groq console", value="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")
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    model_name = "llama-3.1-8b-instant"  # CURRENT working model
    
elif api_provider == "OpenRouter (Free Credits)":
    st.sidebar.info("""
    **OpenRouter:**
    1. Visit https://openrouter.ai
    2. Get 10,000 free tokens
    3. Multiple models available
    """)
    api_key = st.sidebar.text_input("OpenRouter API Key", type="password")
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    model_name = "google/gemma-2-2b-it"  # Free model
    
elif api_provider == "Hugging Face (With Free Token)":
    st.sidebar.info("""
    **Hugging Face:**
    1. Go to https://huggingface.co
    2. Sign up → Settings → Access Tokens
    3. Get free token
    """)
    api_key = st.sidebar.text_input("Hugging Face Token", type="password")
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"

# YouTube Section
st.header("📺 YouTube Video")
youtube_url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...", value="https://www.youtube.com/watch?v=B43D6ja2d-U")

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
        st.error("Invalid YouTube URL")

# Analysis Form
st.header("📝 Video Analysis Form")

with st.form("analysis_form"):
    name = st.text_input("Your Name", placeholder="Optional")
    analysis_type = st.selectbox("Analysis Type", [
        "Summary", "Critical Review", "Educational Content", 
        "Entertainment Value", "Technical Analysis"
    ])
    
    questions = st.text_area(
        "What would you like to know about this video?",
        placeholder="Example: Summarize the main points, analyze the presentation style, suggest improvements, etc.",
        height=120
    )
    
    submitted = st.form_submit_button("🚀 Get FREE AI Analysis")

# API Call Functions
def call_groq_api(api_key, prompt):
    """Call Groq API with CURRENT model"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-8b-instant",  # CURRENT working model
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

def call_openrouter_api(api_key, prompt):
    """Call OpenRouter API with free model"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",  # Required by OpenRouter
        "X-Title": "Video Analysis App"
    }
    
    payload = {
        "model": "google/gemma-2-2b-it",  # Free model
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"OpenRouter Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

def call_huggingface_api(api_key, prompt):
    """Call Hugging Face API with token"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            return {"error": "Model is loading. Wait 30 seconds and try again."}
        else:
            return {"error": f"Hugging Face Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

# Handle Form Submission
if submitted:
    if not questions:
        st.error("Please enter your analysis questions")
    else:
        # Prepare prompt
        prompt = f"""
        Analyze the YouTube video and provide insights:
        
        Video: {youtube_url if youtube_url else 'Not specified'}
        Requested by: {name if name else 'Anonymous'}
        Analysis Type: {analysis_type}
        
        User Questions: {questions}
        
        Please provide a comprehensive, well-structured analysis.
        """
        
        with st.spinner("🤖 Analyzing with FREE AI... This may take 10-30 seconds"):
            
            # Call appropriate API
            if api_provider == "Groq (Recommended - Free)":
                if api_key:
                    response = call_groq_api(api_key, prompt)
                else:
                    st.error("Please enter your Groq API key")
                    response = None
                    
            elif api_provider == "OpenRouter (Free Credits)":
                if api_key:
                    response = call_openrouter_api(api_key, prompt)
                else:
                    st.error("Please enter your OpenRouter API key")
                    response = None
                    
            elif api_provider == "Hugging Face (With Free Token)":
                if api_key:
                    response = call_huggingface_api(api_key, prompt)
                else:
                    st.error("Please enter your Hugging Face token")
                    response = None
            
            # Display results
            if response:
                if "error" in response:
                    st.error(f"❌ API Error: {response['error']}")
                else:
                    st.success("✅ Analysis Complete!")
                    st.subheader("🤖 AI Analysis Result")
                    
                    try:
                        if api_provider == "Groq (Recommended - Free)":
                            content = response['choices'][0]['message']['content']
                            st.write(content)
                            
                        elif api_provider == "OpenRouter (Free Credits)":
                            content = response['choices'][0]['message']['content']
                            st.write(content)
                            
                        elif api_provider == "Hugging Face (With Free Token)":
                            if isinstance(response, list):
                                content = response[0].get('generated_text', str(response))
                            else:
                                content = response.get('generated_text', str(response))
                            st.write(content)
                            
                    except Exception as e:
                        st.error(f"Error parsing response: {str(e)}")
                        st.json(response)

# FREE API KEY INSTRUCTIONS
st.sidebar.markdown("---")
st.sidebar.header("🎯 How to Get FREE API Keys")

with st.sidebar.expander("Groq (Instant Free Access)"):
    st.markdown("""
    1. **Visit** https://console.groq.com
    2. **Sign up** with Google/GitHub
    3. **Get API key** instantly from dashboard
    4. **Use model:** `llama-3.1-8b-instant`
    5. **5,000+ free requests/day**
    """)

with st.sidebar.expander("OpenRouter (10K Free Tokens)"):
    st.markdown("""
    1. **Visit** https://openrouter.ai
    2. **Sign up** for free account
    3. **Get 10,000 free tokens**
    4. **Use model:** `google/gemma-2-2b-it`
    5. **Multiple models available**
    """)

with st.sidebar.expander("Hugging Face (Free Token)"):
    st.markdown("""
    1. **Visit** https://huggingface.co
    2. **Sign up** for free account
    3. **Go to** Settings → Access Tokens
    4. **Create new token**
    5. **Use for API calls**
    """)

# Alternative: Local AI Option
with st.expander("💡 No API Key? Use Local AI (100% Free)"):
    st.markdown("""
    **Option 4: Use Ollama (Completely Free, Runs Locally)**
    
    ```bash
    # Install Ollama
    curl -fsSL https://ollama.ai/install.sh | sh
    
    # Pull a model
    ollama pull llama2
    
    # Run locally - no API keys needed!
    ```
    
    **Advantages:**
    - ✅ 100% free forever
    - ✅ No internet required after setup
    - ✅ No API limits
    - ✅ Complete privacy
    
    **Disadvantages:**
    - ❌ Requires good computer (8GB+ RAM)
    - ❌ Slower than cloud APIs
    """)

# Quick Test Section
st.markdown("---")
st.header("🧪 Quick Test")

if st.button("Test Groq API with Public Demo Key"):
    # This is a demo - users should get their own key
    st.info("Get your FREE key from https://console.groq.com")
    st.write("No demo key provided for security reasons.")

# Footer
st.markdown("---")
st.markdown("💡 **Pro Tip**: Use **Groq** with model `llama-3.1-8b-instant` for instant results!")