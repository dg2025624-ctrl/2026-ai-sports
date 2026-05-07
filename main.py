import streamlit as st
import anthropic
from datetime import date

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="⚾ AI 야구 경기 분석기",
    page_icon="⚾",
    layout="centered",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        text-align: center;
        color: white;
    }
    .hero h1 { font-size: 2rem; margin: 0 0 6px 0; }
    .hero p  { margin: 0; opacity: 0.75; font-size: 0.95rem; }

    .section-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 18px;
    }
    .section-title {
        font-weight: 700;
        font-size: 1rem;
        color: #1e293b;
        margin-bottom: 14px;
    }

    .usage-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 0.85rem;
        color: #1e40af;
        margin-top: 16px;
    }

    .result-box {
        background: white;
        border: 2px solid #0f3460;
        border-radius: 14px;
        padding: 28px 32px;
        margin-top: 20px;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# ── API 클라이언트 ────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("⚠️ Streamlit Secrets에 ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)

client = get_client()

# ── 사이드바 ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    model_choice = st.radio(
        "AI 모델",
        ["claude-sonnet-4-6", "claude-opus-4-6"],
        format_func=lambda m: {
            "claude-sonnet-4-6": "🚀 Sonnet 4.6 (빠름)",
            "claude-opus-4-6":   "🧠 Opus 4.6 (정밀)",
        }[m],
    )
    analysis_style = st.selectbox(
        "분석 스타일",
        ["전문 해설가", "데이터 분석가", "팬 커뮤니티"],
    )
    st.divider()
    st.caption("⚾ KBO · MLB 경기 프리뷰 & 분석 생성기")
    st.caption("🔐 API 키는 Streamlit Secrets로 안전하게 관리됩니다.")

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>⚾ AI 야구 경기 분석기</h1>
    <p>KBO · MLB 경기 정보를 입력하면 AI가 전문 프리뷰 & 분석 리포트를 생성합니다</p>
</div>
""", unsafe_allow_html=True)

# ── 리그 선택 ─────────────────────────────────────────────────
league = st.radio("리그 선택", ["🇰🇷 KBO", "🇺🇸 MLB"], horizontal=True)
league_label = "KBO" if "KBO" in league else "MLB"

# ── 입력 폼 ──────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏟️ 경기 기본 정보</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    home_team = st.text_input("홈팀", placeholder="예) 기아 타이거즈")
with col2:
    away_team = st.text_input("원정팀", placeholder="예) 삼성 라이온즈")

game_date = st.date_input("경기 날짜", value=date.today())
stadium   = st.text_input("경기장 (선택)", placeholder="예) 광주-기아 챔피언스 필드")
st.markdown('</div>', unsafe_allow_html=True)

# ── 최근 전적 ─────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 최근 성적 & 전적</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    home_record = st.text_input(f"{home_team or '홈팀'} 시즌 성적", placeholder="예) 35승 20패")
    home_recent = st.text_area(f"{home_team or '홈팀'} 최근 5경기", placeholder="예) 승 패 승 승 패", height=80)
with col4:
    away_record = st.text_input(f"{away_team or '원정팀'} 시즌 성적", placeholder="예) 30승 25패")
    away_recent = st.text_area(f"{away_team or '원정팀'} 최근 5경기", placeholder="예) 패 승 승 패 승", height=80)

head_to_head = st.text_input("시즌 상대 전적 (선택)", placeholder="예) 홈팀 4승 2패")
st.markdown('</div>', unsafe_allow_html=True)

# ── 선발 투수 ─────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚾ 선발 투수 정보</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    home_pitcher = st.text_input(f"{home_team or '홈팀'} 선발", placeholder="예) 양현종 (8승 3패, ERA 2.85)")
with col6:
    away_pitcher = st.text_input(f"{away_team or '원정팀'} 선발", placeholder="예) 원태인 (7승 5패, ERA 3.10)")
st.markdown('</div>', unsafe_allow_html=True)

# ── 추가 정보 ─────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 추가 정보 (선택)</div>', unsafe_allow_html=True)
extra_info = st.text_area(
    "부상자, 날씨, 특이사항 등",
    placeholder="예) 홈팀 4번 타자 부상 결장 / 우천 가능성 있음",
    height=90,
)
st.markdown('</div>', unsafe_allow_html=True)

# ── 분석 생성 버튼 ────────────────────────────────────────────
generate = st.button("🔍 경기 분석 리포트 생성하기", use_container_width=True, type="primary")

if generate:
    if not home_team or not away_team:
        st.warning("⚠️ 홈팀과 원정팀 이름을 입력해주세요.")
    else:
        style_desc = {
            "전문 해설가": "KBO/MLB 10년 경력의 전문 야구 해설가처럼 깊이 있고 권위 있는 문체로",
            "데이터 분석가": "수치와 통계를 중심으로 논리적이고 객관적인 데이터 분석가 스타일로",
            "팬 커뮤니티": "야구를 사랑하는 열정적인 팬의 시각으로 재미있고 생동감 있게",
        }[analysis_style]

        prompt = f"""
당신은 {style_desc} {league_label} 야구 경기를 분석하는 전문가입니다.
아래 정보를 바탕으로 한국어로 경기 프리뷰 & 분석 리포트를 작성해주세요.

[경기 정보]
- 리그: {league_label}
- 날짜: {game_date.strftime('%Y년 %m월 %d일')}
- 홈팀: {home_team}
- 원정팀: {away_team}
{"- 경기장: " + stadium if stadium else ""}

[성적 & 전적]
- {home_team} 시즌 성적: {home_record or "정보 없음"}
- {home_team} 최근 5경기: {home_recent or "정보 없음"}
- {away_team} 시즌 성적: {away_record or "정보 없음"}
- {away_team} 최근 5경기: {away_recent or "정보 없음"}
{"- 상대 전적: " + head_to_head if head_to_head else ""}

[선발 투수]
- {home_team}: {home_pitcher or "미정"}
- {away_team}: {away_pitcher or "미정"}

{"[추가 정보]\n" + extra_info if extra_info else ""}

다음 구조로 리포트를 작성해주세요:

## ⚾ {game_date.strftime('%m월 %d일')} {home_team} vs {away_team} 프리뷰

### 📌 경기 개요
(경기의 의미와 맥락을 2~3문장으로)

### 🔥 주목 포인트
(이 경기의 핵심 관전 포인트 3가지를 번호로)

### ⚾ 선발 투수 매치업
(양 팀 선발 투수 분석)

### 📊 팀 상태 분석
(홈팀 / 원정팀 각각의 최근 흐름과 강약점)

### 🏆 예상 승부처 & 전망
(승부를 가를 핵심 요소와 경기 결과 전망)

### 💡 주목 선수
(오늘 경기 주목해야 할 선수 2~3명)
"""

        with st.spinner("AI가 경기를 분석하고 있습니다... ⚾"):
            response = client.messages.create(
                model=model_choice,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )

        result        = response.content[0].text
        input_tokens  = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(result)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="usage-box">
            🔢 <strong>토큰 사용량</strong> &nbsp;|&nbsp;
            모델: <strong>{model_choice}</strong> &nbsp;·&nbsp;
            입력: <strong>{input_tokens:,}</strong> &nbsp;·&nbsp;
            출력: <strong>{output_tokens:,}</strong> &nbsp;·&nbsp;
            합계: <strong>{input_tokens + output_tokens:,}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            label="📥 리포트 다운로드 (.txt)",
            data=result,
            file_name=f"{game_date}_{home_team}_vs_{away_team}_분석.txt",
            mime="text/plain",
        )
