import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Global TOP10 Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 글로벌 시가총액 TOP10 주식 대시보드")
st.caption("Yahoo Finance 데이터를 활용한 최근 1년 주가 변화 시각화")

TICKERS = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Alphabet": "GOOGL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "TSMC": "TSM",
    "Meta": "META",
    "Broadcom": "AVGO",
    "Tesla": "TSLA",
    "Berkshire Hathaway": "BRK-B"
}

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

selected_companies = st.multiselect(
    "확인할 기업을 선택하세요",
    options=list(TICKERS.keys()),
    default=list(TICKERS.keys())
)

chart_type = st.radio(
    "그래프 기준",
    ["정규화 수익률 비교", "실제 종가 비교"],
    horizontal=True
)

@st.cache_data
def load_stock_data(tickers, start, end):
    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )["Close"]
    return data

if selected_companies:
    selected_tickers = [TICKERS[name] for name in selected_companies]
    price_data = load_stock_data(selected_tickers, start_date, end_date)

    if isinstance(price_data, pd.Series):
        price_data = price_data.to_frame()

    price_data = price_data.dropna(how="all")
    price_data = price_data.rename(
        columns={v: k for k, v in TICKERS.items()}
    )

    st.subheader("최근 1년 주가 변화")

    if chart_type == "정규화 수익률 비교":
        normalized = price_data / price_data.iloc[0] * 100

        fig = px.line(
            normalized,
            x=normalized.index,
            y=normalized.columns,
            title="최근 1년 주가 변화 비교: 시작일 = 100",
            labels={
                "value": "정규화 지수",
                "Date": "날짜",
                "variable": "기업"
            }
        )

    else:
        fig = px.line(
            price_data,
            x=price_data.index,
            y=price_data.columns,
            title="최근 1년 실제 종가 비교",
            labels={
                "value": "주가",
                "Date": "날짜",
                "variable": "기업"
            }
        )

    fig.update_layout(
        hovermode="x unified",
        legend_title_text="기업",
        height=650
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("수익률 요약")

    returns = ((price_data.iloc[-1] / price_data.iloc[0]) - 1) * 100
    summary = pd.DataFrame({
        "기업": returns.index,
        "1년 수익률(%)": returns.values
    }).sort_values("1년 수익률(%)", ascending=False)

    st.dataframe(
        summary.style.format({"1년 수익률(%)": "{:.2f}"}),
        use_container_width=True
    )

else:
    st.warning("하나 이상의 기업을 선택해주세요.")
