import streamlit as st

def create_sidebar():
    st.sidebar.title(
        "수학의힘 강사 대시보드"
    )

    menu = "Home"

    # =====================
    # 1. 업무 관리
    # =====================
    with st.sidebar.expander(
        "📋 업무 관리",
        expanded=True
    ):

        if st.button("오늘 체크리스트"):
            menu = "오늘 체크리스트"

        if st.button("체크리스트 수정"):
            menu = "체크리스트 수정"

        if st.button("업무 이력"):
            menu = "업무 이력"


    # =====================
    # 학생 관리
    # =====================

    with st.sidebar.expander(
        "👨‍🎓 학생 관리"
    ):

        if st.button("학생 목록"):
            menu = "학생 목록"

        if st.button("학생 상세"):
            menu = "학생 상세"

        if st.button("특이사항"):
            menu = "특이사항"



    # =====================
    # 수업 관리
    # =====================

    with st.sidebar.expander(
        "📚 수업 관리"
    ):

        if st.button("학급 정보"):
            menu = "학급 정보"

        if st.button("진도 관리"):
            menu = "진도 관리"

        if st.button("숙제 관리"):
            menu = "숙제 관리"



    # =====================
    # 평가 관리
    # =====================

    with st.sidebar.expander(
        "📝 평가 관리"
    ):

        if st.button("PDT 입력"):
            menu = "PDT 입력"

        if st.button("평가 결과"):
            menu = "평가 결과"

        if st.button("평가 분석"):
            menu = "평가 분석"



    # =====================
    # 성장 분석
    # =====================

    with st.sidebar.expander(
        "📈 성장 분석"
    ):

        if st.button("학생 성장"):
            menu = "학생 성장"

        if st.button("반별 분석"):
            menu = "반별 분석"

        if st.button("위험 학생"):
            menu = "위험 학생"



    # =====================
    # 리포트
    # =====================

    with st.sidebar.expander(
        "📄 리포트"
    ):

        if st.button("출력"):
            menu = "리포트 출력"



    return menu