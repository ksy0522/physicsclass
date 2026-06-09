import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="🐰 여행요정의 여행지 추천",
    page_icon="✈️",
    layout="centered"
)

# CSS 꾸미기
st.markdown("""
<style>
.main {
    background-color: #FFF8FC;
}

.recommend-box {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    margin-top: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

.title {
    text-align:center;
    color:#ff69b4;
}

.small-text {
    text-align:center;
    color:gray;
}
</style>
""", unsafe_allow_html=True)

# 제목
st.markdown("<h1 class='title'>🐰 여행요정의 여행지 추천 ✈️</h1>", unsafe_allow_html=True)

st.markdown(
    "<p class='small-text'>당신의 여행 취향을 알려주세요!</p>",
    unsafe_allow_html=True
)

st.divider()

# 질문들
style = st.selectbox(
    "🌈 어떤 여행을 좋아하시나요?",
    ["감성 카페", "자연 풍경", "맛집 탐방", "힐링 휴양", "액티비티"]
)

partner = st.selectbox(
    "💖 누구와 가나요?",
    ["혼자", "친구", "연인", "가족"]
)

budget = st.selectbox(
    "💰 예산은 어느 정도인가요?",
    ["10만원 이하", "30만원 이하", "50만원 이하", "100만원 이상"]
)

# 추천 버튼
if st.button("✨ 여행지 추천받기 ✨"):

    result = ""

    if style == "감성 카페":
        result = """
        ☕ 성수동

        • 감성 카페 천국
        • 소품샵 구경 가능
        • 사진 찍기 좋은 거리
        """

    elif style == "자연 풍경":
        result = """
        🌿 제주도

        • 아름다운 바다
        • 오름 트레킹
        • 여유로운 드라이브
        """

    elif style == "맛집 탐방":
        result = """
        🍜 부산

        • 해산물 맛집
        • 돼지국밥
        • 광안리 야경
        """

    elif style == "힐링 휴양":
        result = """
        🌺 오키나와

        • 맑은 바다
        • 한적한 분위기
        • 리조트 휴식
        """

    elif style == "액티비티":
        result = """
        🚴 강원도

        • 서핑
        • 레일바이크
        • 짚라인
        """

    st.balloons()

    st.markdown(
        f"""
        <div class="recommend-box">
        <h2>🎁 추천 여행지</h2>
        <p>{result}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 추가 멘트
    if partner == "가족":
        st.success("👨‍👩‍👧 가족과 함께라면 이동이 편한 코스를 추천드려요!")

    elif partner == "연인":
        st.success("💕 인생샷 찍기 좋은 장소들을 우선 추천했어요!")

    elif partner == "친구":
        st.success("😆 친구들과 추억 만들기 좋은 여행지예요!")

    else:
        st.success("🌸 혼자만의 여유를 즐기기 좋은 여행지예요!")
