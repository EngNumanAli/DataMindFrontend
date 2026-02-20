import streamlit as st
import requests
import base64
import json

# Connect to the FastAPI Backend
BACKEND_URL = "http://localhost:8000/agent/invoke"

st.set_page_config(page_title="Data Agent", layout="wide")
st.title("📊 AI Data Analyst (Client)")

# File Upload
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
query = st.text_area("What do you want to analyze?")

if st.button("Run Agent"):
    if uploaded_file and query:
        with st.status("Processing...") as status:
            try:
                # 1. Convert File to Base64 (To send over network)
                bytes_data = uploaded_file.getvalue()
                base64_str = base64.b64encode(bytes_data).decode('utf-8')
                
                # 2. Prepare Payload
                payload = {
                    "input": {
                        "user_query": query,
                        "file_data": base64_str, # Sending file as text
                        "extracted_data": "",
                        "code_generated_llm": "",
                        "code_output": "",
                        "image_data": "",
                        "code_error": ""
                    }
                }
                
                # 3. Call FastAPI Backend
                response = requests.post(BACKEND_URL, json=payload)
                result = response.json()
                
                # 4. Handle Response
                if response.status_code == 200:
                    output = result.get("output", {})
                    
                    status.update(label="Complete!", state="complete")
                    
                    if output.get("code_error"):
                        st.error(f"Error: {output['code_error']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Python Code")
                        st.code(output.get("code_generated_llm", ""), language="python")
                        st.subheader("Console Output")
                        st.text(output.get("code_output", ""))
                        
                    with col2:
                        st.subheader("Visualization")
                        img_data = output.get("image_data")
                        if img_data:
                            # Convert Base64 back to Image
                            img_bytes = base64.b64decode(img_data)
                            st.image(img_bytes)
                        else:
                            st.info("No graph generated.")
                else:
                    st.error(f"Backend Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection Failed: {str(e)}")
                st.info("Ensure backend.py is running on port 8000")
# import streamlit as st
# import requests
# import base64
# import json

# # ── Backend URL ──────────────────────────────────────────────────────────────
# BACKEND_URL = "http://localhost:8000/agent/invoke"

# # ── Page Config ──────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="DataMind AI",
#     page_icon="⬡",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ── Custom CSS ────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

# /* ── Root Variables ── */
# :root {
#     --bg:        #080B10;
#     --surface:   #0E1319;
#     --border:    #1C2333;
#     --accent:    #00E5FF;
#     --accent2:   #7B61FF;
#     --danger:    #FF4D6D;
#     --success:   #00FFA3;
#     --text:      #E8EDF5;
#     --muted:     #4A5568;
#     --glow:      0 0 30px rgba(0,229,255,0.15);
# }

# /* ── Global Reset ── */
# * { box-sizing: border-box; }

# html, body, [data-testid="stAppViewContainer"] {
#     background: var(--bg) !important;
#     color: var(--text) !important;
#     font-family: 'Syne', sans-serif !important;
# }

# [data-testid="stAppViewContainer"]::before {
#     content: '';
#     position: fixed;
#     top: -50%;
#     left: -50%;
#     width: 200%;
#     height: 200%;
#     background:
#         radial-gradient(ellipse 600px 400px at 20% 10%, rgba(0,229,255,0.04) 0%, transparent 70%),
#         radial-gradient(ellipse 500px 300px at 80% 90%, rgba(123,97,255,0.05) 0%, transparent 70%);
#     pointer-events: none;
#     z-index: 0;
# }

# /* ── Hide Streamlit Branding ── */
# #MainMenu, footer, header { visibility: hidden; }
# [data-testid="stToolbar"] { display: none; }

# /* ── Main Container ── */
# .main .block-container {
#     max-width: 1300px;
#     padding: 2rem 2.5rem 4rem !important;
#     position: relative;
#     z-index: 1;
# }

# /* ── Hero Header ── */
# .hero {
#     display: flex;
#     align-items: center;
#     justify-content: space-between;
#     padding: 2.5rem 0 3rem;
#     border-bottom: 1px solid var(--border);
#     margin-bottom: 2.5rem;
# }
# .hero-left { display: flex; align-items: center; gap: 1.2rem; }
# .hero-icon {
#     width: 52px; height: 52px;
#     background: linear-gradient(135deg, var(--accent), var(--accent2));
#     border-radius: 14px;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 1.4rem;
#     box-shadow: var(--glow);
#     flex-shrink: 0;
# }
# .hero-title {
#     font-size: 1.75rem;
#     font-weight: 800;
#     letter-spacing: -0.03em;
#     background: linear-gradient(135deg, #fff 30%, var(--accent));
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
#     margin: 0; line-height: 1;
# }
# .hero-sub {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.72rem;
#     color: var(--muted);
#     letter-spacing: 0.12em;
#     text-transform: uppercase;
#     margin-top: 0.3rem;
# }
# .status-badge {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.7rem;
#     color: var(--success);
#     background: rgba(0,255,163,0.08);
#     border: 1px solid rgba(0,255,163,0.2);
#     padding: 0.35rem 0.85rem;
#     border-radius: 20px;
#     letter-spacing: 0.1em;
# }
# .status-badge::before { content: '● '; font-size: 0.55rem; }

# /* ── Upload Zone ── */
# .upload-label {
#     font-size: 0.7rem;
#     font-family: 'JetBrains Mono', monospace;
#     color: var(--accent);
#     letter-spacing: 0.15em;
#     text-transform: uppercase;
#     margin-bottom: 0.5rem;
#     display: block;
# }

# [data-testid="stFileUploader"] {
#     background: var(--surface) !important;
#     border: 1px dashed var(--border) !important;
#     border-radius: 12px !important;
#     transition: border-color 0.2s, box-shadow 0.2s !important;
# }
# [data-testid="stFileUploader"]:hover {
#     border-color: var(--accent) !important;
#     box-shadow: var(--glow) !important;
# }
# [data-testid="stFileUploader"] label {
#     color: var(--muted) !important;
#     font-family: 'JetBrains Mono', monospace !important;
#     font-size: 0.8rem !important;
# }
# [data-testid="stFileUploaderDropzone"] {
#     background: transparent !important;
# }

# /* ── Textarea ── */
# .stTextArea textarea {
#     background: var(--surface) !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 12px !important;
#     color: var(--text) !important;
#     font-family: 'JetBrains Mono', monospace !important;
#     font-size: 0.88rem !important;
#     padding: 1rem 1.2rem !important;
#     resize: vertical !important;
#     transition: border-color 0.2s, box-shadow 0.2s !important;
# }
# .stTextArea textarea:focus {
#     border-color: var(--accent) !important;
#     box-shadow: var(--glow) !important;
#     outline: none !important;
# }
# .stTextArea label {
#     font-size: 0.7rem !important;
#     font-family: 'JetBrains Mono', monospace !important;
#     color: var(--accent) !important;
#     letter-spacing: 0.15em !important;
#     text-transform: uppercase !important;
# }

# /* ── Run Button ── */
# .stButton > button {
#     width: 100% !important;
#     background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
#     color: #000 !important;
#     border: none !important;
#     border-radius: 12px !important;
#     padding: 0.85rem 2rem !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 700 !important;
#     font-size: 0.9rem !important;
#     letter-spacing: 0.08em !important;
#     text-transform: uppercase !important;
#     cursor: pointer !important;
#     transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
#     box-shadow: 0 4px 20px rgba(0,229,255,0.25) !important;
# }
# .stButton > button:hover {
#     opacity: 0.88 !important;
#     transform: translateY(-1px) !important;
#     box-shadow: 0 8px 30px rgba(0,229,255,0.35) !important;
# }
# .stButton > button:active {
#     transform: translateY(0) !important;
# }

# /* ── Result Cards ── */
# .result-card {
#     background: var(--surface);
#     border: 1px solid var(--border);
#     border-radius: 16px;
#     padding: 1.5rem 1.8rem;
#     margin-bottom: 1.2rem;
#     position: relative;
#     overflow: hidden;
# }
# .result-card::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0; right: 0;
#     height: 2px;
#     background: linear-gradient(90deg, var(--accent), var(--accent2));
#     border-radius: 2px 2px 0 0;
# }
# .card-label {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.65rem;
#     letter-spacing: 0.2em;
#     text-transform: uppercase;
#     color: var(--muted);
#     margin-bottom: 1rem;
#     display: flex;
#     align-items: center;
#     gap: 0.5rem;
# }
# .card-label span {
#     display: inline-block;
#     width: 6px; height: 6px;
#     background: var(--accent);
#     border-radius: 50%;
#     box-shadow: 0 0 8px var(--accent);
# }

# /* ── Code Block ── */
# .stCode, [data-testid="stCode"] {
#     background: #060810 !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 10px !important;
# }
# .stCode code {
#     font-family: 'JetBrains Mono', monospace !important;
#     font-size: 0.8rem !important;
# }

# /* ── Console Output ── */
# .console-output {
#     background: #060810;
#     border: 1px solid var(--border);
#     border-radius: 10px;
#     padding: 1rem 1.2rem;
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.82rem;
#     color: var(--success);
#     line-height: 1.7;
#     min-height: 60px;
#     white-space: pre-wrap;
#     word-break: break-word;
# }
# .console-output.empty { color: var(--muted); font-style: italic; }

# /* ── Error Box ── */
# .error-box {
#     background: rgba(255,77,109,0.08);
#     border: 1px solid rgba(255,77,109,0.3);
#     border-radius: 12px;
#     padding: 1rem 1.4rem;
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.82rem;
#     color: var(--danger);
#     margin-bottom: 1.2rem;
#     display: flex;
#     align-items: flex-start;
#     gap: 0.75rem;
# }
# .error-box::before { content: '✕'; font-size: 1rem; flex-shrink: 0; }

# /* ── Image Frame ── */
# .image-frame {
#     background: #060810;
#     border: 1px solid var(--border);
#     border-radius: 12px;
#     padding: 1.2rem;
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     min-height: 200px;
# }
# .image-frame img { border-radius: 8px; max-width: 100%; }

# /* ── Empty State ── */
# .empty-state {
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
#     gap: 0.6rem;
#     min-height: 200px;
#     color: var(--muted);
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.78rem;
#     letter-spacing: 0.05em;
# }
# .empty-state .icon { font-size: 2rem; opacity: 0.3; }

# /* ── Divider ── */
# .section-divider {
#     border: none;
#     border-top: 1px solid var(--border);
#     margin: 2rem 0;
# }

# /* ── Status Widget ── */
# [data-testid="stStatus"] {
#     background: var(--surface) !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 12px !important;
#     font-family: 'JetBrains Mono', monospace !important;
# }

# /* ── Columns gap ── */
# [data-testid="stHorizontalBlock"] { gap: 1.5rem !important; }

# /* ── Scrollbar ── */
# ::-webkit-scrollbar { width: 6px; height: 6px; }
# ::-webkit-scrollbar-track { background: var(--bg); }
# ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
# ::-webkit-scrollbar-thumb:hover { background: var(--muted); }
# </style>
# """, unsafe_allow_html=True)

# # ── Hero Header ──────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="hero">
#     <div class="hero-left">
#         <div class="hero-icon">⬡</div>
#         <div>
#             <div class="hero-title">DataMind AI</div>
#             <div class="hero-sub">Intelligent Data Analysis Agent</div>
#         </div>
#     </div>
#     <div class="status-badge">Agent Online</div>
# </div>
# """, unsafe_allow_html=True)

# # ── Input Section ─────────────────────────────────────────────────────────────
# col_left, col_right = st.columns([1, 1.6], gap="large")

# with col_left:
#     st.markdown('<span class="upload-label">📁 &nbsp; Data Source</span>', unsafe_allow_html=True)
#     uploaded_file = st.file_uploader(
#         "Drop your CSV file here",
#         type=["csv"],
#         label_visibility="collapsed"
#     )

#     if uploaded_file:
#         st.markdown(f"""
#         <div style="
#             font-family: 'JetBrains Mono', monospace;
#             font-size: 0.72rem;
#             color: #00FFA3;
#             background: rgba(0,255,163,0.06);
#             border: 1px solid rgba(0,255,163,0.2);
#             border-radius: 8px;
#             padding: 0.5rem 0.9rem;
#             margin-top: 0.6rem;
#             display: flex;
#             align-items: center;
#             gap: 0.5rem;
#         ">
#             ✓ &nbsp; {uploaded_file.name} &nbsp;·&nbsp; {round(uploaded_file.size/1024, 1)} KB
#         </div>
#         """, unsafe_allow_html=True)

# with col_right:
#     query = st.text_area(
#         "ANALYSIS QUERY",
#         placeholder="e.g. Which country has the highest total sales? Show a bar chart.",
#         height=120,
#         label_visibility="visible"
#     )

# # ── Run Button ────────────────────────────────────────────────────────────────
# st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
# run_clicked = st.button("⬡ &nbsp; Run Analysis", use_container_width=True)

# st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# # ── Agent Execution ───────────────────────────────────────────────────────────
# if run_clicked:
#     if uploaded_file and query:
#         with st.status("🔄 &nbsp; Agent Processing...", expanded=True) as status:
#             try:
#                 st.write("📦 Encoding file...")
#                 bytes_data = uploaded_file.getvalue()
#                 base64_str = base64.b64encode(bytes_data).decode('utf-8')

#                 st.write("🔗 Calling backend agent...")
#                 payload = {
#                     "input": {
#                         "user_query": query,
#                         "file_data": base64_str,
#                         "extracted_data": "",
#                         "code_generated_llm": "",
#                         "code_output": "",
#                         "image_data": "",
#                         "code_error": ""
#                     }
#                 }

#                 response = requests.post(BACKEND_URL, json=payload, timeout=400)
#                 result = response.json()

#                 if response.status_code == 200:
#                     output = result.get("output", {})
#                     status.update(label="✓ &nbsp; Analysis Complete", state="complete", expanded=False)

#                     # ── Error Display ──
#                     if output.get("code_error"):
#                         st.markdown(f"""
#                         <div class="error-box">{output['code_error']}</div>
#                         """, unsafe_allow_html=True)

#                     # ── Results Grid ──
#                     res_left, res_right = st.columns([1, 1], gap="large")

#                     with res_left:
#                         # Generated Code
#                         st.markdown("""
#                         <div class="result-card">
#                             <div class="card-label"><span></span> Generated Code</div>
#                         </div>
#                         """, unsafe_allow_html=True)
#                         code_val = output.get("code_generated_llm", "")
#                         if code_val:
#                             st.code(code_val, language="python")
#                         else:
#                             st.markdown('<div class="console-output empty">No code generated.</div>', unsafe_allow_html=True)

#                         # Console Output
#                         st.markdown("""
#                         <div class="result-card" style="margin-top:1.2rem">
#                             <div class="card-label"><span></span> Console Output</div>
#                         </div>
#                         """, unsafe_allow_html=True)
#                         console_val = output.get("code_output", "")
#                         if console_val:
#                             st.markdown(f'<div class="console-output">{console_val}</div>', unsafe_allow_html=True)
#                         else:
#                             st.markdown('<div class="console-output empty">No console output.</div>', unsafe_allow_html=True)

#                     with res_right:
#                         # Visualization
#                         st.markdown("""
#                         <div class="result-card">
#                             <div class="card-label"><span></span> Visualization</div>
#                         </div>
#                         """, unsafe_allow_html=True)
#                         img_data = output.get("image_data")
#                         if img_data:
#                             img_bytes = base64.b64decode(img_data)
#                             st.image(img_bytes, use_container_width=True)
#                         else:
#                             st.markdown("""
#                             <div class="empty-state">
#                                 <div class="icon">◈</div>
#                                 <div>No visualization generated</div>
#                                 <div style="opacity:0.5">Ask for a chart or plot to see results here</div>
#                             </div>
#                             """, unsafe_allow_html=True)
#                 else:
#                     status.update(label="✕ &nbsp; Backend Error", state="error", expanded=False)
#                     st.markdown(f'<div class="error-box">{response.text}</div>', unsafe_allow_html=True)

#             except Exception as e:
#                 status.update(label="✕ &nbsp; Connection Failed", state="error", expanded=False)
#                 st.markdown(f'<div class="error-box">Connection Failed: {str(e)}</div>', unsafe_allow_html=True)
#                 st.markdown("""
#                 <div style="
#                     font-family: 'JetBrains Mono', monospace;
#                     font-size: 0.75rem;
#                     color: #4A5568;
#                     margin-top: 0.5rem;
#                     padding: 0.75rem 1rem;
#                     background: #0E1319;
#                     border-radius: 8px;
#                     border: 1px solid #1C2333;
#                 ">
#                     ℹ Ensure backend.py is running → uvicorn backend:app --port 8000
#                 </div>
#                 """, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div style="
#             font-family: 'JetBrains Mono', monospace;
#             font-size: 0.78rem;
#             color: #FF4D6D;
#             background: rgba(255,77,109,0.06);
#             border: 1px solid rgba(255,77,109,0.2);
#             border-radius: 10px;
#             padding: 0.85rem 1.2rem;
#             display: flex;
#             align-items: center;
#             gap: 0.6rem;
#         ">
#             ✕ &nbsp; Please upload a CSV file and enter your query before running.
#         </div>
#         """, unsafe_allow_html=True)

# # ── Default Empty State ───────────────────────────────────────────────────────
# else:
#     st.markdown("""
#     <div style="
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         justify-content: center;
#         gap: 1rem;
#         padding: 4rem 2rem;
#         text-align: center;
#     ">
#         <div style="font-size: 3rem; opacity: 0.08;">⬡</div>
#         <div style="
#             font-family: 'JetBrains Mono', monospace;
#             font-size: 0.78rem;
#             color: #2A3448;
#             letter-spacing: 0.1em;
#             text-transform: uppercase;
#         ">Upload a CSV and run your query to begin analysis</div>
#     </div>
#     """, unsafe_allow_html=True)