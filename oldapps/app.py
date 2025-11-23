import streamlit as st
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="YouTube Video + DeepSeek AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .video-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .form-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .response-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'api_response' not in st.session_state:
    st.session_state.api_response = None

# Header
st.markdown('<div class="main-header">🎬 YouTube Video + AI Analysis</div>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # DeepSeek API configuration
    st.subheader("DeepSeek API Settings")
    api_key = st.text_input(
        "DeepSeek API Key",
        type="password",
        value=os.getenv('DEEPSEEK_API_KEY', ''),
        help="Get your API key from https://platform.deepseek.com"
    )
    
    api_url = st.selectbox(
        "API Endpoint",
        [
            "https://api.deepseek.com/v1/chat/completions",
            "https://api.deepseek.com/chat/completions"
        ],
        index=0
    )
    
    st.divider()
    st.subheader("📊 App Info")
    st.write("This app allows you to:")
    st.write("• 📺 Embed YouTube videos")
    st.write("• 📝 Fill out analysis forms")
    st.write("• 🤖 Get AI insights from DeepSeek")
    st.write("• 💾 Save and view responses")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # YouTube Video Embed Section
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    st.header("📺 YouTube Video")
    
    youtube_url = st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste the full YouTube video URL here"
    )
    
    if youtube_url:
        # Extract video ID from various YouTube URL formats
        video_id = None
        if "youtube.com/watch?v=" in youtube_url:
            video_id = youtube_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_url:
            video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
        
        if video_id:
            embed_url = f"https://www.youtube.com/embed/{video_id}"
            st.markdown(f"""
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 10px;">
                <iframe src="{embed_url}" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" 
                        allowfullscreen 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
                </iframe>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Please enter a valid YouTube URL")
    else:
        st.info("🔗 Paste a YouTube URL above to embed the video")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Quick Actions Sidebar
    st.header("🚀 Quick Actions")
    
    if st.button("🔄 Reset Form", use_container_width=True):
        st.session_state.form_submitted = False
        st.session_state.api_response = None
        st.rerun()
    
    if st.session_state.api_response:
        if st.button("💾 Save Response", use_container_width=True):
            # Save response to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"response_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(st.session_state.api_response, f, indent=2)
            st.success(f"✅ Response saved as {filename}")

# Form Section
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.header("📝 Analysis Form")

with st.form("analysis_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 Your Name", placeholder="Enter your full name")
        email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
        video_topic = st.text_input("🎯 Video Topic", placeholder="What is the video about?")
    
    with col2:
        analysis_type = st.selectbox(
            "🔍 Analysis Type",
            ["Summary", "Critical Analysis", "Educational Content", "Entertainment Review", "Technical Breakdown"]
        )
        rating = st.slider("⭐ Rating (1-5 stars)", 1, 5, 3)
        urgency = st.select_slider(
            "⏰ Urgency Level",
            options=["Low", "Medium", "High"]
        )
    
    # Detailed analysis questions
    st.subheader("📋 Detailed Analysis")
    key_points = st.text_area(
        "💡 Key Points",
        placeholder="What are the main points covered in the video?",
        height=100
    )
    
    questions = st.text_area(
        "❓ Questions",
        placeholder="What questions do you have after watching the video?",
        height=100
    )
    
    additional_notes = st.text_area(
        "📝 Additional Notes",
        placeholder="Any other observations or comments?",
        height=100
    )
    
    # Form submission
    submitted = st.form_submit_button("🚀 Submit for AI Analysis", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# API Call Function
def call_deepseek_api(api_key, api_url, form_data, youtube_url):
    """Call DeepSeek API with the form data"""
    
    # Prepare the prompt
    prompt = f"""
    Please analyze the following video and form submission:
    
    VIDEO URL: {youtube_url if youtube_url else 'Not provided'}
    
    FORM SUBMISSION DETAILS:
    - Name: {form_data['name']}
    - Video Topic: {form_data['video_topic']}
    - Analysis Type: {form_data['analysis_type']}
    - Rating: {form_data['rating']}/5 stars
    - Urgency: {form_data['urgency']}
    - Key Points: {form_data['key_points']}
    - Questions: {form_data['questions']}
    - Additional Notes: {form_data['additional_notes']}
    
    Please provide a comprehensive analysis based on the above information.
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Handle form submission
if submitted:
    if not api_key:
        st.error("🔑 Please enter your DeepSeek API key in the sidebar")
    elif not name or not video_topic:
        st.error("👤 Please fill in at least your name and video topic")
    else:
        with st.spinner("🤖 Analyzing with DeepSeek AI..."):
            # Prepare form data
            form_data = {
                "name": name,
                "email": email,
                "video_topic": video_topic,
                "analysis_type": analysis_type,
                "rating": rating,
                "urgency": urgency,
                "key_points": key_points,
                "questions": questions,
                "additional_notes": additional_notes,
                "submission_time": datetime.now().isoformat()
            }
            
            # Call API
            api_response = call_deepseek_api(api_key, api_url, form_data, youtube_url)
            
            if api_response:
                st.session_state.form_submitted = True
                st.session_state.api_response = {
                    "form_data": form_data,
                    "api_response": api_response,
                    "timestamp": datetime.now().isoformat()
                }
                st.success("✅ Analysis complete!")
                st.rerun()

# Display API Response
if st.session_state.api_response:
    st.markdown('<div class="response-container">', unsafe_allow_html=True)
    st.header("🤖 DeepSeek AI Analysis")
    
    # Display basic info
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Submission Details")
        st.write(f"**Name:** {st.session_state.api_response['form_data']['name']}")
        st.write(f"**Video Topic:** {st.session_state.api_response['form_data']['video_topic']}")
        st.write(f"**Analysis Type:** {st.session_state.api_response['form_data']['analysis_type']}")
        st.write(f"**Rating:** {st.session_state.api_response['form_data']['rating']} ⭐")
    
    with col2:
        st.subheader("⏰ Metadata")
        submission_time = datetime.fromisoformat(st.session_state.api_response['form_data']['submission_time'])
        st.write(f"**Submitted:** {submission_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Urgency:** {st.session_state.api_response['form_data']['urgency']}")
        if st.session_state.api_response['form_data']['email']:
            st.write(f"**Email:** {st.session_state.api_response['form_data']['email']}")
    
    st.divider()
    
    # Display AI response
    st.subheader("🧠 AI Analysis Result")
    
    try:
        ai_content = st.session_state.api_response['api_response']['choices'][0]['message']['content']
        st.write(ai_content)
        
        # Token usage info
        if 'usage' in st.session_state.api_response['api_response']:
            st.divider()
            st.subheader("📈 Usage Information")
            usage = st.session_state.api_response['api_response']['usage']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Prompt Tokens", usage.get('prompt_tokens', 'N/A'))
            with col2:
                st.metric("Completion Tokens", usage.get('completion_tokens', 'N/A'))
            with col3:
                st.metric("Total Tokens", usage.get('total_tokens', 'N/A'))
                
    except (KeyError, IndexError) as e:
        st.error("❌ Error parsing API response")
        st.json(st.session_state.api_response['api_response'])
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with ❤️ using Streamlit and DeepSeek AI"
    "</div>", 
    unsafe_allow_html=True
)