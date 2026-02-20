import streamlit as st
import requests
import base64
import time

BACKEND_URL = "https://datamindbackend-production.up.railway.app/agent/invoke"
HEALTH_URL  = "https://datamindbackend-production.up.railway.app/health"
MAX_FILE_MB     = 10
REQUEST_TIMEOUT = 400

st.set_page_config(page_title="DataMind AI", page_icon="◎", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');
:root{--bg:#F5F0E8;--surface:#FDFAF4;--border:#DDD5C4;--ink:#1A1612;--ink2:#4A3F35;--muted:#9A8F85;--accent:#C8502A;--success:#2A7A4A;--warn:#B8860B;--danger:#C8302A;--shadow:0 2px 20px rgba(26,22,18,0.08);--shadow-lg:0 8px 40px rgba(26,22,18,0.12)}
*{box-sizing:border-box}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--ink)!important;font-family:'IBM Plex Sans',sans-serif!important}
#MainMenu,footer,header{visibility:hidden}[data-testid="stToolbar"]{display:none}
.main .block-container{max-width:1300px;padding:0 2.5rem 4rem!important}
.masthead{border-bottom:3px solid var(--ink);padding:2rem 0 1.2rem;display:flex;align-items:flex-end;justify-content:space-between}
.masthead-issue{font-family:'IBM Plex Mono',monospace;font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--muted);margin-bottom:0.4rem}
.masthead-title{font-family:'Playfair Display',serif;font-size:3rem;font-weight:900;line-height:0.95;color:var(--ink);letter-spacing:-0.02em}
.masthead-title span{color:var(--accent)}
.masthead-tagline{font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:var(--muted);line-height:1.6;max-width:220px;text-align:right}
.status-pill{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:0.65rem;letter-spacing:0.12em;text-transform:uppercase;padding:0.3rem 0.8rem;border-radius:2px;margin-bottom:0.6rem}
.status-online{background:var(--success);color:#fff}.status-offline{background:var(--danger);color:#fff}
.rule{border:none;border-top:1px solid var(--border);margin:1.5rem 0}
.rule-thick{border:none;border-top:2px solid var(--ink);margin:0.5rem 0 2rem}
.slabel{font-family:'IBM Plex Mono',monospace;font-size:0.62rem;letter-spacing:0.22em;text-transform:uppercase;color:var(--muted);margin-bottom:0.6rem;display:flex;align-items:center;gap:0.6rem}
.slabel::after{content:'';flex:1;height:1px;background:var(--border)}
[data-testid="stFileUploader"]{background:var(--surface)!important;border:1.5px dashed var(--border)!important;border-radius:4px!important}
[data-testid="stFileUploader"]:hover{border-color:var(--accent)!important}
[data-testid="stFileUploaderDropzone"]{background:transparent!important}
[data-testid="stFileUploader"] label{font-family:'IBM Plex Mono',monospace!important;font-size:0.78rem!important;color:var(--muted)!important}
.stTextArea textarea{background:var(--surface)!important;border:1.5px solid var(--border)!important;border-radius:4px!important;color:var(--ink)!important;font-family:'IBM Plex Mono',monospace!important;font-size:0.85rem!important;padding:0.9rem 1rem!important;line-height:1.6!important}
.stTextArea textarea:focus{border-color:var(--accent)!important;outline:none!important}
.stTextArea label{font-family:'IBM Plex Mono',monospace!important;font-size:0.62rem!important;letter-spacing:0.22em!important;text-transform:uppercase!important;color:var(--muted)!important}
.stButton>button{width:100%!important;background:var(--ink)!important;color:var(--bg)!important;border:none!important;border-radius:3px!important;padding:0.9rem 2rem!important;font-family:'IBM Plex Mono',monospace!important;font-weight:500!important;font-size:0.8rem!important;letter-spacing:0.15em!important;text-transform:uppercase!important;box-shadow:var(--shadow)!important}
.stButton>button:hover{background:var(--accent)!important;transform:translateY(-1px)!important}
.stButton>button:disabled{background:var(--border)!important;color:var(--muted)!important}

/* Step boxes */
.step-box{background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--border);border-radius:4px;padding:1rem 1.2rem;margin-bottom:0.5rem;box-shadow:var(--shadow)}
.step-active{border-left-color:var(--accent)!important}
.step-done{border-left-color:var(--success)!important;opacity:0.8}
.step-error{border-left-color:var(--danger)!important}
.step-waiting{opacity:0.4}
.step-row{display:flex;align-items:center;gap:0.75rem}
.step-icon{font-size:1rem;flex-shrink:0;width:1.4rem;text-align:center}
.step-num{font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.15em;color:var(--muted);text-transform:uppercase;flex-shrink:0}
.step-name{font-family:'IBM Plex Sans',sans-serif;font-size:0.88rem;font-weight:500;color:var(--ink)}
.step-detail{font-family:'IBM Plex Mono',monospace;font-size:0.73rem;color:var(--ink2);line-height:1.5;padding-left:3.2rem;margin-top:0.25rem}

/* Chat history */
.chat-container{display:flex;flex-direction:column;gap:1rem;margin-bottom:1.5rem}
.chat-turn{border-radius:6px;overflow:hidden;box-shadow:var(--shadow)}
.chat-turn-header{display:flex;align-items:center;justify-content:space-between;padding:0.6rem 1rem;background:var(--surface);border-bottom:1px solid var(--border)}
.chat-turn-num{font-family:'IBM Plex Mono',monospace;font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--muted)}
.chat-turn-query{font-family:'IBM Plex Sans',sans-serif;font-size:0.9rem;font-weight:500;color:var(--ink);padding:0.8rem 1rem;background:var(--surface);border-bottom:1px solid var(--border)}
.chat-query-label{font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--accent);margin-bottom:0.2rem}
.chat-result{padding:0.8rem 1rem;background:#FDFAF4}
.chat-result-row{display:flex;gap:1rem;align-items:flex-start}
.chat-output{font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:var(--success);background:#1A1612;border-radius:3px;padding:0.6rem 0.8rem;flex:1;line-height:1.6;min-height:40px;white-space:pre-wrap}
.chat-output-empty{color:var(--muted);font-style:italic}
.chat-error{font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:var(--danger);background:#FFF5F5;border:1px solid #F5C5C5;border-radius:3px;padding:0.6rem 0.8rem;flex:1}

/* Result cards */
.result-title{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:var(--ink);margin-bottom:0.2rem}
.result-meta{font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:var(--muted);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.9rem}
.code-topbar{background:#2A2420;padding:0.55rem 1rem;font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#888;letter-spacing:0.15em;text-transform:uppercase;display:flex;align-items:center;gap:0.4rem;border-radius:4px 4px 0 0}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.dot-r{background:#FF5F56}.dot-y{background:#FFBD2E}.dot-g{background:#27C93F}
.console-out{background:#1A1612;border-radius:4px;padding:1rem 1.2rem;font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#7FD992;line-height:1.8;min-height:80px;white-space:pre-wrap;word-break:break-word}
.console-empty{color:#555;font-style:italic}
.img-card{background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:1.2rem}
.error-card{background:#FFF5F5;border:1px solid #F5C5C5;border-left:4px solid var(--danger);border-radius:4px;padding:1rem 1.2rem;font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:var(--danger);line-height:1.6;margin-bottom:1rem}
.error-lbl{font-weight:500;font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.3rem}
.warn-card{background:#FFFBF0;border:1px solid #EDD890;border-left:4px solid var(--warn);border-radius:4px;padding:0.75rem 1rem;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:var(--warn);margin-bottom:1rem}
.empty-box{background:var(--surface);border:1.5px dashed var(--border);border-radius:4px;padding:3rem 2rem;text-align:center;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:var(--muted)}
.empty-icon{font-size:2rem;opacity:0.15;margin-bottom:0.75rem}
.clear-btn-wrap{display:flex;justify-content:flex-end;margin-bottom:0.5rem}

[data-testid="stDownloadButton"] button{background:transparent!important;border:1.5px solid var(--border)!important;color:var(--ink2)!important;font-family:'IBM Plex Mono',monospace!important;font-size:0.72rem!important;letter-spacing:0.1em!important;border-radius:3px!important;padding:0.5rem 1rem!important;margin-top:0.75rem!important}
[data-testid="stHorizontalBlock"]{gap:2rem!important}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
</style>
""", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────
# This is how Streamlit stores data between reruns
# chat_history is the list we pass to backend each request
# turns is the display history for the UI
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "turns" not in st.session_state:
    st.session_state.turns = []         # displayed in UI
if "last_file_name" not in st.session_state:
    st.session_state.last_file_name = None

# ── Helpers ───────────────────────────────────────────────────────────────────
def check_backend():
    try:
        r = requests.get(HEALTH_URL, timeout=3)
        return r.status_code == 200
    except:
        return False

def validate_file(f):
    if f is None: return "No file uploaded."
    if f.size/1024/1024 > MAX_FILE_MB: return f"File too large. Max is {MAX_FILE_MB}MB."
    if not f.name.lower().endswith(".csv"): return "Only CSV files supported."
    return None

def step(icon, num, name, detail, state="waiting"):
    return f'<div class="step-box step-{state}"><div class="step-row"><span class="step-icon">{icon}</span><span class="step-num">{num}</span><span class="step-name">{name}</span></div><div class="step-detail">{detail}</div></div>'

# ── Masthead ──────────────────────────────────────────────────────────────────
backend_online = check_backend()
sc = "status-online" if backend_online else "status-offline"
sl = "● Live" if backend_online else "● Offline"
turn_count = len(st.session_state.turns)

st.markdown(f"""
<div class="masthead">
    <div>
        <div class="masthead-issue">AI Data Intelligence Platform</div>
        <div class="masthead-title">Data<span>Mind</span></div>
    </div>
    <div style="text-align:right">
        <span class="status-pill {sc}">{sl}</span>
        <div class="masthead-tagline">Upload your data.<br>Ask questions.<br>I remember the conversation.</div>
    </div>
</div>
<div class="rule-thick"></div>
""", unsafe_allow_html=True)

if not backend_online:
    st.markdown('<div class="warn-card">⚠ &nbsp; Backend offline — run: <strong>python backend.py</strong></div>', unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
c1, c2 = st.columns([1, 1.6], gap="large")

with c1:
    st.markdown('<div class="slabel">01 &nbsp; Data Source</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("CSV", type=["csv"], label_visibility="collapsed")

    if uploaded_file:
        mb = uploaded_file.size/1024/1024
        ok = mb <= MAX_FILE_MB
        col = "#2A7A4A" if ok else "#C8302A"
        bg  = "#F0FFF4" if ok else "#FFF5F5"
        bd  = "#B0DFC0" if ok else "#F5C5C5"
        ic  = "✓" if ok else "✕"
        st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:{col};background:{bg};border:1px solid {bd};border-radius:3px;padding:0.45rem 0.8rem;margin-top:0.5rem">{ic} &nbsp; {uploaded_file.name} &nbsp;·&nbsp; {mb:.2f} MB</div>', unsafe_allow_html=True)

        # Auto-clear history when a new file is uploaded
        if st.session_state.last_file_name != uploaded_file.name:
            st.session_state.chat_history  = []
            st.session_state.turns         = []
            st.session_state.last_file_name = uploaded_file.name

with c2:
    st.markdown('<div class="slabel">02 &nbsp; Query</div>', unsafe_allow_html=True)
    query = st.text_area(
        "Query",
        placeholder="e.g. Which country has highest sales?\nThen: Now show me a bar chart of that.\nThen: Filter to only top 5...",
        height=130,
        label_visibility="collapsed"
    )
    if turn_count > 0:
        st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.65rem;color:var(--muted);margin-top:0.4rem">💬 {turn_count} turn{"s" if turn_count!=1 else ""} in this session — agent remembers context</div>', unsafe_allow_html=True)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# Buttons row
btn_c1, btn_c2 = st.columns([4, 1], gap="small")
with btn_c1:
    st.markdown('<div class="slabel">03 &nbsp; Execute</div>', unsafe_allow_html=True)
    run = st.button("◎  Run Analysis", use_container_width=True, disabled=not backend_online)
with btn_c2:
    st.markdown('<div class="slabel">Clear</div>', unsafe_allow_html=True)
    if st.button("↺  New Session", use_container_width=True):
        st.session_state.chat_history  = []
        st.session_state.turns         = []
        st.session_state.last_file_name = None
        st.rerun()

st.markdown("<hr class='rule'>", unsafe_allow_html=True)

# ── Agent Run ─────────────────────────────────────────────────────────────────
if run:
    ferr = validate_file(uploaded_file)
    if ferr:
        st.markdown(f'<div class="error-card"><div class="error-lbl">Input Error</div>{ferr}</div>', unsafe_allow_html=True)
        st.stop()
    if not query or not query.strip():
        st.markdown('<div class="error-card"><div class="error-lbl">Input Error</div>Please enter a query.</div>', unsafe_allow_html=True)
        st.stop()

    # ── Live step progress ────────────────────────────────────────────────
    st.markdown('<div class="slabel">Processing Log</div>', unsafe_allow_html=True)
    s1=st.empty(); s2=st.empty(); s3=st.empty(); s4=st.empty(); s5=st.empty()

    s1.markdown(step("⚙","Step 01","Preparing File","Encoding CSV to base64...","active"), unsafe_allow_html=True)
    s2.markdown(step("◌","Step 02","Connecting to Backend","Waiting...","waiting"), unsafe_allow_html=True)
    s3.markdown(step("◌","Step 03","Node 1 — Data Extractor","Waiting...","waiting"), unsafe_allow_html=True)
    s4.markdown(step("◌","Step 04","Node 2 — Code Generator",f"Waiting... (history: {len(st.session_state.chat_history)//2} turns)","waiting"), unsafe_allow_html=True)
    s5.markdown(step("◌","Step 05","Node 3 — E2B Sandbox","Waiting...","waiting"), unsafe_allow_html=True)

    time.sleep(0.3)
    raw = uploaded_file.getvalue()
    b64 = base64.b64encode(raw).decode("utf-8")
    kb  = len(raw)/1024
    s1.markdown(step("✓","Step 01","File Ready",f"Encoded {kb:.1f} KB.","done"), unsafe_allow_html=True)
    s2.markdown(step("⚙","Step 02","Connecting to Backend","Sending request to Railway backend...","active"), unsafe_allow_html=True)

    # Pass chat_history to backend so LLM has context
    payload = {
        "input": {
            "user_query":         query.strip(),
            "file_data":          b64,
            "extracted_data":     "",
            "code_generated_llm": "",
            "code_output":        "",
            "image_data":         "",
            "code_error":         "",
            "chat_history":       st.session_state.chat_history  # ← send history
        }
    }

    try:
        history_turns = len(st.session_state.chat_history)//2
        s3.markdown(step("⚙","Step 03","Node 1 — Data Extractor","Parsing CSV...","active"), unsafe_allow_html=True)
        s4.markdown(step("⚙","Step 04","Node 2 — Code Generator",f"LLM generating code with {history_turns} turns of context...","active"), unsafe_allow_html=True)
        s5.markdown(step("⚙","Step 05","Node 3 — E2B Sandbox","Spinning up secure sandbox...","active"), unsafe_allow_html=True)

        response = requests.post(BACKEND_URL, json=payload, timeout=REQUEST_TIMEOUT)
        s2.markdown(step("✓","Step 02","Connected",f"HTTP {response.status_code}.","done"), unsafe_allow_html=True)

        if response.status_code == 200:
            output  = response.json().get("output", {})
            code_v  = output.get("code_generated_llm", "")
            cons_v  = output.get("code_output", "")
            img_v   = output.get("image_data",  "")
            err_v   = output.get("code_error",  "")

            # ── Update local history from backend response ────────────────
            # Backend returns updated history — we store it for next request
            new_history = output.get("chat_history", st.session_state.chat_history)
            st.session_state.chat_history = new_history

            s3.markdown(step("✓","Step 03","Node 1 — Data Extractor","CSV parsed.","done"), unsafe_allow_html=True)
            s4.markdown(step("✓" if code_v else "✕","Step 04","Node 2 — Code Generator",f"Code generated ({len(code_v)} chars)." if code_v else "No code generated.","done" if code_v else "error"), unsafe_allow_html=True)
            if err_v:
                s5.markdown(step("✕","Step 05","Node 3 — E2B Sandbox",f"Error: {err_v}","error"), unsafe_allow_html=True)
            else:
                hi = "Chart ✓" if img_v else "No chart"
                ho = f"{len(cons_v)} chars" if cons_v else "No output"
                s5.markdown(step("✓","Step 05","Node 3 — E2B Sandbox",f"Done. {ho} · {hi}","done"), unsafe_allow_html=True)

            # ── Store turn for display ────────────────────────────────────
            st.session_state.turns.append({
                "query":   query.strip(),
                "code":    code_v,
                "output":  cons_v,
                "image":   img_v,
                "error":   err_v,
                "turn_num": len(st.session_state.turns) + 1
            })

            st.rerun()  # rerun to show updated history

        else:
            for sx,n in [(s3,"Node 1"),(s4,"Node 2"),(s5,"Node 3")]:
                sx.markdown(step("✕","—",n,"Skipped.","error"), unsafe_allow_html=True)
            try: err = response.json().get("error", response.text)
            except: err = response.text
            st.markdown(f'<div class="error-card"><div class="error-lbl">Backend Error {response.status_code}</div>{err}</div>', unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        s2.markdown(step("✕","Step 02","Connection Failed","Cannot reach backend. Is backend.py running?","error"), unsafe_allow_html=True)
        for sx,n in [(s3,"Node 1"),(s4,"Node 2"),(s5,"Node 3")]:
            sx.markdown(step("✕","—",n,"Skipped — no connection.","error"), unsafe_allow_html=True)
    except requests.exceptions.Timeout:
        s5.markdown(step("✕","Step 05","E2B Sandbox","Request timed out. Try a simpler query.","error"), unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="error-card"><div class="error-lbl">Unexpected Error</div>{str(e)}</div>', unsafe_allow_html=True)


# ── Conversation History Display ──────────────────────────────────────────────
if st.session_state.turns:
    st.markdown('<div class="slabel">Conversation History</div>', unsafe_allow_html=True)

    # Show turns in reverse — newest first
    for turn in reversed(st.session_state.turns):
        n      = turn["turn_num"]
        q      = turn["query"]
        code_v = turn["code"]
        cons_v = turn["output"]
        img_v  = turn["image"]
        err_v  = turn["error"]

        with st.expander(f"Turn {n} — {q[:60]}{'...' if len(q)>60 else ''}", expanded=(n == len(st.session_state.turns))):

            if err_v:
                st.markdown(f'<div class="error-card"><div class="error-lbl">Error</div>{err_v}</div>', unsafe_allow_html=True)

            r1, r2 = st.columns([1,1], gap="large")

            with r1:
                st.markdown('<div class="result-title">Generated Code</div><div class="result-meta">Python · LLM generated</div>', unsafe_allow_html=True)
                if code_v:
                    st.markdown('<div class="code-topbar"><span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span>&nbsp; analysis.py</div>', unsafe_allow_html=True)
                    st.code(code_v, language="python")
                else:
                    st.markdown('<div class="empty-box"><div class="empty-icon">{ }</div>No code</div>', unsafe_allow_html=True)

                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                st.markdown('<div class="result-title">Console Output</div><div class="result-meta">stdout · Sandbox result</div>', unsafe_allow_html=True)
                if cons_v:
                    st.markdown(f'<div class="console-out">{cons_v}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="console-out console-empty">No output printed.</div>', unsafe_allow_html=True)

            with r2:
                st.markdown('<div class="result-title">Visualization</div><div class="result-meta">Chart · PNG from sandbox</div>', unsafe_allow_html=True)
                if img_v:
                    img_bytes = base64.b64decode(img_v)
                    st.markdown('<div class="img-card">', unsafe_allow_html=True)
                    st.image(img_bytes, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.download_button(
                        f"↓  Download Chart (Turn {n})",
                        img_bytes, f"chart_turn_{n}.png", "image/png",
                        use_container_width=True,
                        key=f"dl_{n}"
                    )
                else:
                    st.markdown('<div class="empty-box"><div class="empty-icon">◎</div>No chart.<br><span style="opacity:0.6">Ask for a bar chart, line graph, or pie chart.</span></div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="empty-box" style="padding:4rem 2rem"><div class="empty-icon" style="font-size:2.5rem">◎</div>Upload a CSV and ask your first question to begin.<br><span style="opacity:0.6">You can ask follow-up questions — the agent remembers context.</span></div>', unsafe_allow_html=True)
