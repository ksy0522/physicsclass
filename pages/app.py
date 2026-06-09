import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Top 10 Market Cap",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global Top 10 tickers ─────────────────────────────────────────────────────
TOP10 = {
    "Apple":      "AAPL",
    "NVIDIA":     "NVDA",
    "Microsoft":  "MSFT",
    "Amazon":     "AMZN",
    "Alphabet":   "GOOGL",
    "Saudi Aramco": "2222.SR",
    "Meta":       "META",
    "Berkshire":  "BRK-B",
    "TSMC":       "TSM",
    "Broadcom":   "AVGO",
}

SECTOR_COLORS = {
    "Apple":       "#2196F3",
    "NVIDIA":      "#76B900",
    "Microsoft":   "#00A4EF",
    "Amazon":      "#FF9900",
    "Alphabet":    "#EA4335",
    "Saudi Aramco":"#0D7B3E",
    "Meta":        "#1877F2",
    "Berkshire":   "#6D4C41",
    "TSMC":        "#CE0000",
    "Broadcom":    "#CC0000",
}

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: #0A0E1A;
    }
    .main-header {
        padding: 2rem 0 1rem 0;
        border-bottom: 1px solid #1E2D40;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #E8EDF5;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .main-subtitle {
        font-size: 0.85rem;
        color: #4A6080;
        font-weight: 400;
        margin-top: 4px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .metric-card {
        background: #0F1626;
        border: 1px solid #1E2D40;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.5rem;
    }
    .metric-ticker {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #4A6080;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .metric-name {
        font-size: 1rem;
        font-weight: 600;
        color: #C8D8EC;
        margin: 2px 0 6px 0;
    }
    .metric-price {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.4rem;
        font-weight: 600;
        color: #E8EDF5;
    }
    .metric-change-pos {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #00D4AA;
        font-weight: 500;
    }
    .metric-change-neg {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #FF4D6A;
        font-weight: 500;
    }
    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #8BA5C4;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1E2D40;
    }
    .status-bar {
        font-size: 0.75rem;
        color: #4A6080;
        text-align: right;
        padding: 0.5rem 0;
    }
    [data-testid="stSidebar"] {
        background: #0A0E1A;
        border-right: 1px solid #1E2D40;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #8BA5C4;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: #E8EDF5;
    }
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #1E2D40;
    }
    .plotly-chart-container {
        border: 1px solid #1E2D40;
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ── Data fetching ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=1800)
def fetch_price_data(tickers: list[str], period: str = "1y") -> pd.DataFrame:
    raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]]
    return close


@st.cache_data(ttl=3600)
def fetch_current_info(ticker: str) -> dict:
    try:
        t = yf.Ticker(ticker)
        info = t.info
        return {
            "price":       info.get("currentPrice") or info.get("regularMarketPrice", 0),
            "market_cap":  info.get("marketCap", 0),
            "pe":          info.get("trailingPE", None),
            "week52_high": info.get("fiftyTwoWeekHigh", None),
            "week52_low":  info.get("fiftyTwoWeekLow", None),
        }
    except Exception:
        return {}


def compute_normalized(df: pd.DataFrame) -> pd.DataFrame:
    return (df / df.iloc[0]) * 100


def human_market_cap(val: float) -> str:
    if val >= 1e12:
        return f"${val/1e12:.2f}T"
    if val >= 1e9:
        return f"${val/1e9:.1f}B"
    return f"${val:,.0f}"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    period_map = {"1 Month": "1mo", "3 Months": "3mo", "6 Months": "6mo", "1 Year": "1y"}
    selected_period_label = st.selectbox("Period", list(period_map.keys()), index=3)
    selected_period = period_map[selected_period_label]

    chart_type = st.selectbox("Chart Type", ["Normalized (Base 100)", "Absolute Price", "Candlestick"])

    selected_names = st.multiselect(
        "Companies",
        list(TOP10.keys()),
        default=list(TOP10.keys()),
    )

    st.markdown("---")
    st.markdown("""
    **Data source:** Yahoo Finance  
    **Refresh:** Every 30 min  
    **Universe:** Global Market Cap Top 10  
    """)

if not selected_names:
    st.warning("Please select at least one company from the sidebar.")
    st.stop()

selected_tickers = [TOP10[n] for n in selected_names]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-title">📈 Global Market Cap — Top 10</div>
    <div class="main-subtitle">1-Year Stock Performance · Powered by Yahoo Finance</div>
</div>
""", unsafe_allow_html=True)

# ── Fetch data ────────────────────────────────────────────────────────────────
with st.spinner("Fetching market data…"):
    price_df = fetch_price_data(selected_tickers, period=selected_period)

# Align column names: yfinance may return plain tickers
price_df.columns = [str(c) for c in price_df.columns]
ticker_to_name = {v: k for k, v in TOP10.items()}

# ── KPI row ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Snapshot</div>', unsafe_allow_html=True)
kpi_cols = st.columns(min(len(selected_names), 5))

for i, name in enumerate(selected_names[:10]):
    ticker = TOP10[name]
    col = kpi_cols[i % 5]
    with col:
        try:
            series = price_df[ticker].dropna()
            if len(series) >= 2:
                latest = series.iloc[-1]
                prev   = series.iloc[-2]
                pct    = (latest - prev) / prev * 100
                ytd_pct = (series.iloc[-1] - series.iloc[0]) / series.iloc[0] * 100
                chg_class = "metric-change-pos" if pct >= 0 else "metric-change-neg"
                arrow = "▲" if pct >= 0 else "▼"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-ticker">{ticker}</div>
                    <div class="metric-name">{name}</div>
                    <div class="metric-price">${latest:,.2f}</div>
                    <div class="{chg_class}">{arrow} {abs(pct):.2f}% today &nbsp;|&nbsp; {'+' if ytd_pct>=0 else ''}{ytd_pct:.1f}% period</div>
                </div>
                """, unsafe_allow_html=True)
        except Exception:
            st.markdown(f'<div class="metric-card"><div class="metric-name">{name}</div></div>', unsafe_allow_html=True)

# ── Main chart ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Price Chart</div>', unsafe_allow_html=True)

DARK_BG   = "#0A0E1A"
DARK_GRID = "#1E2D40"
DARK_TEXT = "#8BA5C4"

def apply_layout(fig, hovermode="x unified", height=None, margin=None, title_text=None, extra=None):
    """Apply the shared dark theme layout to a Plotly figure."""
    kwargs = dict(
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        font=dict(family="Inter, sans-serif", color=DARK_TEXT, size=12),
        xaxis=dict(gridcolor=DARK_GRID, zerolinecolor=DARK_GRID, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=DARK_GRID, zerolinecolor=DARK_GRID, tickfont=dict(size=11)),
        legend=dict(
            bgcolor="#0F1626", bordercolor=DARK_GRID, borderwidth=1,
            font=dict(size=11, color="#C8D8EC"),
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
        ),
        hovermode=hovermode,
        hoverlabel=dict(bgcolor="#0F1626", bordercolor=DARK_GRID, font_color="#E8EDF5"),
        margin=margin if margin else dict(l=0, r=0, t=40, b=0),
    )
    if height:
        kwargs["height"] = height
    if title_text:
        kwargs["title"] = dict(text=title_text, font_color="#C8D8EC", font_size=14)
    if extra:
        kwargs.update(extra)
    fig.update_layout(**kwargs)
    return fig

if chart_type == "Normalized (Base 100)":
    norm_df = compute_normalized(price_df[selected_tickers].dropna(how="all"))
    fig = go.Figure()
    for name in selected_names:
        ticker = TOP10[name]
        if ticker not in norm_df.columns:
            continue
        series = norm_df[ticker].dropna()
        color  = SECTOR_COLORS.get(name, "#8BA5C4")
        fig.add_trace(go.Scatter(
            x=series.index, y=series.values,
            mode="lines", name=name,
            line=dict(color=color, width=2),
            hovertemplate=f"<b>{name}</b><br>%{{x|%b %d, %Y}}<br>Index: %{{y:.1f}}<extra></extra>",
        ))
    fig.add_hline(y=100, line_dash="dot", line_color="#4A6080", line_width=1)
    apply_layout(fig, title_text=f"Normalized Performance (Base=100) — {selected_period_label}")
    fig.update_yaxes(ticksuffix="")

elif chart_type == "Absolute Price":
    fig = go.Figure()
    for name in selected_names:
        ticker = TOP10[name]
        if ticker not in price_df.columns:
            continue
        series = price_df[ticker].dropna()
        color  = SECTOR_COLORS.get(name, "#8BA5C4")
        fig.add_trace(go.Scatter(
            x=series.index, y=series.values,
            mode="lines", name=name,
            line=dict(color=color, width=2),
            hovertemplate=f"<b>{name}</b><br>%{{x|%b %d, %Y}}<br>${{y:,.2f}}<extra></extra>",
        ))
    apply_layout(fig, title_text=f"Closing Price (USD) — {selected_period_label}")
    fig.update_yaxes(tickprefix="$")

else:  # Candlestick — single ticker
    pick = st.selectbox("Select company for candlestick", selected_names)
    ticker = TOP10[pick]
    raw_ohlc = yf.download(ticker, period=selected_period, auto_adjust=True, progress=False)
    fig = go.Figure(go.Candlestick(
        x=raw_ohlc.index,
        open=raw_ohlc["Open"].squeeze(),
        high=raw_ohlc["High"].squeeze(),
        low=raw_ohlc["Low"].squeeze(),
        close=raw_ohlc["Close"].squeeze(),
        increasing_line_color="#00D4AA",
        decreasing_line_color="#FF4D6A",
        name=pick,
    ))
    apply_layout(fig, title_text=f"{pick} Candlestick — {selected_period_label}")
    fig.update_xaxes(rangeslider_visible=False)
    fig.update_yaxes(tickprefix="$")

st.plotly_chart(fig, use_container_width=True)

# ── Returns heatmap ───────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Monthly Returns Heatmap</div>', unsafe_allow_html=True)

valid_tickers = [TOP10[n] for n in selected_names if TOP10[n] in price_df.columns]
monthly_returns = (
    price_df[valid_tickers]
    .resample("ME").last()
    .pct_change()
    .dropna(how="all") * 100
)
monthly_returns.columns = [ticker_to_name.get(c, c) for c in monthly_returns.columns]
monthly_returns.index   = monthly_returns.index.strftime("%b %Y")

fig_heat = go.Figure(go.Heatmap(
    z=monthly_returns.T.values,
    x=monthly_returns.index.tolist(),
    y=monthly_returns.columns.tolist(),
    colorscale=[
        [0,   "#FF4D6A"],
        [0.5, "#0A0E1A"],
        [1,   "#00D4AA"],
    ],
    zmid=0,
    text=[[f"{v:.1f}%" if pd.notna(v) else "" for v in row] for row in monthly_returns.T.values],
    texttemplate="%{text}",
    textfont=dict(size=10, color="#E8EDF5"),
    hovertemplate="<b>%{y}</b><br>%{x}<br>Return: %{z:.2f}%<extra></extra>",
    showscale=True,
    colorbar=dict(tickfont=dict(color=DARK_TEXT), title=dict(text="%", font=dict(color=DARK_TEXT))),
))
apply_layout(
    fig_heat,
    hovermode="closest",
    height=max(260, 36 * len(selected_names)),
    margin=dict(l=0, r=60, t=40, b=0),
    title_text="Monthly Return (%)",
    extra=dict(
        xaxis=dict(tickfont=dict(size=10), gridcolor=DARK_GRID),
        yaxis=dict(tickfont=dict(size=11)),
    ),
)
st.plotly_chart(fig_heat, use_container_width=True)

# ── Volume + performance bar ──────────────────────────────────────────────────
col_l, col_r = st.columns(2)

with col_l:
    st.markdown('<div class="section-title">Period Return Comparison</div>', unsafe_allow_html=True)
    returns_data = []
    for name in selected_names:
        ticker = TOP10[name]
        if ticker not in price_df.columns:
            continue
        s = price_df[ticker].dropna()
        if len(s) < 2:
            continue
        ret = (s.iloc[-1] - s.iloc[0]) / s.iloc[0] * 100
        returns_data.append({"Company": name, "Return (%)": ret, "Color": SECTOR_COLORS.get(name, "#8BA5C4")})

    returns_df = pd.DataFrame(returns_data).sort_values("Return (%)", ascending=True)
    fig_bar = go.Figure(go.Bar(
        x=returns_df["Return (%)"],
        y=returns_df["Company"],
        orientation="h",
        marker_color=[SECTOR_COLORS.get(n, "#8BA5C4") for n in returns_df["Company"]],
        text=[f"{v:+.1f}%" for v in returns_df["Return (%)"]],
        textposition="outside",
        textfont=dict(color="#C8D8EC", size=11),
        hovertemplate="<b>%{y}</b><br>Return: %{x:.2f}%<extra></extra>",
    ))
    fig_bar.add_vline(x=0, line_color="#4A6080", line_width=1)
    apply_layout(
        fig_bar,
        hovermode="y",
        height=340,
        margin=dict(l=0, r=60, t=40, b=0),
        title_text=f"Total Return — {selected_period_label}",
        extra=dict(
            title=dict(text=f"Total Return — {selected_period_label}", font_color="#C8D8EC", font_size=13),
            xaxis=dict(ticksuffix="%", gridcolor=DARK_GRID, zerolinecolor="#4A6080"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        ),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_r:
    st.markdown('<div class="section-title">30-Day Volatility</div>', unsafe_allow_html=True)
    vol_data = []
    for name in selected_names:
        ticker = TOP10[name]
        if ticker not in price_df.columns:
            continue
        s = price_df[ticker].dropna()
        if len(s) < 30:
            continue
        daily_ret = s.pct_change().dropna()
        vol = daily_ret.rolling(30).std().iloc[-1] * (252 ** 0.5) * 100
        vol_data.append({"Company": name, "Annualized Vol (%)": vol})

    vol_df = pd.DataFrame(vol_data).sort_values("Annualized Vol (%)", ascending=True)
    fig_vol = go.Figure(go.Bar(
        x=vol_df["Annualized Vol (%)"],
        y=vol_df["Company"],
        orientation="h",
        marker=dict(
            color=vol_df["Annualized Vol (%)"],
            colorscale=[[0, "#00D4AA"], [0.5, "#F5A623"], [1, "#FF4D6A"]],
            showscale=False,
        ),
        text=[f"{v:.1f}%" for v in vol_df["Annualized Vol (%)"]],
        textposition="outside",
        textfont=dict(color="#C8D8EC", size=11),
        hovertemplate="<b>%{y}</b><br>Vol: %{x:.2f}%<extra></extra>",
    ))
    apply_layout(
        fig_vol,
        hovermode="y",
        height=340,
        margin=dict(l=0, r=60, t=40, b=0),
        title_text="Annualized Volatility (30-day rolling)",
        extra=dict(
            xaxis=dict(ticksuffix="%", gridcolor=DARK_GRID),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        ),
    )
    st.plotly_chart(fig_vol, use_container_width=True)

# ── Correlation matrix ────────────────────────────────────────────────────────
if len(selected_names) >= 3:
    st.markdown('<div class="section-title">Correlation Matrix</div>', unsafe_allow_html=True)
    daily_rets = price_df[valid_tickers].pct_change().dropna(how="all")
    daily_rets.columns = [ticker_to_name.get(c, c) for c in daily_rets.columns]
    corr = daily_rets.corr()

    fig_corr = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        zmin=-1, zmax=1, zmid=0,
        colorscale=[
            [0,   "#FF4D6A"],
            [0.5, "#0A0E1A"],
            [1,   "#2196F3"],
        ],
        text=[[f"{v:.2f}" for v in row] for row in corr.values],
        texttemplate="%{text}",
        textfont=dict(size=10, color="#E8EDF5"),
        hovertemplate="<b>%{y} × %{x}</b><br>Correlation: %{z:.3f}<extra></extra>",
        colorbar=dict(tickfont=dict(color=DARK_TEXT)),
    ))
    apply_layout(
        fig_corr,
        hovermode="closest",
        height=420,
        margin=dict(l=0, r=60, t=40, b=0),
        title_text="Daily Return Correlation",
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="status-bar">
    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} KST &nbsp;·&nbsp;
    Data: Yahoo Finance &nbsp;·&nbsp;
    Universe: Global Market Cap Top 10
</div>
""", unsafe_allow_html=True)
