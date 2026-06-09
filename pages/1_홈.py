import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from utils import setup_korean_font, COMMON_CSS, sidebar_api_key

st.set_page_config(page_title="홈 | 반도체 재료 탐색기", page_icon="💎", layout="wide")
setup_korean_font()
st.markdown(COMMON_CSS, unsafe_allow_html=True)
sidebar_api_key()

# ── 히어로 ───────────────────────────────────────────────────────────────────
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

# ── 통계 ─────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("무기화합물", "86,680+")
c2.metric("전자구조 데이터", "DFT 계산")
c3.metric("API 방식", "무료 (회원가입)")
c4.metric("데이터 조회", "실시간")

# ── 기능 카드 ─────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">기능 안내</div>', unsafe_allow_html=True)

features = [
    ("🔍", "소재 검색",     "원소 조합과 밴드갭 범위로\n원하는 재료를 바로 찾기",         "#00c8ff"),
    ("⚡", "밴드갭 탐색기", "도체/반도체/부도체를\n밴드갭 기준으로 분류·시각화",         "#00c864"),
    ("📊", "반도체 비교",   "Si·GaAs·GaN 등 교과서\n주요 반도체 나란히 비교",           "#ffa500"),
    ("🔬", "소재 상세",     "Materials Project ID로\n결정구조·물성 전체 조회",           "#9060ff"),
]

cols = st.columns(4)
for col, (icon, title, desc, color) in zip(cols, features):
    col.markdown(f"""
    <div style="background:#0d1929; border:1px solid {color}44;
                border-top:3px solid {color}; border-radius:12px;
                padding:1.4rem; min-height:160px">
      <div style="font-size:2rem">{icon}</div>
      <div style="font-family:'Space Mono',monospace; font-size:.95rem;
                  font-weight:700; color:#e8edf5; margin:.5rem 0 .3rem">{title}</div>
      <div style="font-size:.82rem; color:#5580a0; white-space:pre-line; line-height:1.5">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# ── 밴드갭 개념 설명 ──────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">밴드갭 개념</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1])

with left:
    st.markdown("""
    <div class="info-box">
    <b>💡 밴드갭(Band Gap)이란?</b><br><br>
    전자가 존재할 수 없는 <b>금지된 에너지 구간의 크기(eV)</b>입니다.<br><br>
    &nbsp;• 밴드갭 = 0 eV &nbsp;→ <span style="color:#ffa500"><b>도체</b></span> — 전자가 자유롭게 이동<br>
    &nbsp;• 밴드갭 0~3 eV → <span style="color:#00c864"><b>반도체</b></span> — 조건에 따라 전류 제어 가능<br>
    &nbsp;• 밴드갭 &gt; 3 eV &nbsp;→ <span style="color:#9060ff"><b>부도체</b></span> — 전자 이동 매우 어려움
    </div>
    """, unsafe_allow_html=True)

with right:
    examples = [
        ("Cu (구리)",   0.0,   True,  "도선, 전극"),
        ("Si (실리콘)", 0.614, False, "CPU, 태양전지"),
        ("GaN (질화갈륨)", 1.7, False, "청색 LED"),
        ("SiO₂ (석영)", 5.9, False, "절연체"),
    ]
    for name, bg, is_metal, use in examples:
        label, badge_cls, color = ("도체","type-metal","#ffa500") if is_metal or bg==0 else \
                                  (("반도체","type-semi","#00c864") if bg < 3 else ("부도체","type-insul","#9060ff"))
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:.8rem;
                    background:#0d1929; border:1px solid #1e3050; border-radius:8px;
                    padding:.55rem 1rem; margin-bottom:.5rem">
          <div style="font-family:'Space Mono',monospace; font-size:1.1rem;
                      font-weight:700; color:{color}; min-width:50px">{bg}</div>
          <div style="font-size:.7rem; color:#5580a0; min-width:24px">eV</div>
          <div style="flex:1">
            <div style="font-size:.88rem; color:#e8edf5; font-weight:600">{name}</div>
            <div style="font-size:.72rem; color:#5580a0">{use}</div>
          </div>
          <span class="type-badge {badge_cls}">{label}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="warn-box">
⚠️ <b>DFT 계산값 주의:</b>
Materials Project의 밴드갭은 DFT 계산값으로 실험값보다 평균 <b>1.6배 과소평가</b>됩니다.
예) Si 실험값 ≈ 1.12 eV, 계산값 ≈ 0.61 eV. 수업에서 이론·실험값 차이를 토론하는 소재로 활용해 보세요!
</div>
""", unsafe_allow_html=True)
