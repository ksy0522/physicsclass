"""
반도체 재료 탐색기 — 멀티페이지 Streamlit 앱
실행: streamlit run app.py
"""
import streamlit as st
from utils import setup_korean_font, COMMON_CSS, sidebar_api_key

st.set_page_config(
    page_title="반도체 재료 탐색기",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)
setup_korean_font()
st.markdown(COMMON_CSS, unsafe_allow_html=True)
sidebar_api_key()

st.markdown("""
<div class="hero">
  <div>
    <span class="hero-tag">Materials Project API</span>
    <span class="hero-tag">반도체 수업</span>
    <span class="hero-tag">DFT 계산값</span>
  </div>
  <h1>💎 반도체 재료 탐색기</h1>
  <p>86,680종 무기화합물의 밴드갭·밀도·결정구조를 실시간으로 탐색하고 비교하세요</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("무기화합물",  "86,680+")
c2.metric("전자구조",    "DFT 계산")
c3.metric("API",         "무료 (회원가입)")
c4.metric("데이터 조회", "실시간")

st.markdown('<div class="sec-head">페이지 안내</div>', unsafe_allow_html=True)

features = [
    ("🔍", "소재 검색",     "원소 조합과 밴드갭 범위로\n원하는 재료를 바로 찾기",       "#00c8ff"),
    ("⚡", "밴드갭 탐색기", "도체/반도체/부도체를\n밴드갭 기준으로 분류·시각화",       "#00c864"),
    ("📊", "반도체 비교",   "Si·GaAs·GaN 등 교과서\n주요 반도체 나란히 비교",         "#ffa500"),
    ("🔬", "소재 상세",     "Materials Project ID로\n결정구조·물성 전체 조회",         "#9060ff"),
]
cols = st.columns(4)
for col, (icon, title, desc, color) in zip(cols, features):
    col.markdown(f"""
    <div style="background:#f8fafc; border:1px solid {color}44;
                border-top:3px solid {color}; border-radius:12px;
                padding:1.4rem; min-height:160px">
      <div style="font-size:2rem">{icon}</div>
      <div style="font-family:'Space Mono',monospace; font-size:.95rem;
                  font-weight:700; color:#1a1a2e; margin:.5rem 0 .3rem">{title}</div>
      <div style="font-size:.82rem; color:#4a6a8a; white-space:pre-line; line-height:1.5">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.info("👈 왼쪽 사이드바에서 페이지를 선택하세요.")
