"""공통 유틸: 폰트·CSS·API 함수"""
import os
import urllib.request
import warnings
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
import streamlit as st

warnings.filterwarnings("ignore")


# ── 한글 폰트 ────────────────────────────────────────────────────────────────
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


# ── 공통 CSS ─────────────────────────────────────────────────────────────────
COMMON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

/* ── 전체 배경 흰색 ── */
.stApp { background: #ffffff; color: #1a1a2e; }

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: #f5f7fa !important;
    border-right: 1px solid #e0e6ed;
}
section[data-testid="stSidebar"] * { color: #2c3e50 !important; }

[data-testid="stSidebarNav"] a {
    color: #3a5a7a !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: .92rem !important;
    border-radius: 8px !important;
    padding: .4rem .8rem !important;
}
[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNav"] [aria-selected="true"] a {
    background: rgba(0,120,200,.08) !important;
    color: #0078c8 !important;
}

/* ── 히어로 배너 (파란 계열 유지, 텍스트는 흰색) ── */
.hero {
    background: linear-gradient(135deg, #0d3b6e 0%, #1a5fa8 60%, #0078c8 100%);
    border: none; border-radius: 16px;
    padding: 2rem 2.5rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,120,200,.2);
}
.hero::before {
    content: ''; position: absolute; inset: 0;
    background:
        repeating-linear-gradient(0deg,   transparent, transparent 28px, rgba(255,255,255,.04) 28px, rgba(255,255,255,.04) 29px),
        repeating-linear-gradient(90deg, transparent, transparent 28px, rgba(255,255,255,.04) 28px, rgba(255,255,255,.04) 29px);
    pointer-events: none;
}
.hero h1 {
    font-family: 'Space Mono', monospace; font-size: 1.9rem; font-weight: 700;
    color: #ffffff; margin: 0 0 .4rem; letter-spacing: -.02em;
}
.hero p { color: rgba(255,255,255,.8); font-size: .95rem; margin: 0; }
.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,.18); border: 1px solid rgba(255,255,255,.4);
    color: #ffffff; padding: 3px 10px; border-radius: 20px;
    font-size: .75rem; font-family: 'Space Mono', monospace;
    margin-right: 6px; margin-bottom: 8px;
}

/* ── 소재 카드 ── */
.mat-card {
    background: #ffffff; border: 1px solid #e0e6ed;
    border-radius: 12px; display: flex; overflow: hidden;
    margin-bottom: .9rem; transition: border-color .2s, box-shadow .2s;
    box-shadow: 0 2px 8px rgba(0,0,0,.06);
}
.mat-card:hover { border-color: #0078c8; box-shadow: 0 4px 16px rgba(0,120,200,.12); }
.mat-card-gauge {
    width: 64px; min-width: 64px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: .8rem .4rem; font-family: 'Space Mono', monospace;
}
.mat-card-gauge .gap-val { font-size: 1.25rem; font-weight: 700; line-height: 1; }
.mat-card-gauge .gap-unit { font-size: .62rem; color: #8a9bb0; margin-top: 2px; }
.mat-card-body { padding: .85rem 1rem; flex: 1; }
.mat-card-body .formula {
    font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700; color: #1a1a2e;
}
.mat-card-body .mpid { font-size: .72rem; color: #8a9bb0; font-family: 'Space Mono', monospace; margin-bottom: .4rem; }
.mat-card-meta { display: flex; gap: .5rem; flex-wrap: wrap; margin-top: .4rem; }
.meta-chip {
    background: #f0f4f8; border: 1px solid #dde3ea;
    border-radius: 6px; padding: 2px 8px; font-size: .73rem; color: #4a6a8a;
}

/* ── 배지 ── */
.type-badge {
    display: inline-block; border-radius: 6px;
    padding: 2px 10px; font-size: .73rem; font-weight: 600; margin-bottom: .3rem;
}
.type-metal { background: rgba(217,119,6,.12);  color: #b45309; border: 1px solid rgba(217,119,6,.3); }
.type-semi  { background: rgba(5,150,105,.12);  color: #047857; border: 1px solid rgba(5,150,105,.3); }
.type-insul { background: rgba(109,40,217,.12); color: #6d28d9; border: 1px solid rgba(109,40,217,.3); }

/* ── 섹션 헤더 ── */
.sec-head {
    font-family: 'Space Mono', monospace; font-size: .7rem;
    letter-spacing: .12em; text-transform: uppercase;
    color: #0078c8; margin: 1.5rem 0 .8rem;
    border-bottom: 2px solid #e0e6ed; padding-bottom: .4rem;
}

/* ── 입력 필드 ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #ffffff !important; border: 1px solid #d0d8e4 !important;
    color: #1a1a2e !important; border-radius: 8px !important;
}
.stSlider > div { color: #2c3e50; }
div[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    color: #0078c8 !important; font-size: 1.4rem !important;
}
div[data-testid="stMetricLabel"] { color: #4a6a8a !important; }

/* ── 버튼 ── */
.stButton > button {
    background: linear-gradient(135deg, #0062a3, #0078c8) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important; padding: .5rem 1.4rem !important;
    box-shadow: 0 2px 8px rgba(0,120,200,.25) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0078c8, #0090e0) !important;
    box-shadow: 0 4px 12px rgba(0,120,200,.35) !important;
}

/* ── 박스 ── */
.info-box {
    background: #eff6ff; border-left: 3px solid #0078c8;
    border-radius: 0 8px 8px 0; padding: .8rem 1rem; margin: .5rem 0;
    font-size: .88rem; color: #1e4a7a; line-height: 1.6;
}
.warn-box {
    background: #fffbeb; border-left: 3px solid #d97706;
    border-radius: 0 8px 8px 0; padding: .8rem 1rem; margin: .5rem 0;
    font-size: .85rem; color: #92400e; line-height: 1.6;
}
</style>
"""


# ── 분류 함수 ────────────────────────────────────────────────────────────────
def classify(bg, is_metal):
    if is_metal or bg == 0:
        return "도체", "type-metal", "#ffa500"
    elif bg < 3.0:
        return "반도체", "type-semi", "#00c864"
    else:
        return "부도체", "type-insul", "#9060ff"


def mat_card_html(r):
    label, badge_cls, color = classify(r["band_gap"], r["is_metal"])
    elem_str = ", ".join(r["elements"])
    return f"""
    <div class="mat-card">
      <div class="mat-card-gauge"
           style="background:linear-gradient(180deg,{color}22,{color}11);border-right:2px solid {color}44">
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
    </div>"""


# ── API 함수 ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def search_materials(api_key, elements_tuple, bg_min, bg_max, max_results=30):
    try:
        from mp_api.client import MPRester
        elements = list(elements_tuple) if elements_tuple else None
        with MPRester(api_key) as mpr:
            docs = mpr.materials.summary.search(
                elements=elements,
                band_gap=(bg_min, bg_max),
                fields=["material_id", "formula_pretty", "band_gap",
                        "density", "formation_energy_per_atom",
                        "energy_above_hull", "is_metal", "nelements", "elements"],
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
                fields=["material_id", "formula_pretty", "band_gap", "density",
                        "formation_energy_per_atom", "energy_above_hull",
                        "is_metal", "nelements", "elements", "volume",
                        "nsites", "symmetry", "theoretical"],
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


# ── API 키 사이드바 위젯 ──────────────────────────────────────────────────────
def sidebar_api_key():
    st.sidebar.markdown("## 💎 반도체 재료 탐색기")
    st.sidebar.markdown("---")
    key = st.sidebar.text_input(
        "🔑 Materials Project API 키",
        type="password",
        placeholder="API 키 입력",
        key="mp_api_key",
        help="https://materialsproject.org → Dashboard에서 무료 발급",
    )
    if not key:
        st.sidebar.markdown("""
        <div style="background:rgba(255,165,0,.08);border-left:3px solid #ffa500;
                    border-radius:0 6px 6px 0;padding:.6rem .8rem;font-size:.78rem;color:#c8a860">
        키가 없으신가요?<br>
        <a href="https://materialsproject.org" target="_blank" style="color:#ffa500">
        materialsproject.org</a>에서<br>무료 가입 후 Dashboard에서 발급
        </div>
        """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="font-size:.75rem;color:#3a5a7a;line-height:1.7">
    📡 데이터: Materials Project<br>
    🧪 86,680+ 무기화합물 DB<br>
    🖥 DFT 계산 기반 물성값
    </div>
    """, unsafe_allow_html=True)
    return key
