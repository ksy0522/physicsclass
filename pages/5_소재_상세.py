import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from utils import setup_korean_font, COMMON_CSS, sidebar_api_key, get_material_detail, classify

st.set_page_config(page_title="소재 상세 | 반도체 재료 탐색기", page_icon="🔬", layout="wide")
setup_korean_font()
st.markdown(COMMON_CSS, unsafe_allow_html=True)
api_key = sidebar_api_key()

st.markdown("""
<div class="hero">
  <h1>🔬 소재 상세</h1>
  <p>Materials Project ID로 소재의 전체 물성 데이터를 조회합니다</p>
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.warning("👈 왼쪽 사이드바에 API 키를 입력해주세요.")
    st.stop()

st.markdown("""
<div class="info-box">
Materials Project ID(mp-숫자)를 입력하면 해당 소재의 결정계·공간군·밀도·안정성 등을 모두 조회합니다.<br>
예시: <code>mp-149</code> (Si), <code>mp-2534</code> (GaAs), <code>mp-804</code> (GaN), <code>mp-8062</code> (SiC)
</div>
""", unsafe_allow_html=True)

# ── 빠른 선택 ─────────────────────────────────────────────────────────────────
QUICK = {"Si": "mp-149", "Ge": "mp-32", "GaAs": "mp-2534",
         "GaN": "mp-804", "ZnO": "mp-2133", "SiC": "mp-8062",
         "InP": "mp-20351", "CdTe": "mp-406"}

st.markdown("**빠른 선택:**")
qcols = st.columns(len(QUICK))
for col, (label, mpid) in zip(qcols, QUICK.items()):
    if col.button(label, key=f"q_{mpid}"):
        st.session_state["detail_id"] = mpid

mpid_input = st.text_input(
    "Materials Project ID 직접 입력",
    value=st.session_state.get("detail_id", "mp-149"),
    placeholder="mp-149",
)

if st.button("🔬 상세 조회"):
    with st.spinner("조회 중..."):
        detail, err = get_material_detail(api_key, mpid_input.strip())
    if err:
        st.error(f"오류: {err}")
    elif detail:
        st.session_state["detail_result"] = detail

if "detail_result" not in st.session_state:
    st.stop()

d = st.session_state["detail_result"]
label, badge_cls, color = classify(d["band_gap"], d["is_metal"])

# ── 소재 헤더 카드 ────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#0d1929,#0a2040);
            border:1px solid {color}55; border-radius:14px;
            padding:1.5rem 2rem; margin:.8rem 0">
  <div style="display:flex; align-items:center; gap:1.5rem; flex-wrap:wrap">
    <div style="text-align:center; min-width:80px">
      <div style="font-family:'Space Mono',monospace; font-size:2.8rem;
                  font-weight:700; color:{color}; line-height:1">{d['band_gap']}</div>
      <div style="font-size:.68rem; color:#5580a0; margin-top:4px">eV (밴드갭)</div>
    </div>
    <div style="flex:1">
      <span class="type-badge {badge_cls}">{label}</span>
      <div style="font-family:'Space Mono',monospace; font-size:2rem;
                  font-weight:700; color:#fff; margin:.2rem 0">{d['formula']}</div>
      <div style="font-size:.82rem; color:#5580a0">{d['id']} &nbsp;·&nbsp;
        {'실험 확인' if not d['theoretical'] else 'DFT 예측값'}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 물성 그리드 ───────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">물성 데이터</div>', unsafe_allow_html=True)

props = [
    ("밀도",          f"{d['density']} g/cm³"),
    ("생성 에너지",   f"{d['formation_energy']} eV/atom"),
    ("안정성 (hull)", f"{d['e_above_hull']} eV/atom"),
    ("원소 수",       f"{d['nelements']}종"),
    ("원소 구성",     ", ".join(d["elements"])),
    ("단위셀 원자 수", f"{d['nsites']} atoms"),
    ("단위셀 부피",   f"{d['volume']} Å³"),
    ("결정계",        d["crystal_system"]),
    ("공간군",        d["space_group"]),
    ("데이터 출처",   "DFT 예측" if d["theoretical"] else "실험 확인"),
]

pc = st.columns(5)
for i, (k, v) in enumerate(props):
    pc[i % 5].markdown(f"""
    <div style="background:#0d1929; border:1px solid #1e3050; border-radius:8px;
                padding:.75rem 1rem; margin-bottom:.6rem">
      <div style="font-size:.68rem; color:#5580a0; margin-bottom:.3rem; text-transform:uppercase;
                  letter-spacing:.06em">{k}</div>
      <div style="font-family:'Space Mono',monospace; font-size:.9rem;
                  color:#e8edf5; font-weight:600">{v}</div>
    </div>
    """, unsafe_allow_html=True)

# ── 수업 연계 포인트 ──────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">수업 연계 포인트</div>', unsafe_allow_html=True)

if d["is_metal"] or d["band_gap"] == 0:
    st.markdown(f"""
    <div class="info-box">
    🔋 <b>{d['formula']}은(는) 도체입니다.</b><br>
    밴드갭이 0 eV로 가전자대와 전도대가 겹쳐 전자가 자유롭게 이동할 수 있습니다.
    전선, 전극, 열전소재 등에 활용됩니다.
    </div>
    """, unsafe_allow_html=True)

elif d["band_gap"] < 3.0:
    solar = "☀️ 태양전지 소재로 적합한 밴드갭 범위(1.0~1.8 eV)입니다." if 1.0 <= d["band_gap"] <= 1.8 else ""
    led   = "💡 가시광선(1.8~3.1 eV) 영역으로 LED·광소자 소재로 활용 가능합니다." if 1.8 < d["band_gap"] <= 3.0 else ""
    stab  = "✅ 열역학적으로 안정한 소재입니다." if d["e_above_hull"] < 0.1 else "⚠️ 약간 불안정하여 합성이 어려울 수 있습니다."
    st.markdown(f"""
    <div class="info-box">
    🔬 <b>{d['formula']}은(는) 밴드갭 {d['band_gap']} eV의 반도체입니다.</b><br>
    {solar} {led}<br>
    안정성 지표 (energy above hull) = {d['e_above_hull']} eV/atom → {stab}
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div class="info-box">
    🛡 <b>{d['formula']}은(는) 밴드갭 {d['band_gap']} eV의 부도체입니다.</b><br>
    전자 이동이 매우 어려워 절연체로 사용됩니다. 게이트 산화막, 기판 소재 등에 활용됩니다.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="warn-box">
⚠️ <b>DFT 계산값 주의:</b>
밴드갭은 실험값 대비 평균 1.6배 과소평가됩니다.
실제 수업에서는 DFT 값과 실험값을 함께 비교하는 토론 자료로 활용하세요.
</div>
""", unsafe_allow_html=True)
