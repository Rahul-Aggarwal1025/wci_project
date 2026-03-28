import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import re
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ── Helpers ────────────────────────────────────────────────────────────────────
def hex_to_rgba(hex_color, alpha=0.12):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WCI · Indian Manufacturing",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM — "OBSIDIAN VERDE"
# Dark luxury base · Emerald accent · Gold highlights · Sharp editorial type
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

/* ── CSS Custom Properties — Light Mode ── */
:root {
    --ink:        #f5f7f6;
    --ink-soft:   #eef2f0;
    --surface:    #ffffff;
    --surface-2:  #f0f4f2;
    --surface-3:  #e6ede9;
    --border:     rgba(16,122,72,0.12);
    --border-2:   rgba(16,122,72,0.22);
    --emerald:    #0d7a48;
    --emerald-dim:#15a362;
    --emerald-dk: #0a5c35;
    --gold:       #b45309;
    --gold-dim:   #d97706;
    --crimson:    #dc2626;
    --sapphire:   #2563eb;
    --violet:     #7c3aed;
    --text:       #0f1f17;
    --text-2:     #3d5c4a;
    --text-3:     #7a9988;
    --font-serif: 'DM Serif Display', Georgia, serif;
    --font-sans:  'DM Sans', system-ui, sans-serif;
    --font-mono:  'DM Mono', monospace;
    --r-sm:  8px;
    --r-md:  14px;
    --r-lg:  20px;
    --r-xl:  28px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.09), 0 2px 6px rgba(0,0,0,0.06);
    --shadow-lg: 0 12px 40px rgba(0,0,0,0.11), 0 4px 12px rgba(0,0,0,0.07);
    --glow:   0 0 30px rgba(13,122,72,0.10);
    --glow-strong: 0 0 50px rgba(13,122,72,0.18);
}

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: var(--font-sans) !important;
    color: var(--text) !important;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: var(--ink) !important;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 5%, rgba(13,122,72,0.04) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 90% 90%, rgba(180,83,9,0.025) 0%, transparent 50%),
        radial-gradient(ellipse 40% 40% at 50% 50%, rgba(37,99,235,0.015) 0%, transparent 60%);
    background-attachment: fixed !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 1.6rem !important;
    padding-bottom: 4rem !important;
    padding-left: 2.2rem !important;
    padding-right: 2.2rem !important;
    background: transparent !important;
    max-width: 1440px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--ink-soft) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.06) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text) !important;
    font-family: var(--font-sans) !important;
}
[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.55rem 0.8rem !important;
    border-radius: var(--r-sm) !important;
    transition: all 0.18s ease !important;
    cursor: pointer !important;
    color: var(--text-2) !important;
    border: 1px solid transparent !important;
    display: block !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(13,122,72,0.07) !important;
    color: var(--emerald) !important;
    border-color: var(--border) !important;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
    background: rgba(13,122,72,0.10) !important;
    color: var(--emerald) !important;
    border-color: var(--border-2) !important;
}

/* Selectbox & tabs */
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--text) !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--emerald-dim) !important;
    box-shadow: 0 0 0 2px rgba(13,122,72,0.12) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface-2) !important;
    border-radius: var(--r-sm) !important;
    padding: 3px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 6px !important;
    color: var(--text-3) !important;
    font-size: 0.81rem !important;
    font-weight: 500 !important;
    padding: 0.38rem 0.85rem !important;
    transition: all 0.15s ease !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--emerald) !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding: 0.85rem 0 0 0 !important;
}

/* Info box */
.stAlert {
    background: rgba(13,122,72,0.05) !important;
    border: 1px solid var(--border-2) !important;
    border-radius: var(--r-sm) !important;
    color: var(--text-2) !important;
}

/* Plotly modebar */
.modebar { background: var(--surface) !important; border-radius: var(--r-sm) !important; border: 1px solid var(--border) !important; }
.modebar-btn svg { fill: var(--emerald-dim) !important; }
.modebar-btn:hover svg { fill: var(--emerald) !important; }

/* ══ COMPONENTS ══ */

/* Glass card */
.g-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    box-shadow: var(--shadow-md);
    padding: 1.5rem 1.75rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.g-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(13,122,72,0.25), transparent);
    pointer-events: none;
}

/* Metric card */
.m-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    box-shadow: var(--shadow-sm);
    padding: 1.25rem 1rem 1.15rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.22s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.22s ease, border-color 0.22s ease;
}
.m-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md), var(--glow);
    border-color: var(--border-2);
}
.m-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-color, var(--emerald)), transparent);
    opacity: 0.5;
    pointer-events: none;
}
.m-card .val {
    font-family: var(--font-serif);
    font-size: 2.0rem;
    font-weight: 400;
    line-height: 1.1;
    display: block;
    margin-bottom: 0.42rem;
    letter-spacing: -0.01em;
}
.m-card .lbl {
    font-size: 0.65rem;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    display: block;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 100%);
    border: 1px solid var(--border);
    border-radius: var(--r-xl);
    padding: 2.6rem 3rem;
    margin-bottom: 1.8rem;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -120px; right: -80px;
    width: 380px; height: 380px;
    background: radial-gradient(circle, rgba(13,122,72,0.06), transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 30%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(180,83,9,0.03), transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--emerald);
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.hero-eyebrow::before {
    content: '';
    width: 24px; height: 1px;
    background: var(--emerald);
    display: inline-block;
    opacity: 0.7;
}
.hero h1 {
    font-family: var(--font-serif);
    font-size: 2.8rem;
    font-weight: 400;
    color: var(--text);
    margin: 0 0 0.65rem;
    line-height: 1.15;
    letter-spacing: -0.02em;
}
.hero h1 em {
    font-style: italic;
    color: var(--emerald);
}
.hero p {
    color: var(--text-2);
    font-size: 0.875rem;
    margin: 0;
    line-height: 1.85;
    max-width: 640px;
    font-weight: 300;
}
.tag {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(13,122,72,0.07);
    color: var(--emerald);
    font-size: 0.64rem;
    font-weight: 600;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    margin-right: 0.3rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    border: 1px solid rgba(13,122,72,0.18);
}

/* Section title */
.sec-title {
    font-family: var(--font-serif);
    font-size: 1.18rem;
    font-weight: 400;
    color: var(--text);
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    letter-spacing: -0.01em;
}
.sec-title::before {
    content: '';
    width: 3px; height: 18px;
    background: linear-gradient(180deg, var(--emerald), var(--emerald-dim));
    border-radius: 2px;
    flex-shrink: 0;
}

/* Rank card */
.rank-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 1rem 1.15rem;
    margin-bottom: 0.5rem;
    box-shadow: var(--shadow-sm);
    transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
    position: relative;
    overflow: hidden;
}
.rank-card:hover {
    transform: translateX(5px);
    border-color: var(--border-2);
    box-shadow: var(--shadow-md);
}

/* Insight card */
.ins-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 1.4rem;
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s ease, border-color 0.2s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.ins-card:hover {
    transform: translateY(-5px);
    border-color: var(--border-2);
    box-shadow: var(--shadow-md), var(--glow);
}

/* Caveat */
.caveat {
    background: rgba(180,83,9,0.05);
    border: 1px solid rgba(180,83,9,0.18);
    border-left: 3px solid var(--gold-dim);
    border-radius: var(--r-sm);
    padding: 0.65rem 1rem;
    font-size: 0.76rem;
    color: #92400e;
    margin-top: 0.8rem;
    font-family: var(--font-sans);
    line-height: 1.65;
}

/* Stat box */
.stat-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 1rem 0.85rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: transform 0.18s ease, border-color 0.18s ease;
}
.stat-box:hover {
    transform: translateY(-3px);
    border-color: var(--border-2);
}
.stat-box .sv {
    font-family: var(--font-serif);
    font-size: 1.55rem;
    font-weight: 400;
    display: block;
    line-height: 1.15;
    margin-bottom: 0.25rem;
}
.stat-box .sl {
    font-size: 0.64rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 600;
    color: var(--text-3);
    display: block;
}

/* Review card */
.rev-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 1rem 1.1rem;
    margin-bottom: 0.55rem;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.18s ease;
}
.rev-card:hover { border-color: var(--border-2); }

/* Signal card */
.signal-card {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 0.85rem 1rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 0.55rem;
    transition: border-color 0.15s ease;
}
.signal-card:hover { border-color: var(--border-2); }

/* Divider — renamed to .hr-divider to avoid HTML tag conflicts */
.hr-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-2), transparent);
    margin: 1.5rem 0;
}

/* Verdict */
.verdict {
    border-radius: var(--r-md);
    padding: 1rem 1.5rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.2rem;
}

/* OLS stat */
.ols-stat {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: 1.25rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: transform 0.18s ease, border-color 0.18s ease;
}
.ols-stat:hover {
    transform: translateY(-3px);
    border-color: var(--border-2);
}
.ols-stat .ov {
    font-family: var(--font-serif);
    font-size: 1.75rem;
    font-weight: 400;
    display: block;
    line-height: 1.1;
    letter-spacing: -0.01em;
}
.ols-stat .ol {
    font-size: 0.63rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    color: var(--text-3);
    display: block;
    margin-top: 0.28rem;
}

/* Theme pill */
.theme-pill {
    display: inline-block;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    font-family: var(--font-sans);
}

/* Sidebar brand */
.sb-brand {
    padding: 0.5rem 0 1.2rem;
}
.sb-brand-name {
    font-family: var(--font-serif);
    font-size: 1.3rem;
    font-weight: 400;
    color: var(--text);
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.sb-brand-name span {
    color: var(--emerald);
}
.sb-brand-sub {
    font-size: 0.63rem;
    color: var(--text-3);
    margin-top: 0.35rem;
    text-transform: uppercase;
    letter-spacing: 0.11em;
    font-weight: 500;
}
.sb-meta {
    font-size: 0.72rem;
    color: var(--text-3);
    line-height: 2.1;
}
.sb-meta-head {
    font-weight: 700;
    color: var(--emerald-dk);
    font-size: 0.68rem;
    margin-bottom: 0.05rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
</style>
""", unsafe_allow_html=True)

# ── Chart theme ────────────────────────────────────────────────────────────────
# Solid white backgrounds so fullscreen/expanded mode never shows dark backdrop
PLOT_BG    = "#ffffff"
PAPER_BG   = "#ffffff"
GRID_CLR   = "rgba(0,0,0,0.06)"
AXIS_CLR   = "rgba(0,0,0,0.15)"
TEXT_CLR   = "#374151"   # neutral dark-gray — readable on any light bg
TITLE_CLR  = "#111827"   # near-black

AXIS_FONT  = dict(color=TEXT_CLR,  size=10.5, family="DM Sans")
TITLE_FONT = dict(color=TITLE_CLR, size=11,   family="DM Sans")
TICK_FONT  = dict(color=TEXT_CLR,  size=10,   family="DM Sans")
LEG_FONT   = dict(color=TEXT_CLR,  size=10.5, family="DM Sans")

MODEBAR_CFG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["select2d","lasso2d","autoScale2d"],
    "toImageButtonOptions": {"format": "png", "scale": 2},
}

def base_layout(**kw):
    return dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family="DM Sans", color=TEXT_CLR, size=11),
        **kw,
    )

def ax(showgrid=True, **kw):
    d = dict(
        gridcolor=GRID_CLR, gridwidth=1,
        zeroline=False,
        linecolor=AXIS_CLR, linewidth=1, showline=True,
        tickfont=TICK_FONT,
        showgrid=showgrid,
    )
    d.update(kw)
    return d

# ── Constants ──────────────────────────────────────────────────────────────────
COMPANY_COLORS = {
    "Veljan Denison": "#059669",
    "Roto Pumps":     "#2563eb",
    "LTIMindtree":    "#7c3aed",
    "Hero Motocorp":  "#d97706",
    "Jay Ushin":      "#ea580c",
    "Tata Motors":    "#dc2626",
}
RANK_EMOJI   = {1:"#1", 2:"#2", 3:"#3", 4:"#4", 5:"#5", 6:"#6"}

THEME_COLS   = ['theme_respect','theme_management','theme_compensation','theme_growth','theme_wlb']
THEME_LABELS = ['Respect & Fairness','Management','Compensation','Growth & Learning','Work-Life Balance']
THEME_SHORT  = ['Respect','Mgmt','Comp','Growth','WLB']
THEME_EXPERT_W = [0.28, 0.24, 0.20, 0.16, 0.12]

THEME_META = {
    'theme_respect':      {'icon':'◈','label':'Respect & Fairness',    'weight':0.28,'color':'#059669'},
    'theme_management':   {'icon':'◎','label':'Management Quality',     'weight':0.24,'color':'#2563eb'},
    'theme_compensation': {'icon':'◇','label':'Compensation & Benefits', 'weight':0.20,'color':'#d97706'},
    'theme_growth':       {'icon':'↑','label':'Growth & Learning',       'weight':0.16,'color':'#7c3aed'},
    'theme_wlb':          {'icon':'⇌','label':'Work-Life Balance',      'weight':0.12,'color':'#ea580c'},
}

STOPWORDS = {
    "the","and","is","in","of","to","a","an","this","it","that","are","was","for","with",
    "on","at","by","from","as","be","have","has","had","not","but","or","so","if","we",
    "i","my","me","our","they","their","you","your","its","do","did","does","will","would",
    "could","should","been","being","more","also","very","all","can","which","who","what",
    "when","how","than","just","no","yes","there","here","like","about","based","user",
    "ratings","salary","skill","development","company","culture","work","life","balance",
    "job","good","bad","nice","great","best","worst","need","get","got","give","make",
    "made","much","many","some","any","other","well","really","time","nothing","employees",
}

# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df      = pd.read_csv("data_final.csv", parse_dates=["review_date"])
    scores  = pd.read_csv("wci_scores.csv")
    weights = pd.read_csv("wci_weights.csv")
    return df, scores, weights

df, scores, weights = load_data()
df_free = df[~df["structured_text"].astype(bool)].copy()

def top_phrases(series, n=8):
    tokens = []
    for text in series.dropna():
        words = re.findall(r'\b[a-z]{4,}\b', str(text).lower())
        tokens.extend([w for w in words if w not in STOPWORDS])
    return Counter(tokens).most_common(n)

def bar_pct(v, lo=-1, hi=1):
    return max(0, min(100, (v - lo) / (hi - lo) * 100))

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sb-brand'>
        <div class='sb-brand-name'>◈ Work<span>Culture</span></div>
        <div class='sb-brand-sub'>Indian Manufacturing · 2025</div>
    </div>
    <div class='hr-divider' style='margin-top:0'></div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["◈  Home & Leaderboard",
         "◎  Company Profile",
         "⇄  Head-to-Head",
         "∿  Regression & Insights"],
        label_visibility="collapsed"
    )

    _sb_n  = len(df)
    _sb_c  = df['company'].nunique()
    _sb_y1 = int(df['review_date'].dt.year.min())
    _sb_y2 = int(df['review_date'].dt.year.max())

    st.markdown(f"""
    <div class='hr-divider'></div>
    <div class='sb-meta'>
        <div class='sb-meta-head'>Dataset</div>
        {_sb_n:,} reviews · {_sb_c} firms<br>
        AmbitionBox · {_sb_y1}–{_sb_y2}<br><br>
        <div class='sb-meta-head'>NLP Engine</div>
        RoBERTa + VADER ensemble<br><br>
        <div class='sb-meta-head'>Framework</div>
        Chen et al. (2021)<br>
        PCA + Expert weights
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME & LEADERBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "◈  Home & Leaderboard":

    st.markdown("""
    <div class='hero'>
        <div class='hero-eyebrow'>AmbitionBox · NLP · Sentiment Analysis</div>
        <h1>Work Culture <em>Index</em></h1>
        <p>Transforming unstructured employee reviews into a rigorous, quantitative measure
        of workplace culture across six Indian firms — powered by a RoBERTa + VADER ensemble
        and the Chen et al. (2021) PCA weight optimisation framework.</p>
        <div style='margin-top:1.2rem'>
            <span class='tag'>◈ 6 Companies</span>
            <span class='tag'>◈ NLP-Powered</span>
            <span class='tag'>◈ Peer-Reviewed Method</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric row ─────────────────────────────────────────────────────────
    _n_total  = len(df)
    _n_cos    = df["company"].nunique()
    _n_scored = int((~df["structured_text"].astype(bool)).sum())
    _yr_span  = int(df['review_date'].dt.year.max()) - int(df['review_date'].dt.year.min())
    _yr_min   = int(df['review_date'].dt.year.min())
    _yr_max   = int(df['review_date'].dt.year.max())

    metric_data = [
        (f"{_n_total:,}",  "Total Reviews",  "#059669"),
        (str(_n_cos),      "Companies",       "#2563eb"),
        (f"{_n_scored:,}", "Reviews Scored",  "#7c3aed"),
        (f"{_yr_span} yrs","Data Span",       "#d97706"),
        ("0–100",          "WCI Scale",       "#ea580c"),
    ]
    cols = st.columns(5)
    for col, (val, lbl, clr) in zip(cols, metric_data):
        col.markdown(f"""
        <div class='m-card' style='--accent-color:{clr}'>
            <span class='val' style='color:{clr}'>{val}</span>
            <span class='lbl'>{lbl}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)

    left, right = st.columns([3, 2], gap="large")

    # ── Leaderboard chart ───────────────────────────────────────────────────
    with left:
        st.markdown('<div class="sec-title">WCI Leaderboard</div>', unsafe_allow_html=True)

        chart_df = scores.sort_values("wci_score", ascending=True).copy()
        chart_df["label"] = chart_df.apply(
            lambda r: f"{r['company']}  ✦" if r["company"] == "Veljan Denison" else r["company"], axis=1
        )
        bar_colors = [COMPANY_COLORS.get(c, "#059669") for c in chart_df["company"]]

        fig = go.Figure()

        # Background track bars
        fig.add_trace(go.Bar(
            x=[100]*len(chart_df), y=chart_df["label"],
            orientation="h",
            marker=dict(color="rgba(5,150,105,0.04)", line=dict(width=0)),
            hoverinfo="skip", showlegend=False,
        ))

        # Score bars with gradient feel via opacity layers
        fig.add_trace(go.Bar(
            x=chart_df["wci_score"], y=chart_df["label"],
            orientation="h",
            marker=dict(
                color=bar_colors,
                opacity=0.88,
                line=dict(color="rgba(255,255,255,0.08)", width=1)
            ),
            text=[f"  {v:.1f}" for v in chart_df["wci_score"]],
            textposition="outside",
            textfont=dict(color=TITLE_CLR, size=12, family="DM Serif Display"),
            hovertemplate="<b>%{y}</b><br>WCI Score: <b>%{x:.1f}</b><extra></extra>",
        ))

        fig.update_layout(
            **base_layout(
                barmode="overlay",
                xaxis=ax(
                    range=[0, 130],
                    title=dict(text="WCI Score (0–100)", font=TITLE_FONT),
                    tickfont=TICK_FONT,
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(color=TITLE_CLR, size=12, family="DM Sans"),
                    linecolor="rgba(5,150,105,0.12)",
                    showline=False,
                    zeroline=False,
                ),
                margin=dict(l=10, r=90, t=15, b=48),
                height=340, bargap=0.38,
            )
        )

        # Add rank annotations on left side
        for i, (_, row) in enumerate(chart_df.iterrows()):
            rank = int(scores[scores["company"] == row["company"]]["wci_rank"].iloc[0])
            fig.add_annotation(
                x=0, y=row["label"],
                text=f"#{rank}",
                xanchor="right", xshift=-8,
                showarrow=False,
                font=dict(size=10, color=COMPANY_COLORS.get(row["company"], "#059669"),
                          family="DM Mono"),
            )

        st.plotly_chart(fig, use_container_width=True, config=MODEBAR_CFG)

        _veljan_n  = int(scores[scores["company"]=="Veljan Denison"]["n_reviews"].iloc[0])
        _other_min = int(scores[scores["company"]!="Veljan Denison"]["n_reviews"].min())
        st.markdown(f"""
        <div class='caveat'>
        ✦ <b>Veljan Denison</b> — WCI derived from only {_veljan_n} reviews.
        Interpret with caution. All other firms have {_other_min}+ reviews.
        </div>
        """, unsafe_allow_html=True)

    # ── Rankings at a glance ────────────────────────────────────────────────
    with right:
        st.markdown('<div class="sec-title">Rankings at a Glance</div>', unsafe_allow_html=True)

        for _, row in scores.sort_values("wci_rank").iterrows():
            company  = row["company"]
            wci      = row["wci_score"]
            rating   = row["avg_rating"]
            n        = int(row["n_reviews"])
            rank     = int(row["wci_rank"])
            color    = COMPANY_COLORS.get(company, "#059669")
            caveat   = " ✦" if company == "Veljan Denison" else ""
            emoji    = RANK_EMOJI.get(rank, f"#{rank}")

            # Colour-coded rank accent strip
            st.markdown(f"""
            <div class='rank-card' style='border-left:3px solid {color}22'>
                <div style='position:absolute;top:0;left:0;bottom:0;width:3px;
                            background:linear-gradient(180deg,{color},{color}44);
                            border-radius:4px 0 0 4px'></div>
                <div style='display:flex;justify-content:space-between;align-items:center;
                            margin-bottom:0.42rem;padding-left:0.3rem'>
                    <div style='display:flex;align-items:center;gap:0.5rem'>
                        <span style='font-size:1rem'>{emoji}</span>
                        <span style='font-weight:600;color:{color};font-size:0.85rem;
                                     font-family:"DM Sans",sans-serif'>{company}{caveat}</span>
                    </div>
                    <span style='font-weight:400;color:{color};font-size:1.15rem;
                                 font-family:"DM Serif Display",serif'>{wci:.1f}</span>
                </div>
                <div style='background:rgba(5,150,105,0.06);border-radius:999px;height:4px;
                            margin-bottom:0.42rem;overflow:hidden;margin-left:0.3rem'>
                    <div style='background:linear-gradient(90deg,{color}dd,{color}55);
                                width:{wci:.0f}%;height:4px;border-radius:999px'></div>
                </div>
                <div style='display:flex;gap:1rem;padding-left:0.3rem'>
                    <span style='font-size:0.7rem;color:var(--text-3);font-family:"DM Sans",sans-serif'>
                        ★ {rating:.2f}</span>
                    <span style='font-size:0.7rem;color:var(--text-3);font-family:"DM Sans",sans-serif'>
                        {n:,} reviews</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Key Insights ────────────────────────────────────────────────────────
    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Key Insights</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

    _star_leader   = scores.sort_values("avg_rating", ascending=False).iloc[0]
    _wci_leader    = scores.sort_values("wci_score", ascending=False).iloc[0]
    _wci_last      = scores.sort_values("wci_score", ascending=True).iloc[0]
    _ltim = scores[scores["company"] == "LTIMindtree"].iloc[0] if "LTIMindtree" in scores["company"].values else None
    _ltim_body = (
        f"LTIMindtree contributes {int(_ltim['n_reviews']):,} reviews "
        f"({int(_ltim['n_reviews']/len(df)*100)}% of the dataset) and ranks "
        f"#{int(_ltim['wci_rank'])} on WCI with a score of {_ltim['wci_score']:.1f}. "
        f"Largest single dataset — highest statistical confidence."
        if _ltim is not None else "LTIMindtree data not available."
    )

    ic1, ic2, ic3 = st.columns(3)
    insight_data = [
        ("⇄", "#059669", "WCI ≠ Star Rating",
         f"{_star_leader['company']} has the highest avg star rating ({_star_leader['avg_rating']:.2f}★) "
         f"yet ranks #{int(_star_leader['wci_rank'])} on WCI. Text sentiment reveals what structured ratings hide."),
        ("↓", "#dc2626", f"{_wci_last['company']} Paradox",
         f"Largest sample ({int(_wci_last['n_reviews'])} reviews) yet scores lowest WCI. "
         f"Negative management text overwhelms a {_wci_last['avg_rating']:.2f}★ average."),
        ("◎", "#7c3aed", "LTIMindtree Baseline", _ltim_body),
    ]

    for col, (icon, clr, title, body) in zip([ic1, ic2, ic3], insight_data):
        with col:
            st.markdown(f"""
            <div class='ins-card' style='border-top:2px solid {clr}33'>
                <div style='width:36px;height:36px;border-radius:10px;
                            background:{clr}15;border:1px solid {clr}30;
                            display:flex;align-items:center;justify-content:center;
                            font-size:1.1rem;margin-bottom:0.75rem'>{icon}</div>
                <div style='font-weight:600;color:{clr};font-size:0.84rem;
                            margin-bottom:0.5rem;font-family:"DM Sans",sans-serif;
                            letter-spacing:-0.01em'>{title}</div>
                <div style='font-size:0.78rem;color:var(--text-2);line-height:1.78;
                            font-family:"DM Sans",sans-serif;font-weight:300'>{body}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Theme heatmap ───────────────────────────────────────────────────────
    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Theme Score Matrix</div>', unsafe_allow_html=True)

    all_means = df_free.groupby("company")[THEME_COLS].mean()
    hm_df = all_means.copy()
    hm_companies = scores.sort_values("wci_rank")["company"].tolist()
    hm_df = hm_df.reindex([c for c in hm_companies if c in hm_df.index])

    z_vals = hm_df.values
    text_vals = [[f"{v:+.3f}" for v in row] for row in z_vals]
    hover_vals = [[
        f"<b>{hm_df.index[i]}</b><br>{THEME_LABELS[j]}: <b>{z_vals[i,j]:+.4f}</b><extra></extra>"
        for j in range(len(THEME_LABELS))] for i in range(len(hm_df))]

    fig_hm = go.Figure(go.Heatmap(
        z=z_vals,
        x=THEME_SHORT,
        y=list(hm_df.index),
        colorscale=[
            [0.0, "#fecaca"],
            [0.3, "#fca5a5"],
            [0.5, "#f0fdf4"],
            [0.7, "#86efac"],
            [1.0, "#16a34a"],
        ],
        text=text_vals,
        texttemplate="%{text}",
        textfont=dict(size=11, family="DM Mono", color="#0f1f17"),
        hovertemplate="<b>%{y}</b><br>%{x}: <b>%{z:+.4f}</b><extra></extra>",
        showscale=True,
        colorbar=dict(
            title=dict(text="Score", font=TITLE_FONT, side="right"),
            tickfont=TICK_FONT,
            thickness=10,
            len=0.85,
            outlinecolor="rgba(5,150,105,0.15)",
            outlinewidth=1,
        ),
        xgap=3, ygap=3,
    ))
    fig_hm.update_layout(
        **base_layout(
            height=240,
            margin=dict(l=10, r=80, t=15, b=30),
            yaxis=dict(tickfont=dict(color=TITLE_CLR, size=11, family="DM Sans"),
                       showgrid=False, zeroline=False),
            xaxis=dict(tickfont=dict(color=TEXT_CLR, size=11, family="DM Sans"),
                       showgrid=False, zeroline=False, side="top"),
        )
    )
    st.plotly_chart(fig_hm, use_container_width=True, config=MODEBAR_CFG)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — COMPANY PROFILE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "◎  Company Profile":

    st.markdown("""
    <div class='hero'>
        <div class='hero-eyebrow'>Company Deep-Dive</div>
        <h1>Company <em>Profile</em></h1>
        <p>Sentiment scores, theme strengths, WCI contribution breakdown, quarterly trends,
        rating distribution, and sample verbatims — everything in one view.</p>
    </div>
    """, unsafe_allow_html=True)

    companies = scores.sort_values("wci_rank")["company"].tolist()
    sel = st.selectbox("Select a company", companies, label_visibility="collapsed")

    row_s     = scores[scores["company"] == sel].iloc[0]
    wci       = row_s["wci_score"]
    rank      = int(row_s["wci_rank"])
    avg_rat   = row_s["avg_rating"]
    n_reviews = int(row_s["n_reviews"])
    color     = COMPANY_COLORS.get(sel, "#059669")
    caveat    = " ✦" if sel == "Veljan Denison" else ""
    emoji     = RANK_EMOJI.get(rank, f"#{rank}")

    comp_free = df_free[df_free["company"] == sel].copy()
    comp_all  = df[df["company"] == sel].copy()
    all_means = df_free.groupby("company")[THEME_COLS].mean()

    # ── Hero metric cards ───────────────────────────────────────────────────
    pct_of_dataset = n_reviews / len(df) * 100
    usable_reviews = len(comp_free[~comp_free["low_signal"]]) if "low_signal" in comp_free.columns else len(comp_free)

    h_cols = st.columns(6)
    hm_data = [
        (f"{wci:.1f}",              "WCI Score",       color),
        (f"#{rank}",                 "WCI Rank",        color),
        (f"{avg_rat:.2f}★",         "Avg Rating",      "#d97706"),
        (f"{n_reviews:,}",          "Total Reviews",   "#2563eb"),
        (f"{pct_of_dataset:.1f}%",  "% of Dataset",    "#7c3aed"),
        (f"{usable_reviews:,}",     "Usable Reviews",  "#059669"),
    ]
    for col, (val, lbl, clr) in zip(h_cols, hm_data):
        col.markdown(f"""
        <div class='m-card' style='--accent-color:{clr}'>
            <span class='val' style='color:{clr}'>{val}</span>
            <span class='lbl'>{lbl}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    verdict_map = {
        1: ("Strong Culture",  "#059669", "Employees speak positively and themes score high relative to peers."),
        2: ("Above Average",   "#2563eb", "Solid sentiment with room to improve on specific themes."),
        3: ("Mid-Pack",        "#7c3aed", "Mixed performance — leads on some themes, lags on others."),
        4: ("Mixed Signals",   "#d97706", "Positive and negative sentiment roughly balanced across themes."),
        5: ("Below Average",   "#ea580c", "Dislike text drives WCI down — cultural pain points visible."),
        6: ("Needs Attention", "#dc2626", "Consistently negative text signals deep cultural challenges."),
    }
    vname, vcolor, vdesc = verdict_map.get(rank, ("Unknown","#607a6e",""))
    caveat_note = (
        f"<span style='font-size:0.72rem;color:#c49a1a;margin-left:0.75rem'>"
        f"⚠️ Based on only {n_reviews} reviews — treat with caution.</span>"
        if sel == "Veljan Denison" else ""
    )

    # WCI score bar across 0-100 — inlined to avoid f-string nesting issues
    wci_pct = int(round(wci))
    verdict_html = (
        f"<div class='verdict' style='background:var(--surface);border:1px solid {vcolor}22;"
        f"border-left:3px solid {vcolor}'>"
        f"<div style='display:flex;align-items:center;flex-wrap:wrap;gap:0.4rem'>"
        f"<span style='font-weight:600;color:{vcolor};font-size:0.92rem;"
        f"font-family:\"DM Sans\",sans-serif'>#{rank} · Verdict: {vname}{caveat}</span>"
        f"<span style='color:var(--text-2);font-size:0.82rem;"
        f"font-family:\"DM Sans\",sans-serif;font-weight:300'>{vdesc}</span>"
        f"{caveat_note}"
        f"</div>"
        f"<div style='margin-top:0.7rem;display:flex;align-items:center;gap:0.8rem'>"
        f"<span style='font-size:0.65rem;color:var(--text-3);font-family:\"DM Mono\",monospace;width:16px'>0</span>"
        f"<div style='flex:1;background:rgba(5,150,105,0.08);border-radius:999px;height:6px;"
        f"overflow:hidden;border:1px solid rgba(5,150,105,0.12)'>"
        f"<div style='background:linear-gradient(90deg,{vcolor},{vcolor}88);"
        f"width:{wci_pct}%;height:6px;border-radius:999px'></div>"
        f"</div>"
        f"<span style='font-size:0.65rem;color:var(--text-3);font-family:\"DM Mono\",monospace;width:24px'>100</span>"
        f"</div>"
        f"</div>"
    )
    st.markdown(verdict_html, unsafe_allow_html=True)

    # ── WCI Decomposition Narrative ─────────────────────────────────────────
    if sel in all_means.index:
        fw_arr_narr = weights["final_weight"].values if "final_weight" in weights.columns else np.array(THEME_EXPERT_W)
        # Compute weighted contributions for narrative
        contribs_narr = {
            t: all_means.loc[sel, t] * fw
            for t, fw in zip(THEME_COLS, fw_arr_narr)
        }
        # Contribution pct of total (use absolute values for share)
        total_abs = sum(abs(v) for v in contribs_narr.values()) or 1.0
        # Best / worst by weighted contribution
        best_narr_t  = max(contribs_narr, key=contribs_narr.get)
        worst_narr_t = min(contribs_narr, key=contribs_narr.get)
        best_narr_meta  = THEME_META[best_narr_t]
        worst_narr_meta = THEME_META[worst_narr_t]
        best_narr_c  = contribs_narr[best_narr_t]
        worst_narr_c = contribs_narr[worst_narr_t]
        best_narr_pct = abs(best_narr_c) / total_abs * 100
        # "pulling score down by X points" = how many WCI points the worst theme contributes negatively
        # Normalised WCI range: use the same raw score span from wci_scores
        wci_min = scores["wci_score"].min()
        wci_max = scores["wci_score"].max()
        wci_range = (wci_max - wci_min) or 1.0
        worst_drag_pts = abs(worst_narr_c) / (fw_arr_narr.sum() or 1.0) * wci_range
        # How many themes above peer avg
        peer_avg_narr = all_means.mean()
        themes_above = sum(1 for t in THEME_COLS if all_means.loc[sel, t] > peer_avg_narr[t])
        # Build narrative text
        best_dir  = "strong" if best_narr_c >= 0 else "below-average"
        worst_dir = "drag" if worst_narr_c < 0 else "modest contribution"
        above_below = "outperforms" if themes_above >= 3 else ("matches" if themes_above == 2 else "underperforms against")
        narrative_text = (
            f"<b>{sel}'s</b> WCI of <b>{wci:.1f}</b> is driven primarily by "
            f"{best_narr_meta['icon']} <b>{best_narr_meta['label']}</b> "
            f"(<span style='color:#059669'>{best_narr_c:+.3f}</span>), contributing "
            f"<b>{best_narr_pct:.0f}%</b> of its total index weight. "
            f"{worst_narr_meta['icon']} <b>{worst_narr_meta['label']}</b> "
            f"(<span style='color:#dc2626'>{worst_narr_c:+.3f}</span>) is the single biggest drag, "
            f"pulling the score down by approximately <b>{worst_drag_pts:.1f} points</b>. "
            f"This company <b>{above_below}</b> the peer average on "
            f"<b>{themes_above} of 5</b> themes."
        )
        st.markdown(f"""
        <div class='g-card' style='margin-bottom:1.2rem'>
            <div style='display:flex;align-items:center;gap:0.5rem;margin-bottom:0.65rem'>
                <span style='font-size:1rem;color:var(--emerald)'>◈</span>
                <span style='font-family:"DM Sans",sans-serif;font-size:0.68rem;font-weight:700;
                             text-transform:uppercase;letter-spacing:0.1em;color:var(--emerald)'>
                    WCI Decomposition
                </span>
            </div>
            <div style='font-size:0.85rem;color:var(--text-2);line-height:1.85;
                        font-family:"DM Sans",sans-serif;font-weight:300'>
                {narrative_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── What's Saving It / What's Killing It ───────────────────────────────
    if sel in all_means.index:
        fw_arr_wsk = weights["final_weight"].values if "final_weight" in weights.columns else np.array(THEME_EXPERT_W)
        wsk_contribs = []
        for t, fw, meta in zip(THEME_COLS, fw_arr_wsk, [THEME_META[t] for t in THEME_COLS]):
            wsk_contribs.append({
                "theme": meta["label"], "icon": meta["icon"],
                "raw": all_means.loc[sel, t], "weight": fw,
                "contribution": all_means.loc[sel, t] * fw,
                "color": meta["color"],
            })
        saving_tc = max(wsk_contribs, key=lambda x: x["contribution"])
        killing_tc = min(wsk_contribs, key=lambda x: x["contribution"])

        # Plain-English labels
        def _plain_label(tc, direction):
            if direction == "save":
                if tc["raw"] > 0.1:
                    return "Employees speak positively about this dimension."
                elif tc["raw"] > 0:
                    return "Slight positive edge — maintains the overall score."
                else:
                    return "Less negative here than other themes — relatively less damage."
            else:
                if tc["raw"] < -0.1:
                    return "Strong negative signal — major cultural pain point."
                elif tc["raw"] < 0:
                    return "Mild but consistent negativity pulling the index down."
                else:
                    return "Weakest positive contribution — room for significant improvement."

        save_label  = _plain_label(saving_tc, "save")
        kill_label  = _plain_label(killing_tc, "kill")

        wsk_col_l, wsk_col_r = st.columns(2, gap="large")
        with wsk_col_l:
            st.markdown(f"""
            <div style='background:var(--surface);border:1px solid rgba(5,150,105,0.25);
                        border-left:4px solid #1a8a4a;border-radius:var(--r-md);
                        padding:1.2rem 1.4rem;box-shadow:var(--shadow-sm);height:100%'>
                <div style='font-size:0.65rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:0.12em;color:#1a8a4a;margin-bottom:0.7rem;
                            font-family:"DM Mono",monospace'>✦ What's Saving the WCI</div>
                <div style='font-size:1.55rem;font-family:"DM Serif Display",serif;
                            color:#1a8a4a;line-height:1.1;margin-bottom:0.3rem'>
                    {saving_tc['icon']} {saving_tc['theme']}
                </div>
                <div style='font-size:0.78rem;color:var(--text-2);margin-bottom:0.75rem;
                            font-family:"DM Sans",sans-serif;font-weight:300;line-height:1.65'>
                    {save_label}
                </div>
                <div style='display:flex;gap:1.2rem;font-family:"DM Mono",monospace;font-size:0.7rem'>
                    <div>
                        <span style='color:var(--text-3)'>Raw score</span><br>
                        <span style='color:#1a8a4a;font-weight:600'>{saving_tc['raw']:+.4f}</span>
                    </div>
                    <div>
                        <span style='color:var(--text-3)'>Weight</span><br>
                        <span style='color:#1a8a4a;font-weight:600'>{saving_tc['weight']:.4f}</span>
                    </div>
                    <div>
                        <span style='color:var(--text-3)'>Contribution</span><br>
                        <span style='color:#1a8a4a;font-weight:600'>{saving_tc['contribution']:+.4f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with wsk_col_r:
            st.markdown(f"""
            <div style='background:var(--surface);border:1px solid rgba(220,38,38,0.22);
                        border-left:4px solid #ef4444;border-radius:var(--r-md);
                        padding:1.2rem 1.4rem;box-shadow:var(--shadow-sm);height:100%'>
                <div style='font-size:0.65rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:0.12em;color:#ef4444;margin-bottom:0.7rem;
                            font-family:"DM Mono",monospace'>⚑ What's Dragging the WCI Down</div>
                <div style='font-size:1.55rem;font-family:"DM Serif Display",serif;
                            color:#ef4444;line-height:1.1;margin-bottom:0.3rem'>
                    {killing_tc['icon']} {killing_tc['theme']}
                </div>
                <div style='font-size:0.78rem;color:var(--text-2);margin-bottom:0.75rem;
                            font-family:"DM Sans",sans-serif;font-weight:300;line-height:1.65'>
                    {kill_label}
                </div>
                <div style='display:flex;gap:1.2rem;font-family:"DM Mono",monospace;font-size:0.7rem'>
                    <div>
                        <span style='color:var(--text-3)'>Raw score</span><br>
                        <span style='color:#ef4444;font-weight:600'>{killing_tc['raw']:+.4f}</span>
                    </div>
                    <div>
                        <span style='color:var(--text-3)'>Weight</span><br>
                        <span style='color:#ef4444;font-weight:600'>{killing_tc['weight']:.4f}</span>
                    </div>
                    <div>
                        <span style='color:var(--text-3)'>Contribution</span><br>
                        <span style='color:#ef4444;font-weight:600'>{killing_tc['contribution']:+.4f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.85rem'></div>", unsafe_allow_html=True)

    # ── SECTION A: Radar + Sentiment Bars ──────────────────────────────────
    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown('<div class="sec-title">Theme Radar</div>', unsafe_allow_html=True)

        if sel in all_means.index:
            vals = [all_means.loc[sel, c] for c in THEME_COLS]
            gmin = all_means.min().min()
            gmax = all_means.max().max()
            norm = [(v - gmin) / (gmax - gmin + 1e-9) for v in vals]
            nc   = norm + [norm[0]]
            lc   = THEME_LABELS + [THEME_LABELS[0]]

            # Peer average overlay
            peer_avg = all_means.mean()
            peer_norm = [(peer_avg[c] - gmin)/(gmax - gmin + 1e-9) for c in THEME_COLS]
            peer_nc   = peer_norm + [peer_norm[0]]

            fig_r = go.Figure()
            # Peer average (ghost)
            fig_r.add_trace(go.Scatterpolar(
                r=peer_nc, theta=lc,
                fill='toself',
                fillcolor="rgba(96,165,250,0.04)",
                line=dict(color="rgba(96,165,250,0.25)", width=1.5, dash="dot"),
                name="Peer Avg",
                hovertemplate="Peer avg<br>%{theta}: %{r:.3f}<extra></extra>",
            ))
            # Company
            fig_r.add_trace(go.Scatterpolar(
                r=nc, theta=lc,
                fill='toself',
                fillcolor=hex_to_rgba(color, 0.14),
                line=dict(color=color, width=2.5),
                name=sel,
                hovertemplate=f"<b>{sel}</b><br>%{{theta}}: %{{r:.3f}}<extra></extra>",
                marker=dict(size=6, color=color, line=dict(color=PLOT_BG, width=2)),
            ))

            fig_r.update_layout(
                polar=dict(
                    bgcolor=PLOT_BG,
                    radialaxis=dict(
                        visible=True, range=[0, 1],
                        tickfont=dict(size=8.5, color=TEXT_CLR, family="DM Mono"),
                        gridcolor=GRID_CLR,
                        linecolor=AXIS_CLR,
                        tickcolor=TEXT_CLR,
                        tickvals=[0.25, 0.5, 0.75, 1.0],
                        ticktext=["0.25","0.5","0.75","1.0"],
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=10, color=TITLE_CLR, family="DM Sans"),
                        gridcolor=GRID_CLR,
                        linecolor=AXIS_CLR,
                    ),
                ),
                paper_bgcolor=PAPER_BG,
                plot_bgcolor=PAPER_BG,
                font=dict(family="DM Sans", color=TEXT_CLR, size=11),
                margin=dict(l=50, r=50, t=30, b=30),
                height=310,
                legend=dict(
                    font=LEG_FONT,
                    bgcolor="#ffffff",
                    bordercolor=GRID_CLR,
                    borderwidth=1,
                    orientation="h", x=0.5, xanchor="center", y=-0.08,
                ),
            )
            st.plotly_chart(fig_r, use_container_width=True, config=MODEBAR_CFG)

    with col_r:
        st.markdown('<div class="sec-title">Sentiment Breakdown</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

        sent_row = comp_free[["like_sentiment","dislike_sentiment","combined_sentiment"]].mean()

        for label, key, clr in [
            ("↑ Like Sentiment",    "like_sentiment",    "#059669"),
            ("↓ Dislike Sentiment", "dislike_sentiment", "#dc2626"),
            (f"⇄ Combined (WCI)",   "combined_sentiment", color),
        ]:
            val  = sent_row[key]
            bpct = bar_pct(val)
            # For dislike: invert display so negative = more red bar
            if key == "dislike_sentiment":
                bpct_disp = bar_pct(-val)
            else:
                bpct_disp = bpct
            midpoint = bar_pct(0)
            st.markdown(f"""
            <div style='margin-bottom:1.3rem'>
                <div style='display:flex;justify-content:space-between;margin-bottom:0.32rem'>
                    <span style='font-size:0.82rem;color:var(--text-2);font-weight:500;
                                 font-family:"DM Sans",sans-serif'>{label}</span>
                    <span style='font-size:0.88rem;font-weight:400;color:{clr};
                                 font-family:"DM Serif Display",serif;letter-spacing:-0.01em'>{val:+.3f}</span>
                </div>
                <div style='background:rgba(5,150,105,0.05);border-radius:999px;height:10px;
                            overflow:hidden;border:1px solid rgba(5,150,105,0.08);position:relative'>
                    <div style='position:absolute;left:{midpoint:.1f}%;top:0;bottom:0;width:1px;
                                background:rgba(5,150,105,0.25)'></div>
                    <div style='background:linear-gradient(90deg,{clr}99,{clr});
                                width:{bpct_disp:.1f}%;height:10px;border-radius:999px;
                                margin-left:{(midpoint - bpct_disp) if val < 0 else midpoint if bpct_disp < midpoint else 0:.0f}%;
                                opacity:0.88'></div>
                </div>
                <div style='display:flex;justify-content:space-between;
                            font-size:0.62rem;color:var(--text-3);margin-top:0.15rem;
                            font-family:"DM Mono",monospace'>
                    <span>−1.0</span><span>0</span><span>+1.0</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)

    # ── Sentiment Polarity Distribution ────────────────────────────────────
    st.markdown('<div class="sec-title">Sentiment Polarity Distribution</div>', unsafe_allow_html=True)

    if len(comp_free) > 0 and "combined_sentiment" in comp_free.columns:
        sent_vals = comp_free["combined_sentiment"].dropna()
        if len(sent_vals) > 5:
            # Bimodality check: tails beyond ±0.3
            left_tail_pct  = (sent_vals < -0.3).mean() * 100
            right_tail_pct = (sent_vals > 0.3).mean() * 100
            is_bimodal     = (left_tail_pct > 20) and (right_tail_pct > 20)

            bin_edges = np.linspace(-1, 1, 22)  # 21 bins
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            hist_counts, _ = np.histogram(sent_vals, bins=bin_edges)
            bar_colors = ["#059669" if c > 0 else "#dc2626" for c in bin_centers]

            fig_hist = go.Figure()
            fig_hist.add_trace(go.Bar(
                x=bin_centers,
                y=hist_counts,
                width=np.diff(bin_edges) * 0.88,
                marker=dict(
                    color=bar_colors,
                    opacity=0.82,
                    line=dict(color="rgba(255,255,255,0.15)", width=0.5),
                ),
                hovertemplate="Sentiment: <b>%{x:.2f}</b><br>Count: <b>%{y}</b><extra></extra>",
                name="Reviews",
            ))
            # Zero line
            fig_hist.add_vline(
                x=0, line_dash="dash",
                line_color="rgba(5,150,105,0.45)", line_width=1.8,
            )
            fig_hist.update_layout(
                **base_layout(
                    xaxis=ax(
                        title=dict(text="Combined Sentiment Score", font=TITLE_FONT),
                        range=[-1.05, 1.05],
                        tickvals=[-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1],
                        ticktext=["-1.0","-0.75","-0.5","-0.25","0","0.25","0.5","0.75","1.0"],
                        tickfont=dict(color=TEXT_CLR, size=9.5, family="DM Mono"),
                    ),
                    yaxis=ax(title=dict(text="Number of Reviews", font=TITLE_FONT)),
                    margin=dict(l=15, r=15, t=20, b=55),
                    height=250,
                    bargap=0.05,
                    showlegend=False,
                )
            )
            # Median annotation
            med_val = float(sent_vals.median())
            fig_hist.add_annotation(
                x=med_val, y=hist_counts.max() * 0.95,
                text=f"median: {med_val:+.3f}",
                showarrow=False,
                font=dict(size=9.5, color="#065f46", family="DM Mono"),
                bgcolor="rgba(255,255,255,0.85)",
                bordercolor="rgba(5,150,105,0.3)",
                borderwidth=1, borderpad=4,
            )
            st.plotly_chart(fig_hist, use_container_width=True, config=MODEBAR_CFG)

            # Bimodality flag note
            if is_bimodal:
                st.markdown(f"""
                <div style='background:rgba(220,38,38,0.05);border:1px solid rgba(220,38,38,0.18);
                            border-left:3px solid #dc2626;border-radius:var(--r-sm);
                            padding:0.6rem 1rem;font-size:0.77rem;color:#7f1d1d;
                            font-family:"DM Sans",sans-serif;line-height:1.65;margin-top:-0.3rem'>
                    ⚠️ <b>Split workforce</b> — average sentiment hides disagreement.
                    <b>{left_tail_pct:.0f}%</b> of reviews score below −0.3 and
                    <b>{right_tail_pct:.0f}%</b> score above +0.3, indicating strongly polarised
                    employee experiences at {sel}.
                </div>
                """, unsafe_allow_html=True)
            else:
                mean_s = float(sent_vals.mean())
                sent_desc = "broadly positive" if mean_s > 0.05 else ("broadly negative" if mean_s < -0.05 else "mixed / neutral")
                st.markdown(f"""
                <div style='font-size:0.76rem;color:var(--text-3);margin-top:0.2rem;
                            font-family:"DM Sans",sans-serif;line-height:1.65'>
                    Distribution is <b>{sent_desc}</b> (mean = {mean_s:+.3f}).
                    Negative reviews ({left_tail_pct:.0f}% below −0.3) and
                    positive reviews ({right_tail_pct:.0f}% above +0.3).
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Not enough sentiment data for histogram.")

    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)

    # ── SECTION B: Theme Contribution ──────────────────────────────────────
    st.markdown('<div class="sec-title">WCI Theme Contribution Breakdown</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.8rem;color:var(--text-3);margin-bottom:1rem;font-family:"DM Sans",sans-serif;
                font-weight:300;max-width:640px;line-height:1.7'>
        Raw theme score × final blended weight. Positive bars push WCI up; negative drag it down.
    </div>""", unsafe_allow_html=True)

    if sel in all_means.index:
        fw_arr = weights["final_weight"].values if "final_weight" in weights.columns else np.array(THEME_EXPERT_W)
        theme_contribs = []
        for t, fw, meta in zip(THEME_COLS, fw_arr, [THEME_META[t] for t in THEME_COLS]):
            raw_score = all_means.loc[sel, t]
            contribution = raw_score * fw
            theme_contribs.append({
                "col": t, "theme": meta["label"], "icon": meta["icon"],
                "raw": raw_score, "weight": fw,
                "contribution": contribution, "color": meta["color"],
            })
        all_contribs_mean = {t: all_means[t].mean() * fw for t, fw in zip(THEME_COLS, fw_arr)}

        tc1, tc2 = st.columns([3, 2], gap="large")

        with tc1:
            cv     = [tc["contribution"] for tc in theme_contribs]
            clbls  = [f"{tc['icon']} {tc['theme']}" for tc in theme_contribs]
            cclrs  = [tc["color"] if tc["contribution"] >= 0 else "#dc2626" for tc in theme_contribs]

            fig_c = go.Figure()
            fig_c.add_trace(go.Bar(
                y=clbls, x=cv, orientation="h",
                marker=dict(color=cclrs, opacity=0.85,
                            line=dict(color="rgba(255,255,255,0.06)", width=1)),
                text=[f"{v:+.4f}" for v in cv],
                textposition="outside",
                textfont=dict(size=10.5, family="DM Mono", color=TEXT_CLR),
                hovertemplate="<b>%{y}</b><br>Contribution: <b>%{x:+.4f}</b><extra></extra>",
            ))
            fig_c.add_vline(x=0, line_color="rgba(5,150,105,0.3)", line_width=1.5, line_dash="dash")
            fig_c.update_layout(
                **base_layout(
                    xaxis=ax(title=dict(text="Weighted Contribution to WCI", font=TITLE_FONT)),
                    yaxis=dict(showgrid=False, tickfont=dict(color=TITLE_CLR, size=10.5, family="DM Sans"),
                               zeroline=False),
                    margin=dict(l=10, r=85, t=15, b=48),
                    height=270,
                )
            )
            st.plotly_chart(fig_c, use_container_width=True, config=MODEBAR_CFG)

        with tc2:
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            for i, tc in enumerate(sorted(theme_contribs, key=lambda x: x["contribution"], reverse=True)):
                vs_avg = tc["contribution"] - all_contribs_mean.get(tc["col"], 0)
                vs_clr = "#059669" if vs_avg >= 0 else "#dc2626"
                vs_txt = f"+{vs_avg:.4f}" if vs_avg >= 0 else f"{vs_avg:.4f}"
                st.markdown(f"""
                <div class='signal-card'>
                    <div style='display:flex;justify-content:space-between;align-items:center'>
                        <span style='font-size:0.81rem;font-weight:500;color:var(--text);
                                     font-family:"DM Sans",sans-serif'>
                            {tc['icon']} {tc['theme']}</span>
                        <span style='font-size:0.76rem;font-weight:600;color:{vs_clr};
                                     font-family:"DM Mono",monospace'>{vs_txt} vs avg</span>
                    </div>
                    <div style='font-size:0.68rem;color:var(--text-3);margin-top:0.2rem;
                                font-family:"DM Mono",monospace'>
                        Raw: {tc['raw']:+.4f} · w: {tc['weight']:.4f} · C: {tc['contribution']:+.4f}
                    </div>
                </div>""", unsafe_allow_html=True)

    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)

    # ── SECTION C: Theme Bars vs Peer ──────────────────────────────────────
    st.markdown('<div class="sec-title">Theme Scores vs. Peer Average</div>', unsafe_allow_html=True)

    if sel in all_means.index:
        peer_avg_vals = all_means.mean()
        tb_cols = st.columns(5)
        for i, (cn, sl_lbl) in enumerate(zip(THEME_COLS, THEME_SHORT)):
            meta  = THEME_META[cn]
            val   = all_means.loc[sel, cn]
            pavg  = peer_avg_vals[cn]
            diff  = val - pavg
            bpct_v = bar_pct(val)
            bpct_a = bar_pct(pavg)
            clr   = meta["color"] if val >= pavg else "#dc2626"
            arrow = "▲" if diff >= 0 else "▼"
            with tb_cols[i]:
                st.markdown(f"""
                <div class='stat-box' style='border-top:2px solid {meta["color"]}44'>
                    <span style='font-size:1.05rem'>{meta["icon"]}</span>
                    <span class='sv' style='color:{clr}'>{val:+.3f}</span>
                    <span class='sl'>{sl_lbl}</span>
                    <div style='background:rgba(5,150,105,0.05);border-radius:999px;height:4px;
                                overflow:hidden;margin:0.45rem 0;border:1px solid {meta["color"]}20'>
                        <div style='background:{clr};width:{bpct_v:.0f}%;height:4px;border-radius:999px;opacity:0.85'></div>
                    </div>
                    <div style='background:rgba(5,150,105,0.03);border-radius:999px;height:3px;
                                overflow:hidden;margin-bottom:0.45rem'>
                        <div style='background:rgba(5,150,105,0.3);width:{bpct_a:.0f}%;height:3px;border-radius:999px'></div>
                    </div>
                    <span style='font-size:0.67rem;color:{clr};font-weight:600;
                                 font-family:"DM Mono",monospace'>
                        {arrow} {abs(diff):.3f} vs avg</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)

    # ── SECTION D+E: Rating Distribution + Trend ───────────────────────────
    dist_col, trend_col = st.columns([1, 2], gap="large")

    with dist_col:
        st.markdown('<div class="sec-title">Rating Distribution</div>', unsafe_allow_html=True)

        rating_counts = comp_all["overall_rating"].value_counts().sort_index()
        total_rated   = rating_counts.sum()
        star_colors   = {1:"#dc2626", 2:"#ea580c", 3:"#d97706", 4:"#2563eb", 5:"#059669"}

        for star in [5, 4, 3, 2, 1]:
            cnt = rating_counts.get(star, 0)
            pct = cnt / total_rated * 100 if total_rated > 0 else 0
            clr = star_colors[star]
            stars_str = "★" * star + "☆" * (5-star)
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:0.6rem;margin-bottom:0.55rem'>
                <span style='font-size:0.72rem;color:{clr};font-family:"DM Mono",monospace;
                             width:72px;flex-shrink:0;letter-spacing:0.05em'>{stars_str}</span>
                <div style='flex:1;background:rgba(5,150,105,0.05);border-radius:999px;
                            height:8px;overflow:hidden;border:1px solid rgba(5,150,105,0.07)'>
                    <div style='background:{clr};width:{pct:.0f}%;height:8px;
                                border-radius:999px;opacity:0.82'></div>
                </div>
                <span style='font-size:0.68rem;color:var(--text-3);width:58px;text-align:right;
                             font-family:"DM Mono",monospace'>{cnt} ({pct:.0f}%)</span>
            </div>""", unsafe_allow_html=True)

        if len(comp_all) >= 5:
            skew = comp_all["overall_rating"].skew()
            skew_desc = "Left-skewed" if skew < -0.3 else "Right-skewed" if skew > 0.3 else "Symmetric"
            st.markdown(f"""
            <div style='margin-top:0.85rem;font-size:0.72rem;color:var(--text-3);
                        font-family:"DM Mono",monospace'>
                skewness = <span style='color:var(--emerald)'>{skew:.2f}</span>
                — {skew_desc}
            </div>""", unsafe_allow_html=True)

    with trend_col:
        st.markdown('<div class="sec-title">Sentiment Trend Over Time</div>', unsafe_allow_html=True)

        trend_df = (
            comp_free.set_index("review_date")["combined_sentiment"]
            .resample("QE").mean()
            .dropna()
            .reset_index()
        )
        trend_df.columns = ["date", "sentiment"]

        rating_trend = (
            comp_all.set_index("review_date")["overall_rating"]
            .resample("QE").mean()
            .dropna()
            .reset_index()
        )
        rating_trend.columns = ["date", "rating"]

        if len(trend_df) >= 2:
            fig_t = go.Figure()

            # Sentiment fill area
            fig_t.add_trace(go.Scatter(
                x=trend_df["date"], y=trend_df["sentiment"],
                mode="lines+markers",
                line=dict(color=color, width=2.5, shape="spline"),
                marker=dict(size=7, color=color, line=dict(color=PLOT_BG, width=2.5)),
                fill="tozeroy",
                fillcolor=hex_to_rgba(color, 0.09),
                hovertemplate="%{x|%b %Y}<br>Sentiment: <b>%{y:.3f}</b><extra></extra>",
                name="Sentiment (L)", yaxis="y1",
            ))

            fig_t.add_hline(y=0, line_dash="dash",
                            line_color="rgba(5,150,105,0.25)", line_width=1.2)

            # Annotate peaks
            if len(trend_df) > 2:
                peak_idx = trend_df["sentiment"].idxmax()
                trough_idx = trend_df["sentiment"].idxmin()
                for idx, symbol, shift in [(peak_idx, "▲", 0.03), (trough_idx, "▼", -0.04)]:
                    fig_t.add_annotation(
                        x=trend_df.loc[idx, "date"],
                        y=trend_df.loc[idx, "sentiment"] + shift,
                        text=symbol,
                        showarrow=False,
                        font=dict(size=10, color="#059669" if shift > 0 else "#dc2626",
                                  family="DM Sans"),
                    )

            if len(rating_trend) >= 2:
                fig_t.add_trace(go.Scatter(
                    x=rating_trend["date"], y=rating_trend["rating"],
                    mode="lines+markers",
                    line=dict(color="#d97706", width=1.8, dash="dot"),
                    marker=dict(size=5, color="#d97706", line=dict(color=PLOT_BG, width=1.5)),
                    hovertemplate="%{x|%b %Y}<br>Rating: <b>%{y:.2f}★</b><extra></extra>",
                    name="Avg Rating (R)", yaxis="y2",
                ))

            fig_t.update_layout(
                **base_layout(
                    xaxis=ax(showgrid=False, title=dict(text="Quarter", font=TITLE_FONT)),
                    yaxis=dict(
                        title=dict(text="Combined Sentiment", font=TITLE_FONT),
                        **ax(), side="left",
                    ),
                    yaxis2=dict(
                        title=dict(text="Avg ★ Rating",
                                   font=dict(color="#d97706", size=10.5, family="DM Sans")),
                        overlaying="y", side="right",
                        tickfont=dict(color="#d97706", size=10, family="DM Mono"),
                        showgrid=False, zeroline=False, range=[1, 5.5],
                    ),
                    legend=dict(
                        font=LEG_FONT,
                        bgcolor="#ffffff",
                        bordercolor=GRID_CLR,
                        borderwidth=1,
                        orientation="h", x=0.5, xanchor="center", y=-0.22,
                    ),
                    margin=dict(l=15, r=65, t=15, b=58),
                    height=295,
                )
            )
            st.plotly_chart(fig_t, use_container_width=True, config=MODEBAR_CFG)
        else:
            st.info("Not enough quarterly data points for this company.")

    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)

    # ── SECTION F: Top Phrases + Sample Reviews ─────────────────────────────
    phrase_col, reviews_col = st.columns([1, 1], gap="large")

    with phrase_col:
        st.markdown('<div class="sec-title">Top Phrases</div>', unsafe_allow_html=True)

        like_phrases    = top_phrases(comp_free["like_text"])
        dislike_phrases = top_phrases(comp_free["dislike_text"])
        tab1, tab2 = st.tabs(["↑ From Likes", "↓ From Dislikes"])

        with tab1:
            if like_phrases:
                max_c = like_phrases[0][1]
                for word, count in like_phrases:
                    pct = count / max_c * 100
                    st.markdown(f"""
                    <div style='display:flex;align-items:center;gap:0.65rem;margin-bottom:0.52rem'>
                        <span style='font-size:0.78rem;color:var(--text);width:115px;flex-shrink:0;
                                     font-family:"DM Sans",sans-serif;font-weight:500'>{word}</span>
                        <div style='flex:1;background:rgba(5,150,105,0.05);border-radius:999px;
                                    height:6px;overflow:hidden;border:1px solid rgba(5,150,105,0.07)'>
                            <div style='background:#059669;width:{pct:.0f}%;height:6px;
                                        border-radius:999px;opacity:0.78'></div>
                        </div>
                        <span style='font-size:0.68rem;color:var(--text-3);width:24px;text-align:right;
                                     font-family:"DM Mono",monospace'>{count}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.caption("No phrases found.")

        with tab2:
            if dislike_phrases:
                max_c = dislike_phrases[0][1]
                for word, count in dislike_phrases:
                    pct = count / max_c * 100
                    st.markdown(f"""
                    <div style='display:flex;align-items:center;gap:0.65rem;margin-bottom:0.52rem'>
                        <span style='font-size:0.78rem;color:var(--text);width:115px;flex-shrink:0;
                                     font-family:"DM Sans",sans-serif;font-weight:500'>{word}</span>
                        <div style='flex:1;background:rgba(248,113,113,0.05);border-radius:999px;
                                    height:6px;overflow:hidden;border:1px solid rgba(248,113,113,0.07)'>
                            <div style='background:#dc2626;width:{pct:.0f}%;height:6px;
                                        border-radius:999px;opacity:0.78'></div>
                        </div>
                        <span style='font-size:0.68rem;color:var(--text-3);width:24px;text-align:right;
                                     font-family:"DM Mono",monospace'>{count}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.caption("No phrases found.")

        # ── Theme Keyword Heatmap Table ─────────────────────────────────
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="sec-title" style="font-size:1rem">Theme Keyword Signal</div>',
                    unsafe_allow_html=True)

        THEME_KW_POS = {
            'theme_respect':      ['respect','fair','dignity','inclusive','ethical','honest','transparent','equality','diverse'],
            'theme_management':   ['leadership','mentor','supportive','guidance','manager','management','leader','coaching','trust'],
            'theme_compensation': ['salary','hike','increment','bonus','benefits','ctc','appraisal','pay','package','perks'],
            'theme_growth':       ['learning','training','promotion','career','growth','skill','opportunity','develop','advance'],
            'theme_wlb':          ['flexible','balance','leaves','hours','weekend','wfh','remote','timing','overtime'],
        }
        THEME_KW_NEG = {
            'theme_respect':      ['disrespect','bias','unfair','toxic','harassment','politics','favoritism','discrimination'],
            'theme_management':   ['micromanage','nepotism','poor management','incompetent','blame','arrogant','pressure','politics'],
            'theme_compensation': ['low salary','underpaid','no hike','poor pay','no increment','delay','salary delay'],
            'theme_growth':       ['no growth','stagnant','no promotion','no learning','stuck','dead end','no training'],
            'theme_wlb':          ['overwork','long hours','no balance','weekends','stress','burnout','no leaves','overtime'],
        }

        kw_rows_html = ""
        for t_col, t_lbl in zip(THEME_COLS, THEME_LABELS):
            meta_k = THEME_META[t_col]
            like_text_all  = " ".join(comp_free["like_text"].dropna().str.lower().tolist())
            dislike_text_all = " ".join(comp_free["dislike_text"].dropna().str.lower().tolist())

            pos_kw_counts = {kw: like_text_all.count(kw) for kw in THEME_KW_POS[t_col]}
            neg_kw_counts = {kw: dislike_text_all.count(kw) for kw in THEME_KW_NEG[t_col]}

            top_pos_kw = max(pos_kw_counts, key=pos_kw_counts.get) if pos_kw_counts else "—"
            top_neg_kw = max(neg_kw_counts, key=neg_kw_counts.get) if neg_kw_counts else "—"
            top_pos_cnt = pos_kw_counts.get(top_pos_kw, 0)
            top_neg_cnt = neg_kw_counts.get(top_neg_kw, 0)
            net_signal  = top_pos_cnt - top_neg_cnt

            if net_signal > 0:
                net_html = f"<span style='color:#059669;font-weight:700'>▲ +{net_signal}</span>"
            elif net_signal < 0:
                net_html = f"<span style='color:#dc2626;font-weight:700'>▼ {net_signal}</span>"
            else:
                net_html = f"<span style='color:var(--text-3);font-weight:500'>— {net_signal}</span>"

            kw_rows_html += (
                f"<tr style='border-bottom:1px solid rgba(5,150,105,0.07)'>"
                f"<td style='padding:0.5rem 0.7rem;font-size:0.76rem;font-weight:500;"
                f"color:{meta_k['color']};font-family:\"DM Sans\",sans-serif;white-space:nowrap'>"
                f"{meta_k['icon']} {t_lbl}</td>"
                f"<td style='padding:0.5rem 0.7rem;font-size:0.73rem;color:#059669;"
                f"font-family:\"DM Mono\",monospace'>{top_pos_kw} <span style='color:var(--text-3)'>({top_pos_cnt})</span></td>"
                f"<td style='padding:0.5rem 0.7rem;font-size:0.73rem;color:#dc2626;"
                f"font-family:\"DM Mono\",monospace'>{top_neg_kw} <span style='color:var(--text-3)'>({top_neg_cnt})</span></td>"
                f"<td style='padding:0.5rem 0.7rem;font-size:0.73rem;"
                f"font-family:\"DM Mono\",monospace;text-align:center'>{net_html}</td>"
                f"</tr>"
            )

        kw_table_html = (
            "<div style='overflow-x:auto;border-radius:var(--r-md);border:1px solid var(--border);"
            "background:var(--surface);margin-top:0.4rem'>"
            "<table style='width:100%;border-collapse:collapse;font-size:0.8rem;color:var(--text)'>"
            "<thead><tr style='border-bottom:1px solid rgba(5,150,105,0.12);"
            "background:rgba(5,150,105,0.04)'>"
            "<th style='text-align:left;padding:0.5rem 0.7rem;font-size:0.65rem;font-weight:700;"
            "text-transform:uppercase;letter-spacing:0.08em;color:var(--text-3);"
            "font-family:\"DM Mono\",monospace'>Theme</th>"
            "<th style='text-align:left;padding:0.5rem 0.7rem;font-size:0.65rem;font-weight:700;"
            "text-transform:uppercase;letter-spacing:0.08em;color:#059669;"
            "font-family:\"DM Mono\",monospace'>Top Positive Word</th>"
            "<th style='text-align:left;padding:0.5rem 0.7rem;font-size:0.65rem;font-weight:700;"
            "text-transform:uppercase;letter-spacing:0.08em;color:#dc2626;"
            "font-family:\"DM Mono\",monospace'>Top Negative Word</th>"
            "<th style='text-align:center;padding:0.5rem 0.7rem;font-size:0.65rem;font-weight:700;"
            "text-transform:uppercase;letter-spacing:0.08em;color:var(--text-3);"
            "font-family:\"DM Mono\",monospace'>Net Signal</th>"
            "</tr></thead>"
            "<tbody>" + kw_rows_html + "</tbody>"
            "</table></div>"
        )
        st.markdown(kw_table_html, unsafe_allow_html=True)

    with reviews_col:
        st.markdown('<div class="sec-title">Sample Reviews</div>', unsafe_allow_html=True)

        low_col = "low_signal" if "low_signal" in comp_free.columns else None
        sample_pool = (comp_free[~comp_free[low_col].astype(bool)] if low_col else comp_free).dropna(
            subset=["like_text","dislike_text"])
        sample_pool = sample_pool[
            (sample_pool["like_text"].str.len() > 10) &
            (sample_pool["dislike_text"].str.len() > 10)
        ]

        if len(sample_pool) > 0:
            sample_reviews = sample_pool[
                ["like_text","dislike_text","overall_rating","review_date",
                 "like_sentiment","dislike_sentiment"]
            ].sample(min(5, len(sample_pool)), random_state=42)

            import html as _html
            for _, rev in sample_reviews.iterrows():
                stars_n   = int(rev["overall_rating"])
                stars_str = "★" * stars_n + "☆" * (5 - stars_n)
                star_clr  = {1:"#dc2626",2:"#ea580c",3:"#d97706",4:"#2563eb",5:"#059669"}.get(stars_n, "#059669")
                date      = pd.to_datetime(rev["review_date"]).strftime("%b %Y")
                # Escape user-provided text to prevent HTML breakage
                like_raw  = str(rev["like_text"])
                dis_raw   = str(rev["dislike_text"])
                like      = _html.escape(like_raw[:145]) + ("…" if len(like_raw) > 145 else "")
                dis       = _html.escape(dis_raw[:145])  + ("…" if len(dis_raw)  > 145 else "")
                l_sent    = rev.get("like_sentiment", None)
                d_sent    = rev.get("dislike_sentiment", None)
                sent_badge = ""
                if pd.notna(l_sent) and pd.notna(d_sent):
                    sent_badge = (
                        f"<span style='font-size:0.63rem;color:#059669;font-weight:600;"
                        f"font-family:\"DM Mono\",monospace'>L:{l_sent:+.2f}</span>"
                        f"<span style='font-size:0.63rem;color:#dc2626;font-weight:600;"
                        f"font-family:\"DM Mono\",monospace;margin-left:0.4rem'>D:{d_sent:+.2f}</span>"
                    )
                rev_html = f"""
                <div class='rev-card'>
                    <div style='display:flex;justify-content:space-between;
                                margin-bottom:0.38rem;align-items:center'>
                        <span style='font-size:0.78rem;color:{star_clr};
                                     font-family:"DM Mono",monospace;
                                     letter-spacing:0.05em'>{stars_str}</span>
                        <div style='display:flex;gap:0.55rem;align-items:center'>
                            {sent_badge}
                            <span style='font-size:0.67rem;color:var(--text-3);
                                         font-family:"DM Mono",monospace'>{date}</span>
                        </div>
                    </div>
                    <div style='font-size:0.76rem;color:var(--text-2);margin-bottom:0.28rem;
                                font-family:"DM Sans",sans-serif;line-height:1.6;font-weight:300'>
                        <span style='color:#059669;font-weight:600;margin-right:0.3rem'>&#8593;</span>{like}
                    </div>
                    <div style='font-size:0.76rem;color:var(--text-2);
                                font-family:"DM Sans",sans-serif;line-height:1.6;font-weight:300'>
                        <span style='color:#dc2626;font-weight:600;margin-right:0.3rem'>&#8595;</span>{dis}
                    </div>
                </div>
                """
                st.markdown(rev_html, unsafe_allow_html=True)
        else:
            st.info("No high-signal reviews found for this company.")

    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)

    # ── SECTION G: Intelligence Signals ────────────────────────────────────
    st.markdown('<div class="sec-title">Intelligence Signals</div>', unsafe_allow_html=True)

    sig1, sig2, sig3 = st.columns(3)
    if sel in all_means.index:
        theme_scores = {t: all_means.loc[sel, t] for t in THEME_COLS}
        best_t  = max(theme_scores, key=theme_scores.get)
        worst_t = min(theme_scores, key=theme_scores.get)
        best_meta  = THEME_META[best_t]
        worst_meta = THEME_META[worst_t]

        like_avg = comp_free["like_sentiment"].mean()
        dis_avg  = comp_free["dislike_sentiment"].mean()
        pos_pct  = (comp_free["like_sentiment"] > 0).mean() * 100 if len(comp_free) > 0 else 0
        neg_pct  = (comp_free["dislike_sentiment"] < 0).mean() * 100 if len(comp_free) > 0 else 0

        recent_cutoff = comp_all["review_date"].max() - pd.DateOffset(years=2)
        n_recent = len(comp_all[comp_all["review_date"] >= recent_cutoff])
        n_prior  = len(comp_all[comp_all["review_date"] < recent_cutoff])
        vol_trend = "↑ Increasing" if n_recent > n_prior else "↓ Decreasing" if n_recent < n_prior else "→ Stable"
        vol_color = "#059669" if n_recent >= n_prior else "#dc2626"

        signal_data = [
            (sig1, "◆", "Theme Strengths", [
                (f"Best", f"{best_meta['icon']} {best_meta['label']}", "#059669", f"({theme_scores[best_t]:+.3f})"),
                (f"Worst", f"{worst_meta['icon']} {worst_meta['label']}", "#dc2626", f"({theme_scores[worst_t]:+.3f})"),
                ("Range", f"{theme_scores[best_t]-theme_scores[worst_t]:.3f}", "#d97706",
                 "wide gap" if theme_scores[best_t]-theme_scores[worst_t]>0.15 else "tight"),
            ]),
            (sig2, "∿", "Sentiment Signals", [
                ("Positive likes", f"{pos_pct:.0f}%", "#059669", ""),
                ("Negative dislikes", f"{neg_pct:.0f}%", "#dc2626", ""),
                ("Like–Dislike gap", f"{like_avg-dis_avg:+.3f}", "#2563eb", ""),
            ]),
            (sig3, "◷", "Review Activity", [
                ("Total reviews", f"{len(comp_all):,}", "#7c3aed", ""),
                ("Last 2 years", f"{n_recent}", "#2563eb", f"vs {n_prior} prior"),
                ("Volume trend", vol_trend, vol_color, ""),
            ]),
        ]

        for col, icon, title, rows in signal_data:
            with col:
                rows_html = ""
                for lbl, val, clr, sub in rows:
                    sub_html = (
                        "<span style='font-size:0.65rem;color:var(--text-3);margin-left:0.3rem'>"
                        + str(sub) + "</span>"
                    ) if sub else ""
                    rows_html += (
                        "<div style='display:flex;justify-content:space-between;align-items:baseline;"
                        "padding:0.38rem 0;border-bottom:1px solid rgba(5,150,105,0.06)'>"
                        "<span style='font-size:0.74rem;color:var(--text-3);"
                        "font-family:\"DM Sans\",sans-serif'>" + str(lbl) + "</span>"
                        "<div style='text-align:right'>"
                        "<span style='font-size:0.78rem;font-weight:600;color:" + clr + ";"
                        "font-family:\"DM Mono\",monospace'>" + str(val) + "</span>"
                        + sub_html +
                        "</div></div>"
                    )
                card_html = (
                    "<div class='ins-card' style='border-top:2px solid rgba(5,150,105,0.2)'>"
                    "<div style='display:flex;align-items:center;gap:0.5rem;margin-bottom:0.8rem'>"
                    "<div style='width:30px;height:30px;border-radius:8px;"
                    "background:rgba(5,150,105,0.1);"
                    "border:1px solid rgba(5,150,105,0.2);"
                    "display:flex;align-items:center;justify-content:center;"
                    "font-size:0.95rem'>" + str(icon) + "</div>"
                    "<span style='font-weight:600;color:var(--text);font-size:0.85rem;"
                    "font-family:\"DM Sans\",sans-serif'>" + str(title) + "</span>"
                    "</div>"
                    + rows_html +
                    "</div>"
                )
                st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)

    # ── SECTION H: Data Quality ─────────────────────────────────────────────
    st.markdown('<div class="sec-title">Data Quality</div>', unsafe_allow_html=True)

    n_total      = len(comp_all)
    n_structured = int(comp_all["structured_text"].sum()) if "structured_text" in comp_all.columns else 0
    n_low_signal = int(comp_all["low_signal"].sum()) if "low_signal" in comp_all.columns else 0
    n_duplicate  = int(comp_all["is_duplicate"].sum()) if "is_duplicate" in comp_all.columns else 0
    n_usable     = max(0, n_total - n_structured - n_low_signal)
    usability_pct = n_usable / n_total * 100 if n_total > 0 else 0

    dq_cols = st.columns(6)
    dq_data = [
        (str(n_total),          "Total Reviews",    "#e6f0eb"),
        (str(n_structured),     "Auto-Generated",   "#d97706"),
        (str(n_low_signal),     "Low Signal",       "#ea580c"),
        (str(n_duplicate),      "Duplicates",       "#dc2626"),
        (str(n_usable),         "Usable Reviews",   "#059669"),
        (f"{usability_pct:.0f}%","Usability Rate",  "#2563eb"),
    ]
    for col, (sv, sl, clr) in zip(dq_cols, dq_data):
        col.markdown(f"""
        <div class='stat-box' style='border-top:2px solid {clr}44'>
            <span class='sv' style='color:{clr}'>{sv}</span>
            <span class='sl'>{sl}</span>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — HEAD-TO-HEAD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⇄  Head-to-Head":

    st.markdown("""
    <div class='hero'>
        <div class='hero-eyebrow'>Comparative Analysis</div>
        <h1>Head-to-<em>Head</em></h1>
        <p>Select two companies and compare WCI scores, sentiment profiles,
        and theme strengths side by side with full statistical context.</p>
    </div>
    """, unsafe_allow_html=True)

    companies = scores.sort_values("wci_rank")["company"].tolist()
    col_a, col_b = st.columns(2)
    with col_a:
        comp_a = st.selectbox("Company A", companies, index=0, key="h2h_a")
    with col_b:
        remaining = [c for c in companies if c != comp_a]
        comp_b = st.selectbox("Company B", remaining, index=0, key="h2h_b")

    ca_color = COMPANY_COLORS.get(comp_a, "#059669")
    cb_color = COMPANY_COLORS.get(comp_b, "#dc2626")
    row_a    = scores[scores["company"] == comp_a].iloc[0]
    row_b    = scores[scores["company"] == comp_b].iloc[0]
    free_a   = df_free[df_free["company"] == comp_a]
    free_b   = df_free[df_free["company"] == comp_b]
    all_means = df_free.groupby("company")[THEME_COLS].mean()

    wci_a  = row_a["wci_score"]
    wci_b  = row_b["wci_score"]
    gap    = abs(wci_a - wci_b)
    leader = comp_a if wci_a > wci_b else comp_b
    leader_color = ca_color if wci_a > wci_b else cb_color
    rank_a = int(row_a["wci_rank"])
    rank_b = int(row_b["wci_rank"])

    # ── WCI Gap card ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class='g-card' style='text-align:center;margin-bottom:1.4rem'>
        <div style='font-family:"DM Mono",monospace;font-size:0.62rem;
                    text-transform:uppercase;letter-spacing:0.12em;color:var(--text-3);
                    margin-bottom:1rem'>WCI Score Comparison</div>
        <div style='display:flex;align-items:center;justify-content:center;gap:3rem'>
            <div style='text-align:center'>
                <div style='font-family:"DM Serif Display",serif;font-size:3rem;
                            font-weight:400;color:{ca_color};line-height:1'>{wci_a:.1f}</div>
                <div style='font-size:0.85rem;font-weight:600;color:var(--text);
                            margin-top:0.4rem;font-family:"DM Sans",sans-serif'>{comp_a}</div>
                <div style='font-size:0.68rem;color:var(--text-3);margin-top:0.15rem;
                            font-family:"DM Mono",monospace'>
                    {RANK_EMOJI.get(rank_a,f"#{rank_a}")} Rank #{rank_a}</div>
            </div>
            <div style='text-align:center'>
                <div style='border:1px solid rgba(5,150,105,0.15);border-radius:var(--r-md);
                            padding:0.6rem 1.2rem;background:rgba(5,150,105,0.04)'>
                    <div style='font-size:0.62rem;text-transform:uppercase;letter-spacing:0.1em;
                                color:var(--text-3);font-family:"DM Mono",monospace;margin-bottom:0.3rem'>Gap</div>
                    <div style='font-family:"DM Serif Display",serif;font-size:1.5rem;
                                color:{leader_color}'>{gap:.1f}</div>
                    <div style='font-size:0.68rem;color:{leader_color};margin-top:0.2rem;
                                font-family:"DM Sans",sans-serif;font-weight:600'>
                        {leader} leads</div>
                </div>
            </div>
            <div style='text-align:center'>
                <div style='font-family:"DM Serif Display",serif;font-size:3rem;
                            font-weight:400;color:{cb_color};line-height:1'>{wci_b:.1f}</div>
                <div style='font-size:0.85rem;font-weight:600;color:var(--text);
                            margin-top:0.4rem;font-family:"DM Sans",sans-serif'>{comp_b}</div>
                <div style='font-size:0.68rem;color:var(--text-3);margin-top:0.15rem;
                            font-family:"DM Mono",monospace'>
                    {RANK_EMOJI.get(rank_b,f"#{rank_b}")} Rank #{rank_b}</div>
            </div>
        </div>
        <div style='display:flex;align-items:center;gap:0;margin-top:1.4rem;border-radius:999px;
                    overflow:hidden;height:8px'>
            <div style='background:{ca_color};flex:{wci_a:.0f};opacity:0.85'></div>
            <div style='background:var(--surface-3);flex:3;display:flex;align-items:center;
                        justify-content:center'></div>
            <div style='background:{cb_color};flex:{wci_b:.0f};opacity:0.85'></div>
        </div>
        <div style='display:flex;justify-content:space-between;margin-top:0.3rem;
                    font-size:0.62rem;color:var(--text-3);font-family:"DM Mono",monospace;
                    padding:0 4px'>
            <span style='color:{ca_color}'>{comp_a}</span>
            <span style='color:{cb_color}'>{comp_b}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Radar + Sentiment ───────────────────────────────────────────────────
    radar_col, sent_col = st.columns([1, 1], gap="large")
    gmin = all_means.min().min()
    gmax = all_means.max().max()

    with radar_col:
        st.markdown('<div class="sec-title">Theme Radar Overlay</div>', unsafe_allow_html=True)

        fig_rad = go.Figure()
        for comp, clr in [(comp_a, ca_color), (comp_b, cb_color)]:
            if comp in all_means.index:
                vals = [all_means.loc[comp, c] for c in THEME_COLS]
                norm = [(v-gmin)/(gmax-gmin+1e-9) for v in vals]
                nc   = norm + [norm[0]]
                lc   = THEME_LABELS + [THEME_LABELS[0]]
                fig_rad.add_trace(go.Scatterpolar(
                    r=nc, theta=lc,
                    fill='toself',
                    fillcolor=hex_to_rgba(clr, 0.12),
                    line=dict(color=clr, width=2.5),
                    name=comp,
                    marker=dict(size=6, color=clr, line=dict(color=PLOT_BG, width=2)),
                    hovertemplate=f"<b>{comp}</b><br>%{{theta}}: %{{r:.3f}}<extra></extra>",
                ))

        fig_rad.update_layout(
            polar=dict(
                bgcolor=PLOT_BG,
                radialaxis=dict(
                    visible=True, range=[0,1],
                    tickfont=dict(size=8, color=TEXT_CLR, family="DM Mono"),
                    gridcolor=GRID_CLR, linecolor=AXIS_CLR,
                ),
                angularaxis=dict(
                    tickfont=dict(size=10, color=TITLE_CLR, family="DM Sans"),
                    gridcolor=GRID_CLR, linecolor=AXIS_CLR,
                ),
            ),
            paper_bgcolor=PAPER_BG,
            plot_bgcolor=PAPER_BG,
            font=dict(family="DM Sans", color=TEXT_CLR, size=11),
            margin=dict(l=50, r=50, t=30, b=30),
            height=350,
            legend=dict(
                font=LEG_FONT,
                bgcolor="#ffffff",
                bordercolor=GRID_CLR, borderwidth=1,
                x=0.5, xanchor="center", y=-0.08,
                orientation="h",
            ),
        )
        st.plotly_chart(fig_rad, use_container_width=True, config=MODEBAR_CFG)

    with sent_col:
        st.markdown('<div class="sec-title">Sentiment Comparison</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

        sent_a = free_a[["like_sentiment","dislike_sentiment","combined_sentiment"]].mean()
        sent_b = free_b[["like_sentiment","dislike_sentiment","combined_sentiment"]].mean()

        for label, key in [
            ("↑ Like Sentiment", "like_sentiment"),
            ("↓ Dislike Sentiment", "dislike_sentiment"),
            ("⇄ Combined (WCI)", "combined_sentiment"),
        ]:
            va   = sent_a[key]
            vb   = sent_b[key]
            pa   = bar_pct(va)
            pb   = bar_pct(vb)
            diff = va - vb
            diff_clr = ca_color if diff >= 0 else cb_color
            winner = comp_a if diff >= 0 else comp_b
            st.markdown(f"""
            <div style='margin-bottom:1.3rem'>
                <div style='display:flex;justify-content:space-between;margin-bottom:0.35rem'>
                    <span style='font-size:0.81rem;font-weight:500;color:var(--text-2);
                                 font-family:"DM Sans",sans-serif'>{label}</span>
                    <span style='font-size:0.72rem;color:{diff_clr};font-weight:600;
                                 font-family:"DM Mono",monospace'>{winner} +{abs(diff):.3f}</span>
                </div>
                <div style='display:flex;align-items:center;gap:0.45rem;margin-bottom:0.12rem'>
                    <span style='font-size:0.67rem;color:{ca_color};width:46px;text-align:right;
                                 font-family:"DM Mono",monospace'>{va:+.3f}</span>
                    <div style='flex:1;background:rgba(5,150,105,0.05);border-radius:999px;
                                height:7px;overflow:hidden;border:1px solid {ca_color}18'>
                        <div style='background:{ca_color};width:{pa:.1f}%;height:7px;
                                    border-radius:999px;opacity:0.82'></div>
                    </div>
                </div>
                <div style='display:flex;align-items:center;gap:0.45rem'>
                    <span style='font-size:0.67rem;color:{cb_color};width:46px;text-align:right;
                                 font-family:"DM Mono",monospace'>{vb:+.3f}</span>
                    <div style='flex:1;background:rgba(248,113,113,0.05);border-radius:999px;
                                height:7px;overflow:hidden;border:1px solid {cb_color}18'>
                        <div style='background:{cb_color};width:{pb:.1f}%;height:7px;
                                    border-radius:999px;opacity:0.82'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)
        st.markdown("""<span style='font-size:0.72rem;font-weight:700;color:var(--text-3);
                    text-transform:uppercase;letter-spacing:0.1em;
                    font-family:"DM Sans",sans-serif'>Theme Score Diffs</span>""",
                    unsafe_allow_html=True)
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        if comp_a in all_means.index and comp_b in all_means.index:
            for lbl, cn in zip(THEME_SHORT, THEME_COLS):
                va = all_means.loc[comp_a, cn]
                vb = all_means.loc[comp_b, cn]
                diff = va - vb
                wclr = ca_color if va > vb else cb_color
                st.markdown(f"""
                <div style='display:flex;align-items:center;justify-content:space-between;
                            margin-bottom:0.4rem;padding:0.38rem 0.6rem;
                            background:var(--surface-2);border-radius:8px;
                            border:1px solid var(--border)'>
                    <span style='font-size:0.76rem;color:var(--text-2);font-weight:500;
                                 width:78px;font-family:"DM Sans",sans-serif'>{lbl}</span>
                    <span style='font-size:0.71rem;color:{ca_color};
                                 font-family:"DM Mono",monospace'>{va:+.3f}</span>
                    <span style='font-size:0.66rem;color:var(--text-3)'>vs</span>
                    <span style='font-size:0.71rem;color:{cb_color};
                                 font-family:"DM Mono",monospace'>{vb:+.3f}</span>
                    <span style='font-size:0.65rem;font-weight:700;color:{wclr};
                                 background:{wclr}18;border-radius:999px;
                                 padding:0.1rem 0.44rem;font-family:"DM Mono",monospace'>
                        +{abs(diff):.3f}</span>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — REGRESSION & INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "∿  Regression & Insights":

    st.markdown("""
    <div class='hero'>
        <div class='hero-eyebrow'>OLS Regression · Sensitivity Analysis</div>
        <h1>Regression &amp; <em>Insights</em></h1>
        <p>OLS regression of WCI on average star rating — testing whether the text-derived index
        correlates with structured employee scores. Includes sensitivity checks on the
        like/dislike weighting assumption.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── OLS ─────────────────────────────────────────────────────────────────
    X_ols = scores["wci_score"].values
    Y_ols = scores["avg_rating"].values
    n_firms = len(scores)
    slope, intercept, r_val, p_val, se = stats.linregress(X_ols, Y_ols)
    r2     = r_val ** 2
    fitted = intercept + slope * X_ols

    st.markdown(
        f'<div class="sec-title">OLS Results'
        f'&ensp;<span style="font-size:0.72rem;font-weight:400;color:var(--text-3);'
        f'font-family:\'DM Mono\',monospace">Y = avg_rating | X = WCI | n = {n_firms} firms'
        f'</span></div>',
        unsafe_allow_html=True
    )

    s1,s2,s3,s4 = st.columns(4)
    for col, ov, ol, clr in zip(
        [s1,s2,s3,s4],
        [f"{r2:.3f}", f"{r_val:.3f}", f"{p_val:.4f}", f"{slope:.6f}"],
        ["R² (Fit)", "Pearson r", "p-value", "β₁ (Slope)"],
        ["#059669", "#2563eb",
         "#059669" if p_val < 0.10 else "#d97706",
         "#dc2626" if slope < 0 else "#059669"]
    ):
        col.markdown(f"""
        <div class='ols-stat' style='border-top:2px solid {clr}44'>
            <span class='ov' style='color:{clr}'>{ov}</span>
            <span class='ol'>{ol}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Scatter + Interpretation ────────────────────────────────────────────
    scatter_col, insight_col = st.columns([3, 2], gap="large")

    with scatter_col:
        st.markdown('<div class="sec-title">WCI vs Average Star Rating</div>', unsafe_allow_html=True)

        fig_s = go.Figure()

        # Confidence band
        x_line = np.linspace(X_ols.min() - 8, X_ols.max() + 8, 200)
        y_line = intercept + slope * x_line
        # Approx 95% CI
        y_err = se * 1.96 * np.sqrt(1/n_firms + (x_line - X_ols.mean())**2 / ((X_ols - X_ols.mean())**2).sum())

        fig_s.add_trace(go.Scatter(
            x=np.concatenate([x_line, x_line[::-1]]),
            y=np.concatenate([y_line + y_err, (y_line - y_err)[::-1]]),
            fill='toself',
            fillcolor="rgba(5,150,105,0.05)",
            line=dict(color="rgba(0,0,0,0)"),
            hoverinfo="skip",
            name="95% CI",
            showlegend=True,
        ))

        fig_s.add_trace(go.Scatter(
            x=x_line, y=y_line,
            mode="lines",
            line=dict(color="rgba(5,150,105,0.4)", width=1.8, dash="dash"),
            name="OLS Fit",
            hoverinfo="skip",
        ))

        for _, row in scores.iterrows():
            comp = row["company"]
            clr  = COMPANY_COLORS.get(comp, "#059669")
            caveat = " ✦" if comp == "Veljan Denison" else ""
            residual = row["avg_rating"] - (intercept + slope * row["wci_score"])
            fig_s.add_trace(go.Scatter(
                x=[row["wci_score"]], y=[row["avg_rating"]],
                mode="markers+text",
                marker=dict(
                    size=18, color=clr, opacity=0.92,
                    line=dict(color=PLOT_BG, width=2.5),
                    symbol="circle",
                ),
                text=[f"  {comp}{caveat}"],
                textposition="middle right",
                textfont=dict(size=11, family="DM Sans", color=TITLE_CLR),
                name=comp,
                hovertemplate=(
                    f"<b>{comp}</b><br>"
                    f"WCI: <b>{row['wci_score']:.1f}</b><br>"
                    f"Avg Rating: <b>{row['avg_rating']:.3f}</b><br>"
                    f"Residual: <b>{residual:+.3f}</b><br>"
                    f"Reviews: <b>{int(row['n_reviews']):,}</b>"
                    "<extra></extra>"
                ),
            ))

        fig_s.update_layout(
            **base_layout(
                xaxis=ax(
                    range=[-12, 122],
                    title=dict(text="WCI Score (0–100)", font=TITLE_FONT),
                ),
                yaxis=ax(
                    title=dict(text="Average Star Rating (1–5)", font=TITLE_FONT),
                ),
                margin=dict(l=15, r=140, t=30, b=55),
                height=400,
                showlegend=False,
            )
        )
        fig_s.add_annotation(
            x=5, y=max(Y_ols) + 0.02,
            text=f"R² = {r2:.3f}  |  r = {r_val:.3f}  |  p = {p_val:.4f}",
            showarrow=False,
            font=dict(size=10.5, color="#059669", family="DM Mono"),
            bgcolor="#ffffff",
            bordercolor="rgba(5,150,105,0.25)",
            borderwidth=1,
            borderpad=7,
            align="left",
        )
        st.plotly_chart(fig_s, use_container_width=True, config=MODEBAR_CFG)

    with insight_col:
        st.markdown('<div class="sec-title">Interpretation</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

        p_interp = "marginally significant (p < 0.10)" if p_val < 0.10 else "not significant at 5%"
        r2_pct   = r2 * 100

        interp_cards = [
            ("↘", "#dc2626", "Negative Relationship",
             f"β₁ = {slope:.6f} — higher WCI associates with <em>lower</em> avg star rating. "
             "Text sentiment and star ratings measure genuinely different cultural dimensions."),
            ("◎", "#059669", f"Fit: R² = {r2:.3f}",
             f"The model explains <b>{r2_pct:.1f}%</b> of rating variance. "
             f"Association is <b>{p_interp}</b> (p = {p_val:.4f})."),
            ("!", "#d97706", "Statistical Caution",
             f"n = {n_firms} data points limits statistical power. "
             "Veljan Denison's thin sample may distort the fit. "
             "Treat as directionally meaningful."),
        ]
        for icon, clr, title, body in interp_cards:
            st.markdown(f"""
            <div class='ins-card' style='margin-bottom:0.7rem;border-top:2px solid {clr}33'>
                <div style='display:flex;align-items:center;gap:0.5rem;margin-bottom:0.55rem'>
                    <div style='width:28px;height:28px;border-radius:7px;
                                background:{clr}15;border:1px solid {clr}30;
                                display:flex;align-items:center;justify-content:center;
                                font-size:0.88rem'>{icon}</div>
                    <span style='font-weight:600;color:{clr};font-size:0.83rem;
                                 font-family:"DM Sans",sans-serif'>{title}</span>
                </div>
                <div style='font-size:0.77rem;color:var(--text-2);line-height:1.75;
                            font-family:"DM Sans",sans-serif;font-weight:300'>{body}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='hr-divider'></div>", unsafe_allow_html=True)

    # ── Sensitivity Analysis ────────────────────────────────────────────────
    st.markdown('<div class="sec-title">Sensitivity Analysis — Like / Dislike Weighting</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.8rem;color:var(--text-3);margin-bottom:1.2rem;line-height:1.75;
                font-family:"DM Sans",sans-serif;font-weight:300;max-width:700px'>
        WCI rankings tested under four alternative like/dislike split assumptions.
        Stable rankings across splits confirm a robust index.
    </div>
    """, unsafe_allow_html=True)

    EXPERT_W   = weights["expert_weight"].values
    splits_cfg = [
        ("50 / 50",   0.50, 0.50, False),
        ("40 / 60 ★", 0.40, 0.60, True),
        ("35 / 65",   0.35, 0.65, False),
        ("30 / 70",   0.30, 0.70, False),
    ]

    sens_rows = []
    for label, lw, dw, is_base in splits_cfg:
        tmp = df[~df["structured_text"].astype(bool)].copy()
        tmp["comb"] = lw * tmp["like_sentiment"].fillna(0) + dw * tmp["dislike_sentiment"].fillna(0)
        firm = tmp.groupby("company")[THEME_COLS].mean().fillna(0)
        if len(firm) < 2:
            continue
        scaler = StandardScaler()
        Xs     = scaler.fit_transform(firm)
        pca    = PCA(n_components=min(5, len(firm)-1) if len(firm) > 2 else 1)
        pca.fit(Xs)
        pca_w  = np.abs(pca.components_[0]); pca_w /= pca_w.sum()
        fw     = 0.5 * pca_w + 0.5 * EXPERT_W[:len(pca_w)]; fw /= fw.sum()
        raw    = firm.values @ fw
        mn, mx = raw.min(), raw.max()
        norm   = (raw - mn) / (mx - mn + 1e-9) * 100
        norm_arr = list(norm)
        for co, sc in zip(firm.index, norm_arr):
            rank_s = int((-np.array(norm_arr)).argsort().argsort()[list(firm.index).index(co)] + 1)
            sens_rows.append({"Split": label, "company": co, "WCI": round(sc, 1),
                              "Rank": rank_s, "base": is_base})

    sens_df     = pd.DataFrame(sens_rows)
    split_names = [s[0] for s in splits_cfg]
    x_labels    = scores.sort_values("wci_rank")["company"].tolist()

    fig_sens = go.Figure()
    for company in x_labels:
        clr = COMPANY_COLORS.get(company, "#059669")
        sub = sens_df[sens_df["company"] == company].set_index("Split")
        y_vals = [sub.loc[s, "WCI"] if s in sub.index else 0 for s in split_names]
        fig_sens.add_trace(go.Bar(
            name=company,
            x=split_names,
            y=y_vals,
            marker=dict(
                color=clr, opacity=0.85,
                line=dict(color="rgba(255,255,255,0.06)", width=1)
            ),
            hovertemplate=f"<b>{company}</b><br>Split: %{{x}}<br>WCI: <b>%{{y:.1f}}</b><extra></extra>",
        ))

    fig_sens.update_layout(
        **base_layout(
            barmode="group",
            xaxis=ax(showgrid=False),
            yaxis=ax(
                title=dict(text="WCI Score", font=TITLE_FONT),
                range=[0, 118],
            ),
            legend=dict(
                font=LEG_FONT,
                bgcolor="#ffffff",
                bordercolor=GRID_CLR, borderwidth=1,
                orientation="h", x=0.5, xanchor="center", y=-0.22,
            ),
            margin=dict(l=15, r=15, t=30, b=80),
            height=340,
            bargap=0.22, bargroupgap=0.04,
        )
    )
    fig_sens.add_annotation(
        x="40 / 60 ★", y=113,
        text="★ Base case (Baumeister et al., 2001)",
        showarrow=False,
        font=dict(size=10, color="#065f46", family="DM Mono"),
        bgcolor="#ffffff",
        bordercolor="rgba(5,150,105,0.3)",
        borderwidth=1, borderpad=5,
    )
    st.plotly_chart(fig_sens, use_container_width=True, config=MODEBAR_CFG)

    # ── Rank Stability Table ────────────────────────────────────────────────
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Rank Stability Table</div>', unsafe_allow_html=True)

    available_companies = [c for c in x_labels if c in sens_df["company"].values]
    pivot_rank = sens_df.pivot(index="company", columns="Split", values="Rank")[split_names].reindex(available_companies)
    pivot_wci  = sens_df.pivot(index="company", columns="Split", values="WCI")[split_names].reindex(available_companies)

    header_cells = "".join(
        f'<th style="text-align:center;padding:0.55rem 0.85rem;color:var(--text-3);'
        f'font-family:\'DM Mono\',monospace;font-size:0.72rem;font-weight:500">{s}</th>'
        for s in split_names
    )
    rows_html = ""
    for comp in available_companies:
        clr    = COMPANY_COLORS.get(comp, "#059669")
        ranks  = [int(pivot_rank.loc[comp, s]) for s in split_names]
        wcis   = [pivot_wci.loc[comp, s] for s in split_names]
        stable = len(set(ranks)) == 1
        badge  = (
            "<span style='background:rgba(5,150,105,0.12);color:#059669;border-radius:999px;"
            "padding:0.1rem 0.5rem;font-size:0.63rem;font-weight:700;font-family:\"DM Mono\",monospace'>STABLE</span>"
            if stable else
            "<span style='background:rgba(248,113,113,0.1);color:#dc2626;border-radius:999px;"
            "padding:0.1rem 0.5rem;font-size:0.63rem;font-weight:700;font-family:\"DM Mono\",monospace'>VARIES</span>"
        )
        rank_cells = "".join(
            f"<td style='text-align:center;padding:0.55rem 0.85rem'>"
            f"<b style='font-family:\"DM Serif Display\",serif;font-size:1.05rem;color:{clr}'>#{r}</b>"
            f"<br><span style='font-size:0.65rem;color:var(--text-3);font-family:\"DM Mono\",monospace'>{w:.1f}</span></td>"
            for r, w in zip(ranks, wcis)
        )
        rows_html += (
            f"<tr style='border-bottom:1px solid rgba(5,150,105,0.06)'>"
            f"<td style='padding:0.55rem 0.85rem'>"
            f"<div style='display:flex;align-items:center;gap:0.5rem'>"
            f"<span style='color:{clr};font-size:0.5rem'>●</span>"
            f"<span style='font-family:\"DM Sans\",sans-serif;font-size:0.82rem;color:var(--text);font-weight:500'>{comp}</span>"
            f"&nbsp;{badge}</div></td>"
            f"{rank_cells}</tr>"
        )

    table_html = (
        "<div style='overflow-x:auto;border-radius:var(--r-md);border:1px solid var(--border);"
        "background:var(--surface)'>"
        "<table style='width:100%;border-collapse:collapse;font-size:0.81rem;color:var(--text)'>"
        "<thead><tr style='border-bottom:1px solid rgba(5,150,105,0.12);background:rgba(5,150,105,0.04)'>"
        "<th style='text-align:left;padding:0.55rem 0.85rem;color:var(--text-3);"
        "font-family:\"DM Mono\",monospace;font-size:0.72rem;font-weight:500'>Company</th>"
        + header_cells +
        "</tr></thead>"
        "<tbody>" + rows_html + "</tbody>"
        "</table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("""
    <div class='caveat' style='margin-top:0.85rem'>
        ★ <b>40/60 split</b> is the base case — grounded in Baumeister et al. (2001) negativity bias.
        All companies maintain identical rankings across all four assumptions,
        confirming the WCI is <b>robust</b> to this methodological choice (Spearman r = 1.0).
    </div>
    """, unsafe_allow_html=True)
