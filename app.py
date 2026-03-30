import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Graphura Intelligence Engine",
    page_icon="◈",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:      #f5f4f0;
    --s1:      #ffffff;
    --s2:      #f0eeea;
    --border:  #e0ddd6;
    --dark:    #111111;
    --blue:    #1a56db;
    --blue2:   #1e429f;
    --muted:   #6b7280;
    --muted2:  #9ca3af;
    --green:   #057a55;
    --greenl:  #def7ec;
    --yellow:  #92400e;
    --yellowl: #fef3c7;
    --red:     #9b1c1c;
    --redl:    #fde8e8;
    --orange:  #92400e;
    --orangel: #fff3cd;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    background-color: var(--bg) !important;
    color: var(--dark) !important;
    font-family: 'Outfit', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAV ── */
.nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 3rem;
    background: var(--dark);
    border-bottom: 1px solid #222;
}
.nav-brand {
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.nav-brand em { font-style: normal; color: #60a5fa; }
.nav-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #6b7280;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    border: 1px solid #333;
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
}

/* ── HERO ── */
.hero {
    padding: 3.5rem 3rem 3rem 3rem;
    background: var(--dark);
    border-bottom: 3px solid var(--blue);
}
.hero-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.28em;
    color: #60a5fa;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.08;
    color: #ffffff;
    margin-bottom: 1rem;
}
.hero-h1 em { font-style: normal; color: #60a5fa; }
.hero-p {
    font-size: 0.9rem;
    color: #9ca3af;
    line-height: 1.85;
    max-width: 520px;
    font-weight: 300;
}
.hero-stats {
    display: flex;
    gap: 3rem;
    margin-top: 2rem;
    padding-top: 1.75rem;
    border-top: 1px solid #222;
}
.stat-n {
    font-family: 'Outfit', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
}
.stat-n em { font-style: normal; color: #60a5fa; }
.stat-l {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #4b5563;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

/* ── BODY ── */
.body-wrap { padding: 2.5rem 3rem; }

/* ── SECTION LABEL ── */
.sec-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    color: var(--blue);
    text-transform: uppercase;
    padding-bottom: 0.75rem;
    border-bottom: 1.5px solid var(--border);
    margin-bottom: 1.25rem;
    font-weight: 500;
}

/* ── CARD ── */
.card {
    background: var(--s1);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

/* ── PILLAR BADGE ── */
.pillar-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    padding: 0.7rem 1.1rem;
    margin-top: 0.75rem;
}
.pillar-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: var(--muted2);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.pillar-val {
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--blue2);
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    background: var(--s1);
    border: 1.5px dashed var(--border);
    border-radius: 10px;
}
.empty-icon { font-size: 2rem; margin-bottom: 0.75rem; opacity: 0.25; }
.empty-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: var(--muted2);
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

/* ── RESULT BOX ── */
.result-box {
    border-radius: 10px;
    padding: 2.25rem;
    text-align: center;
    margin-bottom: 1rem;
}
.rb-priority { background: var(--greenl);  border: 1.5px solid #0e9f6e; }
.rb-good     { background: #f0fdf4;         border: 1.5px solid #86efac; }
.rb-average  { background: var(--yellowl); border: 1.5px solid #f59e0b; }
.rb-bad      { background: var(--redl);    border: 1.5px solid #f87171; }

.rb-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    margin-bottom: 0.3rem;
}
.rb-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.rb-bar-wrap {
    height: 4px;
    background: rgba(0,0,0,0.1);
    border-radius: 2px;
    max-width: 180px;
    margin: 1.1rem auto 0 auto;
    overflow: hidden;
}
.rb-bar-fill { height: 100%; border-radius: 2px; }

/* ── REASON ROW ── */
.reason-row {
    font-size: 0.83rem;
    color: #374151;
    padding: 0.55rem 0;
    border-bottom: 1px solid var(--border);
    line-height: 1.5;
}
.reason-row:last-child { border: none; }

/* ── ML CARD ── */
.ml-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    color: var(--blue2);
    text-transform: uppercase;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 100px;
    margin-bottom: 0.85rem;
}
.ml-label {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
}
.ml-conf {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    margin-top: 0.2rem;
    letter-spacing: 0.1em;
}
.prob-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.65rem;
}
.prob-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: var(--muted);
    text-transform: uppercase;
    width: 55px;
}
.prob-track {
    flex: 1;
    height: 5px;
    background: var(--border);
    border-radius: 3px;
    overflow: hidden;
}
.prob-fill { height: 100%; border-radius: 3px; }
.prob-pct {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    width: 40px;
    text-align: right;
    font-weight: 500;
}

/* ── SUMMARY TABLE ── */
.s-table { width: 100%; border-collapse: collapse; }
.s-table tr { border-bottom: 1px solid var(--border); }
.s-table tr:last-child { border: none; }
.s-table td { padding: 0.65rem 0; font-size: 0.83rem; color: var(--dark); }
.s-table td:first-child {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: var(--muted2);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    width: 150px;
}

/* ── BUTTON ── */
.stButton > button {
    background: var(--dark) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    padding: 0.9rem 2rem !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: var(--blue) !important;
}

/* Selectbox */
div[data-testid="stSelectbox"] > div > div {
    background: var(--s1) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--dark) !important;
    font-family: 'Outfit', sans-serif !important;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}
div[data-testid="stNumberInput"] input {
    background: var(--s1) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--dark) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── FOOTER ── */
.g-footer {
    text-align: center;
    padding: 2rem 0 1.5rem 0;
    margin-top: 2rem;
    border-top: 1px solid var(--border);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: var(--muted2);
    letter-spacing: 0.22em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────────
@st.cache_resource
def load_models():
    try:
        model        = pickle.load(open('model_graphura.pkl',  'rb'))
        le_dict      = pickle.load(open('label_encoders.pkl',  'rb'))
        target_le    = pickle.load(open('target_encoder.pkl',  'rb'))
        feature_cols = pickle.load(open('feature_cols.pkl',    'rb'))
        X_cols       = pickle.load(open('x_cols.pkl',          'rb'))
        return model, le_dict, target_le, feature_cols, X_cols, True
    except:
        return None, None, None, None, None, False

model, le_dict, target_le, feature_cols, X_cols, loaded = load_models()


# ─────────────────────────────────────────────
# RULE ENGINE
# ─────────────────────────────────────────────
def rule_engine(platform, day, pillar, synced, post_type):
    score, reasons = 0, []

    if day in ['Thursday', 'Friday']:
        score += 3; reasons.append(f'● {day} — best performing day  +3')
    elif day in ['Monday', 'Saturday']:
        score += 1; reasons.append(f'◐ {day} — average day  +1')
    else:
        reasons.append(f'○ {day} — low engagement day  +0')

    if platform == 'Linkedin':
        score += 2; reasons.append('● LinkedIn — high engagement platform  +2')
    else:
        score += 1; reasons.append('◐ Instagram — lower engagement rate  +1')

    pm = {'Authority': 3, 'Value': 2, 'Engagement': 1, 'Community': 1}
    if pillar in pm:
        score += pm[pillar]
        reasons.append(f'● {pillar} pillar  +{pm[pillar]}')
    else:
        reasons.append('○ Pillar unknown  +0')

    if synced == 'Yes':
        score += 2; reasons.append('● Synced — cross platform boost  +2')
    else:
        reasons.append('○ Not synced  +0')

    pt = post_type.lower()
    if pt == 'carousel':
        score += 2; reasons.append('● Carousel — highest avg engagement  +2')
    elif pt == 'video':
        score += 1; reasons.append('◐ Video — good reach  +1')
    else:
        reasons.append('○ Image — standard  +0')

    if score >= 8:
        return 'PRIORITY POST', score, reasons, 'rb-priority', '#057a55', '⚡'
    elif score >= 5:
        return 'GOOD TO POST',  score, reasons, 'rb-good',     '#16a34a', '✓'
    elif score >= 3:
        return 'AVERAGE',       score, reasons, 'rb-average',  '#b45309', '△'
    else:
        return 'RECONSIDER',    score, reasons, 'rb-bad',      '#dc2626', '✕'


# ─────────────────────────────────────────────
# ML PREDICT
# ─────────────────────────────────────────────
def ml_predict(platform, post_type, days, boosted, synced,
               pillar, caption, hashtags, duration):
    if not loaded: return None
    try:
        inp = {
            'platform': platform, 'post_type': post_type.lower(),
            'days': days, 'boosted': boosted, 'synced': synced,
            'content_pillar': pillar, 'time_slot': 'Unknown',
            'caption_length': caption
        }
        enc = {}
        for col in feature_cols:
            le = le_dict[col]; val = inp[col]
            enc[col + '_enc'] = le.transform([val])[0] if val in le.classes_ else 0
        enc['hashtag_count']  = hashtags
        enc['duration_(sec)'] = duration
        X     = pd.DataFrame([enc])[X_cols]
        pred  = model.predict(X)[0]
        proba = model.predict_proba(X)[0]
        label = target_le.inverse_transform([pred])[0]
        conf  = round(max(proba) * 100, 1)
        return label, conf, proba
    except:
        return None


# ══════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════

# NAV
st.markdown("""
<div class="nav">
    <div class="nav-brand">GRAPH<em>URA</em></div>
    <div class="nav-chip">Post Intelligence Engine &nbsp;·&nbsp; v1.0</div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <div class="hero-tag">◈ Calendar Intelligence Support Engine</div>
    <div class="hero-h1">Analyse Your Post.<br><em>Before</em> You Post.</div>
    <div class="hero-p">
        Feed your post parameters into the engine. Get a data-driven
        recommendation powered by EDA insights and a trained
        Random Forest model — instantly.
    </div>
    <div class="hero-stats">
        <div><div class="stat-n">175</div><div class="stat-l">Posts Analysed</div></div>
        <div><div class="stat-n"><em>2</em></div><div class="stat-l">Platforms</div></div>
        <div><div class="stat-n">12</div><div class="stat-l">Max Score</div></div>
        <div><div class="stat-n">3</div><div class="stat-l">Performance Tiers</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# BODY
st.markdown('<div class="body-wrap">', unsafe_allow_html=True)
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="sec-label">01 — Post Parameters</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        platform  = st.selectbox('Platform',   ['Linkedin', 'Instagram'])
        post_type = st.selectbox('Post Type',  ['Image', 'Carousel', 'Video'])
        synced    = st.selectbox('Synced',     ['No', 'Yes'])
    with c2:
        day     = st.selectbox('Day', ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
        boosted = st.selectbox('Boosted',        ['No', 'Yes'])
        caption = st.selectbox('Caption Length', ['Short', 'Medium', 'Long'])

    st.markdown('<div class="sec-label" style="margin-top:1.5rem;">02 — Content Details</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        hashtags = st.number_input('Hashtag Count', min_value=0, max_value=30, value=0)
    with c4:
        duration = st.number_input('Duration (sec)', min_value=0, max_value=600, value=0)

    pillar_map = {'image': 'Authority', 'carousel': 'Value', 'video': 'Engagement'}
    pillar = pillar_map.get(post_type.lower(), 'Community')

    st.markdown(f"""
    <div class="pillar-badge">
        <span class="pillar-tag">Auto Pillar</span>
        <span class="pillar-val">{pillar}</span>
        <span style="font-size:0.72rem;color:#9ca3af;">← from post type</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<br><br>', unsafe_allow_html=True)
    analyse = st.button('RUN ANALYSIS ◈')


with right:
    st.markdown('<div class="sec-label">03 — Intelligence Output</div>', unsafe_allow_html=True)

    if not analyse:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">◈</div>
            <div class="empty-text">Set parameters and click Run Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        result, score, reasons, css, color, icon = rule_engine(
            platform, day, pillar, synced, post_type
        )
        pct = int((score / 12) * 100)

        st.markdown(f"""
        <div class="result-box {css}">
            <div class="rb-title" style="color:{color};">{icon} {result}</div>
            <div class="rb-sub">Rule Engine Score — {score} / 12</div>
            <div class="rb-bar-wrap">
                <div class="rb-bar-fill" style="width:{pct}%;background:{color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.58rem;color:#9ca3af;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.75rem;">Scoring Breakdown</div>', unsafe_allow_html=True)
        for r in reasons:
            st.markdown(f'<div class="reason-row">{r}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-label" style="margin-top:1.5rem;">04 — ML Prediction</div>', unsafe_allow_html=True)

        if loaded:
            ml = ml_predict(platform, post_type, day, boosted,
                            synced, pillar, caption, hashtags, duration)
            if ml:
                label, conf, proba = ml
                lc = {'High': '#057a55', 'Medium': '#b45309', 'Low': '#dc2626'}.get(label, '#111')
                pc_map = {'High': '#057a55', 'Medium': '#d97706', 'Low': '#dc2626'}

                st.markdown(f"""
                <div class="card">
                    <div class="ml-tag">Random Forest Classifier</div>
                    <div class="ml-label" style="color:{lc};">{label} Performance</div>
                    <div class="ml-conf">Confidence — {conf}%</div>
                    <div style="margin-top:1.25rem;">
                """, unsafe_allow_html=True)

                for i, cls in enumerate(target_le.classes_):
                    p  = round(proba[i] * 100, 1)
                    pc = pc_map.get(cls, '#111')
                    st.markdown(f"""
                    <div class="prob-row">
                        <span class="prob-name">{cls}</span>
                        <div class="prob-track">
                            <div class="prob-fill" style="width:{p}%;background:{pc};"></div>
                        </div>
                        <span class="prob-pct" style="color:{pc};">{p}%</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('</div></div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                            color:#9ca3af;line-height:2.2;letter-spacing:0.1em;">
                    MODEL FILES NOT FOUND<br>
                    <span style="color:#d1d5db;font-size:0.6rem;">
                    model_graphura.pkl &nbsp;·&nbsp; label_encoders.pkl<br>
                    target_encoder.pkl &nbsp;·&nbsp; feature_cols.pkl &nbsp;·&nbsp; x_cols.pkl
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sec-label" style="margin-top:1.5rem;">05 — Post Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <table class="s-table">
                <tr><td>Platform</td>      <td>{platform}</td></tr>
                <tr><td>Day</td>           <td>{day}</td></tr>
                <tr><td>Post Type</td>     <td>{post_type}</td></tr>
                <tr><td>Pillar</td>        <td style="color:{color};font-weight:600;">{pillar}</td></tr>
                <tr><td>Synced</td>        <td>{synced}</td></tr>
                <tr><td>Boosted</td>       <td>{boosted}</td></tr>
                <tr><td>Caption</td>       <td>{caption}</td></tr>
                <tr><td>Hashtags</td>      <td>{hashtags}</td></tr>
                <tr><td>Rule Score</td>    <td style="color:{color};font-weight:600;">{score} / 12</td></tr>
                <tr><td>Result</td>        <td style="color:{color};font-weight:700;">{result}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="g-footer">
    Graphura &nbsp;·&nbsp; Calendar Intelligence Support Engine &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)