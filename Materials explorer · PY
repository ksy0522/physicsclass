import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib import font_manager
import urllib.request
import os
import warnings
warnings.filterwarnings("ignore")

# ── 한글 폰트 설정 ──────────────────────────────────────────────────────────
@st.cache_resource
def setup_korean_font():
    font_path = "/tmp/NanumGothic.ttf"
    if not os.path.exists(font_path):
        url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
        urllib.request.urlretrieve(url, font_path)
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)
    mpl.rcParams["font.family"] = prop.get_name()
    mpl.rcParams["axes.unicode_minus"] = False

setup_korean_font()

# ── 페이지 설정 ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="반도체 재료 탐색기",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 디자인 토큰 ─────────────────────────────────────────────────────────────
# 팔레트: 결정 격자를 연상시키는 딥 네이비 + 아쿠아 포인트 + 앰버 강조
# 시그니처: 밴드갭 값을 소재 카드 왼쪽에 크게 세로로 배치 (측정 눈금자 느낌)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}
.stApp {
    background: #080f1a;
    color: #e8edf5;
}
section[data-testid="stSidebar"] {
    background: #0d1929 !important;
    border-right: 1px solid #1e3050;
}
section[data-testid="stSidebar"] * { color: #c8d6e8 !important; }

/* 히어로 배너 */
.hero {
    background: linear-gradient(135deg, #0d1929 0%, #0a2040 60%, #0d2d4a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 28px,
        rgba(0,200,255,0.04) 28px, rgba(0,200,255,0.04) 29px
    ),
    repeating-linear-gradient(
        90deg, transparent, transparent 28px,
        rgba(0,200,255,0.04) 28px, rgba(0,200,255,0.04) 29px
    );
    pointer-events: none;
}
.hero h1 {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem; font-weight: 700;
    color: #ffffff; margin: 0 0 .4rem;
    letter-spacing: -0.02em;
}
.hero p { color: #7fa8cc; font-size: .95rem; margin: 0; }
.hero-tag {
    display: inline-block;
    background: rgba(0,200,255,0.12);
    border: 1px solid rgba(0,200,255,0.3);
    color: #00c8ff;
    padding: 3px 10px; border-radius: 20px;
    font-size: .75rem; font-family: 'Space Mono', monospace;
    margin-right: 6px; margin-bottom: 8px;
}

/* 소재 카드 — 시그니처: 왼쪽 밴드갭 눈금자 */
.mat-card {
    background: #0d1929;
    border: 1px solid #1e3050;
    border-radius: 12px;
    display: flex;
    overflow: hidden;
    margin-bottom: .9rem;
    transition: border-color .2s;
}
.mat-card:hover { border-color: #00c8ff; }
.mat-card-gauge {
    width: 64px; min-width: 64px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: .8rem .4rem;
    font-family: 'Space Mono', monospace;
}
.mat-card-gauge .gap-val {
    font-size: 1.25rem; font-weight: 700; line-height: 1;
}
.mat-card-gauge .gap-unit {
    font-size: .62rem; color: #7fa8cc; margin-top: 2px;
}
.mat-card-body {
    padding: .85rem 1rem; flex: 1;
}
.mat-card-body .formula {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem; font-weight: 700; color: #e8edf5;
}
.mat-card-body .mpid {
    font-size: .72rem; color: #5580a0;
    font-family: 'Space Mono', monospace; margin-bottom: .4rem;
}
.mat-card-meta {
    display: flex; gap: .5rem; flex-wrap: wrap; margin-top: .4rem;
}
.meta-chip {
    background: #0a1e32; border: 1px solid #1e3a5f;
    border-radius: 6px; padding: 2px 8px;
    font-size: .73rem; color: #7fa8cc;
}
.type-badge {
    display: inline-block; border-radius: 6px;
    padding: 2px 10px; font-size: .73rem; font-weight: 600;
    margin-bottom: .3rem;
}
.type-metal    { background: rgba(255,165,0,.15);  color: #ffa500; border: 1px solid rgba(255,165,0,.3); }
.type-semi     { background: rgba(0,200,100,.15);  color: #00c864; border: 1px solid rgba(0,200,100,.3); }
.type-insul    { background: rgba(120,80,255,.15); color: #9060ff; border: 1px solid rgba(120,80,255,.3); }

/* 섹션 헤더 */
.sec-head {
    font-family: 'Space Mono', monospace;
    font-size: .7rem; letter-spacing: .12em; text-transform: uppercase;
    color: #00c8ff; margin: 1.5rem 0 .8rem;
    border-bottom: 1px solid #1e3050; padding-bottom: .4rem;
}

/* 입력 필드 */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #0d1929 !important;
    border: 1px solid #1e3050 !important;
    color: #e8edf5 !important;
    border-radius: 8px !important;
}
.stSlider > div { color: #c8d6e8; }
div[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    color: #00c8ff !important; font-size: 1.4rem !important;
}
div[data-testid="stMetricLabel"] { color: #7fa8cc !important; }

/* 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #004d80, #006fa6) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important; padding: .5rem 1.4rem !important;
}
.stButton > button:hover { background: linear-gradient(135deg, #006fa6, #0090cc) !important; }

/* info box */
.info-box {
    background: rgba(0,200,255,.07);
    border-left: 3px solid #00c8ff;
    border-radius: 0 8px 8px 0;
    padding: .8rem 1rem; margin: .5rem 0;
    font-size: .88rem; color: #a8c8e0; line-height: 1.6;
}
.warn-box {
    background: rgba(255,165,0,.07);
    border-left: 3px solid #ffa500;
    border-radius: 0 8px 8px 0;
    padding: .8rem 1rem; margin: .5rem 0;
    font-size: .85rem; color: #c8a860; line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ── API 연결 함수 ───────────────────────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def search_materials(api_key, elements, bg_min, bg_max, max_results=30):
    try:
        from mp_api.client import MPRester
        with MPRester(api_key) as mpr:
            docs = mpr.materials.summary.search(
                elements=elements if elements else None,
                band_gap=(bg_min, bg_max),
                fields=["material_id","formula_pretty","band_gap",
                        "density","formation_energy_per_atom",
                        "energy_above_hull","is_metal","nelements","elements"],
                num_chunks=1, chunk_size=max_results,
            )
        return [
            {
                "id": d.material_id,
                "formula": d.formula_pretty,
                "band_gap": round(float(d.band_gap or 0), 3),
                "density": round(float(d.density or 0), 2),
                "formation_energy": round(float(d.formation_energy_per_atom or 0), 3),
                "e_above_hull": round(float(d.energy_above_hull or 0), 4),
                "is_metal": bool(d.is_metal),
                "nelements": int(d.nelements or 0),
                "elements": [str(e) for e in (d.elements or [])],
            }
            for d in docs
        ], None
    except Exception as e:
        return [], str(e)

@st.cache_data(ttl=600, show_spinner=False)
def get_material_detail(api_key, mpid):
    try:
        from mp_api.client import MPRester
        with MPRester(api_key) as mpr:
            docs = mpr.materials.summary.search(
                material_ids=[mpid],
                fields=["material_id","formula_pretty","band_gap","density",
                        "formation_energy_per_atom","energy_above_hull",
                        "is_metal","nelements","elements","volume",
                        "nsites","symmetry","theoretical"],
            )
        if not docs:
            return None, "데이터 없음"
        d = docs[0]
        sym = d.symmetry
        return {
            "id": d.material_id,
            "formula": d.formula_pretty,
            "band_gap": round(float(d.band_gap or 0), 3),
            "density": round(float(d.density or 0), 3),
            "formation_energy": round(float(d.formation_energy_per_atom or 0), 3),
            "e_above_hull": round(float(d.energy_above_hull or 0), 4),
            "is_metal": bool(d.is_metal),
            "nelements": int(d.nelements or 0),
            "elements": [str(e) for e in (d.elements or [])],
            "volume": round(float(d.volume or 0), 2),
            "nsites": int(d.nsites or 0),
            "crystal_system": str(sym.crystal_system.value) if sym else "N/A",
            "space_group": str(sym.symbol) if sym else "N/A",
            "theoretical": bool(d.theoretical),
        }, None
    except Exception as e:
        return None, str(e)

# ── 유틸 함수 ───────────────────────────────────────────────────────────────
def classify(bg, is_metal):
    if is_metal or bg == 0:
        return "도체", "type-metal", "#ffa500"
    elif bg < 3.0:
        return "반도체", "type-semi", "#00c864"
    else:
        return "부도체", "type-insul", "#9060ff"

def gauge_color(bg):
    if bg == 0:   return "#ffa500"
    elif bg < 3:  return "#00c864"
    else:         return "#9060ff"

# ── 사이드바 ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💎 재료 탐색기")
    st.markdown("---")

    api_key = st.text_input(
        "Materials Project API 키",
        type="password",
        placeholder="발급받은 API 키 입력",
        help="https://materialsproject.org → 로그인 → Dashboard에서 발급"
    )

    st.markdown("""
    <div class="warn-box">
    🔑 API 키가 없으신가요?<br>
    <a href="https://materialsproject.org" target="_blank" style="color:#ffa500">
    materialsproject.org</a>에서 무료 가입 후 Dashboard에서 발급하세요.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    menu = st.radio(
        "메뉴",
        ["🏠 홈", "🔍 소재 검색", "⚡ 밴드갭 탐색기", "📊 반도체 비교", "🔬 소재 상세"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("""
    <div style="font-size:.78rem; color:#4a6a8a; line-height:1.7">
    📡 데이터: Materials Project<br>
    🧪 86,680+ 무기화합물 DB<br>
    🖥 DFT 계산 기반 물성값
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 홈
# ════════════════════════════════════════════════════════════════════════════
if menu == "🏠 홈":
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
    stats = [
        ("86,680+", "무기화합물"),
        ("DFT 계산", "전자구조 데이터"),
        ("무료 API", "회원가입 후 발급"),
        ("실시간 조회", "밴드갭·밀도·안정성"),
    ]
    for col, (val, label) in zip([c1, c2, c3, c4], stats):
        col.metric(label, val)

    st.markdown('<div class="sec-head">기능 안내</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    features = [
        ("🔍", "소재 검색", "원소 조합과 밴드갭 범위로\n원하는 재료를 바로 찾기"),
        ("⚡", "밴드갭 탐색기", "도체/반도체/부도체를\n밴드갭 기준으로 분류·시각화"),
        ("📊", "반도체 비교", "Si·GaAs·GaN 등 교과서\n주요 반도체 나란히 비교"),
        ("🔬", "소재 상세보기", "Materials Project ID로\n결정구조·물성 전체 조회"),
    ]
    for i, (icon, title, desc) in enumerate(features):
        col = r1 if i < 2 else r2
        col.markdown(f"""
        <div style="background:#0d1929; border:1px solid #1e3050; border-radius:12px;
                    padding:1.2rem 1.4rem; margin-bottom:.8rem">
          <div style="font-size:1.6rem">{icon}</div>
          <div style="font-family:'Space Mono',monospace; font-size:.95rem;
                      font-weight:700; color:#e8edf5; margin:.3rem 0">{title}</div>
          <div style="font-size:.83rem; color:#5580a0; white-space:pre-line">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    💡 <b>밴드갭(Band Gap)이란?</b><br>
    전자가 존재할 수 없는 금지된 에너지 구간의 크기(eV)입니다.<br>
    • 밴드갭 = 0 (도체) → 전자가 자유롭게 이동<br>
    • 밴드갭 0~3 eV (반도체) → 조건에 따라 전류 흐름 제어 가능<br>
    • 밴드갭 > 3 eV (부도체) → 전자 이동 매우 어려움
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# 소재 검색
# ════════════════════════════════════════════════════════════════════════════
elif menu == "🔍 소재 검색":
    st.markdown('<div class="sec-head">소재 검색</div>', unsafe_allow_html=True)

    if not api_key:
        st.warning("왼쪽 사이드바에 API 키를 입력해주세요.")
        st.stop()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### 🔧 검색 조건")
        elem_input = st.text_input(
            "포함 원소 (쉼표 구분, 비워두면 전체)",
            placeholder="예: Si, Ge  /  Ga, As  /  Ga, N",
        )
        bg_range = st.slider("밴드갭 범위 (eV)", 0.0, 8.0, (0.0, 3.0), 0.1)
        max_res = st.select_slider("최대 결과 수", [10, 20, 30, 50], value=20)
        run = st.button("🔍 검색", use_container_width=True)

    with col2:
        if run:
            elements = [e.strip() for e in elem_input.split(",") if e.strip()] if elem_input else []
            with st.spinner("Materials Project 조회 중..."):
                results, err = search_materials(api_key, elements, bg_range[0], bg_range[1], max_res)

            if err:
                st.error(f"API 오류: {err}")
            elif not results:
                st.info("검색 결과가 없습니다. 조건을 변경해보세요.")
            else:
                st.success(f"**{len(results)}개** 소재를 찾았습니다.")

                # 통계
                metals = sum(1 for r in results if r["is_metal"])
                semis  = sum(1 for r in results if not r["is_metal"] and r["band_gap"] < 3)
                insuls = sum(1 for r in results if not r["is_metal"] and r["band_gap"] >= 3)
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("도체", f"{metals}종")
                mc2.metric("반도체", f"{semis}종")
                mc3.metric("부도체", f"{insuls}종")

                # 카드 목록
                st.markdown('<div class="sec-head">검색 결과</div>', unsafe_allow_html=True)
                for r in sorted(results, key=lambda x: x["band_gap"]):
                    label, badge_cls, color = classify(r["band_gap"], r["is_metal"])
                    elem_str = ", ".join(r["elements"])
                    st.markdown(f"""
                    <div class="mat-card">
                      <div class="mat-card-gauge" style="background:linear-gradient(180deg,{color}22,{color}11);
                           border-right:2px solid {color}44">
                        <span class="gap-val" style="color:{color}">{r['band_gap']}</span>
                        <span class="gap-unit">eV</span>
                      </div>
                      <div class="mat-card-body">
                        <span class="type-badge {badge_cls}">{label}</span>
                        <div class="formula">{r['formula']}</div>
                        <div class="mpid">{r['id']}</div>
                        <div class="mat-card-meta">
                          <span class="meta-chip">밀도 {r['density']} g/cm³</span>
                          <span class="meta-chip">생성에너지 {r['formation_energy']} eV/atom</span>
                          <span class="meta-chip">원소 {elem_str}</span>
                        </div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# 밴드갭 탐색기
# ════════════════════════════════════════════════════════════════════════════
elif menu == "⚡ 밴드갭 탐색기":
    st.markdown('<div class="sec-head">밴드갭 탐색기</div>', unsafe_allow_html=True)

    if not api_key:
        st.warning("왼쪽 사이드바에 API 키를 입력해주세요.")
        st.stop()

    st.markdown("""
    <div class="info-box">
    밴드갭에 따른 소재 분류를 실제 Materials Project 데이터로 시각화합니다.<br>
    조건을 설정하고 <b>데이터 불러오기</b>를 누르면 분포 그래프가 그려집니다.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        elem_bg = st.text_input("원소 필터 (선택)", placeholder="예: Si  /  Ga, N", key="bg_elem")
    with c2:
        bg_max_val = st.slider("최대 밴드갭 (eV)", 1.0, 10.0, 6.0, 0.5)
    with c3:
        n_fetch = st.select_slider("데이터 수", [20, 30, 50, 80], value=50)

    if st.button("📡 데이터 불러오기", use_container_width=False):
        elements = [e.strip() for e in elem_bg.split(",") if e.strip()] if elem_bg else []
        with st.spinner("데이터 조회 중..."):
            results, err = search_materials(api_key, elements, 0.0, bg_max_val, n_fetch)

        if err:
            st.error(f"API 오류: {err}")
        elif not results:
            st.info("결과 없음")
        else:
            st.session_state["bg_results"] = results

    if "bg_results" in st.session_state:
        results = st.session_state["bg_results"]
        bg_vals = [r["band_gap"] for r in results]
        labels_list = ["도체" if r["is_metal"] or r["band_gap"]==0
                       else ("반도체" if r["band_gap"] < 3 else "부도체")
                       for r in results]

        fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
        fig.patch.set_facecolor("#080f1a")

        # ── 히스토그램
        ax1 = axes[0]
        ax1.set_facecolor("#0d1929")
        colors_hist = ["#ffa500" if b==0 else ("#00c864" if b<3 else "#9060ff") for b in bg_vals]
        n_bins = min(25, len(set(round(b,1) for b in bg_vals)))
        counts, edges, patches_h = ax1.hist(bg_vals, bins=n_bins,
                                             color="#006fa6", edgecolor="#0d1929", linewidth=.5)
        for patch, bv in zip(patches_h, [(edges[i]+edges[i+1])/2 for i in range(len(edges)-1)]):
            if bv == 0: patch.set_facecolor("#ffa500")
            elif bv < 3: patch.set_facecolor("#00c864")
            else: patch.set_facecolor("#9060ff")
        ax1.axvline(3.0, color="white", lw=1.2, ls="--", alpha=0.5, label="반도체/부도체 경계 (3 eV)")
        ax1.set_title("밴드갭 분포", color="white", fontweight="bold", pad=10)
        ax1.set_xlabel("밴드갭 (eV)", color="#7fa8cc")
        ax1.set_ylabel("소재 수", color="#7fa8cc")
        ax1.tick_params(colors="#5580a0")
        for sp in ax1.spines.values(): sp.set_color("#1e3050")
        legend_patches = [
            mpatches.Patch(color="#ffa500", label="도체 (0 eV)"),
            mpatches.Patch(color="#00c864", label="반도체 (0~3 eV)"),
            mpatches.Patch(color="#9060ff", label="부도체 (>3 eV)"),
        ]
        ax1.legend(handles=legend_patches, fontsize=8,
                   facecolor="#0d1929", edgecolor="#1e3050", labelcolor="white")

        # ── 파이 차트
        ax2 = axes[1]
        ax2.set_facecolor("#0d1929")
        cnt = {"도체": labels_list.count("도체"),
               "반도체": labels_list.count("반도체"),
               "부도체": labels_list.count("부도체")}
        pie_vals = [v for v in cnt.values() if v > 0]
        pie_labs = [k for k, v in cnt.items() if v > 0]
        pie_cols = {"도체": "#ffa500", "반도체": "#00c864", "부도체": "#9060ff"}
        pie_colors = [pie_cols[l] for l in pie_labs]
        wedges, texts, autotexts = ax2.pie(
            pie_vals, labels=pie_labs, colors=pie_colors,
            autopct="%1.0f%%", startangle=90,
            textprops={"color": "white", "fontsize": 10},
            wedgeprops={"linewidth": 2, "edgecolor": "#080f1a"},
        )
        for at in autotexts: at.set_fontsize(9)
        ax2.set_title("도체·반도체·부도체 비율", color="white", fontweight="bold", pad=10)

        # ── 산점도 (밴드갭 vs 밀도)
        ax3 = axes[2]
        ax3.set_facecolor("#0d1929")
        for r in results:
            c = "#ffa500" if (r["is_metal"] or r["band_gap"]==0) else ("#00c864" if r["band_gap"]<3 else "#9060ff")
            ax3.scatter(r["band_gap"], r["density"], color=c, s=40, alpha=0.75, edgecolors="none")
        ax3.axvline(3.0, color="white", lw=1, ls="--", alpha=0.4)
        ax3.set_title("밴드갭 vs 밀도", color="white", fontweight="bold", pad=10)
        ax3.set_xlabel("밴드갭 (eV)", color="#7fa8cc")
        ax3.set_ylabel("밀도 (g/cm³)", color="#7fa8cc")
        ax3.tick_params(colors="#5580a0")
        for sp in ax3.spines.values(): sp.set_color("#1e3050")

        fig.tight_layout(pad=2)
        st.pyplot(fig)
        plt.close()

        # 상위 반도체 목록
        semis_only = sorted([r for r in results if not r["is_metal"] and 0 < r["band_gap"] < 3],
                            key=lambda x: x["band_gap"])
        if semis_only:
            st.markdown('<div class="sec-head">반도체 소재 목록 (밴드갭 오름차순)</div>', unsafe_allow_html=True)
            for r in semis_only[:15]:
                st.markdown(f"""
                <div class="mat-card">
                  <div class="mat-card-gauge" style="background:linear-gradient(180deg,#00c86422,#00c86411);
                       border-right:2px solid #00c86444">
                    <span class="gap-val" style="color:#00c864">{r['band_gap']}</span>
                    <span class="gap-unit">eV</span>
                  </div>
                  <div class="mat-card-body">
                    <span class="type-badge type-semi">반도체</span>
                    <div class="formula">{r['formula']}</div>
                    <div class="mpid">{r['id']}</div>
                    <div class="mat-card-meta">
                      <span class="meta-chip">밀도 {r['density']} g/cm³</span>
                      <span class="meta-chip">원소 {", ".join(r['elements'])}</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# 반도체 비교
# ════════════════════════════════════════════════════════════════════════════
elif menu == "📊 반도체 비교":
    st.markdown('<div class="sec-head">주요 반도체 비교</div>', unsafe_allow_html=True)

    if not api_key:
        st.warning("왼쪽 사이드바에 API 키를 입력해주세요.")
        st.stop()

    # 교과서 대표 반도체 프리셋
    PRESETS = {
        "Si (실리콘)":          "mp-149",
        "Ge (저마늄)":          "mp-32",
        "GaAs (갈륨비소)":      "mp-2534",
        "GaN (질화갈륨)":       "mp-804",
        "ZnO (산화아연)":       "mp-2133",
        "InP (인화인듐)":       "mp-20351",
        "CdTe (텔루르화카드뮴)":"mp-406",
        "SiC (탄화규소)":       "mp-8062",
    }

    selected = st.multiselect(
        "비교할 반도체 선택 (최대 6개)",
        list(PRESETS.keys()),
        default=["Si (실리콘)", "Ge (저마늄)", "GaAs (갈륨비소)", "GaN (질화갈륨)"],
        max_selections=6,
    )

    if st.button("📡 데이터 불러오기", use_container_width=False) and selected:
        data = {}
        with st.spinner("조회 중..."):
            for name in selected:
                mpid = PRESETS[name]
                detail, err = get_material_detail(api_key, mpid)
                if detail:
                    data[name] = detail
        st.session_state["compare_data"] = data

    if "compare_data" in st.session_state and st.session_state["compare_data"]:
        data = st.session_state["compare_data"]
        names = list(data.keys())

        # 카드 행
        cols = st.columns(len(names))
        for col, name in zip(cols, names):
            d = data[name]
            label, badge_cls, color = classify(d["band_gap"], d["is_metal"])
            col.markdown(f"""
            <div style="background:#0d1929; border:1px solid {color}66;
                        border-radius:12px; padding:1rem; text-align:center">
              <div style="font-family:'Space Mono',monospace; font-size:2rem;
                          font-weight:700; color:{color}">{d['band_gap']}</div>
              <div style="font-size:.65rem; color:#5580a0; margin-bottom:.4rem">eV</div>
              <div style="font-family:'Space Mono',monospace; font-size:1rem;
                          font-weight:700; color:#e8edf5">{d['formula']}</div>
              <div style="font-size:.72rem; color:#5580a0">{name.split('(')[0].strip()}</div>
              <div style="margin-top:.5rem">
                <span class="type-badge {badge_cls}">{label}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # 그래프
        st.markdown('<div class="sec-head">물성 비교 차트</div>', unsafe_allow_html=True)
        fig, axes = plt.subplots(1, 3, figsize=(13, 5))
        fig.patch.set_facecolor("#080f1a")
        bar_colors = ["#00c8ff", "#00c864", "#ffa500", "#9060ff", "#ff6060", "#60ffcc"]

        short_names = [n.split("(")[0].strip() for n in names]

        for ax in axes:
            ax.set_facecolor("#0d1929")
            ax.tick_params(colors="#5580a0")
            for sp in ax.spines.values(): sp.set_color("#1e3050")

        # 밴드갭
        bg_vals = [data[n]["band_gap"] for n in names]
        bars = axes[0].bar(short_names, bg_vals,
                           color=bar_colors[:len(names)], edgecolor="#0d1929", linewidth=1.5)
        axes[0].axhline(3.0, color="white", lw=1, ls="--", alpha=0.4)
        axes[0].set_title("밴드갭 (eV)", color="white", fontweight="bold")
        axes[0].set_ylabel("eV", color="#7fa8cc")
        for bar, val in zip(bars, bg_vals):
            axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                         f"{val}", ha="center", va="bottom", color="white", fontsize=9,
                         fontfamily="monospace")

        # 밀도
        den_vals = [data[n]["density"] for n in names]
        bars2 = axes[1].bar(short_names, den_vals,
                            color=bar_colors[:len(names)], edgecolor="#0d1929", linewidth=1.5)
        axes[1].set_title("밀도 (g/cm³)", color="white", fontweight="bold")
        axes[1].set_ylabel("g/cm³", color="#7fa8cc")
        for bar, val in zip(bars2, den_vals):
            axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                         f"{val}", ha="center", va="bottom", color="white", fontsize=9,
                         fontfamily="monospace")

        # 생성 에너지
        fe_vals = [data[n]["formation_energy"] for n in names]
        colors_fe = [bar_colors[i] for i in range(len(names))]
        bars3 = axes[2].bar(short_names, fe_vals,
                            color=colors_fe, edgecolor="#0d1929", linewidth=1.5)
        axes[2].axhline(0, color="white", lw=0.8, alpha=0.3)
        axes[2].set_title("생성 에너지 (eV/atom)", color="white", fontweight="bold")
        axes[2].set_ylabel("eV/atom", color="#7fa8cc")
        for bar, val in zip(bars3, fe_vals):
            ypos = bar.get_height() + 0.02 if val >= 0 else bar.get_height() - 0.08
            axes[2].text(bar.get_x() + bar.get_width()/2, ypos,
                         f"{val}", ha="center", va="bottom", color="white", fontsize=9,
                         fontfamily="monospace")

        fig.tight_layout(pad=2)
        st.pyplot(fig)
        plt.close()

        # 상세 표
        st.markdown('<div class="sec-head">상세 물성 테이블</div>', unsafe_allow_html=True)
        prop_rows = {
            "화학식": "formula", "밴드갭 (eV)": "band_gap",
            "밀도 (g/cm³)": "density",
            "생성 에너지 (eV/atom)": "formation_energy",
            "안정성 (eV/atom above hull)": "e_above_hull",
        }
        table_html = "<table style='width:100%;border-collapse:collapse;font-family:Space Grotesk,sans-serif;font-size:.85rem'>"
        table_html += "<tr style='border-bottom:2px solid #1e3050'>"
        table_html += "<th style='padding:.6rem 1rem;text-align:left;color:#00c8ff;font-family:Space Mono,monospace'>물성</th>"
        for n in names:
            table_html += f"<th style='padding:.6rem 1rem;text-align:center;color:#e8edf5'>{n.split('(')[0]}</th>"
        table_html += "</tr>"
        for prop_label, key in prop_rows.items():
            table_html += "<tr style='border-bottom:1px solid #1e3050'>"
            table_html += f"<td style='padding:.55rem 1rem;color:#7fa8cc'>{prop_label}</td>"
            for n in names:
                val = data[n][key]
                if key == "band_gap":
                    _, badge_cls, color = classify(val, data[n]["is_metal"])
                    cell = f"<span style='color:{color};font-family:Space Mono,monospace;font-weight:700'>{val}</span>"
                else:
                    cell = f"<span style='font-family:Space Mono,monospace'>{val}</span>"
                table_html += f"<td style='padding:.55rem 1rem;text-align:center;color:#c8d6e8'>{cell}</td>"
            table_html += "</tr>"
        table_html += "</table>"
        st.markdown(f"""
        <div style="background:#0d1929;border:1px solid #1e3050;border-radius:12px;
                    overflow:hidden;margin-top:.5rem">{table_html}</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="warn-box">
        ⚠️ <b>DFT 계산값 주의사항:</b> 밴드갭은 DFT 계산값으로 실험값 대비 평균 1.6배 과소평가됩니다.
        예) Si 실험값 ≈ 1.12 eV, 계산값 ≈ 0.6~0.7 eV. 수업에서 이론·실험값 차이를 토론하는 소재로 활용해 보세요!
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# 소재 상세
# ════════════════════════════════════════════════════════════════════════════
elif menu == "🔬 소재 상세":
    st.markdown('<div class="sec-head">소재 상세 조회</div>', unsafe_allow_html=True)

    if not api_key:
        st.warning("왼쪽 사이드바에 API 키를 입력해주세요.")
        st.stop()

    st.markdown("""
    <div class="info-box">
    Materials Project ID(mp-숫자)를 입력하면 해당 소재의 전체 물성을 조회합니다.<br>
    예시: <code>mp-149</code> (Si), <code>mp-2534</code> (GaAs), <code>mp-804</code> (GaN)
    </div>
    """, unsafe_allow_html=True)

    quick_btns = {
        "Si": "mp-149", "Ge": "mp-32", "GaAs": "mp-2534",
        "GaN": "mp-804", "ZnO": "mp-2133", "SiC": "mp-8062",
    }
    st.markdown("**빠른 선택:**")
    qcols = st.columns(len(quick_btns))
    for col, (label, mpid) in zip(qcols, quick_btns.items()):
        if col.button(label, key=f"q_{mpid}"):
            st.session_state["detail_id"] = mpid

    mpid_input = st.text_input(
        "Materials Project ID 직접 입력",
        value=st.session_state.get("detail_id", "mp-149"),
        placeholder="mp-149",
    )

    if st.button("🔬 상세 조회", use_container_width=False):
        with st.spinner("조회 중..."):
            detail, err = get_material_detail(api_key, mpid_input.strip())
        if err:
            st.error(f"오류: {err}")
        elif detail:
            st.session_state["detail_result"] = detail

    if "detail_result" in st.session_state:
        d = st.session_state["detail_result"]
        label, badge_cls, color = classify(d["band_gap"], d["is_metal"])

        # 헤더
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0d1929,#0a2040);
                    border:1px solid {color}55; border-radius:14px; padding:1.5rem 2rem; margin:.8rem 0">
          <div style="display:flex; align-items:center; gap:1.5rem">
            <div style="text-align:center; min-width:80px">
              <div style="font-family:'Space Mono',monospace; font-size:2.5rem;
                          font-weight:700; color:{color}; line-height:1">{d['band_gap']}</div>
              <div style="font-size:.7rem; color:#5580a0">eV (밴드갭)</div>
            </div>
            <div>
              <span class="type-badge {badge_cls}">{label}</span>
              <div style="font-family:'Space Mono',monospace; font-size:1.8rem;
                          font-weight:700; color:#ffffff; margin:.2rem 0">{d['formula']}</div>
              <div style="font-size:.8rem; color:#5580a0">{d['id']}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 물성 그리드
        props = [
            ("밀도", f"{d['density']} g/cm³"),
            ("생성 에너지", f"{d['formation_energy']} eV/atom"),
            ("안정성(hull)", f"{d['e_above_hull']} eV/atom"),
            ("원소 수", f"{d['nelements']}종"),
            ("원소 구성", ", ".join(d["elements"])),
            ("단위셀 원자 수", f"{d['nsites']} atoms"),
            ("단위셀 부피", f"{d['volume']} Å³"),
            ("결정계", d["crystal_system"]),
            ("공간군", d["space_group"]),
            ("이론값 여부", "예측" if d["theoretical"] else "실험 확인"),
        ]
        pc = st.columns(5)
        for i, (k, v) in enumerate(props):
            pc[i % 5].markdown(f"""
            <div style="background:#0d1929; border:1px solid #1e3050; border-radius:8px;
                        padding:.7rem .9rem; margin-bottom:.6rem">
              <div style="font-size:.7rem; color:#5580a0; margin-bottom:.2rem">{k}</div>
              <div style="font-family:'Space Mono',monospace; font-size:.9rem;
                          color:#e8edf5; font-weight:600">{v}</div>
            </div>
            """, unsafe_allow_html=True)

        # 수업 연계 설명
        if not d["is_metal"] and 0 < d["band_gap"] < 3:
            st.markdown(f"""
            <div class="info-box">
            🏫 <b>수업 연계 포인트</b><br>
            {d['formula']}은(는) 밴드갭 <b>{d['band_gap']} eV</b>의 반도체 소재입니다.<br>
            {"가시광선(1.8~3.1 eV) 영역에 해당하여 LED·태양전지 소재로 활용 가능합니다." if 1.8 <= d['band_gap'] <= 3.1 else ""}
            {"적외선 영역으로 태양전지·적외선 센서에 활용됩니다." if d['band_gap'] < 1.8 else ""}
            안정성 지표(energy above hull) = {d['e_above_hull']} eV/atom
            {"→ 열역학적으로 안정한 소재입니다." if d['e_above_hull'] < 0.1 else "→ 약간 불안정하여 합성이 어려울 수 있습니다."}
            </div>
            """, unsafe_allow_html=True)
