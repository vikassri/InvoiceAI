"""
Invoice Extractor — NVIDIA GenAI (Gemma 3)
Run: streamlit run invoice_extractor.py
Requires: pip install streamlit requests
Set env var: NVIDIA_KEY=your_key_here
"""

import os
import base64
import json
import requests
import streamlit as st
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Invoice Extractor by Vikas Srivastava",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme initialization ───────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "light"

IS_DARK = st.session_state.theme == "dark"

THEMES = {
    "dark": {
        "app_bg":"#0a0d14","sidebar_bg":"#0f1320","sidebar_border":"#1e2535",
        "card_bg":"#111827","card_border":"#1e2d42","input_bg":"#111827","input_border":"#1e2d42",
        "tab_list_bg":"#0f1320","tab_active_bg":"#1e2d42","json_bg":"#080c14",
        "table_head_bg":"#0f1a2e","table_row_hover":"#111e30","table_border":"#131d2e",
        "scrollbar_track":"#080c14","scrollbar_thumb":"#1e2d42",
        "upload_border":"#1e3a5f","upload_ph_border":"#1a2540",
        "text_primary":"#e8eaf0","text_secondary":"#5a6480","text_muted":"#3a4a60",
        "text_dim":"#2a3a50","text_hdr":"#3a4a60","text_table_hdr":"#4a6080",
        "text_table_val":"#c8d4e4","text_input":"#e2e8f0","text_card":"#e2e8f0",
        "accent":"#76e0a8","accent_dim":"rgba(118,224,168,0.12)",
        "accent_btn":"linear-gradient(135deg,#1a4731,#0f6e3a)",
        "accent_btn_hover":"linear-gradient(135deg,#166534,#047857)",
        "accent_btn_border":"#166534","accent_btn_text":"#a7f3d0",
        "accent_btn_shadow":"rgba(74,222,128,0.15)",
        "dl_btn_bg":"#111827","dl_btn_color":"#60a5fa","dl_btn_border":"#1e3a5f",
        "banner_warn_bg":"#2e1a0d","banner_warn_border":"#78350f","banner_warn_text":"#fbbf24",
        "banner_err_bg":"#2e0d0d","banner_err_border":"#7f1d1d","banner_err_text":"#f87171",
        "banner_info_bg":"#0d1e3a","banner_info_border":"#1e3a5f","banner_info_text":"#93c5fd",
        "tag_green_bg":"#0d2e1e","tag_green_color":"#4ade80","tag_green_border":"#166534",
        "tag_orange_bg":"#2e1a0d","tag_orange_color":"#fb923c","tag_orange_border":"#7c2d12",
        "section_border":"#151f30","page_title":"#ffffff",
        "creator_bg":"#111827","creator_border":"#1e2d42","creator_label":"#5a6480",
        "footer_text":"#2a3a50",
    },
    "light": {
        "app_bg":"#f8fafc","sidebar_bg":"#ffffff","sidebar_border":"#e2e8f0",
        "card_bg":"#ffffff","card_border":"#e2e8f0","input_bg":"#ffffff","input_border":"#cbd5e1",
        "tab_list_bg":"#f1f5f9","tab_active_bg":"#ffffff","json_bg":"#f8fafc",
        "table_head_bg":"#f1f5f9","table_row_hover":"#f8fafc","table_border":"#e9eef5",
        "scrollbar_track":"#f1f5f9","scrollbar_thumb":"#cbd5e1",
        "upload_border":"#94a3b8","upload_ph_border":"#94a3b8",
        "text_primary":"#0f172a","text_secondary":"#475569","text_muted":"#94a3b8",
        "text_dim":"#94a3b8","text_hdr":"#64748b","text_table_hdr":"#475569",
        "text_table_val":"#334155","text_input":"#0f172a","text_card":"#334155",
        "accent":"#059669","accent_dim":"rgba(5,150,105,0.1)",
        "accent_btn":"linear-gradient(135deg,#d1fae5,#a7f3d0)",
        "accent_btn_hover":"linear-gradient(135deg,#a7f3d0,#6ee7b7)",
        "accent_btn_border":"#34d399","accent_btn_text":"#065f46",
        "accent_btn_shadow":"rgba(5,150,105,0.2)",
        "dl_btn_bg":"#eff6ff","dl_btn_color":"#2563eb","dl_btn_border":"#bfdbfe",
        "banner_warn_bg":"#fffbeb","banner_warn_border":"#fbbf24","banner_warn_text":"#92400e",
        "banner_err_bg":"#fef2f2","banner_err_border":"#fca5a5","banner_err_text":"#991b1b",
        "banner_info_bg":"#eff6ff","banner_info_border":"#93c5fd","banner_info_text":"#1e40af",
        "tag_green_bg":"#f0fdf4","tag_green_color":"#166534","tag_green_border":"#86efac",
        "tag_orange_bg":"#fff7ed","tag_orange_color":"#c2410c","tag_orange_border":"#fdba74",
        "section_border":"#e2e8f0","page_title":"#0f172a",
        "creator_bg":"#f1f5f9","creator_border":"#e2e8f0","creator_label":"#64748b",
        "footer_text":"#94a3b8",
    },
}

T = THEMES[st.session_state.theme]

# ── Inject CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');
html,body,[class*="css"]{{font-family:'DM Sans',sans-serif;}}
.stApp{{background:{T['app_bg']} !important;color:{T['text_primary']};}}
#MainMenu,footer,header{{visibility:hidden;}}
.block-container{{padding-top:1.5rem;padding-bottom:2rem;}}
[data-testid="stSidebar"]{{background:{T['sidebar_bg']} !important;border-right:1px solid {T['sidebar_border']};}}
.page-title{{font-size:2rem;font-weight:600;color:{T['page_title']};letter-spacing:-0.5px;line-height:1.2;margin-bottom:0.2rem;}}
.page-subtitle{{color:{T['text_secondary']};font-size:0.9rem;font-weight:300;margin-bottom:1.2rem;}}
.creator-badge{{display:inline-flex;align-items:center;gap:0.5rem;background:{T['creator_bg']};border:1px solid {T['creator_border']};border-radius:99px;padding:0.25rem 0.85rem;font-size:0.72rem;}}
.creator-badge .lbl{{color:{T['creator_label']};}}
.card{{background:{T['card_bg']};border:1px solid {T['card_border']};border-radius:12px;padding:1.5rem;margin-bottom:1rem;}}
.metric-row{{display:flex;gap:0.75rem;margin-bottom:1.25rem;}}
.metric-card{{flex:1;background:{T['card_bg']};border:1px solid {T['card_border']};border-radius:10px;padding:1rem 1.2rem;text-align:center;}}
.metric-card .val{{font-family:'DM Mono',monospace;font-size:1.75rem;font-weight:500;color:{T['accent']};line-height:1;}}
.metric-card .lbl{{font-size:0.7rem;color:{T['text_muted']};text-transform:uppercase;letter-spacing:0.08em;margin-top:0.35rem;}}
.tag{{display:inline-block;padding:2px 10px;border-radius:99px;font-size:0.7rem;font-weight:500;letter-spacing:0.05em;text-transform:uppercase;}}
.tag-green{{background:{T['tag_green_bg']};color:{T['tag_green_color']};border:1px solid {T['tag_green_border']};}}
.tag-orange{{background:{T['tag_orange_bg']};color:{T['tag_orange_color']};border:1px solid {T['tag_orange_border']};}}
.json-viewer{{background:{T['json_bg']};border:1px solid {T['card_border']};border-radius:10px;padding:1.25rem 1.5rem;font-family:'DM Mono',monospace;font-size:0.82rem;line-height:1.7;overflow-x:auto;white-space:pre-wrap;word-break:break-word;color:{T['text_secondary']};max-height:520px;overflow-y:auto;}}
.field-table{{width:100%;border-collapse:collapse;font-size:0.875rem;}}
.field-table th{{background:{T['table_head_bg']};color:{T['text_table_hdr']};font-weight:500;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;padding:0.6rem 1rem;text-align:left;border-bottom:1px solid {T['card_border']};}}
.field-table td{{padding:0.65rem 1rem;border-bottom:1px solid {T['table_border']};color:{T['text_table_val']};vertical-align:top;}}
.field-table tr:last-child td{{border-bottom:none;}}
.field-table tr:hover td{{background:{T['table_row_hover']};}}
.field-key{{font-family:'DM Mono',monospace;font-size:0.78rem;color:{T['dl_btn_color']};white-space:nowrap;}}
.banner-warn{{background:{T['banner_warn_bg']};border:1px solid {T['banner_warn_border']};border-radius:8px;padding:0.75rem 1rem;color:{T['banner_warn_text']};font-size:0.875rem;margin-bottom:1rem;}}
.banner-error{{background:{T['banner_err_bg']};border:1px solid {T['banner_err_border']};border-radius:8px;padding:0.75rem 1rem;color:{T['banner_err_text']};font-size:0.875rem;margin-bottom:1rem;}}
.banner-info{{background:{T['banner_info_bg']};border:1px solid {T['banner_info_border']};border-radius:8px;padding:0.75rem 1rem;color:{T['banner_info_text']};font-size:0.875rem;margin-bottom:1rem;}}
.section-hdr{{font-size:0.72rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:{T['text_hdr']};margin:1.5rem 0 0.6rem;padding-bottom:0.4rem;border-bottom:1px solid {T['section_border']};}}
.stTextInput>div>div>input,.stSelectbox>div>div,.stTextArea textarea{{background:{T['input_bg']} !important;border:1px solid {T['input_border']} !important;color:{T['text_input']} !important;border-radius:8px !important;}}
.stTextInput>div>div>input:focus,.stTextArea textarea:focus{{border-color:{T['accent']} !important;box-shadow:0 0 0 2px {T['accent_dim']} !important;}}
.stButton>button{{background:{T['accent_btn']} !important;color:{T['accent_btn_text']} !important;border:1px solid {T['accent_btn_border']} !important;border-radius:8px !important;font-weight:500 !important;transition:all 0.2s !important;}}
.stButton>button:hover{{background:{T['accent_btn_hover']} !important;transform:translateY(-1px) !important;box-shadow:0 4px 16px {T['accent_btn_shadow']} !important;}}
.stDownloadButton>button{{background:{T['dl_btn_bg']} !important;color:{T['dl_btn_color']} !important;border:1px solid {T['dl_btn_border']} !important;border-radius:8px !important;font-family:'DM Mono',monospace !important;font-size:0.8rem !important;}}
[data-testid="stFileUploader"]{{background:{T['card_bg']};border:2px dashed {T['upload_border']};border-radius:12px;padding:0.5rem;}}
.stSlider>div>div>div>div{{background:{T['accent']} !important;}}
.stTabs [data-baseweb="tab-list"]{{background:{T['tab_list_bg']};border-radius:8px;padding:3px;gap:2px;}}
.stTabs [data-baseweb="tab"]{{background:transparent;color:{T['text_muted']};border-radius:6px;font-size:0.82rem;font-weight:500;}}
.stTabs [aria-selected="true"]{{background:{T['tab_active_bg']} !important;color:{T['accent']} !important;}}
.stSpinner>div{{border-top-color:{T['accent']} !important;}}
::-webkit-scrollbar{{width:5px;height:5px;}}
::-webkit-scrollbar-track{{background:{T['scrollbar_track']};}}
::-webkit-scrollbar-thumb{{background:{T['scrollbar_thumb']};border-radius:99px;}}
</style>
""", unsafe_allow_html=True)


# ── Constants ──────────────────────────────────────────────────────────────────
INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODELS = [
    "microsoft/phi-3.5-vision-instruct",
]
SYSTEM_PROMPTS = {
    "Invoice Extraction": "Extract all invoice details in clean JSON format. Include: invoice_number, date, due_date, vendor, bill_to, line_items (array with description/qty/unit_price/total), subtotal, tax, total_amount, payment_terms, notes., Please do not create or assume any data your self, incase you unable to parse though error like unable to parse",
    "Receipt Parsing":    "Parse this receipt and return JSON with: store_name, date, items (name/price), subtotal, tax, total, payment_method. Please do not create and assume any data your self, incase you unable to parse though error like unable to parse",
    "PO / Order Form":    "Extract purchase order details as JSON: po_number, order_date, vendor, ship_to, items (sku/description/qty/price), total. Please do not create and assume any data your self, incase you unable to parse though error like unable to parse",
    "Custom":             "",
}


# ── Helpers ────────────────────────────────────────────────────────────────────
def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

def flatten_dict(d, parent_key="", sep=" › "):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep))
        elif isinstance(v, list):
            if all(isinstance(i, dict) for i in v):
                for idx, item in enumerate(v):
                    items.update(flatten_dict(item, f"{new_key}[{idx}]", sep))
            else:
                items[new_key] = ", ".join(str(i) for i in v)
        else:
            items[new_key] = v
    return items

def call_nvidia_api(api_key, model, image_b64, system_prompt, max_tokens, temperature, top_p):
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    user_content = f"{system_prompt}\n\n" + f'<img src="data:image/png;base64,{image_b64}" />'
    payload = {"model": model, "messages": [{"role": "user", "content": user_content}],
               "max_tokens": max_tokens, "temperature": temperature, "top_p": top_p, "stream": False}
    resp = requests.post(INVOKE_URL, headers=headers, json=payload, timeout=90)
    resp.raise_for_status()
    return resp.json()

def parse_json_from_content(content):
    cleaned = content.replace("```json","").replace("```","").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start != -1 and end != -1:
        return json.loads(cleaned[start:end+1])
    raise ValueError("No valid JSON found in model response")


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Brand
    st.markdown(f"""
    <div style='margin-bottom:1.2rem'>
        <div style='font-size:1.2rem;font-weight:600;color:{T["page_title"]}'>🧾 InvoiceAI</div>
        <div style='font-size:0.75rem;color:{T["text_muted"]};margin-top:2px'>Powered by Vikas Srivastava</div>
    </div>""", unsafe_allow_html=True)

    # ── Auth ───────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-hdr">🔑 Authentication</div>', unsafe_allow_html=True)
    api_key_input = st.text_input(
        "NVIDIA API Key", value=os.getenv("NVIDIA_KEY",""), type="password",
        placeholder="nvapi-••••••••••••", help="Get your key at build.nvidia.com",
        label_visibility="collapsed",
    )
    if api_key_input:
        st.markdown('<div class="tag tag-green">● Key set</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="tag tag-orange">● No key set</div>', unsafe_allow_html=True)

    # ── Model ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-hdr">🤖 Model</div>', unsafe_allow_html=True)
    selected_model = st.selectbox("Model", MODELS, index=0, label_visibility="collapsed")

    # ── Extraction Mode ────────────────────────────────────────────────────────
    st.markdown('<div class="section-hdr">📋 Extraction Mode</div>', unsafe_allow_html=True)
    extraction_mode = st.selectbox("Mode", list(SYSTEM_PROMPTS.keys()), label_visibility="collapsed")
    if extraction_mode == "Custom":
        active_prompt = st.text_area("Prompt", height=90, placeholder="Describe what to extract…", label_visibility="collapsed")
    else:
        active_prompt = SYSTEM_PROMPTS[extraction_mode]
        with st.expander("View prompt", expanded=False):
            st.code(active_prompt, language=None)

    # ── Parameters ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-hdr">⚙️ Parameters</div>', unsafe_allow_html=True)
    max_tokens  = st.slider("Max tokens",  128, 2048, 512,  step=64)
    temperature = st.slider("Temperature", 0.0, 1.0,  0.20, step=0.05)
    top_p       = st.slider("Top-p",       0.1, 1.0,  0.70, step=0.05)

    st.markdown("---")
    st.markdown(
        f'<div style="font-size:0.7rem;color:{T["text_dim"]};line-height:1.6">'
        'Images encoded to base64 locally.<br>Max ~131k chars sent to API.<br>No data stored server-side.'
        '</div>', unsafe_allow_html=True,
    )

        # ── Theme toggle ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-hdr">🎨 Appearance</div>', unsafe_allow_html=True)
    col_d, col_l = st.columns(2)
    with col_d:
        if st.button("🌙  Dark",  width='stretch',
                     type="primary" if st.session_state.theme=="dark" else "secondary"):
            st.session_state.theme = "dark"; st.rerun()
    with col_l:
        if st.button("☀️  Light", width='stretch',
                     type="primary" if st.session_state.theme=="light" else "secondary"):
            st.session_state.theme = "light"; st.rerun()

    # Current theme indicator
    theme_icon = "🌙" if IS_DARK else "☀️"
    st.markdown(
        f'<div style="text-align:center;font-size:0.7rem;color:{T["text_muted"]};'
        f'margin-top:0.3rem">{theme_icon} Active: <strong>{st.session_state.theme.capitalize()} Mode</strong></div>',
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
h_left, h_right = st.columns([3, 1])
with h_left:
    st.markdown(
        '<div class="page-title">Invoice Extractor</div>'
        f'<div class="page-subtitle">Upload an invoice image → AI extracts structured data via NVIDIA NIM'
        f'&nbsp;&nbsp;·&nbsp;&nbsp;{st.session_state.theme.capitalize()} Theme</div>',
        unsafe_allow_html=True,
    )

# API key guard
if not api_key_input:
    st.markdown(
        '<div class="banner-warn">⚠ Set your <strong>NVIDIA_KEY</strong> in the sidebar or as an environment variable.</div>',
        unsafe_allow_html=True,
    )
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
col_upload, col_results = st.columns([1,1], gap="large")

# ── Upload ─────────────────────────────────────────────────────────────────────
with col_upload:
    st.markdown('<div class="section-hdr">📎 Invoice Image</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Drop invoice here", type=["png","jpg","jpeg","webp","bmp"], label_visibility="collapsed")

    if uploaded:
        st.image(uploaded, width='stretch', caption=f"{uploaded.name}  ({uploaded.size/1024:.1f} KB)")
        b64    = image_to_base64(uploaded.getvalue())
        b64_kb = len(b64) / 1024
        st.markdown(
            f'<div class="banner-info">📐 Base64 size: <strong>{b64_kb:.0f} KB</strong> ',
            unsafe_allow_html=True,
        )
        extract_btn = st.button("⚡  Extract Invoice Data", width='stretch')
    else:
        st.markdown(
            f'<div style="text-align:center;padding:3rem 1rem;color:{T["text_muted"]};'
            f'border:2px dashed {T["upload_ph_border"]};border-radius:12px;font-size:0.875rem">'
            f'📤 Drag & drop or click to upload<br>'
            f'<span style="font-size:0.75rem;color:{T["text_dim"]}">PNG · JPG · WEBP · BMP</span>'
            f'</div>', unsafe_allow_html=True,
        )
        extract_btn = False


# ── Results ────────────────────────────────────────────────────────────────────
with col_results:
    st.markdown('<div class="section-hdr">📊 Extracted Data</div>', unsafe_allow_html=True)

    for key in ("last_result","last_usage"):
        if key not in st.session_state: st.session_state[key] = None
    if "history" not in st.session_state: st.session_state.history = []

    if extract_btn and uploaded:
        with st.spinner("🤖 Analyzing invoice…"):
            try:
                t0  = datetime.now()
                raw = call_nvidia_api(api_key_input, selected_model, b64,
                                      active_prompt, max_tokens, temperature, top_p)
                elapsed = (datetime.now() - t0).total_seconds()
                content = raw["choices"][0]["message"]["content"]
                usage   = raw.get("usage", {})
                try:
                    data = parse_json_from_content(content)
                    st.session_state.last_result = data
                    st.session_state.last_usage  = {**usage, "elapsed_s": round(elapsed,2)}
                    st.session_state.history.append({
                        "file": uploaded.name, "time": datetime.now().strftime("%H:%M:%S"),
                        "model": selected_model.split("/")[-1],
                        "tokens": usage.get("total_tokens",0), "elapsed": round(elapsed,2),
                    })
                except (ValueError, json.JSONDecodeError) as je:
                    st.markdown(f'<div class="banner-warn">⚠ Could not parse JSON.<br><small>{je}</small></div>', unsafe_allow_html=True)
                    st.session_state.last_result = {"_raw_response": content}
                    st.session_state.last_usage  = {**usage, "elapsed_s": round(elapsed,2)}
            except requests.HTTPError as e:
                st.markdown(f'<div class="banner-error">✗ API error {e.response.status_code}: {e.response.text[:200]}</div>', unsafe_allow_html=True)
            except requests.exceptions.Timeout:
                st.markdown('<div class="banner-error">✗ Request timed out (90s).</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="banner-error">✗ Unexpected error: {e}</div>', unsafe_allow_html=True)

    if st.session_state.last_result:
        data  = st.session_state.last_result
        usage = st.session_state.last_usage or {}
        pt, ct, tt, el = (usage.get(k,"—") for k in ("prompt_tokens","completion_tokens","total_tokens","elapsed_s"))

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card"><div class="val">{pt}</div><div class="lbl">Prompt Tokens</div></div>
            <div class="metric-card"><div class="val">{ct}</div><div class="lbl">Completion</div></div>
            <div class="metric-card"><div class="val">{tt}</div><div class="lbl">Total Tokens</div></div>
            <div class="metric-card"><div class="val">{el}s</div><div class="lbl">Latency</div></div>
        </div>""", unsafe_allow_html=True)

        tab_table, tab_json, tab_dl = st.tabs(["📋 Table","{ } JSON","⬇ Download"])

        with tab_table:
            flat = flatten_dict(data)
            rows = ""
            for k, v in flat.items():
                val = str(v) if v is not None else f'<span style="color:{T["text_dim"]}">null</span>'
                rows += f'<tr><td><span class="field-key">{k}</span></td><td style="color:{T["text_table_val"]}">{val}</td></tr>'
            st.markdown(f'<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>{rows}</tbody></table>', unsafe_allow_html=True)

        with tab_json:
            st.markdown(f'<div class="json-viewer">{json.dumps(data,indent=2)}</div>', unsafe_allow_html=True)

        with tab_dl:
            flat       = flatten_dict(data)
            json_bytes = json.dumps(data, indent=2).encode()
            fname      = f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
            st.download_button("⬇  Download JSON", data=json_bytes, file_name=fname, mime="application/json", width='stretch')
            st.markdown(f'<div class="banner-info" style="margin-top:0.75rem">📄 {len(flat)} fields · {len(json_bytes)} bytes · {fname}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align:center;padding:4rem 1rem;color:{T["text_muted"]};font-size:0.875rem">← Upload an invoice and click Extract</div>', unsafe_allow_html=True)


# ── History ────────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="section-hdr">🕑 Session History</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(st.session_state.history), 5))
    for i, h in enumerate(reversed(st.session_state.history[-5:])):
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="padding:0.85rem;text-align:center">
                <div style="font-size:0.72rem;color:{T['accent']};font-family:'DM Mono',monospace">{h['time']}</div>
                <div style="font-size:0.82rem;color:{T['text_card']};margin:0.2rem 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="{h['file']}">{h['file']}</div>
                <div style="font-size:0.7rem;color:{T['text_muted']}">{h['model']}</div>
                <div style="font-size:0.7rem;color:{T['text_muted']}">{h['tokens']} tokens · {h['elapsed']}s</div>
            </div>""", unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────

st.markdown(
    f'<div style="text-align:center;padding:2rem 0 0.5rem;font-size:0.7rem;color:{T["footer_text"]}">'
    f'InvoiceAI&nbsp;·&nbsp;NVIDIA NIM&nbsp;·&nbsp;{st.session_state.theme.capitalize()}'
    f'</div>',
    unsafe_allow_html=True,
)