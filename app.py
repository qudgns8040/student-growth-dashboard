import streamlit as st

student_page = st.Page(
    "pages/student.py",
    title="학생 현황",
    icon="👨‍🎓"
)

growth_page = st.Page(
    "pages/growth.py",
    title="성장 분석",
    icon="📈"
)

class_page = st.Page(
    "pages/class_analysis.py",
    title="학급 분석",
    icon="🏫"
)

report_page = st.Page(
    "pages/report.py",
    title="리포트",
    icon="📄"
)

pg = st.navigation(
    [
        student_page,
        growth_page,
        class_page,
        report_page
    ]
)

st.set_page_config(
    page_title="학생 성장 대시보드",
    layout="wide"
)

pg.run()