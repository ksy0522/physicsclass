import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from utils import setup_korean_font, COMMON_CSS, sidebar_api_key, search_materials, mat_card_html, classify

st.set_page_config(page_title="소재 검색 | 반도체 재료 탐색기", page_icon="🔍", layout="wide")
setup_korean_font()
st.markdown(COMMON_CSS, unsafe_allow_html=True)
api_key = sidebar_api_key()

# ── 페이지 헤더 ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🔍 소재 검색</h1>
  <p>원소 조합과 밴드갭 범위로 Materials Project DB에서 소재를 탐색합니다</p>
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.warning("👈 왼쪽 사이드바에 API 키를 입력해주세요.")
    st.stop()

# ── 검색 조건 ─────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">검색 조건</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    elem_input = st.text_input(
        "포함 원소 (쉼표 구분, 비워두면 전체)",
        placeholder="예: Si, Ge  /  Ga, As  /  Ga, N",
    )
with col2:
    bg_range = st.slider("밴드갭 범위 (eV)", 0.0, 8.0, (0.0, 3.0), 0.1)
with col3:
    max_res = st.select_slider("최대 결과 수", [10, 20, 30, 50], value=20)

run = st.button("🔍 검색 실행", use_container_width=False)

# ── 검색 실행 ─────────────────────────────────────────────────────────────────
if run:
    elements = tuple(e.strip() for e in elem_input.split(",") if e.strip()) if elem_input else ()
    with st.spinner("Materials Project 조회 중..."):
        results, err = search_materials(api_key, elements, bg_range[0], bg_range[1], max_res)

    if err:
        st.error(f"API 오류: {err}")
    elif not results:
        st.info("검색 결과가 없습니다. 조건을 변경해보세요.")
    else:
        st.session_state["search_results"] = results

if "search_results" in st.session_state:
    results = st.session_state["search_results"]

    # 통계
    metals = sum(1 for r in results if r["is_metal"])
    semis  = sum(1 for r in results if not r["is_metal"] and r["band_gap"] < 3)
    insuls = sum(1 for r in results if not r["is_metal"] and r["band_gap"] >= 3)

    st.markdown('<div class="sec-head">검색 결과 요약</div>', unsafe_allow_html=True)
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("전체", f"{len(results)}종")
    mc2.metric("도체",   f"{metals}종")
    mc3.metric("반도체", f"{semis}종")
    mc4.metric("부도체", f"{insuls}종")

    # 정렬 옵션
    sort_by = st.radio("정렬 기준", ["밴드갭 ↑", "밀도 ↑", "생성에너지 ↑"], horizontal=True)
    sort_key = {"밴드갭 ↑": "band_gap", "밀도 ↑": "density", "생성에너지 ↑": "formation_energy"}[sort_by]

    st.markdown('<div class="sec-head">소재 목록</div>', unsafe_allow_html=True)
    for r in sorted(results, key=lambda x: x[sort_key]):
        st.markdown(mat_card_html(r), unsafe_allow_html=True)
