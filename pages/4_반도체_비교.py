import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import matplotlib.pyplot as plt
from utils import setup_korean_font, COMMON_CSS, sidebar_api_key, get_material_detail, classify

st.set_page_config(page_title="반도체 비교 | 반도체 재료 탐색기", page_icon="📊", layout="wide")
setup_korean_font()
st.markdown(COMMON_CSS, unsafe_allow_html=True)
api_key = sidebar_api_key()

st.markdown("""
<div class="hero">
  <h1>📊 반도체 비교</h1>
  <p>교과서 대표 반도체들의 물성을 나란히 비교합니다</p>
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.warning("👈 왼쪽 사이드바에 API 키를 입력해주세요.")
    st.stop()

PRESETS = {
    "Si (실리콘)":           "mp-149",
    "Ge (저마늄)":           "mp-32",
    "GaAs (갈륨비소)":       "mp-2534",
    "GaN (질화갈륨)":        "mp-804",
    "ZnO (산화아연)":        "mp-2133",
    "InP (인화인듐)":        "mp-20351",
    "CdTe (텔루르화카드뮴)": "mp-406",
    "SiC (탄화규소)":        "mp-8062",
}

selected = st.multiselect(
    "비교할 반도체 선택 (최대 6개)",
    list(PRESETS.keys()),
    default=["Si (실리콘)", "Ge (저마늄)", "GaAs (갈륨비소)", "GaN (질화갈륨)"],
    max_selections=6,
)

if st.button("📡 데이터 불러오기") and selected:
    data = {}
    with st.spinner("조회 중..."):
        for name in selected:
            detail, err = get_material_detail(api_key, PRESETS[name])
            if detail:
                data[name] = detail
    st.session_state["compare_data"] = data

if "compare_data" not in st.session_state or not st.session_state["compare_data"]:
    st.stop()

data  = st.session_state["compare_data"]
names = list(data.keys())
BAR_COLORS = ["#00c8ff", "#00c864", "#ffa500", "#9060ff", "#ff6060", "#60ffcc"]
short_names = [n.split("(")[0].strip() for n in names]

# ── 요약 카드 행 ──────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">소재 요약</div>', unsafe_allow_html=True)
cols = st.columns(len(names))
for col, name in zip(cols, names):
    d = data[name]
    _, badge_cls, color = classify(d["band_gap"], d["is_metal"])
    label = "도체" if d["is_metal"] or d["band_gap"] == 0 else ("반도체" if d["band_gap"] < 3 else "부도체")
    col.markdown(f"""
    <div style="background:#f8fafc; border:1px solid {color}66;
                border-top:3px solid {color}; border-radius:12px;
                padding:1rem; text-align:center">
      <div style="font-family:'Space Mono',monospace; font-size:2rem;
                  font-weight:700; color:{color}; line-height:1">{d['band_gap']}</div>
      <div style="font-size:.65rem; color:#4a6a8a; margin-bottom:.4rem">eV</div>
      <div style="font-family:'Space Mono',monospace; font-size:.95rem;
                  font-weight:700; color:#1a1a2e">{d['formula']}</div>
      <div style="font-size:.72rem; color:#4a6a8a; margin-bottom:.4rem">{name.split('(')[0].strip()}</div>
      <span class="type-badge {badge_cls}">{label}</span>
    </div>
    """, unsafe_allow_html=True)

# ── 비교 차트 ─────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">물성 비교 차트</div>', unsafe_allow_html=True)

fig, axes = plt.subplots(1, 3, figsize=(13, 5))
fig.patch.set_facecolor("white")

for ax in axes:
    ax.set_facecolor("#f8fafc")
    ax.tick_params(colors="#333333")
    for sp in ax.spines.values(): sp.set_color("#dde3ea")

def labeled_bar(ax, vals, title, ylabel):
    bars = ax.bar(short_names, vals,
                  color=BAR_COLORS[:len(names)], edgecolor="white", linewidth=1.5)
    ax.set_title(title, color="white", fontweight="bold")
    ax.set_ylabel(ylabel, color="#333333")
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + abs(max(vals, default=0)) * 0.02,
                f"{val}", ha="center", va="bottom",
                color="white", fontsize=9, fontfamily="monospace")

labeled_bar(axes[0], [data[n]["band_gap"] for n in names], "밴드갭 (eV)", "eV")
axes[0].axhline(3.0, color="white", lw=1, ls="--", alpha=0.4)

labeled_bar(axes[1], [data[n]["density"] for n in names], "밀도 (g/cm³)", "g/cm³")

fe_vals = [data[n]["formation_energy"] for n in names]
labeled_bar(axes[2], fe_vals, "생성 에너지 (eV/atom)", "eV/atom")
axes[2].axhline(0, color="white", lw=0.8, alpha=0.3)

fig.tight_layout(pad=2)
st.pyplot(fig)
plt.close()

# ── 상세 테이블 ───────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">상세 물성 테이블</div>', unsafe_allow_html=True)

prop_rows = {
    "화학식": "formula",
    "밴드갭 (eV)": "band_gap",
    "밀도 (g/cm³)": "density",
    "생성 에너지 (eV/atom)": "formation_energy",
    "안정성 (eV above hull)": "e_above_hull",
}

tbl = "<table style='width:100%;border-collapse:collapse;font-size:.85rem'>"
tbl += "<tr style='border-bottom:2px solid #dde3ea'>"
tbl += "<th style='padding:.6rem 1rem;text-align:left;color:#00c8ff;font-family:Space Mono,monospace'>물성</th>"
for n in names:
    tbl += f"<th style='padding:.6rem 1rem;text-align:center;color:#1a1a2e'>{n.split('(')[0]}</th>"
tbl += "</tr>"

for prop_label, key in prop_rows.items():
    tbl += "<tr style='border-bottom:1px solid #dde3ea'>"
    tbl += f"<td style='padding:.55rem 1rem;color:#3a5a7a'>{prop_label}</td>"
    for n in names:
        val = data[n][key]
        if key == "band_gap":
            _, _, color = classify(val, data[n]["is_metal"])
            cell = f"<span style='color:{color};font-family:Space Mono,monospace;font-weight:700'>{val}</span>"
        else:
            cell = f"<span style='font-family:Space Mono,monospace'>{val}</span>"
        tbl += f"<td style='padding:.55rem 1rem;text-align:center;color:#2c3e50'>{cell}</td>"
    tbl += "</tr>"
tbl += "</table>"

st.markdown(f"""
<div style="background:#f8fafc;border:1px solid #dde3ea;border-radius:12px;overflow:hidden">
{tbl}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="warn-box">
⚠️ <b>DFT 계산값 주의사항:</b>
밴드갭은 DFT 계산값으로 실험값 대비 평균 1.6배 과소평가됩니다.
예) Si 실험값 ≈ 1.12 eV, 계산값 ≈ 0.61 eV.
수업에서 이론·실험값 차이를 토론하는 소재로 활용해 보세요!
</div>
""", unsafe_allow_html=True)
