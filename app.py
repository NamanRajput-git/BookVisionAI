import streamlit as st
import requests
import base64
import os

# Backend URL - configure via environment variable for deployment
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
# Page configuration
st.set_page_config(
    page_title="BookVision AI",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look with background pattern
st.markdown("""
<style>
    /* Background pattern */
    .stApp {
        background: 
            linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(102, 126, 234, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(118, 75, 162, 0.05) 0%, transparent 50%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23667eea' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
    }
    
    /* Content wrapper */
    .main .block-container {
        position: relative;
        z-index: 1;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        padding: 2.5rem 3rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.85);
        font-size: 1.15rem;
        margin-top: 0.75rem;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        color: white;
        padding: 0.75rem 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Card styling */
    .section-card {
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(10px);
    }
    
    /* Section headers */
    .section-header {
        color: #a8b2d1;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.06);
    }
    
    div[data-testid="stMetric"] label {
        color: #8892b0;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: white;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    
    /* Image container */
    .stImage {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.06);
    }
    
    /* Text colors */
    .stMarkdown {
        color: #ccd6f6;
    }
    
    h1, h2, h3 {
        color: #e6f1ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>BookVision AI</h1>
    <p>Transform book pages into stunning illustrations using AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.markdown('<p class="section-header">Book Details</p>', unsafe_allow_html=True)
    book = st.text_input(
        "Book Name",
        placeholder="e.g., Anna Karenina",
        help="Enter the book title for context lookup"
    )
    
    author = st.text_input(
        "Author Name",
        placeholder="e.g., Leo Tolstoy",
        help="Enter the author name for better search accuracy"
    )
    
    st.markdown("---")
    
    st.markdown('<p class="section-header">Upload Page</p>', unsafe_allow_html=True)
    image = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a photo or scan of a book page"
    )
    
    st.markdown("---")
    
    generate_btn = st.button("Generate Illustration", use_container_width=True)

# Main content area
if image is not None:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### Uploaded Page")
        st.image(image, use_column_width=True)

if generate_btn and image is not None:
    with st.spinner("Creating your illustration..."):
        try:
            files = {"file": image}
            params = {"book_name": book, "author_name": author}
            
            r = requests.post(
                f"{BACKEND_URL}/process-page/",
                params=params,
                files=files,
                timeout=120
            )
            
            if r.status_code == 200:
                data = r.json()
                
                # Results in second column
                with col2:
                    st.markdown("### Generated Illustration")
                    if data.get("image"):
                        img_bytes = base64.b64decode(data["image"])
                        st.image(img_bytes, use_column_width=True)
                    else:
                        st.info("Image generation in progress...")
                
                # Metrics row
                st.markdown("---")
                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    confidence = data.get("ocr_confidence", 0)
                    st.metric(
                        "OCR Confidence",
                        f"{confidence:.1%}",
                        delta="Good" if confidence > 0.7 else "Low"
                    )
                
                with m2:
                    summary_len = len(data.get("summary", ""))
                    st.metric("Summary Length", f"{summary_len} chars")
                
                with m3:
                    prompt_len = len(data.get("image_prompt", ""))
                    st.metric("Prompt Length", f"{prompt_len} chars")
                
                with m4:
                    evaluation = data.get("evaluation", {})
                    faithfulness = evaluation.get("faithfulness_score", 0)
                    hallucination = evaluation.get("hallucination", False)
                    st.metric(
                        "Faithfulness",
                        f"{faithfulness}/5",
                        delta="No hallucination" if not hallucination else "Hallucination detected"
                    )
                
                # Summary section
                st.markdown("---")
                st.markdown("### Page Analysis")
                
                with st.expander("View Summary", expanded=True):
                    st.markdown(data.get("summary", "No summary available"))
                
                with st.expander("View Generated Prompt"):
                    st.code(data.get("image_prompt", ""), language=None)
            
            else:
                st.error(f"Error {r.status_code}: {r.text}")
                
        except requests.exceptions.Timeout:
            st.error("Request timed out. The image generation may take longer than expected.")
        except Exception as e:
            st.error(f"Connection Error: {e}")

elif generate_btn and image is None:
    st.warning("Please upload an image first.")
