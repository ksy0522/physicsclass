import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils import setup_korean_font, COMMON_CSS, sidebar_api_key, search_materials, classify, mat_card_html

st.set_page_config(page_title="밴드갭 탐색기 | 반도체 재료 탐색기", page_icon="⚡", layout="wide")
setup_korean_font()
st.markdown(COMMON_CSS, unsafe_allow_html=True)
api_key = sidebar_api_key()

st.markdown("""
<div class="hero">
  <h1>⚡ 밴드갭 탐색기</h1>
  <p>실제 Materials Project 데이터로 도체·반도체·부도체 분포를 시각화합니다</p>
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.warning("👈 왼쪽 사이드바에 API 키를 입력해주세요.")
    st.stop()

st.markdown("""
<div class="info-box">
조건을 설정하고 <b>데이터 불러오기</b>를 누르면 밴드갭 분포 그래프가 그려집니다.
</div>
""", unsafe_allow_html=True)

# ── 조건 ──────────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    elem_bg = st.text_input("원소 필터 (선택)", placeholder="예: Si  /  Ga, N", key="bg_elem")
with c2:
    bg_max_val = st.slider("최대 밴드갭 (eV)", 1.0, 10.0, 6.0, 0.5)
with c3:
    n_fetch = st.select_slider("데이터 수", [20, 30, 50, 80], value=50)

if st.button("📡 데이터 불러오기"):
    elements = tuple(e.strip() for e in elem_bg.split(",") if e.strip()) if elem_bg else ()
    with st.spinner("데이터 조회 중..."):
        results, err = search_materials(api_key, elements, 0.0, bg_max_val, n_fetch)
    if err:
        st.error(f"API 오류: {err}")
    elif not results:
        st.info("결과 없음")
    else:
        st.session_state["bg_results"] = results

if "bg_results" not in st.session_state:
    st.stop()

results = st.session_state["bg_results"]
bg_vals = [r["band_gap"] for r in results]
labels_list = [
    "도체" if (r["is_metal"] or r["band_gap"] == 0)
    else ("반도체" if r["band_gap"] < 3 else "부도체")
    for r in results
]

# ── 시각화 ────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">밴드갭 분포 시각화</div>', unsafe_allow_html=True)

fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
fig.patch.set_facecolor("white")

# 히스토그램
ax1 = axes[0]
ax1.set_facecolor("#f8fafc")
n_bins = min(25, len(set(round(b, 1) for b in bg_vals)))
counts, edges, patches_h = ax1.hist(bg_vals, bins=n_bins, color="#006fa6",
                                     edgecolor="white", linewidth=.5)
for patch, mid in zip(patches_h, [(edges[i] + edges[i+1]) / 2 for i in range(len(edges)-1)]):
    patch.set_facecolor("#ffa500" if mid == 0 else ("#00c864" if mid < 3 else "#9060ff"))
ax1.axvline(3.0, color="white", lw=1.2, ls="--", alpha=0.5)
legend_patches = [
    mpatches.Patch(color="#ffa500", label="도체 (0 eV)"),
    mpatches.Patch(color="#00c864", label="반도체 (0~3 eV)"),
    mpatches.Patch(color="#9060ff", label="부도체 (>3 eV)"),
]
ax1.legend(handles=legend_patches, fontsize=8, facecolor="#f8fafc",
           edgecolor="#dde3ea", labelcolor="#1a1a2e")
ax1.set_title("밴드갭 분포", color="white", fontweight="bold", pad=10)
ax1.set_xlabel("밴드갭 (eV)", color="#333333")
ax1.set_ylabel("소재 수", color="#333333")
ax1.tick_params(colors="#333333")
for sp in ax1.spines.values(): sp.set_color("#dde3ea")

# 파이 차트
ax2 = axes[1]
ax2.set_facecolor("#f8fafc")
cnt = {k: labels_list.count(k) for k in ["도체", "반도체", "부도체"]}
pie_vals = [v for v in cnt.values() if v > 0]
pie_labs = [k for k, v in cnt.items() if v > 0]
pie_cols_map = {"도체": "#ffa500", "반도체": "#00c864", "부도체": "#9060ff"}
_, _, autotexts = ax2.pie(
    pie_vals, labels=pie_labs,
    colors=[pie_cols_map[l] for l in pie_labs],
    autopct="%1.0f%%", startangle=90,
    textprops={"color": "white", "fontsize": 10},
    wedgeprops={"linewidth": 2, "edgecolor": "#ffffff"},
)
for at in autotexts: at.set_fontsize(9)
ax2.set_title("도체·반도체·부도체 비율", color="white", fontweight="bold", pad=10)

# 산점도 (밴드갭 vs 밀도)
ax3 = axes[2]
ax3.set_facecolor("#f8fafc")
for r in results:
    c = "#ffa500" if (r["is_metal"] or r["band_gap"] == 0) else ("#00c864" if r["band_gap"] < 3 else "#9060ff")
    ax3.scatter(r["band_gap"], r["density"], color=c, s=40, alpha=0.75, edgecolors="none")
ax3.axvline(3.0, color="white", lw=1, ls="--", alpha=0.4)
ax3.set_title("밴드갭 vs 밀도", color="white", fontweight="bold", pad=10)
ax3.set_xlabel("밴드갭 (eV)", color="#333333")
ax3.set_ylabel("밀도 (g/cm³)", color="#333333")
ax3.tick_params(colors="#333333")
for sp in ax3.spines.values(): sp.set_color("#dde3ea")

fig.tight_layout(pad=2)
st.pyplot(fig)
plt.close()

# ── 반도체 목록 ───────────────────────────────────────────────────────────────
semis_only = sorted(
    [r for r in results if not r["is_metal"] and 0 < r["band_gap"] < 3],
    key=lambda x: x["band_gap"]
)
if semis_only:
    st.markdown(f'<div class="sec-head">반도체 소재 목록 ({len(semis_only)}종, 밴드갭 오름차순)</div>',
                unsafe_allow_html=True)
    for r in semis_only[:15]:
        st.markdown(mat_card_html(r), unsafe_allow_html=True)
