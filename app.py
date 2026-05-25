import streamlit as st
from google import genai
from PIL import Image
from pdf2image import convert_from_bytes
import io

# Safe, zero-dependency canvas compiler to prevent 'glyf' server crashes
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor

# Initialize Gemini Client
client = genai.Client()

# Core Page Layout Configuration
st.set_page_config(
    page_title="Healthcare Assistant — Smart Clinical Portal", 
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize single-page app router navigation state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"  # Changed from Workspace to Home

# --- DEPENDENCY-FREE PDF COMPILER ---
def safe_generate_pdf(markdown_text):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer, 
        pagesize=letter, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'MainHeader', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=HexColor('#0f172a'), spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'SubHeader', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=HexColor('#64748b'), spaceAfter=20
    )
    section_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=18, textColor=HexColor('#1e3a8a'), spaceBefore=16, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'ClinicalBody', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.5, leading=16, textColor=HexColor('#1e293b'), spaceAfter=6
    )
    
    story.append(Paragraph("Clinical Synthesis Report", title_style))
    story.append(Paragraph("Automated Healthcare Assistant Data Stream", subtitle_style))
    
    lines = markdown_text.split('\n')
    for line in lines:
        cleaned = line.strip().replace('**', '').replace('*', '')
        if not cleaned:
            continue
            
        if line.startswith('##'):
            cleaned_heading = cleaned.replace('##', '').strip()
            story.append(Paragraph(cleaned_heading, section_style))
        else:
            story.append(Paragraph(cleaned, body_style))
            
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

# --- REFINED LIQUID GLASS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: -apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif !important;
        background: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 70%, #020617 100%) !important;
    }
    
    header, [data-testid="stHeader"] { background: transparent !important; }
    
    .apple-disclaimer {
        background: rgba(255, 69, 58, 0.04) !important;
        backdrop-filter: blur(30px) saturate(200%) !important;
        border: 1px solid rgba(255, 69, 58, 0.12) !important;
        border-radius: 16px;
        padding: 14px 20px;
        margin-bottom: 25px;
    }
    
    .apple-title {
        font-size: clamp(2.0rem, 4.5vw, 3.0rem) !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px !important;
    }
    
    .apple-subtitle {
        font-size: clamp(0.95rem, 2vw, 1.15rem) !important;
        color: #94a3b8;
        margin-bottom: 35px !important;
    }
    
    .liquid-glass-card, .output-pane, .info-feature-card {
        background: rgba(255, 255, 255, 0.01) !important;
        backdrop-filter: blur(35px) saturate(210%) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 24px !important;
        padding: 24px;
        margin-bottom: 15px;
    }

    .output-pane h2 {
        font-size: 1.15rem !important;
        color: #38bdf8 !important;
        border-left: 3px solid #0ea5e9;
        padding-left: 8px;
        margin-top: 22px !important;
        margin-bottom: 10px !important;
    }
    
    div[data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(35px) saturate(210%) !important;
        border: 2px dashed rgba(255, 255, 255, 0.18) !important;
        border-radius: 24px !important;
        min-height: 180px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px !important;
    }
    
    div.stDownloadButton > button {
        background: linear-gradient(180deg, #007aff 0%, #0051ba 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3) !important;
        width: 100% !important;
        margin-top: 15px;
        transition: transform 0.2s ease;
    }
    div.stDownloadButton > button:hover {
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. NEW TOP NAVIGATION BAR (Home & About) ---
nav_col1, nav_col2 = st.columns([2, 1])
with nav_col1:
    st.markdown("<p style='font-weight:700; font-size:1.2rem; color:#fff; margin:0; padding-top:4px;'>🏥 Healthcare <span style='font-weight:300; color:#64748b;'>Assistant</span></p>", unsafe_allow_html=True)
with nav_col2:
    btn_space1, btn_space2 = st.columns(2)
    with btn_space1:
        if st.button("💻 Home", use_container_width=True, type="secondary" if st.session_state.current_page == "About" else "primary"):
            st.session_state.current_page = "Home"
            st.rerun()
    with btn_space2:
        if st.button("ℹ️ About", use_container_width=True, type="primary" if st.session_state.current_page == "About" else "secondary"):
            st.session_state.current_page = "About"
            st.rerun()

st.markdown("<hr style='margin-top:0; margin-bottom:25px; opacity:0.1;'>", unsafe_allow_html=True)

# --- 2. RENDER VIEWPORT: HOME PAGE ---
if st.session_state.current_page == "Home":
    st.markdown(
        """
        <div class="apple-disclaimer">
            <span style="color:#FF453A; font-weight:600;">⚠️ Regulatory Notice & Medical Reference Disclaimer</span>
            <p style="margin-top: 4px; font-size:0.85rem; color:#ff9f0a; margin-bottom:0;">
                <b>Automated Context Architecture:</b> For administrative organization workflows. This portal does not issue diagnostics or medical evaluations. Verify all output elements directly against certified source records.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown('<h1 class="apple-title">AI-Based Smart Healthcare Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="apple-subtitle">Unstructured clinical data. Structured medical clarity. Instantly.</p>', unsafe_allow_html=True)

    # Pure clinical data parsing instructions - completely clean from administrative noise
    ROBUST_SYSTEM_PROMPT = """
    You are an expert medical transcriptionist and clinical data analyst. Parse the health document asset cleanly.
    
    CRITICAL INSTRUCTIONS:
    - DO NOT extract, format, or list general document metadata (such as document type labels, translation certification details, registration codes, processing dates, or file parameters).
    - Avoid outputting JSON text blocks, raw code snippets, code block markup, or dictionary formats entirely.
    
    Structure your processing report solely into these target medical data sections:
    
    ## 👤 Patient Profile & Clinical Demographics
    * **Patient Name:** [Name]
    * **Date of Birth / Age:** [Extract info here]
    * **Presenting History:** [Summary of baseline history or clinical problems]
    
    ## 🩺 Objective Findings & Diagnostic Evaluations
    * **Physical Examination:** [Findings and structural clinical presentation observations]
    * **Neuroimaging / Advanced Scans (MRI):** [Abnormalities, lesions, or space-occupying structures]
    * **Electrophysiological Testing:** [Details about Evoked Potentials, EMG records, and baseline metrics]
    
    ## 📋 Management Plan & Recommended Treatments
    * **Diagnostic Synthesis:** [Primary clinical assessment or diagnostic category]
    * **Urgent Treatment Directives:** [Hospitalization status and directives]
    * **Therapeutic Regimen:** [Medications, dosing protocols, frequency, and treatment course duration]
    """

    st.markdown("<p style='color:#94a3b8; font-size:0.85rem; font-weight: 500; margin-bottom:6px;'>DIGITAL FILE DESK</p>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload Healthcare Document Panels", type=["pdf", "png", "jpg", "jpeg", "webp"], accept_multiple_files=True, label_visibility="collapsed")

    if uploaded_files:
        pages_to_process = []
        for uploaded_file in uploaded_files:
            uploaded_file.seek(0)
            if uploaded_file.type == "application/pdf":
                try:
                    pages_to_process.extend(convert_from_bytes(uploaded_file.read()))
                except Exception as e:
                    st.error(f"Failed decoding PDF: {e}")
            else:
                pages_to_process.append(Image.open(uploaded_file))

        if pages_to_process:
            canvas_left, canvas_right = st.columns([1, 1], gap="large")
            
            with canvas_left:
                st.markdown("<h3 style='font-size:1.3rem; margin-bottom:15px; font-weight:500;'>Source Matrix</h3>", unsafe_allow_html=True)
                for page_img in pages_to_process:
                    with st.container():
                        st.markdown('<div class="liquid-glass-card">', unsafe_allow_html=True)
                        st.image(page_img, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

            with canvas_right:
                st.markdown("<h3 style='font-size:1.3rem; margin-bottom:15px; font-weight:500;'>Synthesized Clinical Insights</h3>", unsafe_allow_html=True)
                with st.container():
                    st.markdown('<div class="output-pane">', unsafe_allow_html=True)
                    
                    with st.spinner("Compiling visual clinical layouts..."):
                        try:
                            response = client.models.generate_content(
                                model='gemini-2.5-flash', 
                                contents=[ROBUST_SYSTEM_PROMPT] + pages_to_process
                            )
                            
                            display_output = response.text
                            st.markdown(display_output)
                            
                            pdf_bytes = safe_generate_pdf(display_output)
                            
                            st.markdown("<br><hr style='opacity:0.1;'><br>", unsafe_allow_html=True)
                            
                            # Clean, specific download button text update
                            st.download_button(
                                label="📥 Download PDF Report",
                                data=pdf_bytes,
                                file_name="clinical_summary_report.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Clinical Processing Failure: {str(e)}")
                    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. RENDER VIEWPORT: NEW ABOUT PAGE WITH "ABOUT ME" ---
elif st.session_state.current_page == "About":
    st.markdown('<h1 class="apple-title">About the Platform & Developer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="apple-subtitle">The technical vision and developer profile behind Healthcare Assistant.</p>', unsafe_allow_html=True)
    
    # About Me Spotlight Section
    st.markdown("""
    <div class="liquid-glass-card" style="margin-bottom: 30px;">
        <h3 style="color:#007aff; margin-top:0;">👨‍💻 About Me & My Vision</h3>
        <p style="font-size:1.05rem; line-height:1.6; color:#e2e8f0; text-align: justify;">
            Welcome! I am a clinical systems developer dedicated to creating high-performance, intelligent interfaces that transform messy, unstructured medical assets into structured executive clarity. My mission with this smart assistant is to bridge the gap between advanced vision models and real-world administrative tasks, drastically reducing documentation friction for healthcare setups everywhere.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_feat1, col_feat2, col_feat3 = st.columns(3, gap="medium")
    with col_feat1:
        st.markdown("""
        <div class="info-feature-card">
            <h4 style="color:#38bdf8; margin-bottom:10px;">👁️ Multimodal Vision Processing</h4>
            <p style="font-size:0.9rem; line-height:1.5; color:#94a3b8;">
                Instead of processing fragile text layers, the portal maps out the visual and text layout of direct report matrices instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_feat2:
        st.markdown("""
        <div class="info-feature-card">
            <h4 style="color:#34c759; margin-bottom:10px;">⚡ Safe Local Memory Arrays</h4>
            <p style="font-size:0.9rem; line-height:1.5; color:#94a3b8;">
                Utilizes system-native memory buffers to map and process complex document pages directly without external file logs.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_feat3:
        st.markdown("""
        <div class="info-feature-card">
            <h4 style="color:#af52de; margin-bottom:10px;">🧠 Zero-Dependency PDF Exports</h4>
            <p style="font-size:0.9rem; line-height:1.5; color:#94a3b8;">
                Engineered with an independent rendering layer that converts clinical summaries directly to printable A4 PDF charts without server library crashes.
            </p>
        </div>
        """, unsafe_allow_html=True)
