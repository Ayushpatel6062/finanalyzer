import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import requests

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="FinAnalyzer — AI-Powered Financial Analysis",
    page_icon="₣",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    /* Global */
    .stApp { background-color: #0B0E11; }
    section[data-testid="stSidebar"] { background-color: #141820; border-right: 1px solid #1E2530; }
    .stApp header { background-color: transparent !important; }

    /* Typography */
    h1, h2, h3, h4, h5, h6, p, li, span, div, label {
        font-family: 'DM Sans', -apple-system, sans-serif !important;
    }
    h1 { color: #E8ECF1 !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
    h2 { color: #E8ECF1 !important; font-weight: 700 !important; }
    h3 { color: #E8ECF1 !important; font-weight: 600 !important; }
    p, li { color: #7A8599 !important; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #161B24;
        border: 1px solid #1E2530;
        border-radius: 12px;
        padding: 18px 20px;
        transition: all 0.2s;
    }
    [data-testid="stMetric"]:hover {
        border-color: #2A6FDB;
        box-shadow: 0 0 20px rgba(42,111,219,0.12);
    }
    [data-testid="stMetricLabel"] p { color: #7A8599 !important; font-size: 12px !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.05em; }
    [data-testid="stMetricValue"] div { color: #E8ECF1 !important; font-size: 26px !important; font-weight: 700 !important; }
    [data-testid="stMetricDelta"] div { font-weight: 600 !important; }

    /* Tables */
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    table { background: #161B24 !important; }
    th { background: #141820 !important; color: #7A8599 !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.06em; }
    td { color: #E8ECF1 !important; border-bottom: 1px solid #1E253008 !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 2px; background: #141820; border-radius: 10px; padding: 3px; border: 1px solid #1E2530; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; color: #7A8599; font-weight: 500; padding: 8px 18px; }
    .stTabs [aria-selected="true"] { background: #2A6FDB !important; color: white !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2A6FDB, #A855F7) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 20px rgba(42,111,219,0.3);
        transition: all 0.3s;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 28px rgba(42,111,219,0.5);
        transform: translateY(-1px);
    }

    /* Inputs */
    .stNumberInput input, .stTextInput input {
        background: #141820 !important;
        border: 1px solid #1E2530 !important;
        color: #E8ECF1 !important;
        border-radius: 8px !important;
        font-family: 'DM Mono', monospace !important;
    }
    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: #2A6FDB !important;
        box-shadow: 0 0 0 1px #2A6FDB !important;
    }

    /* Expander */
    .streamlit-expanderHeader { background: #161B24 !important; border: 1px solid #1E2530 !important; border-radius: 10px !important; color: #E8ECF1 !important; }
    .streamlit-expanderContent { background: #161B24 !important; border: 1px solid #1E2530 !important; border-top: none !important; }

    /* Dividers */
    hr { border-color: #1E2530 !important; }

    /* Sidebar */
    section[data-testid="stSidebar"] .stRadio label { color: #E8ECF1 !important; }
    section[data-testid="stSidebar"] h1 { font-size: 22px !important; }
    section[data-testid="stSidebar"] .stRadio [role="radiogroup"] { gap: 4px; }

    /* Header bar */
    .header-bar {
        background: linear-gradient(135deg, #141820CC, #161B24CC);
        border: 1px solid #1E2530;
        border-radius: 14px;
        padding: 20px 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
    }
    .header-title {
        font-size: 28px; font-weight: 700; color: #E8ECF1;
        background: linear-gradient(135deg, #2A6FDB, #A855F7);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .header-sub { font-size: 13px; color: #7A8599; margin: 4px 0 0 0; }
    .ai-badge {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 4px 12px; border-radius: 8px; font-size: 11px; font-weight: 600;
        background: rgba(168,85,247,0.12); color: #A855F7;
    }
    .status-dot {
        width: 8px; height: 8px; border-radius: 50%; background: #22C55E;
        box-shadow: 0 0 8px rgba(34,197,94,0.4); display: inline-block;
    }

    /* Section cards */
    .section-card {
        background: #161B24;
        border: 1px solid #1E2530;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .ratio-header { font-size: 14px; font-weight: 600; margin: 0 0 14px 0; }

    /* AI Analysis */
    .ai-output {
        background: #141820;
        border: 1px solid #1E2530;
        border-radius: 12px;
        padding: 24px;
        position: relative;
        overflow: hidden;
        color: #7A8599;
        line-height: 1.7;
        font-size: 14px;
    }
    .ai-output::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #2A6FDB, #A855F7, #06B6D4);
    }

    /* Hide default streamlit elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── SAMPLE DATA ───
def get_default_data():
    return {
        "companyName": "TechVision Inc.",
        "years": ["2021", "2022", "2023"],
        "incomeStatement": {
            "revenue": [2450000, 3180000, 4025000],
            "cogs": [980000, 1240000, 1530000],
            "grossProfit": [1470000, 1940000, 2495000],
            "operatingExpenses": [735000, 890000, 1050000],
            "operatingIncome": [735000, 1050000, 1445000],
            "interestExpense": [45000, 52000, 48000],
            "taxExpense": [172500, 249500, 349250],
            "netIncome": [517500, 748500, 1047750],
            "ebitda": [860000, 1210000, 1625000],
            "depreciation": [125000, 160000, 180000],
        },
        "balanceSheet": {
            "cash": [450000, 620000, 890000],
            "accountsReceivable": [310000, 405000, 520000],
            "inventory": [185000, 230000, 275000],
            "totalCurrentAssets": [945000, 1255000, 1685000],
            "ppe": [1200000, 1450000, 1680000],
            "totalAssets": [2345000, 2955000, 3665000],
            "accountsPayable": [220000, 285000, 340000],
            "shortTermDebt": [150000, 180000, 120000],
            "totalCurrentLiabilities": [370000, 465000, 460000],
            "longTermDebt": [500000, 450000, 380000],
            "totalLiabilities": [870000, 915000, 840000],
            "totalEquity": [1475000, 2040000, 2825000],
            "retainedEarnings": [875000, 1440000, 2225000],
        },
        "cashFlow": {
            "operatingCashFlow": [680000, 920000, 1280000],
            "capitalExpenditures": [250000, 310000, 350000],
            "freeCashFlow": [430000, 610000, 930000],
            "dividendsPaid": [100000, 125000, 150000],
            "netCashFlow": [180000, 170000, 270000],
        },
    }


# ─── UTILITY FUNCTIONS ───
def fmt(n):
    if n is None or pd.isna(n): return "N/A"
    if abs(n) >= 1e6: return f"${n/1e6:.1f}M"
    if abs(n) >= 1e3: return f"${n/1e3:.1f}K"
    return f"${n:.0f}"

def pct(n):
    if n is None or pd.isna(n): return "N/A"
    return f"{n*100:.1f}%"

def rat(n):
    if n is None or pd.isna(n): return "N/A"
    return f"{n:.2f}"

def safe_div(a, b):
    if b == 0 or b is None: return None
    return a / b


# ─── CALCULATE RATIOS ───
def calculate_ratios(data):
    ratios = []
    for i in range(len(data["years"])):
        IS = data["incomeStatement"]
        BS = data["balanceSheet"]
        CF = data["cashFlow"]
        r = {
            "Year": data["years"][i],
            # Profitability
            "Gross Margin": safe_div(IS["grossProfit"][i], IS["revenue"][i]),
            "Operating Margin": safe_div(IS["operatingIncome"][i], IS["revenue"][i]),
            "Net Margin": safe_div(IS["netIncome"][i], IS["revenue"][i]),
            "EBITDA Margin": safe_div(IS["ebitda"][i], IS["revenue"][i]),
            "ROE": safe_div(IS["netIncome"][i], BS["totalEquity"][i]),
            "ROA": safe_div(IS["netIncome"][i], BS["totalAssets"][i]),
            # Liquidity
            "Current Ratio": safe_div(BS["totalCurrentAssets"][i], BS["totalCurrentLiabilities"][i]),
            "Quick Ratio": safe_div(BS["totalCurrentAssets"][i] - BS["inventory"][i], BS["totalCurrentLiabilities"][i]),
            "Cash Ratio": safe_div(BS["cash"][i], BS["totalCurrentLiabilities"][i]),
            # Leverage
            "Debt/Equity": safe_div(BS["totalLiabilities"][i], BS["totalEquity"][i]),
            "Debt/Assets": safe_div(BS["totalLiabilities"][i], BS["totalAssets"][i]),
            "Interest Coverage": safe_div(IS["operatingIncome"][i], IS["interestExpense"][i]),
            # Efficiency
            "Asset Turnover": safe_div(IS["revenue"][i], BS["totalAssets"][i]),
            "Receivables Turnover": safe_div(IS["revenue"][i], BS["accountsReceivable"][i]),
            "DSO": safe_div(BS["accountsReceivable"][i] * 365, IS["revenue"][i]),
            "Inventory Turnover": safe_div(IS["cogs"][i], BS["inventory"][i]),
            # Cash Flow
            "Operating CF Margin": safe_div(CF["operatingCashFlow"][i], IS["revenue"][i]),
            "FCF Margin": safe_div(CF["freeCashFlow"][i], IS["revenue"][i]),
            "FCF/Net Income": safe_div(CF["freeCashFlow"][i], IS["netIncome"][i]),
            # Growth
            "Revenue Growth": safe_div(IS["revenue"][i] - IS["revenue"][i-1], IS["revenue"][i-1]) if i > 0 else None,
            "Net Income Growth": safe_div(IS["netIncome"][i] - IS["netIncome"][i-1], IS["netIncome"][i-1]) if i > 0 else None,
            "EBITDA Growth": safe_div(IS["ebitda"][i] - IS["ebitda"][i-1], IS["ebitda"][i-1]) if i > 0 else None,
            # Raw
            "Revenue": IS["revenue"][i],
            "Net Income": IS["netIncome"][i],
            "EBITDA": IS["ebitda"][i],
            "Total Assets": BS["totalAssets"][i],
            "Total Liabilities": BS["totalLiabilities"][i],
            "Total Equity": BS["totalEquity"][i],
            "Operating CF": CF["operatingCashFlow"][i],
            "Free CF": CF["freeCashFlow"][i],
            "CapEx": CF["capitalExpenditures"][i],
        }
        ratios.append(r)
    return ratios


# ─── CHART HELPERS ───
COLORS = {
    "accent": "#2A6FDB", "green": "#22C55E", "red": "#EF4444",
    "amber": "#F59E0B", "purple": "#A855F7", "cyan": "#06B6D4",
    "bg": "#0B0E11", "card": "#161B24", "border": "#1E2530",
    "text": "#E8ECF1", "muted": "#7A8599",
}
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(22,27,36,0.6)",
    font=dict(family="DM Sans", color="#7A8599", size=12),
    margin=dict(l=50, r=20, t=40, b=40),
    xaxis=dict(gridcolor="#1E2530", showline=False),
    yaxis=dict(gridcolor="#1E2530", showline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    hoverlabel=dict(bgcolor="#141820", bordercolor="#1E2530", font=dict(family="DM Sans")),
)

def make_revenue_chart(ratios):
    years = [r["Year"] for r in ratios]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=[r["Revenue"] for r in ratios], mode="lines+markers", name="Revenue",
        line=dict(color=COLORS["accent"], width=3), fill="tozeroy", fillcolor="rgba(42,111,219,0.1)", marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=years, y=[r["Net Income"] for r in ratios], mode="lines+markers", name="Net Income",
        line=dict(color=COLORS["green"], width=3), fill="tozeroy", fillcolor="rgba(34,197,94,0.1)", marker=dict(size=8)))
    fig.update_layout(**CHART_LAYOUT, title="Revenue & Net Income Trend", yaxis_tickprefix="$")
    return fig

def make_margins_chart(ratios):
    years = [r["Year"] for r in ratios]
    fig = go.Figure()
    for name, color in [("Gross Margin", COLORS["green"]), ("Operating Margin", COLORS["accent"]),
                         ("Net Margin", COLORS["amber"]), ("EBITDA Margin", COLORS["purple"])]:
        vals = [r[name]*100 if r[name] else 0 for r in ratios]
        fig.add_trace(go.Scatter(x=years, y=vals, mode="lines+markers", name=name,
            line=dict(color=color, width=2.5), marker=dict(size=7)))
    fig.update_layout(**CHART_LAYOUT, title="Profitability Margins (%)", yaxis_ticksuffix="%")
    return fig

def make_balance_chart(ratios):
    years = [r["Year"] for r in ratios]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=years, y=[r["Total Assets"] for r in ratios], name="Total Assets", marker_color=COLORS["accent"], marker_cornerradius=6))
    fig.add_trace(go.Bar(x=years, y=[r["Total Liabilities"] for r in ratios], name="Total Liabilities", marker_color=COLORS["red"], marker_cornerradius=6))
    fig.add_trace(go.Bar(x=years, y=[r["Total Equity"] for r in ratios], name="Total Equity", marker_color=COLORS["green"], marker_cornerradius=6))
    fig.update_layout(**CHART_LAYOUT, title="Balance Sheet Composition", barmode="group", yaxis_tickprefix="$")
    return fig

def make_cashflow_chart(ratios):
    years = [r["Year"] for r in ratios]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=years, y=[r["Operating CF"] for r in ratios], name="Operating CF", marker_color=COLORS["accent"], marker_cornerradius=6))
    fig.add_trace(go.Bar(x=years, y=[r["Free CF"] for r in ratios], name="Free CF", marker_color=COLORS["green"], marker_cornerradius=6))
    fig.add_trace(go.Bar(x=years, y=[r["CapEx"] for r in ratios], name="CapEx", marker_color=COLORS["amber"], marker_cornerradius=6))
    fig.update_layout(**CHART_LAYOUT, title="Cash Flow Analysis", barmode="group", yaxis_tickprefix="$")
    return fig

def make_radar_chart(latest):
    categories = ["Profitability", "Liquidity", "Solvency", "Efficiency", "Cash Flow", "Growth"]
    values = [
        min((latest["Net Margin"] or 0) * 100 / 30 * 100, 100),
        min((latest["Current Ratio"] or 0) / 3 * 100, 100),
        min((1 - (latest["Debt/Assets"] or 0)) * 100, 100),
        min((latest["Asset Turnover"] or 0) / 2 * 100, 100),
        min((latest["FCF Margin"] or 0) * 100 / 25 * 100, 100),
        min((latest["Revenue Growth"] or 0) * 100 / 40 * 100, 100),
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]],
        fill="toself", fillcolor="rgba(42,111,219,0.15)", line=dict(color=COLORS["accent"], width=2),
        marker=dict(size=6, color=COLORS["accent"])))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans", color="#7A8599", size=11),
        margin=dict(l=60, r=60, t=40, b=40), title="Financial Health Radar",
        polar=dict(
            bgcolor="rgba(22,27,36,0.6)",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="#1E2530"),
            angularaxis=dict(gridcolor="#1E2530", linecolor="#1E2530"),
        ),
    )
    return fig

def make_asset_pie(data):
    i = len(data["years"]) - 1
    bs = data["balanceSheet"]
    labels = ["Cash", "Receivables", "Inventory", "PP&E", "Other"]
    other = max(0, bs["totalAssets"][i] - bs["totalCurrentAssets"][i] - bs["ppe"][i])
    values = [bs["cash"][i], bs["accountsReceivable"][i], bs["inventory"][i], bs["ppe"][i], other]
    colors = [COLORS["accent"], COLORS["green"], COLORS["amber"], COLORS["purple"], COLORS["cyan"]]
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.55, marker=dict(colors=colors, line=dict(color="#0B0E11", width=2)),
        textfont=dict(color="#E8ECF1", size=12), textinfo="label+percent"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans", color="#7A8599"),
        margin=dict(l=20, r=20, t=40, b=20), title="Asset Composition (Latest Year)",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)))
    return fig


# ─── INIT SESSION STATE ───
if "data" not in st.session_state:
    st.session_state.data = get_default_data()
if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = ""

data = st.session_state.data
ratios = calculate_ratios(data)
latest = ratios[-1] if ratios else {}


# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
        <div style="width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;
            background:linear-gradient(135deg,#2A6FDB,#A855F7);font-size:18px;font-weight:700;color:white;">₣</div>
        <div>
            <div style="font-size:18px;font-weight:700;color:#E8ECF1;letter-spacing:-0.02em;">FinAnalyzer</div>
            <div style="font-size:10px;color:#7A8599;text-transform:uppercase;letter-spacing:0.08em;">AI-Powered Analysis</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""<div style="display:flex;align-items:center;gap:6px;margin:12px 0 20px;">
        <span class="status-dot"></span>
        <span style="font-size:11px;color:#7A8599;">AI Online</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio("**Navigation**", [
        "📊 Dashboard",
        "📐 Financial Ratios",
        "📈 Charts",
        "✦ AI Analysis",
        "✏️ Edit Data",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"**Company:** {data['companyName']}")
    st.markdown(f"**Period:** {data['years'][0]} – {data['years'][-1]}")
    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px;color:#4A5568;margin-top:20px;">
        Built by Ayush<br>Powered by Claude AI
    </div>
    """, unsafe_allow_html=True)


# ─── HEADER ───
st.markdown(f"""
<div class="header-bar">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
        <div>
            <p class="header-title">₣ FinAnalyzer</p>
            <p class="header-sub">AI-Powered Financial Statement Analysis • {data['companyName']}</p>
        </div>
        <div class="ai-badge">✦ Powered by Claude AI</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# 📊 DASHBOARD
# ═══════════════════════════════════════════════
if page == "📊 Dashboard":
    st.markdown(f"### Executive Dashboard")
    st.caption(f"Financial overview for {data['companyName']} ({data['years'][0]}–{data['years'][-1]})")

    # KPI Row 1
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        delta_rev = f"{latest['Revenue Growth']*100:.1f}%" if latest.get("Revenue Growth") else None
        st.metric("💰 Revenue", fmt(latest["Revenue"]), delta=delta_rev)
    with c2:
        delta_ni = f"{latest['Net Income Growth']*100:.1f}%" if latest.get("Net Income Growth") else None
        st.metric("📈 Net Income", fmt(latest["Net Income"]), delta=delta_ni)
    with c3:
        delta_eb = f"{latest['EBITDA Growth']*100:.1f}%" if latest.get("EBITDA Growth") else None
        st.metric("⚡ EBITDA", fmt(latest["EBITDA"]), delta=delta_eb)
    with c4:
        st.metric("🏦 Free Cash Flow", fmt(latest["Free CF"]))

    # KPI Row 2
    c5, c6, c7, c8 = st.columns(4)
    with c5: st.metric("📊 Net Margin", pct(latest["Net Margin"]))
    with c6: st.metric("🎯 ROE", pct(latest["ROE"]))
    with c7: st.metric("💧 Current Ratio", rat(latest["Current Ratio"]))
    with c8: st.metric("⚖️ Debt / Equity", rat(latest["Debt/Equity"]))

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Charts Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_revenue_chart(ratios), use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(make_radar_chart(latest), use_container_width=True, config={"displayModeBar": False})

    # Charts Row 2
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(make_margins_chart(ratios), use_container_width=True, config={"displayModeBar": False})
    with col4:
        st.plotly_chart(make_asset_pie(data), use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════
# 📐 FINANCIAL RATIOS
# ═══════════════════════════════════════════════
elif page == "📐 Financial Ratios":
    st.markdown("### Financial Ratios")
    st.caption("Comprehensive ratio analysis across all periods")

    ratio_groups = [
        ("🔵 Profitability Ratios", ["Gross Margin", "Operating Margin", "Net Margin", "EBITDA Margin", "ROE", "ROA"], pct),
        ("🟢 Liquidity Ratios", ["Current Ratio", "Quick Ratio", "Cash Ratio"], rat),
        ("🟡 Leverage Ratios", ["Debt/Equity", "Debt/Assets"], rat),
        ("🟢 Efficiency Ratios", ["Asset Turnover", "Receivables Turnover", "Inventory Turnover"], rat),
        ("🟣 Cash Flow Ratios", ["Operating CF Margin", "FCF Margin", "FCF/Net Income"], None),
        ("🔴 Growth Metrics", ["Revenue Growth", "Net Income Growth", "EBITDA Growth"], pct),
    ]

    for group_name, metrics, formatter in ratio_groups:
        st.markdown(f"<div class='section-card'><p class='ratio-header' style='color:#E8ECF1;'>{group_name}</p></div>", unsafe_allow_html=True)

        rows = []
        for m in metrics:
            row = {"Metric": m}
            for r in ratios:
                val = r.get(m)
                if val is None:
                    row[r["Year"]] = "—"
                elif formatter == pct:
                    row[r["Year"]] = pct(val)
                elif formatter == rat:
                    row[r["Year"]] = rat(val)
                elif m == "DSO" and val is not None:
                    row[r["Year"]] = f"{val:.0f} days"
                elif "Interest Coverage" in m and val is not None:
                    row[r["Year"]] = f"{val:.2f}x"
                elif m in ["Operating CF Margin", "FCF Margin"]:
                    row[r["Year"]] = pct(val)
                else:
                    row[r["Year"]] = rat(val)
            rows.append(row)

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Interest Coverage separately
    st.markdown("<div class='section-card'><p class='ratio-header' style='color:#E8ECF1;'>🟡 Interest Coverage</p></div>", unsafe_allow_html=True)
    ic_rows = [{"Metric": "Interest Coverage"}]
    for r in ratios:
        val = r.get("Interest Coverage")
        ic_rows[0][r["Year"]] = f"{val:.2f}x" if val else "N/A"
    st.dataframe(pd.DataFrame(ic_rows), use_container_width=True, hide_index=True)

    # DSO
    st.markdown("<div class='section-card'><p class='ratio-header' style='color:#E8ECF1;'>📅 Days Sales Outstanding</p></div>", unsafe_allow_html=True)
    dso_rows = [{"Metric": "DSO"}]
    for r in ratios:
        val = r.get("DSO")
        dso_rows[0][r["Year"]] = f"{val:.0f} days" if val else "N/A"
    st.dataframe(pd.DataFrame(dso_rows), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════
# 📈 CHARTS
# ═══════════════════════════════════════════════
elif page == "📈 Charts":
    st.markdown("### Visual Analytics")
    st.caption("Interactive charts and visualizations")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_revenue_chart(ratios), use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(make_margins_chart(ratios), use_container_width=True, config={"displayModeBar": False})

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(make_balance_chart(ratios), use_container_width=True, config={"displayModeBar": False})
    with col4:
        st.plotly_chart(make_cashflow_chart(ratios), use_container_width=True, config={"displayModeBar": False})

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(make_radar_chart(latest), use_container_width=True, config={"displayModeBar": False})
    with col6:
        st.plotly_chart(make_asset_pie(data), use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════
# ✦ AI ANALYSIS
# ═══════════════════════════════════════════════
elif page == "✦ AI Analysis":
    st.markdown("### ✦ AI-Powered Analysis")
    st.caption("Deep financial analysis powered by Claude AI")

    col_btn, col_status = st.columns([1, 3])
    with col_btn:
        run_ai = st.button("✦ Generate AI Analysis", use_container_width=True)

    if run_ai:
        with st.spinner("🔮 Claude AI is analyzing financial statements..."):
            prompt = f"""You are an expert financial analyst. Analyze the following financial data for {data['companyName']} and provide a comprehensive, actionable analysis.

FINANCIAL DATA ({', '.join(data['years'])}):
Revenue: {' → '.join([fmt(x) for x in data['incomeStatement']['revenue']])}
Net Income: {' → '.join([fmt(x) for x in data['incomeStatement']['netIncome']])}
EBITDA: {' → '.join([fmt(x) for x in data['incomeStatement']['ebitda']])}
Total Assets: {' → '.join([fmt(x) for x in data['balanceSheet']['totalAssets']])}
Total Equity: {' → '.join([fmt(x) for x in data['balanceSheet']['totalEquity']])}
Free Cash Flow: {' → '.join([fmt(x) for x in data['cashFlow']['freeCashFlow']])}

KEY RATIOS (Latest - {latest['Year']}):
Gross Margin: {pct(latest['Gross Margin'])} | Operating Margin: {pct(latest['Operating Margin'])} | Net Margin: {pct(latest['Net Margin'])}
ROE: {pct(latest['ROE'])} | ROA: {pct(latest['ROA'])} | Current Ratio: {rat(latest['Current Ratio'])}
D/E: {rat(latest['Debt/Equity'])} | Interest Coverage: {rat(latest['Interest Coverage'])}x
Revenue Growth: {pct(latest['Revenue Growth'])} | FCF Margin: {pct(latest['FCF Margin'])}

Provide:
1. **Executive Summary** (2-3 sentences)
2. **Profitability Analysis**
3. **Liquidity & Solvency Assessment**
4. **Growth Trajectory**
5. **Cash Flow Quality**
6. **Key Risks & Red Flags**
7. **Strategic Recommendations** (3-5 actionable items)
8. **Overall Rating** (Strong Buy / Buy / Hold / Sell / Strong Sell) with justification

Be specific with numbers and concise. Use markdown formatting."""

            try:
                api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
                if not api_key:
                    st.session_state.ai_analysis = """## ⚠️ API Key Required

To enable AI-powered analysis, add your Anthropic API key to Streamlit secrets:

1. Go to your Streamlit Cloud app settings
2. Click **Secrets** in the left sidebar
3. Add: `ANTHROPIC_API_KEY = "your-api-key-here"`
4. Save and rerun

---

**Demo Analysis (Sample)**

### 1. Executive Summary
TechVision Inc. demonstrates exceptional financial performance with consistent growth across all metrics. Revenue grew 64.3% over two years while maintaining healthy margins and a strong balance sheet with declining leverage.

### 2. Profitability Analysis
- Gross margin stable at ~62%, indicating strong pricing power
- Operating margin improved from 30.0% to 35.9%, showing operational leverage
- Net margin expanded from 21.1% to 26.0%, reflecting efficient cost management
- EBITDA margin at 40.4% — well above industry averages

### 3. Liquidity & Solvency Assessment
- Current ratio of 3.66x provides ample short-term liquidity buffer
- Debt-to-Equity of 0.30x is conservative and declining year-over-year
- Interest coverage of 30.1x — no debt servicing concerns

### 4. Growth Trajectory
- Revenue CAGR of ~28% over the analysis period
- Net income growth of 40.0% YoY in the latest year
- Growth is accelerating, not decelerating — a very positive signal

### 5. Cash Flow Quality
- FCF margin of 23.1% is excellent
- FCF/Net Income ratio of 0.89x indicates high earnings quality
- Operating cash flow consistently exceeds net income

### 6. Key Risks & Red Flags
- Rapid growth may strain operational capacity
- Accounts receivable growing faster than revenue (potential collection risk)
- Limited debt could mean underutilization of leverage for growth

### 7. Strategic Recommendations
1. **Invest in scalable infrastructure** to support continued 25%+ growth
2. **Monitor DSO trends** — ensure receivables collection keeps pace
3. **Consider strategic debt** for M&A or R&D investment at current low leverage
4. **Maintain dividend discipline** — current payout ratio is conservative
5. **Explore international expansion** given strong domestic performance

### 8. Overall Rating: **Strong Buy** ⭐⭐⭐⭐⭐
Exceptional profitability, accelerating growth, conservative balance sheet, and strong cash generation make TechVision a compelling investment opportunity."""
                else:
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "Content-Type": "application/json",
                            "x-api-key": api_key,
                            "anthropic-version": "2023-06-01",
                        },
                        json={
                            "model": "claude-sonnet-4-20250514",
                            "max_tokens": 2000,
                            "messages": [{"role": "user", "content": prompt}],
                        },
                    )
                    result = response.json()
                    if "content" in result:
                        st.session_state.ai_analysis = "\n".join(
                            [c.get("text", "") for c in result["content"]]
                        )
                    else:
                        st.session_state.ai_analysis = f"Error: {result.get('error', {}).get('message', 'Unknown error')}"
            except Exception as e:
                st.session_state.ai_analysis = f"Connection error: {str(e)}\n\nPlease check your API key and try again."

    if st.session_state.ai_analysis:
        st.markdown(f"""<div class="ai-output"></div>""", unsafe_allow_html=True)
        st.markdown(st.session_state.ai_analysis)
    else:
        st.markdown("""
        <div style="background:#141820;border:1px dashed #1E2530;border-radius:12px;padding:48px;text-align:center;">
            <div style="font-size:40px;margin-bottom:12px;opacity:0.3;">✦</div>
            <p style="color:#7A8599;font-size:14px;margin:0;">Click "Generate AI Analysis" for a comprehensive financial assessment powered by Claude AI</p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# ✏️ EDIT DATA
# ═══════════════════════════════════════════════
elif page == "✏️ Edit Data":
    st.markdown("### ✏️ Financial Data Input")
    st.caption("Edit company financials below. Derived fields auto-calculate on save.")

    # Company Name
    new_name = st.text_input("Company Name", value=data["companyName"])
    if new_name != data["companyName"]:
        st.session_state.data["companyName"] = new_name

    tab1, tab2, tab3 = st.tabs(["📋 Income Statement", "📊 Balance Sheet", "💰 Cash Flow"])

    with tab1:
        st.markdown("##### Income Statement")
        fields = [
            ("revenue", "Revenue"), ("cogs", "Cost of Goods Sold"),
            ("operatingExpenses", "Operating Expenses"), ("interestExpense", "Interest Expense"),
            ("taxExpense", "Tax Expense"), ("depreciation", "Depreciation & Amortization"),
        ]
        for key, label in fields:
            cols = st.columns([2] + [1]*len(data["years"]))
            cols[0].markdown(f"**{label}**")
            for yi, year in enumerate(data["years"]):
                new_val = cols[yi+1].number_input(
                    f"{label} {year}", value=data["incomeStatement"][key][yi],
                    key=f"is_{key}_{yi}", label_visibility="collapsed", step=1000
                )
                if new_val != data["incomeStatement"][key][yi]:
                    st.session_state.data["incomeStatement"][key][yi] = new_val
                    IS = st.session_state.data["incomeStatement"]
                    IS["grossProfit"][yi] = IS["revenue"][yi] - IS["cogs"][yi]
                    IS["operatingIncome"][yi] = IS["grossProfit"][yi] - IS["operatingExpenses"][yi]
                    IS["netIncome"][yi] = IS["operatingIncome"][yi] - IS["interestExpense"][yi] - IS["taxExpense"][yi]
                    IS["ebitda"][yi] = IS["operatingIncome"][yi] + IS["depreciation"][yi]

    with tab2:
        st.markdown("##### Balance Sheet")
        fields = [
            ("cash", "Cash & Equivalents"), ("accountsReceivable", "Accounts Receivable"),
            ("inventory", "Inventory"), ("ppe", "PP&E"), ("totalAssets", "Total Assets"),
            ("accountsPayable", "Accounts Payable"), ("shortTermDebt", "Short-Term Debt"),
            ("longTermDebt", "Long-Term Debt"), ("totalEquity", "Total Equity"),
            ("retainedEarnings", "Retained Earnings"),
        ]
        for key, label in fields:
            cols = st.columns([2] + [1]*len(data["years"]))
            cols[0].markdown(f"**{label}**")
            for yi, year in enumerate(data["years"]):
                new_val = cols[yi+1].number_input(
                    f"{label} {year}", value=data["balanceSheet"][key][yi],
                    key=f"bs_{key}_{yi}", label_visibility="collapsed", step=1000
                )
                if new_val != data["balanceSheet"][key][yi]:
                    st.session_state.data["balanceSheet"][key][yi] = new_val
                    BS = st.session_state.data["balanceSheet"]
                    BS["totalCurrentAssets"][yi] = BS["cash"][yi] + BS["accountsReceivable"][yi] + BS["inventory"][yi]
                    BS["totalCurrentLiabilities"][yi] = BS["accountsPayable"][yi] + BS["shortTermDebt"][yi]
                    BS["totalLiabilities"][yi] = BS["totalCurrentLiabilities"][yi] + BS["longTermDebt"][yi]

    with tab3:
        st.markdown("##### Cash Flow Statement")
        fields = [
            ("operatingCashFlow", "Operating Cash Flow"), ("capitalExpenditures", "Capital Expenditures"),
            ("dividendsPaid", "Dividends Paid"), ("netCashFlow", "Net Cash Flow"),
        ]
        for key, label in fields:
            cols = st.columns([2] + [1]*len(data["years"]))
            cols[0].markdown(f"**{label}**")
            for yi, year in enumerate(data["years"]):
                new_val = cols[yi+1].number_input(
                    f"{label} {year}", value=data["cashFlow"][key][yi],
                    key=f"cf_{key}_{yi}", label_visibility="collapsed", step=1000
                )
                if new_val != data["cashFlow"][key][yi]:
                    st.session_state.data["cashFlow"][key][yi] = new_val
                    CF = st.session_state.data["cashFlow"]
                    CF["freeCashFlow"][yi] = CF["operatingCashFlow"][yi] - CF["capitalExpenditures"][yi]

    st.markdown("---")
    if st.button("🔄 Reset to Sample Data"):
        st.session_state.data = get_default_data()
        st.rerun()


# ─── FOOTER ───
st.markdown("---")
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;">
    <span style="font-size:11px;color:#4A5568;">FinAnalyzer — AI-Powered Financial Statement Analysis</span>
    <span style="font-size:11px;color:#4A5568;">Built by Ayush • Powered by Claude AI</span>
</div>
""", unsafe_allow_html=True)
