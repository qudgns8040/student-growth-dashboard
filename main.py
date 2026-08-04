import streamlit as st
from datetime import datetime

from sidebar import create_sidebar

#체크리스트페이지 불러오기
from modules.checklist.checklist_view import show_checklist_page

# =====================
# 기본 설정
# =====================

st.set_page_config(
    page_title="수학의힘 강사 대시보드",
    page_icon="📚",
    layout="wide"
)

# 변수선언 + 함수호출
# 변수 : 선택된 함수 리턴값
# 함수 : 사이드바 생성

menu = create_sidebar()



# =====================
# Home 화면
# =====================

if menu == "Home":
    st.title(
        "수학의힘 강사 대시보드"
    )
    # 날짜 불러오기
    today = datetime.now().strftime(
        "%Y-%m-%d"
    )
    st.write(
        f"오늘 날짜 : {today}"
    )
    st.divider()



# ---------------------
# 요약 카드
# ---------------------

col1, col2, col3 = st.columns(3)

# metric () : 숫자, 지표 카드형태로 보여주는 컴포넌트
# metric (
#     label,
#     value,
#     delta=None
# )

with col1:
    st.metric(
        label="오늘 업무 진행률",
        value="70%",
        delta="+10%"
    )

with col2:

    st.metric(
        "담당 학급",
        "4개"
    )

with col3:

    st.metric(
        "관리 학생",
        "39명"
    )
st.divider() # 가로선


# ---------------------
# 오늘 수업 일정
# ---------------------

st.subheader(
    "오늘 수업 일정"
)

# 스케줄 값 임시 생성
# 리스트 [(튜플), (튜플), (튜플), (튜플)] 
schedule = [
    ("15:30", "6MR1(현행)"),
    ("16:25", "4MR(선행)"),
    ("20:05", "7MS1(현행)"),
    ("21:00", "7MS2(선행)")
]

# 스케줄 반복문 호출
# time = 튜플 첫째 = 시간
# cls = 튜플 둘째 = 클래스
# **{a}** : 굵게 처리
for time, cls in schedule:
    st.write(
        f"**{time}** | {cls}"
    )

st.divider()



# ---------------------
# 담당 반 현황
# ---------------------

st.subheader(
        "담당 반 현황"
    )
# classes = 리스트[(튜플),튜플]
classes = [
    ("6MR1(현행)", "6-2_알파"),
    ("4MR(선행)", "4-2_베타"),
    ("7MS1(현행)", "2-1_수심달"),
    ("7MS2(선행)", "2-2_개념유형_(하)")
]
for cls, book in classes:
    st.write(
        f"- {cls} | 교재 : {book}"
    )



st.divider()



# =====================
# 기능 페이지 출력
# =====================

if menu == "홈":
    st.title("홈")

elif menu == "오늘 체크리스트":
   show_checklist_page()

elif menu == "체크리스트 수정":
    st.title(
        "체크리스트 수정"
    )
    st.info(
        "체크리스트 수정 기능 공사중"
    )

elif menu == "업무 이력":
    st.title(
        "업무 이력"
    )
    st.info(
        "업무 이력 기능 공사중"
    )

elif menu == "학생 목록":
    st.title(
        "학생 목록"
    )
    st.info(
        "학생 목록 기능 공사중"
    )

elif menu == "학생 상세 수정":
    st.title(
        "학생 상세"
    )
    st.info(
        "학생 상세 기능 공사중"
    )

else:
    st.title(menu)
    st.info(
        f"{menu} 기능 구현 공사중"
    )
    