# =============================================================================
#  LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
#  Professional Streamlit Analytics Dashboard
#  BSc Clinical Research · Internship Final Project
# =============================================================================
#
#  Run:  py -m streamlit run app.py
#  Deps: pip install streamlit pandas plotly
#
#  Place your four CSV files in the SAME folder as app.py, OR in a sub-folder
#  called "data/".  The loader checks both locations automatically.
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIGURATION  ·  must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Food Wastage Management System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL STYLES  ·  dark glassmorphism theme via injected CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #07090f; color: #dde3ed; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 3rem 2rem; max-width: 100% !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 4px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0b0e17 0%, #0f172a 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] label {
    color: #64748b !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: rgba(72,199,142,0.15) !important;
    color: #48c78e !important;
    border: 1px solid rgba(72,199,142,0.28) !important;
    border-radius: 6px !important;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(120deg, #091a14 0%, #0a2a1e 40%, #0c1829 100%);
    border: 1px solid rgba(72,199,142,0.18);
    border-radius: 20px;
    padding: 2.4rem 3rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(72,199,142,0.1) 0%, transparent 68%);
}
.hero::after {
    content: "";
    position: absolute; bottom: -60px; left: 25%;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,179,237,0.07) 0%, transparent 65%);
}
.hero-tag {
    display: inline-block;
    background: rgba(72,199,142,0.1);
    border: 1px solid rgba(72,199,142,0.25);
    color: #48c78e;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    padding: 0.22rem 0.8rem; border-radius: 20px;
    margin-bottom: 0.9rem;
}
.hero-title {
    font-size: 2rem; font-weight: 800; line-height: 1.18;
    background: linear-gradient(90deg, #48c78e 0%, #63b3ed 55%, #a78bfa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 0.5rem 0;
}
.hero-sub {
    font-size: 0.9rem; color: #475569; font-weight: 400; margin: 0;
    max-width: 680px;
}

/* ── KPI Cards ── */
.kpi-wrap { height: 100%; }
.kpi {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.45rem 1.55rem;
    height: 100%; position: relative; overflow: hidden;
    transition: transform .2s, border-color .2s;
}
.kpi:hover { transform: translateY(-3px); border-color: rgba(99,179,237,0.25); }
.kpi::before {
    content: ""; position: absolute;
    top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0;
}
.kpi-g::before { background: linear-gradient(90deg,#48c78e,#06d6a0); }
.kpi-b::before { background: linear-gradient(90deg,#63b3ed,#3b82f6); }
.kpi-v::before { background: linear-gradient(90deg,#a78bfa,#8b5cf6); }
.kpi-o::before { background: linear-gradient(90deg,#fb923c,#f59e0b); }
.kpi-ico   { font-size: 2rem; display:block; margin-bottom: .7rem; }
.kpi-label { font-size:.69rem; font-weight:700; letter-spacing:.1em;
             text-transform:uppercase; color:#4a5568; margin-bottom:.35rem; }
.kpi-val   { font-size:2.3rem; font-weight:800; color:#f0f4f8; line-height:1; margin-bottom:.4rem; }
.kpi-note  { font-size:.75rem; color:#48c78e; font-weight:500; }

/* ── Section headers ── */
.sec-hdr {
    display:flex; align-items:center; gap:.7rem;
    padding: .6rem 0 .7rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin: 1.8rem 0 1.1rem 0;
}
.sec-ico {
    width:34px; height:34px; border-radius:9px;
    display:flex; align-items:center; justify-content:center; font-size:1rem;
}
.si-g { background:rgba(72,199,142,0.14); }
.si-b { background:rgba(99,179,237,0.14); }
.si-v { background:rgba(167,139,250,0.14); }
.si-o { background:rgba(251,146,60,0.14); }
.sec-title { font-size:1.05rem; font-weight:700; color:#e2e8f0; margin:0; }
.sec-sub   { font-size:.74rem; color:#475569; margin:0; }

/* ── Chart card ── */
.chart-card {
    background:rgba(255,255,255,0.025);
    border:1px solid rgba(255,255,255,0.055);
    border-radius:15px; padding:1.1rem 1rem .6rem 1rem;
    margin-bottom:.8rem;
}

/* ── Insight cards ── */
.ins {
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.065);
    border-radius:13px; padding:1.1rem 1.25rem;
    height:100%; position:relative; overflow:hidden;
}
.ins::after {
    content:""; position:absolute; bottom:-20px; right:-20px;
    width:72px; height:72px; border-radius:50%; opacity:.07;
}
.ins-g::after{background:#48c78e;} .ins-b::after{background:#63b3ed;}
.ins-v::after{background:#a78bfa;} .ins-o::after{background:#fb923c;}
.ins-t::after{background:#2dd4bf;} .ins-p::after{background:#f472b6;}
.ins-ico   { font-size:1.4rem; margin-bottom:.5rem; }
.ins-label { font-size:.66rem; font-weight:700; letter-spacing:.1em;
             text-transform:uppercase; color:#3d4f63; margin-bottom:.25rem; }
.ins-val   { font-size:1.05rem; font-weight:700; color:#e8edf4; margin-bottom:.18rem; }
.ins-note  { font-size:.72rem; color:#4a5568; }

/* ── Sidebar logo ── */
.sb-logo {
    text-align:center; padding:1.3rem 0 1.6rem 0;
    border-bottom:1px solid rgba(255,255,255,0.05); margin-bottom:1.4rem;
}
.sb-ico  { font-size:2.4rem; }
.sb-name { font-size:1.05rem; font-weight:800; display:block; margin-top:.3rem;
           background:linear-gradient(90deg,#48c78e,#63b3ed);
           -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.sb-sub  { font-size:.64rem; color:#374151; text-transform:uppercase; letter-spacing:.1em; }

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(90deg,#48c78e,#06b6d4) !important;
    color:#07090f !important; font-weight:700 !important;
    border:none !important; border-radius:9px !important;
    padding:.5rem 1.3rem !important; font-size:.82rem !important;
    letter-spacing:.04em !important;
}
.stDownloadButton > button:hover { opacity:.85 !important; }

/* ── Search input ── */
.stTextInput > div > div > input {
    background:rgba(255,255,255,0.04) !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:9px !important; color:#dde3ed !important;
}
.stTextInput > div > div > input:focus {
    border-color:rgba(72,199,142,0.35) !important;
    box-shadow:0 0 0 2px rgba(72,199,142,0.1) !important;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  PLOTLY SHARED THEME DICT
# ─────────────────────────────────────────────────────────────────────────────
_CT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#7a8fa8", size=11),
    title_font=dict(family="Inter", color="#dde3ed", size=13, weight="bold"),
    margin=dict(t=46, b=28, l=26, r=26),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#7a8fa8", size=11)),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.045)", linecolor="rgba(255,255,255,0.07)",
        tickfont=dict(color="#4d6070", size=11), title_font=dict(color="#4d6070"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.045)", linecolor="rgba(255,255,255,0.07)",
        tickfont=dict(color="#4d6070", size=11), title_font=dict(color="#4d6070"),
    ),
)

# Brand colour palette
PAL = ["#48c78e", "#63b3ed", "#a78bfa", "#fb923c",
       "#f472b6", "#2dd4bf", "#facc15", "#f87171", "#818cf8", "#34d399"]


# ─────────────────────────────────────────────────────────────────────────────
#  ROBUST FILE LOADER  ·  checks same folder then data/ sub-folder
# ─────────────────────────────────────────────────────────────────────────────
def _find(filename: str) -> Path:
    """Return Path to *filename*, checking script dir then data/ sub-folder."""
    base = Path(__file__).parent
    for candidate in [base / filename, base / "data" / filename]:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"❌  '{filename}' not found.\n"
        f"Place it in the same folder as app.py or in a sub-folder called data/."
    )


@st.cache_data(show_spinner=False)
def load_all():
    """Load and lightly clean all four datasets. Results are cached."""
    providers = pd.read_csv(_find("providers_data.csv"))
    receivers = pd.read_csv(_find("receivers_data.csv"))
    food      = pd.read_csv(_find("food_listings_data.csv"))
    claims    = pd.read_csv(_find("claims_data.csv"))

    # ── Parse dates ──────────────────────────────────────────────────────────
    food["Expiry_Date"]   = pd.to_datetime(food["Expiry_Date"],
                                           format="%m/%d/%Y", errors="coerce")
    claims["Timestamp"]   = pd.to_datetime(claims["Timestamp"],
                                           format="%m/%d/%Y %H:%M", errors="coerce")

    # ── Derived time columns ─────────────────────────────────────────────────
    food["Expiry_Month"]  = food["Expiry_Date"].dt.to_period("M").dt.to_timestamp()
    claims["Claim_Month"] = claims["Timestamp"].dt.to_period("M").dt.to_timestamp()
    claims["Claim_Hour"]  = claims["Timestamp"].dt.hour

    return providers, receivers, food, claims


# ── Load data (with user-friendly error handling) ────────────────────────────
try:
    providers_raw, receivers_raw, food_raw, claims_raw = load_all()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR  ·  logo + filters
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:

    # ── Branding ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="sb-logo">
        <span class="sb-ico">🌿</span>
        <span class="sb-name">FoodBridge</span>
        <span class="sb-sub">Management System</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🔧 Dashboard Filters**")
    st.markdown("---")

    # ── Provider Type ─────────────────────────────────────────────────────────
    all_ptypes = sorted(food_raw["Provider_Type"].dropna().unique())
    sel_ptypes = st.multiselect("Provider Type", all_ptypes, default=all_ptypes)

    # ── Food Type ─────────────────────────────────────────────────────────────
    all_ftypes = sorted(food_raw["Food_Type"].dropna().unique())
    sel_ftypes = st.multiselect("Food Type", all_ftypes, default=all_ftypes)

    # ── Meal Type ─────────────────────────────────────────────────────────────
    all_mtypes = sorted(food_raw["Meal_Type"].dropna().unique())
    sel_mtypes = st.multiselect("Meal Type", all_mtypes, default=all_mtypes)

    # ── City (derived from food Location column) ──────────────────────────────
    all_locs = sorted(food_raw["Location"].dropna().unique())
    sel_locs = st.multiselect("Location / City", all_locs, default=all_locs)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Dataset summary card ──────────────────────────────────────────────────
    st.markdown("""
    <div style="background:rgba(72,199,142,0.05);border:1px solid rgba(72,199,142,0.13);
                border-radius:11px;padding:.95rem 1.1rem;">
        <div style="font-size:.65rem;color:#374151;text-transform:uppercase;
                    letter-spacing:.1em;font-weight:700;margin-bottom:.55rem;">
            Dataset Info
        </div>
        <div style="font-size:.78rem;color:#64748b;line-height:1.9;">
            📅 Snapshot: March 2025<br>
            🏙️ Multi-city network<br>
            🔗 Four linked tables
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  APPLY SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────
def _filt(df, col, sel):
    """Filter df by col membership; if sel is empty return df unchanged."""
    return df if not sel else df[df[col].isin(sel)]

food      = food_raw.copy()
food      = _filt(food, "Provider_Type", sel_ptypes)
food      = _filt(food, "Food_Type",     sel_ftypes)
food      = _filt(food, "Meal_Type",     sel_mtypes)
food      = _filt(food, "Location",      sel_locs)
providers = _filt(providers_raw, "Type", sel_ptypes)   # sync provider filter
claims    = claims_raw[claims_raw["Food_ID"].isin(food["Food_ID"])]


# ─────────────────────────────────────────────────────────────────────────────
#  COMPUTED KPI VALUES
# ─────────────────────────────────────────────────────────────────────────────
n_providers  = len(providers_raw)
n_receivers  = len(receivers_raw)
n_listings   = len(food)
n_claims     = len(claims)
total_qty    = int(food["Quantity"].sum())
completed    = (claims["Status"] == "Completed").sum()
comp_rate    = round(completed / n_claims * 100, 1) if n_claims else 0.0


# ─────────────────────────────────────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">🌿 Analytics Dashboard · Internship Project</div>
    <h1 class="hero-title">Local Food Wastage Management System</h1>
    <p class="hero-sub">
        Connecting surplus food providers with receivers across the city network.
        Real-time intelligence on listings, claims, and distribution efficiency.
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION A — KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────
def kpi(icon, label, value, note, accent):
    return f"""<div class="kpi-wrap"><div class="kpi kpi-{accent}">
        <span class="kpi-ico">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-val">{value}</div>
        <div class="kpi-note">{note}</div>
    </div></div>"""

c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi("🏪", "Total Providers",   f"{n_providers:,}",
                "Registered supply partners", "g"), unsafe_allow_html=True)
c2.markdown(kpi("🤝", "Total Receivers",   f"{n_receivers:,}",
                "NGOs, shelters & individuals", "b"), unsafe_allow_html=True)
c3.markdown(kpi("🍽️", "Food Listings",     f"{n_listings:,}",
                f"{total_qty:,} total units available", "v"), unsafe_allow_html=True)
c4.markdown(kpi("📋", "Total Claims",      f"{n_claims:,}",
                f"{comp_rate}% completion rate", "o"), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER — section header HTML
# ─────────────────────────────────────────────────────────────────────────────
def sec(icon, title, sub, si_cls="si-g"):
    st.markdown(f"""
    <div class="sec-hdr">
        <div class="sec-ico {si_cls}">{icon}</div>
        <div>
            <div class="sec-title">{title}</div>
            <div class="sec-sub">{sub}</div>
        </div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION B — FOOD SUPPLY OVERVIEW  (2 charts)
# ─────────────────────────────────────────────────────────────────────────────
sec("📊", "Food Supply Overview",
    "Listings by provider type and food category", "si-g")

left, right = st.columns([1.25, 1])

# ── Chart 1: Listings by Provider Type (horizontal bar) ─────────────────────
with left:
    ptype_df = (food.groupby("Provider_Type")
                    .agg(Listings=("Food_ID","count"), Qty=("Quantity","sum"))
                    .reset_index()
                    .sort_values("Listings", ascending=True))

    fig1 = go.Figure(go.Bar(
        y=ptype_df["Provider_Type"], x=ptype_df["Listings"],
        orientation="h",
        marker=dict(color=PAL[:len(ptype_df)],
                    line=dict(color="rgba(255,255,255,0.04)", width=1)),
        text=ptype_df["Listings"], textposition="outside",
        textfont=dict(color="#7a8fa8", size=12),
        hovertemplate="<b>%{y}</b><br>Listings: %{x:,}<extra></extra>",
    ))
    fig1.update_layout(title="Food Listings by Provider Type",
                       height=280, bargap=.35, **_CT,
                       )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chart 2: Food Type Distribution (donut) ──────────────────────────────────
with right:
    ftype_df = food["Food_Type"].value_counts().reset_index()
    ftype_df.columns = ["Food_Type", "Count"]
    fcolors = {"Vegetarian":"#48c78e","Non-Vegetarian":"#f87171","Vegan":"#a78bfa"}

    fig2 = go.Figure(go.Pie(
        labels=ftype_df["Food_Type"], values=ftype_df["Count"],
        hole=.58,
        marker=dict(colors=[fcolors.get(t, "#63b3ed") for t in ftype_df["Food_Type"]],
                    line=dict(color="#07090f", width=3)),
        textinfo="percent", textfont=dict(size=12, color="#dde3ed"),
        hovertemplate="<b>%{label}</b><br>%{value} listings · %{percent}<extra></extra>",
    ))
    fig2.add_annotation(text=f"<b>{n_listings:,}</b><br>listings",
                        x=.5, y=.5, showarrow=False,
                        font=dict(size=16, color="#dde3ed", family="Inter"),
                        align="center")
    fig2.update_layout(title="Food Type Distribution", height=280,
                       showlegend=True, **_CT,
                       )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION C — GEOGRAPHIC INTELLIGENCE  (2 charts)
# ─────────────────────────────────────────────────────────────────────────────
sec("🗺️", "Geographic Intelligence",
    "Top locations by listing volume and provider city distribution", "si-b")

left2, right2 = st.columns([1.4, 1])

# ── Chart 3: Top 10 Cities / Locations by Food Listings ──────────────────────
with left2:
    top10 = (food.groupby("Location")
                 .agg(Listings=("Food_ID","count"), Qty=("Quantity","sum"))
                 .reset_index()
                 .sort_values("Listings", ascending=False)
                 .head(10)
                 .sort_values("Listings", ascending=True))

    fig3 = go.Figure(go.Bar(
        y=top10["Location"], x=top10["Listings"],
        orientation="h",
        marker=dict(
            color=top10["Listings"],
            colorscale=[[0,"#152840"],[.5,"#2563eb"],[1,"#48c78e"]],
            showscale=False,
            line=dict(color="rgba(255,255,255,0.04)", width=1),
        ),
        text=top10["Listings"], textposition="outside",
        textfont=dict(color="#7a8fa8", size=11),
        hovertemplate="<b>%{y}</b><br>Listings: %{x}<extra></extra>",
    ))
    fig3.update_layout(title="Top 10 Locations by Food Listings",
                       height=340, bargap=.3, **_CT,
                      )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chart 4: Provider Type count from providers table ────────────────────────
with right2:
    prov_type = providers["Type"].value_counts().reset_index()
    prov_type.columns = ["Type", "Count"]

    fig4 = go.Figure(go.Bar(
        x=prov_type["Type"], y=prov_type["Count"],
        marker=dict(color=PAL[:len(prov_type)],
                    line=dict(color="rgba(255,255,255,0.04)", width=1)),
        text=prov_type["Count"], textposition="outside",
        textfont=dict(color="#7a8fa8", size=12),
        hovertemplate="<b>%{x}</b><br>Providers: %{y}<extra></extra>",
    ))
    fig4.update_layout(title="Providers by Organisation Type",
                       height=340, bargap=.35, **_CT,
                       )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION D — MEAL TYPES & CLAIMS ANALYSIS  (2 charts)
# ─────────────────────────────────────────────────────────────────────────────
sec("📋", "Meal Types & Claims Analysis",
    "Meal category breakdown and claim lifecycle status", "si-v")

left3, right3 = st.columns(2)

# ── Chart 5: Meal Type Distribution (pie) ────────────────────────────────────
with left3:
    meal_df = food["Meal_Type"].value_counts().reset_index()
    meal_df.columns = ["Meal_Type", "Count"]

    fig5 = go.Figure(go.Pie(
        labels=meal_df["Meal_Type"], values=meal_df["Count"],
        hole=0,
        marker=dict(colors=PAL[:len(meal_df)],
                    line=dict(color="#07090f", width=3)),
        textinfo="label+percent",
        textfont=dict(size=11, color="#dde3ed"),
        pull=[.04]*len(meal_df),
        hovertemplate="<b>%{label}</b><br>%{value} listings · %{percent}<extra></extra>",
    ))
    fig5.update_layout(title="Meal Type Distribution", height=310,
                       showlegend=False, **_CT,
                       )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chart 6: Claims Status Donut ──────────────────────────────────────────────
with right3:
    status_df = claims["Status"].value_counts().reset_index()
    status_df.columns = ["Status", "Count"]
    scolors = {"Completed":"#48c78e","Pending":"#fb923c","Cancelled":"#f87171"}

    fig6 = go.Figure(go.Pie(
        labels=status_df["Status"], values=status_df["Count"],
        hole=.60,
        marker=dict(colors=[scolors.get(s,"#64748b") for s in status_df["Status"]],
                    line=dict(color="#07090f", width=3)),
        textinfo="percent", textfont=dict(size=12, color="#dde3ed"),
        hovertemplate="<b>%{label}</b><br>%{value} claims · %{percent}<extra></extra>",
    ))
    fig6.add_annotation(
        text=f"<b>{n_claims:,}</b><br>claims",
        x=.5, y=.5, showarrow=False,
        font=dict(size=16, color="#dde3ed", family="Inter"), align="center",
    )
    fig6.update_layout(title="Claims Status Distribution", height=310,
                       showlegend=True, **_CT,
                    
                       )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION E — TEMPORAL TRENDS  (2 charts)
# ─────────────────────────────────────────────────────────────────────────────
sec("📈", "Temporal Trends",
    "Monthly expiry patterns and top listed food items", "si-o")

left4, right4 = st.columns(2)

# ── Chart 7: Monthly Expiry Trend (area line) ─────────────────────────────────
with left4:
    monthly = (food.groupby("Expiry_Month")
                   .agg(Listings=("Food_ID","count"), Qty=("Quantity","sum"))
                   .reset_index()
                   .sort_values("Expiry_Month"))

    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(
        x=monthly["Expiry_Month"], y=monthly["Listings"],
        fill="tozeroy", fillcolor="rgba(72,199,142,0.08)",
        line=dict(color="#48c78e", width=2.5),
        mode="lines+markers",
        marker=dict(color="#48c78e", size=7, line=dict(color="#07090f", width=2)),
        name="Listings",
        hovertemplate="<b>%{x|%b %Y}</b><br>Listings: %{y}<extra></extra>",
    ))
    fig7.add_trace(go.Scatter(
        x=monthly["Expiry_Month"], y=monthly["Qty"],
        yaxis="y2", fill="tozeroy", fillcolor="rgba(99,179,237,0.05)",
        line=dict(color="#63b3ed", width=2, dash="dot"),
        mode="lines", name="Quantity",
        hovertemplate="<b>%{x|%b %Y}</b><br>Qty: %{y:,}<extra></extra>",
    ))
    fig7.update_layout(
        title="Monthly Expiry Trend", height=300,
        yaxis=dict(title="Listings", gridcolor="rgba(255,255,255,0.04)",
                   tickfont=dict(color="#4d6070")),
        yaxis2=dict(title="Quantity", overlaying="y", side="right",
                    tickfont=dict(color="#63b3ed"), showgrid=False),
        hovermode="x unified",
        
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chart 8: Top 10 Most Listed Food Items (bar) ──────────────────────────────
with right4:
    top_items = (food["Food_Name"].value_counts()
                                 .head(10)
                                 .reset_index())
    top_items.columns = ["Food_Name", "Count"]
    top_items = top_items.sort_values("Count", ascending=True)

    fig8 = go.Figure(go.Bar(
        y=top_items["Food_Name"], x=top_items["Count"],
        orientation="h",
        marker=dict(
            color=top_items["Count"],
            colorscale=[[0,"#1c2d40"],[.5,"#a78bfa"],[1,"#48c78e"]],
            showscale=False,
            line=dict(color="rgba(255,255,255,0.04)", width=1),
        ),
        text=top_items["Count"], textposition="outside",
        textfont=dict(color="#7a8fa8", size=11),
        hovertemplate="<b>%{y}</b><br>Listings: %{x}<extra></extra>",
    ))
    fig8.update_layout(title="Top 10 Most Listed Food Items",
                       height=300, bargap=.3, **_CT,
                       )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION F — KEY INSIGHTS  (6 cards)
# ─────────────────────────────────────────────────────────────────────────────
sec("💡", "Key Insights",
    "Auto-generated findings from the filtered dataset", "si-g")

# ── Compute insight values ────────────────────────────────────────────────────
top_food_type   = food["Food_Type"].mode()[0]  if len(food) else "N/A"
top_meal_type   = food["Meal_Type"].mode()[0]  if len(food) else "N/A"
top_provider    = (food.groupby("Provider_Type")["Food_ID"].count().idxmax()
                   if len(food) else "N/A")
top_loc         = (food.groupby("Location")["Food_ID"].count().idxmax()
                   if len(food) else "N/A")
top_loc_cnt     = (food.groupby("Location")["Food_ID"].count().max()
                   if len(food) else 0)

food_type_pct   = (food["Food_Type"].value_counts(normalize=True).iloc[0]*100
                   if len(food) else 0)
meal_type_pct   = (food["Meal_Type"].value_counts(normalize=True).iloc[0]*100
                   if len(food) else 0)
ptype_cnt       = (food.groupby("Provider_Type")["Food_ID"].count().max()
                   if len(food) else 0)

def ins(icon, label, val, note, cls):
    return f"""<div class="ins ins-{cls}">
        <div class="ins-ico">{icon}</div>
        <div class="ins-label">{label}</div>
        <div class="ins-val">{val}</div>
        <div class="ins-note">{note}</div>
    </div>"""

i1,i2,i3,i4,i5,i6 = st.columns(6)
i1.markdown(ins("🥗","Top Food Type",
                top_food_type, f"{food_type_pct:.1f}% of listings","g"),
            unsafe_allow_html=True)
i2.markdown(ins("🍳","Top Meal Type",
                top_meal_type, f"{meal_type_pct:.1f}% of listings","b"),
            unsafe_allow_html=True)
i3.markdown(ins("🏭","Lead Provider",
                top_provider, f"{ptype_cnt:,} listings","v"),
            unsafe_allow_html=True)
i4.markdown(ins("📍","Top Location",
                top_loc[:17]+("…" if len(top_loc)>17 else ""),
                f"{top_loc_cnt} listings","o"),
            unsafe_allow_html=True)
i5.markdown(ins("✅","Completion Rate",
                f"{comp_rate:.1f}%", f"{completed:,} of {n_claims:,} claims","t"),
            unsafe_allow_html=True)
i6.markdown(ins("📦","Total Qty",
                f"{total_qty:,}", "Food units available","p"),
            unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION G — INTERACTIVE DATA EXPLORER
# ─────────────────────────────────────────────────────────────────────────────
sec("🔍", "Interactive Data Explorer",
    "Search, browse and export filtered food listings", "si-b")

# ── Search bar + download ────────────────────────────────────────────────────
s_col, dl_col = st.columns([4, 1])
with s_col:
    query = st.text_input(
        "Search", placeholder="Search food name or location…",
        label_visibility="collapsed"
    )

# ── Build display dataframe ───────────────────────────────────────────────────
display = food.copy()
if query:
    mask = (display["Food_Name"].str.contains(query, case=False, na=False) |
            display["Location"].str.contains(query, case=False, na=False))
    display = display[mask]

show_cols = ["Food_ID","Food_Name","Food_Type","Meal_Type",
             "Quantity","Provider_Type","Location","Expiry_Date"]
display = display[show_cols].copy()
display["Expiry_Date"] = display["Expiry_Date"].dt.strftime("%d %b %Y")
display = display.reset_index(drop=True)

st.markdown(
    f"<p style='font-size:.76rem;color:#374151;margin-bottom:.5rem;'>"
    f"Showing <b style='color:#48c78e'>{len(display):,}</b> records"
    + (f" matching <b style='color:#fb923c'>'{query}'</b>" if query else "")
    + "</p>",
    unsafe_allow_html=True,
)

st.dataframe(
    display,
    use_container_width=True,
    height=340,
    hide_index=True,
    column_config={
        "Food_ID":       st.column_config.NumberColumn("ID",       format="%d"),
        "Food_Name":     st.column_config.TextColumn("Food Name"),
        "Food_Type":     st.column_config.TextColumn("Type"),
        "Meal_Type":     st.column_config.TextColumn("Meal"),
        "Quantity":      st.column_config.NumberColumn("Qty",      format="%d"),
        "Provider_Type": st.column_config.TextColumn("Provider"),
        "Location":      st.column_config.TextColumn("Location"),
        "Expiry_Date":   st.column_config.TextColumn("Expiry"),
    },
)

with dl_col:
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.download_button(
        label="⬇ Export CSV",
        data=display.to_csv(index=False).encode("utf-8"),
        file_name="food_listings_export.csv",
        mime="text/csv",
    )


# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:1.4rem 0;
            border-top:1px solid rgba(255,255,255,0.045);">
    <span style="font-size:.76rem;color:#1e2d3d;">
        🌿 Local Food Wastage Management System &nbsp;·&nbsp;
        BSc Clinical Research Internship Project &nbsp;·&nbsp;
        Built with Streamlit &amp; Plotly
    </span>
</div>
""", unsafe_allow_html=True)