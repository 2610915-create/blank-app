import pandas as pd
import streamlit as st

# 페이지 제목 설정
st.set_page_config(page_title="공부 시간 관리 프로그램", page_icon="📝", layout="centered")
st.title("📝 공부 시간 관리 프로그램")

# 1. 스트림릿 세션 상태(Session State) 초기화
# 웹 페이지가 새로고침되어도 데이터가 초기화되지 않도록 유지합니다.
if "study_records" not in st.session_state:
    st.session_state.study_records = {}

# 사이드바 또는 상단에 설명 추가
st.sidebar.markdown("### 💡 사용 방법")
st.sidebar.info(
    "1. 과목과 시간을 입력하고 추가 버튼을 누르세요.\n"
    "2. 하단에서 현재까지의 기록과 총 시간을 확인할 수 있습니다."
)

# --- 섹션 1: 공부 기록 추가 ---
st.header("📥 공부 기록 추가하기")

# 컬럼을 나누어 입력창을 나란히 배치
col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("📚 공부 과목을 입력해주세요", placeholder="예: 파이썬, 수학, 영어")

with col2:
    # min_value=1로 설정하여 자연스럽게 숫자만 입력받도록 유도합니다.
    subject_time = st.number_input("⏱️ 공부 시간(분)을 입력해주세요", min_value=1, value=30, step=5)

# 기록 추가 버튼
if st.button("🚀 기록 추가", use_container_width=True):
    if subject.strip() == "":
        st.warning("⚠️ 과목 이름을 입력해주세요!")
    else:
        # 기존에 있는 과목이면 누적, 없으면 새로 추가
        if subject in st.session_state.study_records:
            st.session_state.study_records[subject] += subject_time
        else:
            st.session_state.study_records[subject] = subject_time
            
        st.success(f"🎉 [{subject}] 과목에 {subject_time}분이 성공적으로 추가되었습니다!")

st.divider() # 구분선

# --- 섹션 2: 공부 기록 조회 및 총 시간 ---
st.header("📊 공부 기록 및 통계")

if not st.session_state.study_records:
    st.info("아직 등록된 공부 기록이 없습니다. 위의 입력창에서 기록을 추가해 보세요!")
else:
    # 딕셔너리 데이터를 판다스 데이터프레임으로 변환하여 시각화
    df = pd.DataFrame(
        list(st.session_state.study_records.items()), 
        columns=["과목", "공부 시간(분)"]
    )
    
    # 총 시간 계산
    total_time = df["공부 시간(분)"].sum()
    
    # 상단에 총 시간 하이라이트 (st.metric 활용)
    st.metric(label="🔥 총 공부 시간", value=f"{total_time} 분")
    
    # 깔끔한 표(DataFrame) 형태로 출력
    st.subheader("📋 과목별 상세 기록")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 선택 사항: 기록 전체 초기화 버튼
    if st.button("🗑️ 모든 기록 초기화", type="primary"):
        st.session_state.study_records = {}
        st.rerun()