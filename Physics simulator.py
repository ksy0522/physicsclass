import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import matplotlib.gridspec as gridspec
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')

# ── 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="역학과 에너지 시뮬레이터",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 스타일 ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
  html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
  .main { background: #f8f9fa; }
  .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%); }

  .hero-banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  }
  .hero-banner h1 { font-size: 2rem; font-weight: 700; margin: 0; }
  .hero-banner p  { font-size: 1rem; opacity: 0.85; margin: 0.4rem 0 0; }

  .module-card {
    background: white;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    border-left: 5px solid #3d5a99;
  }
  .module-card.green  { border-left-color: #2ecc71; }
  .module-card.orange { border-left-color: #e67e22; }
  .module-card.purple { border-left-color: #9b59b6; }
  .module-card.teal   { border-left-color: #1abc9c; }

  .formula-box {
    background: linear-gradient(135deg, #e8f4f8, #d6eaf8);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    border-left: 4px solid #2980b9;
    font-size: 0.92rem;
    line-height: 1.7;
    margin: 0.5rem 0;
  }
  .info-badge {
    display: inline-block;
    background: #3d5a99;
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    margin-right: 4px;
  }
  .result-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #2c3e50;
  }
  div[data-testid="stMetricValue"] { font-size: 1.4rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 사이드바 ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚛️ 역학과 에너지")
    st.markdown("---")
    menu = st.radio(
        "단원 선택",
        [
            "🏠 홈",
            "📐 힘의 합성",
            "🎯 포물선 운동",
            "🔄 등속 원운동",
            "🌊 진자 운동",
            "🌍 케플러 법칙과 중력",
            "⚡ 역학적 에너지 보존",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem; color:#666; line-height:1.6">
    📚 교과서: 역학과 에너지<br>
    ✏️ 저자: 최혁준 외<br>
    🏫 고등학교 물리학
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
#  홈
# ════════════════════════════════════════════════════════════════════════════
if menu == "🏠 홈":
    st.markdown("""
    <div class="hero-banner">
      <h1>⚛️ 역학과 에너지 인터랙티브 시뮬레이터</h1>
      <p>교과서 단원을 직접 조작하며 배우는 물리 시뮬레이션</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    cards = [
        ("📐", "힘의 합성", "벡터 합성으로\n합력의 크기와 방향 탐구", "#3d5a99"),
        ("🎯", "포물선 운동", "수평·비스듬히 던진 물체의\n궤적과 에너지 분석", "#2ecc71"),
        ("🔄", "등속 원운동", "구심력·구심 가속도와\n원운동의 주기·속력", "#e67e22"),
        ("🌊", "진자 운동", "단진자 주기·진폭과\n에너지 교환 시각화", "#9b59b6"),
        ("🌍", "케플러 법칙", "행성 타원 궤도와\n케플러 3법칙 확인", "#1abc9c"),
        ("⚡", "역학적 에너지 보존", "운동·퍼텐셜 에너지 교환과\n에너지 보존 법칙", "#e74c3c"),
    ]
    for i, (icon, title, desc, color) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:white; border-radius:14px; padding:1.4rem;
                        box-shadow:0 4px 20px rgba(0,0,0,.07);
                        border-top:4px solid {color}; margin-bottom:1rem; min-height:140px">
              <div style="font-size:2rem">{icon}</div>
              <div style="font-weight:700; font-size:1rem; margin:.4rem 0">{title}</div>
              <div style="font-size:.85rem; color:#666; white-space:pre-line">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.info("👈 왼쪽 사이드바에서 단원을 선택하세요!")


# ════════════════════════════════════════════════════════════════════════════
#  힘의 합성
# ════════════════════════════════════════════════════════════════════════════
elif menu == "📐 힘의 합성":
    st.markdown('<div class="module-card"><h2>📐 힘의 합성</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    두 힘 <b>F₁</b>, <b>F₂</b>가 이루는 각도 θ일 때 합력의 크기:<br>
    &nbsp;&nbsp;&nbsp;|<b>F</b>| = √(F₁² + F₂² + 2F₁F₂cosθ)<br>
    합력의 방향(x축 기준):<br>
    &nbsp;&nbsp;&nbsp;φ = arctan[(F₁sinα + F₂sinβ) / (F₁cosα + F₂cosβ)]
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### ⚙️ 파라미터 설정")
        F1     = st.slider("F₁ 크기 (N)", 1, 100, 40)
        angle1 = st.slider("F₁ 방향 (°)", 0, 360, 30)
        F2     = st.slider("F₂ 크기 (N)", 1, 100, 60)
        angle2 = st.slider("F₂ 방향 (°)", 0, 360, 120)

        a1, a2 = np.radians(angle1), np.radians(angle2)
        Rx = F1 * np.cos(a1) + F2 * np.cos(a2)
        Ry = F1 * np.sin(a1) + F2 * np.sin(a2)
        R  = np.sqrt(Rx**2 + Ry**2)
        Ra = np.degrees(np.arctan2(Ry, Rx)) % 360

        st.markdown("#### 📊 계산 결과")
        st.metric("합력 크기", f"{R:.1f} N")
        st.metric("합력 방향", f"{Ra:.1f} °")

    with col2:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(-110, 110); ax.set_ylim(-110, 110)
        ax.axhline(0, color='lightgray', lw=1); ax.axvline(0, color='lightgray', lw=1)
        ax.set_aspect('equal'); ax.grid(True, alpha=0.3)
        ax.set_title("힘의 벡터 합성", fontsize=14, fontweight='bold', pad=12)

        def draw_arrow(ax, dx, dy, color, label, lw=2.5):
            ax.annotate("", xy=(dx, dy), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=color,
                                        lw=lw, mutation_scale=18))
            ax.text(dx * 1.1, dy * 1.1, label, color=color, fontsize=11, fontweight='bold')

        F1x = F1 * np.cos(a1); F1y = F1 * np.sin(a1)
        F2x = F2 * np.cos(a2); F2y = F2 * np.sin(a2)

        draw_arrow(ax, F1x, F1y, '#3498db', f'F₁={F1}N')
        draw_arrow(ax, F2x, F2y, '#e74c3c', f'F₂={F2}N')

        # 평행사변형
        ax.plot([F1x, F1x + F2x, F2x], [F1y, F1y + F2y, F2y],
                '--', color='gray', alpha=0.5, lw=1.5)

        draw_arrow(ax, Rx, Ry, '#27ae60', f'F합={R:.1f}N', lw=3)

        # 각도 호
        theta_arr = np.linspace(0, a1, 50)
        ax.plot(15 * np.cos(theta_arr), 15 * np.sin(theta_arr), color='#3498db', lw=1.5)
        ax.text(18 * np.cos(a1 / 2), 18 * np.sin(a1 / 2), f'{angle1}°', color='#3498db', fontsize=9)

        ax.set_xlabel("x (N)"); ax.set_ylabel("y (N)")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()


# ════════════════════════════════════════════════════════════════════════════
#  포물선 운동
# ════════════════════════════════════════════════════════════════════════════
elif menu == "🎯 포물선 운동":
    st.markdown('<div class="module-card green"><h2>🎯 포물선 운동</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    수평: x = v₀cosθ · t &nbsp;|&nbsp; vₓ = v₀cosθ (일정)<br>
    수직: y = v₀sinθ · t − ½gt² &nbsp;|&nbsp; vᵧ = v₀sinθ − gt<br>
    최고점 높이: H = (v₀sinθ)² / 2g &nbsp;&nbsp; 수평 도달 거리: R = v₀²sin2θ / g
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### ⚙️ 초기 조건")
        v0    = st.slider("초기 속력 v₀ (m/s)", 5, 50, 20)
        theta = st.slider("발사 각도 θ (°)", 1, 89, 45)
        h0    = st.slider("초기 높이 h₀ (m)", 0, 50, 0)
        g     = st.number_input("중력 가속도 g (m/s²)", value=9.8, step=0.1)

        rad = np.radians(theta)
        v0x = v0 * np.cos(rad); v0y = v0 * np.sin(rad)

        # 착지 시간
        a_coef = -0.5 * g; b_coef = v0y; c_coef = h0
        disc = b_coef**2 - 4 * a_coef * c_coef
        t_land = (-b_coef - np.sqrt(disc)) / (2 * a_coef)
        t_peak = v0y / g

        H = h0 + v0y**2 / (2 * g)
        R = v0x * t_land

        st.markdown("#### 📊 결과")
        st.metric("최고 높이", f"{H:.2f} m")
        st.metric("수평 도달 거리", f"{R:.2f} m")
        st.metric("체공 시간", f"{t_land:.2f} s")

    with col2:
        t  = np.linspace(0, t_land, 400)
        x  = v0x * t
        y  = h0 + v0y * t - 0.5 * g * t**2

        vx = np.full_like(t, v0x)
        vy = v0y - g * t
        speed = np.sqrt(vx**2 + vy**2)
        KE    = 0.5 * speed**2            # 단위질량당
        PE    = g * np.maximum(y, 0)

        fig = plt.figure(figsize=(8, 7))
        gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.4)

        ax1 = fig.add_subplot(gs[0, :])
        sc  = ax1.scatter(x, y, c=speed, cmap='RdYlGn_r', s=15, zorder=3)
        ax1.plot(x, y, 'k-', alpha=0.2, lw=1)
        ax1.axhline(0, color='saddlebrown', lw=2)
        ax1.fill_between(x, np.minimum(y, 0), 0, color='saddlebrown', alpha=0.15)
        ax1.scatter([0], [h0], s=120, color='blue', zorder=5, label='발사점')
        ax1.scatter([R], [0], s=120, color='red',  zorder=5, label='착지점', marker='x')
        ax1.scatter([v0x * t_peak], [H], s=120, color='green', zorder=5, label='최고점', marker='^')
        plt.colorbar(sc, ax=ax1, label='속력 (m/s)')
        ax1.set_title("포물선 궤적 (색상 = 속력)", fontweight='bold')
        ax1.set_xlabel("x (m)"); ax1.set_ylabel("y (m)")
        ax1.legend(fontsize=9); ax1.grid(True, alpha=0.3)

        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(t, vx, label='vₓ', color='#3498db', lw=2)
        ax2.plot(t, vy, label='vᵧ', color='#e74c3c', lw=2)
        ax2.plot(t, speed, label='|v|', color='#2ecc71', lw=2, ls='--')
        ax2.axhline(0, color='gray', lw=0.8, ls='--')
        ax2.set_title("속도 성분 vs 시간", fontweight='bold')
        ax2.set_xlabel("t (s)"); ax2.set_ylabel("속도 (m/s)")
        ax2.legend(fontsize=9); ax2.grid(True, alpha=0.3)

        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(t, KE, label='운동에너지 (질량 1kg)', color='#e74c3c', lw=2)
        ax3.plot(t, PE, label='퍼텐셜에너지 (질량 1kg)', color='#3498db', lw=2)
        ax3.plot(t, KE + PE, label='역학적에너지', color='#2c3e50', lw=2, ls='--')
        ax3.set_title("에너지 변화 vs 시간", fontweight='bold')
        ax3.set_xlabel("t (s)"); ax3.set_ylabel("에너지 (J/kg)")
        ax3.legend(fontsize=9); ax3.grid(True, alpha=0.3)

        st.pyplot(fig)
        plt.close()


# ════════════════════════════════════════════════════════════════════════════
#  등속 원운동
# ════════════════════════════════════════════════════════════════════════════
elif menu == "🔄 등속 원운동":
    st.markdown('<div class="module-card orange"><h2>🔄 등속 원운동</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    주기: T = 2πr / v &nbsp;&nbsp; 각속도: ω = 2π/T = v/r<br>
    구심 가속도: a = v²/r = rω² &nbsp;&nbsp; 구심력: F = mv²/r = mrω²
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### ⚙️ 파라미터")
        r = st.slider("반지름 r (m)", 0.5, 10.0, 3.0, 0.5)
        v = st.slider("속력 v (m/s)", 1.0, 30.0, 6.0, 0.5)
        m = st.slider("질량 m (kg)", 0.1, 10.0, 1.0, 0.1)

        T  = 2 * np.pi * r / v
        omega = v / r
        a_c = v**2 / r
        F_c = m * a_c

        st.markdown("#### 📊 결과")
        st.metric("주기 T", f"{T:.3f} s")
        st.metric("각속도 ω", f"{omega:.3f} rad/s")
        st.metric("구심 가속도", f"{a_c:.3f} m/s²")
        st.metric("구심력", f"{F_c:.3f} N")

    with col2:
        # 애니메이션 대신 한 순간 + 속도/가속도 벡터 표시 (여러 위상)
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
        ax = axes[0]
        circle = plt.Circle((0, 0), r, fill=False, color='#3498db', lw=2.5)
        ax.add_patch(circle)
        ax.set_xlim(-(r + 2), r + 2); ax.set_ylim(-(r + 2), r + 2)
        ax.set_aspect('equal'); ax.grid(True, alpha=0.3)
        ax.set_title("등속 원운동 벡터", fontweight='bold')
        ax.plot(0, 0, 'ko', ms=6)

        for phi in np.linspace(0, 2 * np.pi, 8, endpoint=False):
            px = r * np.cos(phi); py = r * np.sin(phi)
            # 속도 벡터 (접선 방향)
            vvx = -np.sin(phi) * (v * 0.4); vvy = np.cos(phi) * (v * 0.4)
            # 구심 가속도 벡터 (중심 방향)
            ax_v = -np.cos(phi) * (a_c * 0.15); ay_v = -np.sin(phi) * (a_c * 0.15)

            ax.annotate("", xy=(px + vvx, py + vvy), xytext=(px, py),
                        arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=1.5, mutation_scale=12))
            ax.annotate("", xy=(px + ax_v, py + ay_v), xytext=(px, py),
                        arrowprops=dict(arrowstyle="-|>", color='#2ecc71', lw=1.5, mutation_scale=12))
            ax.scatter([px], [py], color='#3498db', s=40, zorder=5)

        ax.plot([], [], color='#e74c3c', label='속도(접선)')
        ax.plot([], [], color='#2ecc71', label='구심가속도(중심)')
        ax.legend(fontsize=9, loc='upper right')
        ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")

        # 구심력 vs 반지름 그래프
        ax2 = axes[1]
        r_arr = np.linspace(0.1, 15, 200)
        Fc_arr = m * v**2 / r_arr
        ax2.plot(r_arr, Fc_arr, color='#9b59b6', lw=2.5)
        ax2.axvline(r, color='red', ls='--', lw=1.5, label=f'현재 r={r}m')
        ax2.scatter([r], [F_c], s=100, color='red', zorder=5)
        ax2.set_title("구심력 F = mv²/r", fontweight='bold')
        ax2.set_xlabel("반지름 r (m)"); ax2.set_ylabel("구심력 F (N)")
        ax2.legend(fontsize=10); ax2.grid(True, alpha=0.3)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close()


# ════════════════════════════════════════════════════════════════════════════
#  진자 운동
# ════════════════════════════════════════════════════════════════════════════
elif menu == "🌊 진자 운동":
    st.markdown('<div class="module-card purple"><h2>🌊 진자 운동 (단진자)</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    주기: T = 2π√(L/g) &nbsp; (진폭이 작을 때)<br>
    각도 운동 방정식: d²θ/dt² = −(g/L)sinθ<br>
    역학적 에너지: E = ½mv² + mgL(1−cosθ) = mgL(1−cosθ₀) (일정)
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### ⚙️ 파라미터")
        L        = st.slider("줄 길이 L (m)", 0.1, 5.0, 1.0, 0.1)
        theta0_d = st.slider("초기 각도 θ₀ (°)", 1, 80, 30)
        m        = st.slider("질량 m (kg)", 0.1, 5.0, 1.0, 0.1)
        g        = 9.8

        theta0 = np.radians(theta0_d)
        T_approx = 2 * np.pi * np.sqrt(L / g)
        T_cycles = 2
        dt = 0.01
        t_arr = np.arange(0, T_approx * T_cycles, dt)

        # Verlet 수치 적분 (비선형)
        theta = np.zeros(len(t_arr)); omega = np.zeros(len(t_arr))
        theta[0] = theta0
        for i in range(1, len(t_arr)):
            alpha = -(g / L) * np.sin(theta[i - 1])
            omega[i] = omega[i - 1] + alpha * dt
            theta[i] = theta[i - 1] + omega[i] * dt

        st.metric("주기 T (근사)", f"{T_approx:.3f} s")
        st.metric("진동수", f"{1/T_approx:.3f} Hz")
        max_v = np.sqrt(2 * g * L * (1 - np.cos(theta0)))
        st.metric("최대 속력", f"{max_v:.3f} m/s")

    with col2:
        fig, axes = plt.subplots(2, 2, figsize=(9, 7))
        fig.suptitle("단진자 운동 분석", fontsize=14, fontweight='bold')

        x_arr = L * np.sin(theta)
        y_arr = -L * np.cos(theta)

        # 궤적
        ax1 = axes[0, 0]
        ax1.plot(x_arr, y_arr, color='#9b59b6', lw=2, alpha=0.7)
        ax1.plot([0, x_arr[0]], [0, y_arr[0]], 'k--', alpha=0.4)
        ax1.scatter([0], [0], s=80, color='black', zorder=5)
        ax1.scatter([x_arr[0]], [y_arr[0]], s=120, color='#9b59b6', zorder=5, label='초기 위치')
        ax1.scatter([0], [-L], s=120, color='#e74c3c', zorder=5, marker='v', label='최저점')
        ax1.set_xlim(-L * 1.3, L * 1.3); ax1.set_ylim(-L * 1.3, 0.3)
        ax1.set_aspect('equal'); ax1.grid(True, alpha=0.3)
        ax1.set_title("진자 궤적"); ax1.legend(fontsize=8)

        # θ vs t
        ax2 = axes[0, 1]
        ax2.plot(t_arr, np.degrees(theta), color='#3498db', lw=2)
        ax2.set_title("각도 θ vs 시간"); ax2.set_xlabel("t (s)")
        ax2.set_ylabel("θ (°)"); ax2.grid(True, alpha=0.3)
        ax2.axhline(0, color='gray', lw=0.8, ls='--')

        # ω vs t
        ax3 = axes[1, 0]
        ax3.plot(t_arr, np.degrees(omega), color='#e74c3c', lw=2)
        ax3.set_title("각속도 ω vs 시간"); ax3.set_xlabel("t (s)")
        ax3.set_ylabel("ω (°/s)"); ax3.grid(True, alpha=0.3)

        # 에너지
        KE_arr = 0.5 * m * (L * omega)**2
        h_arr  = L * (1 - np.cos(theta))
        PE_arr = m * g * h_arr
        E_arr  = KE_arr + PE_arr

        ax4 = axes[1, 1]
        ax4.plot(t_arr, KE_arr, color='#e74c3c', lw=2, label='운동에너지')
        ax4.plot(t_arr, PE_arr, color='#3498db', lw=2, label='퍼텐셜에너지')
        ax4.plot(t_arr, E_arr,  color='#2c3e50', lw=1.5, ls='--', label='역학적에너지')
        ax4.set_title("에너지 변화"); ax4.set_xlabel("t (s)")
        ax4.set_ylabel("에너지 (J)"); ax4.legend(fontsize=9); ax4.grid(True, alpha=0.3)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close()


# ════════════════════════════════════════════════════════════════════════════
#  케플러 법칙
# ════════════════════════════════════════════════════════════════════════════
elif menu == "🌍 케플러 법칙과 중력":
    st.markdown('<div class="module-card teal"><h2>🌍 케플러 법칙과 중력</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    <b>제1법칙(타원 궤도):</b> 행성은 태양을 한 초점으로 하는 타원 궤도를 돈다.<br>
    <b>제2법칙(면적 속도 일정):</b> 태양~행성 선분이 같은 시간 동안 같은 넓이를 쓸어 지난다.<br>
    <b>제3법칙(조화 법칙):</b> T² ∝ a³ &nbsp;(a: 긴반지름, T: 공전 주기)
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### ⚙️ 궤도 파라미터")
        a = st.slider("긴반지름 a (AU)", 0.5, 5.0, 1.5, 0.1)
        e = st.slider("이심률 e (0=원, 1=포물선)", 0.0, 0.95, 0.4, 0.01)

        b = a * np.sqrt(1 - e**2)
        c = a * e  # 초점 거리
        T = a**1.5  # 케플러 3법칙 (지구=1 AU, 1 yr 기준)

        r_per = a * (1 - e)  # 근일점
        r_aph = a * (1 + e)  # 원일점

        st.metric("짧은반지름 b", f"{b:.3f} AU")
        st.metric("공전 주기 T", f"{T:.3f} 년")
        st.metric("근일점 거리", f"{r_per:.3f} AU")
        st.metric("원일점 거리", f"{r_aph:.3f} AU")

        st.markdown("---")
        st.markdown("#### 🪐 태양계 비교")
        planets = {"수성": (0.387, 0.206), "금성": (0.723, 0.007),
                   "지구": (1.000, 0.017), "화성": (1.524, 0.093),
                   "목성": (5.203, 0.049)}
        for name, (pa, pe) in planets.items():
            pT = pa**1.5
            st.markdown(f"**{name}**: a={pa} AU, T={pT:.2f} yr")

    with col2:
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        # 궤도 그림
        ax1 = axes[0]
        nu   = np.linspace(0, 2 * np.pi, 500)
        r_arr = a * (1 - e**2) / (1 + e * np.cos(nu))
        x_orb = r_arr * np.cos(nu)
        y_orb = r_arr * np.sin(nu)

        ax1.plot(x_orb, y_orb, color='#1abc9c', lw=2.5, label='궤도')
        # 태양
        ax1.scatter([c], [0], color='#f39c12', s=300, zorder=5, label='태양(초점)')
        ax1.scatter([-c], [0], color='gray', s=50, zorder=5, alpha=0.5, label='빈 초점')
        # 행성
        idx_planet = len(nu) // 6
        ax1.scatter([x_orb[idx_planet]], [y_orb[idx_planet]],
                    color='#3498db', s=120, zorder=5, label='행성')

        # 면적 색칠 (제2법칙)
        n_wedge = 40
        for start in [0, len(nu)//3, 2*len(nu)//3]:
            seg = np.concatenate([[start], range(start, start + n_wedge)])
            xs  = np.append([c], x_orb[start:start + n_wedge])
            ys  = np.append([0], y_orb[start:start + n_wedge])
            ax1.fill(xs, ys, alpha=0.2, color=['#e74c3c', '#3498db', '#2ecc71'][seg[0] % 3])

        ax1.set_aspect('equal'); ax1.grid(True, alpha=0.3)
        ax1.set_title("타원 궤도와 면적 속도 일정", fontweight='bold')
        ax1.set_xlabel("x (AU)"); ax1.set_ylabel("y (AU)")
        ax1.legend(fontsize=9)

        # T² vs a³
        ax2 = axes[1]
        a_arr  = np.linspace(0.2, 6, 200)
        T2_arr = a_arr**3
        ax2.plot(a_arr, T2_arr, color='#9b59b6', lw=2.5, label='T² = a³')

        for name, (pa, _) in planets.items():
            pT = pa**1.5
            ax2.scatter([pa**3], [pT**2], s=80, zorder=5)
            ax2.text(pa**3 + 0.05, pT**2, name, fontsize=9)

        ax2.scatter([a**3], [T**2], s=150, color='#e74c3c', zorder=5, label=f'현재 행성 a={a}AU')
        ax2.set_title("케플러 제3법칙: T² ∝ a³", fontweight='bold')
        ax2.set_xlabel("a³ (AU³)"); ax2.set_ylabel("T² (년²)")
        ax2.legend(fontsize=9); ax2.grid(True, alpha=0.3)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close()


# ════════════════════════════════════════════════════════════════════════════
#  역학적 에너지 보존
# ════════════════════════════════════════════════════════════════════════════
elif menu == "⚡ 역학적 에너지 보존":
    st.markdown('<div class="module-card" style="border-left-color:#e74c3c"><h2>⚡ 역학적 에너지 보존</h2></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    역학적 에너지 E = 운동에너지 + 퍼텐셜에너지 = ½mv² + mgh = 일정<br>
    비보존력(마찰)이 없을 때: E₁ = E₂ &nbsp;→&nbsp; ½mv₁² + mgh₁ = ½mv₂² + mgh₂
    </div>
    """, unsafe_allow_html=True)

    scenario = st.radio("시나리오 선택", ["🎢 롤러코스터 (언덕)", "📦 경사면 미끄럼", "⚽ 자유 낙하"], horizontal=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### ⚙️ 파라미터")
        m   = st.slider("질량 m (kg)", 0.1, 20.0, 5.0, 0.1)
        g   = 9.8
        mu  = st.slider("마찰 계수 μ (0=마찰 없음)", 0.0, 0.5, 0.0, 0.01)

        if scenario == "🎢 롤러코스터 (언덕)":
            h1 = st.slider("출발 높이 h₁ (m)", 1.0, 30.0, 20.0, 0.5)
            h2 = st.slider("언덕 높이 h₂ (m)", 0.0, 25.0, 10.0, 0.5)
            v1 = 0.0
            E_loss = m * g * mu * (h1 - h2) if h1 > h2 else 0
            v2_sq  = (2 / m) * (0.5 * m * v1**2 + m * g * h1 - m * g * h2 - E_loss)
            v2     = np.sqrt(max(v2_sq, 0))
            st.metric("언덕 꼭대기 속력", f"{v2:.2f} m/s")

        elif scenario == "📦 경사면 미끄럼":
            h    = st.slider("높이 h (m)", 1.0, 20.0, 5.0, 0.5)
            deg  = st.slider("경사각 (°)", 10, 80, 30)
            L_ramp = h / np.sin(np.radians(deg))
            E_loss = mu * m * g * np.cos(np.radians(deg)) * L_ramp
            v_bot  = np.sqrt(max(2 * g * h - 2 * E_loss / m, 0))
            st.metric("경사면 길이", f"{L_ramp:.2f} m")
            st.metric("바닥 도달 속력", f"{v_bot:.2f} m/s")

        else:  # 자유 낙하
            h = st.slider("낙하 높이 h (m)", 1.0, 100.0, 20.0, 0.5)
            v_ground = np.sqrt(2 * g * h)
            st.metric("바닥 도달 속력", f"{v_ground:.2f} m/s")

    with col2:
        fig, axes = plt.subplots(1, 2, figsize=(9, 5))

        if scenario == "🎢 롤러코스터 (언덕)":
            x_pts = [0, 1, 2, 3, 4]
            h_pts = [h1, h1 * 0.5, h2, h2 * 0.3, 0]

            ax1 = axes[0]
            ax1.fill_between(x_pts, h_pts, alpha=0.3, color='saddlebrown')
            ax1.plot(x_pts, h_pts, 'k-', lw=2)
            ax1.scatter([0], [h1], s=150, color='#3498db', zorder=5, label=f'출발 h={h1}m')
            ax1.scatter([2], [h2], s=150, color='#e74c3c', zorder=5, label=f'언덕 h={h2}m')
            ax1.set_title("롤러코스터 경로", fontweight='bold')
            ax1.set_xlabel("위치"); ax1.set_ylabel("높이 (m)")
            ax1.legend(fontsize=9); ax1.grid(True, alpha=0.3)

            h_arr  = np.linspace(0, h1, 100)
            KE_arr = m * g * (h1 - h_arr)
            PE_arr = m * g * h_arr
            ax2 = axes[1]
            ax2.plot(h_arr, KE_arr, color='#e74c3c', lw=2, label='운동에너지')
            ax2.plot(h_arr, PE_arr, color='#3498db', lw=2, label='퍼텐셜에너지')
            ax2.plot(h_arr, KE_arr + PE_arr, color='#2c3e50', lw=2, ls='--', label='역학적에너지')
            ax2.axvline(h2, color='green', ls=':', lw=1.5, label=f'언덕 h={h2}m')
            ax2.set_title("높이에 따른 에너지", fontweight='bold')
            ax2.set_xlabel("높이 (m)"); ax2.set_ylabel("에너지 (J)")
            ax2.legend(fontsize=9); ax2.grid(True, alpha=0.3)

        elif scenario == "📦 경사면 미끄럼":
            deg_r   = np.radians(deg)
            t_total = np.sqrt(2 * h / (g * (np.sin(deg_r) - mu * np.cos(deg_r))))
            t_arr   = np.linspace(0, t_total, 200)
            acc     = g * (np.sin(deg_r) - mu * np.cos(deg_r))
            s_arr   = 0.5 * acc * t_arr**2
            v_arr   = acc * t_arr
            h_arr   = h - s_arr * np.sin(deg_r)

            KE_arr  = 0.5 * m * v_arr**2
            PE_arr  = m * g * np.maximum(h_arr, 0)

            ax1 = axes[0]
            # 경사면 그림
            Lx = L_ramp * np.cos(deg_r); Ly = L_ramp * np.sin(deg_r)
            ax1.fill([0, Lx, Lx, 0], [0, 0, Ly, 0], color='saddlebrown', alpha=0.3)
            ax1.plot([0, Lx], [Ly, 0], 'k-', lw=2)
            ax1.set_title("경사면 미끄럼", fontweight='bold')
            ax1.set_xlabel("x (m)"); ax1.set_ylabel("y (m)")
            ax1.set_aspect('equal'); ax1.grid(True, alpha=0.3)

            ax2 = axes[1]
            ax2.plot(t_arr, KE_arr, color='#e74c3c', lw=2, label='운동에너지')
            ax2.plot(t_arr, PE_arr, color='#3498db', lw=2, label='퍼텐셜에너지')
            ax2.plot(t_arr, KE_arr + PE_arr, color='#2c3e50', lw=2, ls='--', label='역학적에너지')
            ax2.set_title("시간에 따른 에너지", fontweight='bold')
            ax2.set_xlabel("t (s)"); ax2.set_ylabel("에너지 (J)")
            ax2.legend(fontsize=9); ax2.grid(True, alpha=0.3)

        else:
            t_arr  = np.linspace(0, np.sqrt(2 * h / g), 200)
            y_arr  = h - 0.5 * g * t_arr**2
            v_arr  = g * t_arr
            KE_arr = 0.5 * m * v_arr**2
            PE_arr = m * g * y_arr

            ax1 = axes[0]
            ax1.plot(np.zeros_like(y_arr), y_arr, color='#3498db', lw=2)
            ax1.axhline(0, color='saddlebrown', lw=2)
            ax1.scatter([0], [h], s=150, color='#3498db', label=f'출발 h={h}m')
            ax1.scatter([0], [0], s=150, color='#e74c3c', marker='x', label='도달점')
            ax1.set_title("자유 낙하 경로", fontweight='bold')
            ax1.set_xlabel("x"); ax1.set_ylabel("높이 (m)")
            ax1.legend(fontsize=9); ax1.grid(True, alpha=0.3)

            ax2 = axes[1]
            ax2.plot(t_arr, KE_arr, color='#e74c3c', lw=2, label='운동에너지')
            ax2.plot(t_arr, PE_arr, color='#3498db', lw=2, label='퍼텐셜에너지')
            ax2.plot(t_arr, KE_arr + PE_arr, color='#2c3e50', lw=2, ls='--', label='역학적에너지')
            ax2.set_title("시간에 따른 에너지", fontweight='bold')
            ax2.set_xlabel("t (s)"); ax2.set_ylabel("에너지 (J)")
            ax2.legend(fontsize=9); ax2.grid(True, alpha=0.3)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close()
